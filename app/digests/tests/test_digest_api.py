import copy
import json
from typing import Dict, List
from unittest.mock import patch

from django.conf import settings
from django.test.client import Client
import pytest
from rest_framework.test import APIClient

from digests.models import Digest

DIGESTS_URL = '/digests'


@pytest.mark.django_db
def test_can_get_digest(client: Client):
    response = client.get(DIGESTS_URL, **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE})
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-01 00:00:00')
def test_has_expected_data_in_response(can_preview_header: Dict,
                                       client: Client,
                                       preview_digest: Digest,
                                       digest_image_json: Dict,
                                       digest_content_json: List[Dict],
                                       digest_related_content_json: List[Dict],
                                       digest_subjects_json: List[Dict]):
    response = client.get(DIGESTS_URL,
                          **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE}, **can_preview_header)
    data = response.data['items'][0]
    assert response.data['total'] == 1
    assert len(response.data['items']) == 1
    assert data['id'] == '2'
    assert data['title'] == 'Neighborhood watch'
    assert data['published'] == "2018-07-06T09:06:01Z"
    assert data['updated'] == "2018-01-01T00:00:00Z"
    assert data['image'] == digest_image_json
    assert data['subjects'] == digest_subjects_json
    assert data['content'] == digest_content_json
    assert data['relatedContent'] == digest_related_content_json


@pytest.mark.django_db
def test_can_get_digest_by_id(can_preview_header: Dict,
                              client: Client,
                              preview_digest: Digest,
                              digest_json: Dict):
    response = client.get(f'{DIGESTS_URL}/{preview_digest.id}',
                          **{'ACCEPT': settings.DIGEST_CONTENT_TYPE}, **can_preview_header)
    assert response.data['id'] == digest_json['id']
    assert response.content_type == settings.DIGEST_CONTENT_TYPE


@pytest.mark.django_db
def test_has_digests_content_type_header(can_preview_header: Dict,
                                         client: Client):
    response = client.get(DIGESTS_URL, **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE}, **can_preview_header)
    assert response.status_code == 200
    assert response.content_type == settings.DIGESTS_CONTENT_TYPE


@pytest.mark.django_db
def test_can_ingest_digest_post(rest_client: APIClient, digest_json: Dict, can_edit_headers: Dict):
    response = rest_client.post(DIGESTS_URL, data=json.dumps(digest_json),
                                content_type=settings.DIGEST_CONTENT_TYPE,
                                **can_edit_headers)
    assert response.status_code == 201

@pytest.mark.django_db
def test_can_ingest_digest_put(rest_client: APIClient, digest_json: Dict, can_edit_headers: Dict):
    response = rest_client.put(f'{DIGESTS_URL}/{digest_json["id"]}', data=json.dumps(digest_json),
                                content_type=settings.DIGEST_CONTENT_TYPE,
                                **can_edit_headers)
    assert response.status_code == 204


@pytest.mark.django_db
def test_is_ordered_by_descending_published_date(client: Client, preview_digest: Digest, digest_json: Dict):
    # add second digest with newer published date
    digest_data = copy.deepcopy(digest_json)
    new_pub_date = "2018-10-07T00:00:00Z"
    digest_data['id'] = '10'
    digest_data['published'] = new_pub_date

    new_digest = Digest.objects.create(**digest_data)
    new_digest.save()

    response = client.get(DIGESTS_URL, **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE,
                                          settings.CONSUMER_GROUPS_HEADER: 'view-unpublished-content'})
    assert response.status_code == 200
    assert len(response.data['items']) == 2
    # check most recently published digest is first
    assert response.data['items'][0]['id'] == '10'
    assert response.data['items'][0]['published'] == new_pub_date

    
@pytest.mark.django_db
def test_will_fail_to_ingest_digest_without_headers(rest_client: APIClient, digest_json: Dict):
    response = rest_client.post(DIGESTS_URL, data=json.dumps(digest_json),
                                content_type=settings.DIGEST_CONTENT_TYPE)
    assert response.status_code == 403


@pytest.mark.django_db
def test_only_shows_published_digests_with_no_auth_header(client: Client, preview_digest: Digest):
    response = client.get(DIGESTS_URL, **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE})
    assert response.status_code == 200
    assert len(response.data['items']) == 0

    preview_digest.stage = 'published'
    preview_digest.save()

    response = client.get(DIGESTS_URL, **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE})
    assert response.status_code == 200
    assert len(response.data['items']) == 1
    assert response.data['items'][0]['id'] == preview_digest.id


@pytest.mark.parametrize('stage', [
    'preview',
    'published',
])
@pytest.mark.django_db
def test_can_filter_on_digest_stage(stage: str,
                                    can_preview_header: Dict,
                                    client: Client,
                                    preview_digest: Digest,
                                    published_digest: Digest):
    response = client.get(f'{DIGESTS_URL}?stage={stage}',
                          **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE}, **can_preview_header)
    assert response.status_code == 200
    assert response.data['total'] == 1
    assert response.data['items'][0]['stage'] == stage

@pytest.mark.django_db
def test_is_paginated(client: Client, multiple_published_digests):
    per_page = 3
    def _count_items(page):
        response = client.get(f'{DIGESTS_URL}?per-page={per_page}&page={page}')
        assert response.status_code == 200
        assert response.data['total'] == len(multiple_published_digests)
        items = len(response.data['items'])
        assert items <= per_page
        return items

    last_page = 4
    total = sum([_count_items(page) for page in range(1, last_page)]) + _count_items(page=last_page)

    assert total == len(multiple_published_digests)

@pytest.mark.django_db
def test_page_invalid(client: Client):
    response = client.get(f'{DIGESTS_URL}?page=the_second_one_please')
    assert response.status_code == 400
    assert response.data == {'title': '`page` parameter is invalid'}

@pytest.mark.django_db
def test_per_page_invalid(client: Client, multiple_published_digests):
    response = client.get(f'{DIGESTS_URL}?per-page=as_many_as_you_can')
    assert response.status_code == 400
    assert response.data == {'title': '`per-page` parameter is invalid'}

@pytest.mark.django_db
def test_page_too_small(client: Client):
    response = client.get(f'{DIGESTS_URL}?page=0')
    assert response.status_code == 400
    assert response.data == {'title': '`page` parameter is too small'}

@pytest.mark.django_db
def test_per_page_too_small(client: Client, multiple_published_digests):
    response = client.get(f'{DIGESTS_URL}?per-page=0')
    assert response.status_code == 400
    assert response.data == {'title': '`per-page` parameter is too small'}

@pytest.mark.django_db
def test_page_too_large(client: Client, multiple_published_digests):
    all_digests = len(multiple_published_digests)
    response = client.get(f'{DIGESTS_URL}?per-page={all_digests}&page=2')
    assert response.status_code == 404

@pytest.mark.django_db
def test_per_page_too_large(client: Client, multiple_published_digests):
    response = client.get(f'{DIGESTS_URL}?per-page=101&page=1')
    assert response.status_code == 400
    assert response.data == {'title': '`per-page` parameter is too large'}
