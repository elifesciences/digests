import json
from typing import Dict
from unittest.mock import patch, MagicMock

from django.conf import settings
import pytest
from rest_framework.test import APIClient

from digests.models import Digest

DIGESTS_URL = '/digests'


@pytest.mark.django_db(transaction=True)
@patch('digests.api.event_publisher')
def test_can_send_event_when_creating_a_digest(event_publisher: MagicMock,
                                               rest_client: APIClient,
                                               digest_json: Dict,
                                               can_edit_headers: Dict):
    response = rest_client.post(DIGESTS_URL, data=json.dumps(digest_json),
                                content_type=settings.DIGEST_CONTENT_TYPE,
                                **can_edit_headers)
    assert response.status_code == 201

    assert event_publisher.assert_called
    assert event_publisher.publish.call_args[0] == (
        {'id': digest_json['id'], 'type': 'digest'},
    )


@pytest.mark.django_db(transaction=True)
@patch('digests.api.event_publisher')
def test_can_send_event_when_patching_a_digest(event_publisher: MagicMock,
                                               can_edit_headers: Dict,
                                               preview_digest: Digest,
                                               digest_json: Dict,
                                               rest_client: APIClient):
    response = rest_client.patch(f'{DIGESTS_URL}/{preview_digest.id}',
                                 data=json.dumps({'stage': 'published'}),
                                 content_type=settings.DIGEST_CONTENT_TYPE,
                                 **can_edit_headers)
    assert response.status_code == 204
    assert event_publisher.assert_called
    assert event_publisher.publish.call_args[0] == (
        {'id': digest_json['id'], 'type': 'digest'},
    )


@pytest.mark.django_db(transaction=True)
@patch('digests.api.event_publisher')
def test_can_send_event_when_updating_a_digest_via_put(event_publisher: MagicMock,
                                                       can_edit_headers: Dict,
                                                       preview_digest: Digest,
                                                       digest_json: Dict,
                                                       rest_client: APIClient):
    response = rest_client.put(f'{DIGESTS_URL}/{preview_digest.id}',
                               data=json.dumps(digest_json),
                               content_type=settings.DIGEST_CONTENT_TYPE,
                               **can_edit_headers)
    assert response.status_code == 204
    assert event_publisher.assert_called
    assert event_publisher.publish.call_args[0] == (
        {'id': digest_json['id'], 'type': 'digest'},
    )
