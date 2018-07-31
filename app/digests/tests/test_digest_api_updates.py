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
@pytest.mark.freeze_time('2018-01-01 00:00:00')
def test_wont_update_digest_id_via_patch(digest: Digest,
                                         digest_json: Dict,
                                         rest_client: APIClient):
    new_id = '123456'
    response = rest_client.patch(f'{DIGESTS_URL}/{digest.id}',
                                 data=json.dumps({'id': new_id}),
                                 content_type=settings.DIGEST_CONTENT_TYPE)
    assert response.status_code == 200
    assert response.data['id'] != new_id


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-01 00:00:00')
def test_can_update_digest_content_via_patch(digest: Digest,
                                             digest_content_json: Dict,
                                             rest_client: APIClient):
    new_content = deepcopy(digest_content_json)
    new_text = 'foo'
    new_content[0]['text'] = new_text
    response = rest_client.patch(f'{DIGESTS_URL}/{digest.id}',
                                 data=json.dumps({'content': new_content}),
                                 content_type=settings.DIGEST_CONTENT_TYPE)
    assert response.status_code == 200
    assert response.data['content'][0]['text'] == new_text


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-01 00:00:00')
def test_can_update_digest_related_content_via_patch(digest: Digest,
                                                     digest_related_content_json: Dict,
                                                     rest_client: APIClient):
    new_content = deepcopy(digest_related_content_json)
    new_text = 'foo'
    new_content[0]['title'] = new_text
    response = rest_client.patch(f'{DIGESTS_URL}/{digest.id}',
                                 data=json.dumps({'relatedContent': new_content}),
                                 content_type=settings.DIGEST_CONTENT_TYPE)
    assert response.status_code == 200
    assert response.data['relatedContent'][0]['title'] == new_text


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-01 00:00:00')
def test_can_update_digest_subjects_via_patch(digest: Digest,
                                              digest_subjects_json: Dict,
                                              rest_client: APIClient):
    new_subjects = deepcopy(digest_subjects_json)
    new_name = 'foo'
    new_subjects[0]['name'] = new_name
    response = rest_client.patch(f'{DIGESTS_URL}/{digest.id}',
                                 data=json.dumps({'subjects': new_subjects}),
                                 content_type=settings.DIGEST_CONTENT_TYPE)
    assert response.status_code == 200
    assert response.data['subjects'][0]['name'] == new_name


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-01 00:00:00')
def test_can_update_digest_image_via_patch(digest: Digest,
                                           digest_image_json: Dict,
                                           rest_client: APIClient):
    new_image = deepcopy(digest_image_json)
    new_alt = 'some alt'
    new_image['thumbnail']['alt'] = new_alt
    response = rest_client.patch(f'{DIGESTS_URL}/{digest.id}',
                                 data=json.dumps({'image': new_image}),
                                 content_type=settings.DIGEST_CONTENT_TYPE)
    assert response.status_code == 200
    assert response.data['image']['thumbnail']['alt'] == new_alt


@pytest.mark.parametrize('key, value', [
    ('image', {}),
    ('subjects', [{"foo": "bar"}]),
    ('content', []),
    ('relatedContent', {}),
])
@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-01 00:00:00')
def test_will_reject_invalid_json_field_updates(key: str,
                                                value: str,
                                                digest: Digest,
                                                digest_json: Dict,
                                                rest_client: APIClient):
    response = rest_client.patch(f'{DIGESTS_URL}/{digest.id}',
                                 data=json.dumps({key: value}),
                                 content_type=settings.DIGEST_CONTENT_TYPE)
    assert response.status_code == 400


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-01 00:00:00')
def test_can_update_digest_via_put(digest: Digest,
                                   digest_json: Dict,
                                   rest_client: APIClient):
    new_data = deepcopy(digest_json)
    new_data['title'] = 'New Title'
    new_data['stage'] = 'published'

    response = rest_client.put(f'{DIGESTS_URL}/{digest.id}',
                               data=json.dumps(new_data),
                               content_type=settings.DIGEST_CONTENT_TYPE)
    assert response.status_code == 200
    assert response.data['title'] == 'New Title'
    assert response.data['stage'] == 'published'
    assert response.data['updated'] == '2018-01-01T00:00:00Z'


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-01 00:00:00')
def test_reject_invalid_data_via_put(digest: Digest,
                                     digest_json: Dict,
                                     rest_client: APIClient):
    new_data = deepcopy(digest_json)
    new_data['content'] = {}
    new_data['image'] = {}

    response = rest_client.put(f'{DIGESTS_URL}/{digest.id}',
                               data=json.dumps(new_data),
                               content_type=settings.DIGEST_CONTENT_TYPE)
    assert response.status_code == 400
