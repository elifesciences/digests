from copy import deepcopy
import json
from typing import Dict

from django.conf import settings
import pytest
from rest_framework.test import APIClient

from digests.models import Digest

DIGESTS_URL = '/digests'


@pytest.mark.parametrize('key, value', [
    ('title', 'Some New Title'),
    ('impactStatement', 'New Impact Statement'),
    ('stage', 'published'),
    ('published', '2019-07-06T09:06:01Z'),
])
@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-01 00:00:00')
def test_can_update_digest_via_patch(key: str,
                                     value: str,
                                     digest: Digest,
                                     digest_json: Dict,
                                     rest_client: APIClient):
    response = rest_client.patch(f'{DIGESTS_URL}/{digest.id}',
                                 data=json.dumps({key: value}),
                                 content_type=settings.DIGEST_CONTENT_TYPE)
    assert response.status_code == 200
    assert response.data[key] == value
    assert response.data['updated'] == '2018-01-01T00:00:00Z'


@pytest.mark.django_db
def test_wont_update_digest_id_via_patch(digest: Digest,
                                         digest_json: Dict,
                                         rest_client: APIClient):
    new_id = 'Some new id'
    response = rest_client.patch(f'{DIGESTS_URL}/{digest.id}',
                                 data=json.dumps({'id': new_id}),
                                 content_type=settings.DIGEST_CONTENT_TYPE)
    assert response.status_code == 200
    assert response.data['id'] != new_id
