from copy import deepcopy
from typing import Dict

import pytest
from rest_framework.test import APIClient

DIGESTS_URL = '/digests'


@pytest.mark.django_db
def test_returns_400_for_missing_image_data(rest_client: APIClient,
                                            digest_json: Dict):
    data = deepcopy(digest_json)
    del data['image']
    response = rest_client.post(DIGESTS_URL, data=data, format='json')
    assert response.status_code == 400
    assert response.data['error'] == "'image' is a required property"


@pytest.mark.django_db
def test_returns_400_for_invalid_image_data(rest_client: APIClient,
                                            digest_json: Dict):
    data = deepcopy(digest_json)
    del data['image']['thumbnail']['source']['uri']
    response = rest_client.post(DIGESTS_URL, data=data, format='json')
    assert response.status_code == 400
    assert response.data['error'] == "image.thumbnail.source = 'uri' is a required property"


@pytest.mark.django_db
def test_returns_400_for_invalid_subject_data(rest_client: APIClient,
                                              digest_json: Dict):
    data = deepcopy(digest_json)
    del data['subjects'][0]['id']
    response = rest_client.post(DIGESTS_URL, data=data, format='json')
    assert response.status_code == 400
    assert response.data['error'] == "subjects.0 = 'id' is a required property"


@pytest.mark.django_db
def test_returns_400_for_missing_content_data(rest_client: APIClient,
                                              digest_json: Dict):
    data = deepcopy(digest_json)
    del data['content']
    response = rest_client.post(DIGESTS_URL, data=data, format='json')
    assert response.status_code == 400
    assert response.data['error'] == "'content' is a required property"


@pytest.mark.django_db
def test_returns_400_for_invalid_content_data(rest_client: APIClient,
                                              digest_json: Dict):
    data = deepcopy(digest_json)
    data['content'][0] = {'foo': 'bar'}
    response = rest_client.post(DIGESTS_URL, data=data, format='json')
    assert response.status_code == 400
    assert response.data['error'] == "content.0 = {'foo': 'bar'} is not valid under any of the given schemas"
