from copy import deepcopy
import json
from typing import Dict

from django.conf import settings
import pytest
from rest_framework.test import APIClient

DIGESTS_URL = '/digests'


@pytest.mark.django_db
def test_returns_400_for_missing_image_data(can_edit_headers: Dict,
                                            rest_client: APIClient,
                                            digest_json: Dict):
    data = deepcopy(digest_json)
    del data['image']
    response = rest_client.post(DIGESTS_URL, data=json.dumps(data),
                                content_type=settings.DIGEST_CONTENT_TYPE,
                                **can_edit_headers)
    assert response.status_code == 400
    assert response.data['title'] == "'image' is a required property"
    assert response.content_type == settings.ERROR_CONTENT_TYPE


@pytest.mark.django_db
def test_returns_400_for_invalid_image_data(can_edit_headers: Dict,
                                            rest_client: APIClient,
                                            digest_json: Dict):
    data = deepcopy(digest_json)
    del data['image']['thumbnail']['source']['uri']
    response = rest_client.post(DIGESTS_URL, data=json.dumps(data),
                                content_type=settings.DIGEST_CONTENT_TYPE,
                                **can_edit_headers)
    assert response.status_code == 400
    assert response.data['title'] == "image.thumbnail.source = 'uri' is a required property"
    assert response.content_type == settings.ERROR_CONTENT_TYPE


@pytest.mark.django_db
def test_returns_400_for_invalid_subject_data(can_edit_headers: Dict,
                                              rest_client: APIClient,
                                              digest_json: Dict):
    data = deepcopy(digest_json)
    del data['subjects'][0]['id']
    response = rest_client.post(DIGESTS_URL, data=json.dumps(data),
                                content_type=settings.DIGEST_CONTENT_TYPE,
                                **can_edit_headers)
    assert response.status_code == 400
    assert response.data['title'] == "subjects.0 = 'id' is a required property"
    assert response.content_type == settings.ERROR_CONTENT_TYPE


@pytest.mark.django_db
def test_returns_400_for_missing_content_data(can_edit_headers: Dict,
                                              rest_client: APIClient,
                                              digest_json: Dict):
    data = deepcopy(digest_json)
    del data['content']
    response = rest_client.post(DIGESTS_URL, data=json.dumps(data),
                                content_type=settings.DIGEST_CONTENT_TYPE,
                                **can_edit_headers)
    assert response.status_code == 400
    assert response.data['title'] == "'content' is a required property"
    assert response.content_type == settings.ERROR_CONTENT_TYPE


@pytest.mark.django_db
def test_returns_400_for_invalid_content_data(can_edit_headers: Dict,
                                              rest_client: APIClient,
                                              digest_json: Dict):
    data = deepcopy(digest_json)
    data['content'][0] = {'foo': 'bar'}
    response = rest_client.post(DIGESTS_URL, data=json.dumps(data),
                                content_type=settings.DIGEST_CONTENT_TYPE,
                                **can_edit_headers)
    assert response.status_code == 400
    assert response.data['title'] == "content.0 = {'foo': 'bar'} is not valid under any of the given schemas"
    assert response.content_type == settings.ERROR_CONTENT_TYPE
