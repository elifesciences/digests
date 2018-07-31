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
def test_has_expected_data_in_response(client: Client,
                                       digest: Digest,
                                       digest_image_json: Dict,
                                       digest_content_json: List[Dict],
                                       digest_related_content_json: List[Dict],
                                       digest_subjects_json: List[Dict]):
    response = client.get(DIGESTS_URL, **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE})
    data = response.data['items'][0]
    assert response.data['total'] == 1
    assert len(response.data['items']) == 1
    assert data['id'] == '2'
    assert data['title'] == 'Neighborhood watch'
    assert data['published'] == "2018-07-06T09:06:01Z"
    assert data['updated'] == "2018-07-06T16:23:24Z"
    assert data['image'] == digest_image_json
    assert data['subjects'] == digest_subjects_json
    assert data['content'] == digest_content_json
    assert data['relatedContent'] == digest_related_content_json


@pytest.mark.django_db
def test_can_get_digest_by_id(client: Client,
                              digest: Digest,
                              digest_json: Dict):
    response = client.get(f'{DIGESTS_URL}/{digest.id}', **{'ACCEPT': settings.DIGEST_CONTENT_TYPE})
    assert response.data == digest_json
    assert response.content_type == settings.DIGEST_CONTENT_TYPE


@pytest.mark.django_db
def test_has_digests_content_type_header(client: Client):
    response = client.get(DIGESTS_URL, **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE})
    assert response.status_code == 200
    assert response.content_type == settings.DIGESTS_CONTENT_TYPE


@pytest.mark.django_db
def test_can_ingest_digest(rest_client: APIClient, digest_json: Dict):
    response = rest_client.post(DIGESTS_URL, data=json.dumps(digest_json),
                                content_type=settings.DIGEST_CONTENT_TYPE)
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

    response = client.get(DIGESTS_URL, **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE})
    assert response.status_code == 200

    # check most recently published digest is first
    assert response.data['items'][0]['id'] == '10'
    assert response.data['items'][0]['published'] == new_pub_date

