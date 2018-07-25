from typing import Dict, List

from django.conf import settings
from django.test.client import Client
import pytest

from digests.models import Digest


@pytest.mark.django_db
def test_can_get_digest(client: Client):
    response = client.get('/digests')
    assert response.status_code == 200


@pytest.mark.django_db
def test_has_expected_data_in_response(client: Client,
                                       digest: Digest,
                                       digest_image_json: Dict,
                                       digest_content_json: List[Dict],
                                       digest_related_content_json: List[Dict],
                                       digest_subjects_json: List[Dict]):
    response = client.get('/digests')
    data = response.data[0]
    assert len(response.data) == 1
    assert data['id'] == '2'
    assert data['title'] == 'Neighborhood watch'
    assert data['published'] == "2018-07-06T09:06:01Z"
    assert data['updated'] == "2018-07-06T16:23:24Z"
    assert data['image'] == digest_image_json
    assert data['subjects'] == digest_subjects_json
    assert data['content'] == digest_content_json
    assert data['relatedContent'] == digest_related_content_json


@pytest.mark.django_db
def test_has_digest_content_type_header(client: Client):
    response = client.get('/digests')
    assert response.status_code == 200
    assert response.content_type == settings.DIGESTS_CONTENT_TYPE
