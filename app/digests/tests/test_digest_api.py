import copy
import json
from typing import Dict, List

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
def test_has_expected_data_in_response(auth_header: Dict,
                                       client: Client,
                                       digest: Digest,
                                       digest_image_json: Dict,
                                       digest_content_json: List[Dict],
                                       digest_related_content_json: List[Dict],
                                       digest_subjects_json: List[Dict]):
    response = client.get(DIGESTS_URL,
                          **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE}, **auth_header)
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
def test_can_get_digest_by_id(auth_header: Dict,
                              client: Client,
                              digest: Digest,
                              digest_json: Dict):
    response = client.get(f'{DIGESTS_URL}/{digest.id}',
                          **{'ACCEPT': settings.DIGEST_CONTENT_TYPE}, **auth_header)
    assert response.data['id'] == digest_json['id']
    assert response.content_type == settings.DIGEST_CONTENT_TYPE


@pytest.mark.django_db
def test_has_digests_content_type_header(auth_header: Dict, client: Client):
    response = client.get(DIGESTS_URL, **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE}, **auth_header)
    assert response.status_code == 200
    assert response.content_type == settings.DIGESTS_CONTENT_TYPE


@pytest.mark.django_db
def test_can_ingest_digest(rest_client: APIClient, digest_json: Dict, can_edit_headers: Dict):
    response = rest_client.post(DIGESTS_URL, data=json.dumps(digest_json),
                                content_type=settings.DIGEST_CONTENT_TYPE,
                                **can_edit_headers)
    assert response.status_code == 201


@pytest.mark.django_db
def test_is_ordered_by_descending_published_date(client: Client, digest: Digest, digest_json: Dict):
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
def test_only_shows_published_digests_with_no_auth_header(client: Client, digest: Digest):
    response = client.get(DIGESTS_URL, **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE})
    assert response.status_code == 200
    assert len(response.data['items']) == 0

    digest.stage = 'published'
    digest.save()

    response = client.get(DIGESTS_URL, **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE})
    assert response.status_code == 200
    assert len(response.data['items']) == 1
    assert response.data['items'][0]['id'] == digest.id

@pytest.mark.parametrize('stage', [
    'preview',
    'published',
])
@pytest.mark.django_db
def test_can_filter_on_digest_stage(stage: str, 
                                    auth_header: Dict, 
                                    client: Client,
                                    digest: Digest, 
                                    published_digest: Digest):
    response = client.get(f'{DIGESTS_URL}?stage={stage}', 
                          **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE}, **auth_header)
    assert response.status_code == 200
    assert response.data['total'] == 1
    assert response.data['items'][0]['stage'] == stage

