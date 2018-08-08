from typing import Dict

from django.conf import settings
from django.test.client import Client
import pytest

DIGESTS_URL = '/digests'


@pytest.mark.django_db
def test_has_private_cache_control_when_authenticated(can_preview_header: Dict,
                                                      client: Client):
    response = client.get(DIGESTS_URL,
                          **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE},
                          **can_preview_header)
    assert response.status_code == 200
    assert response['cache-control'] == 'private, max-age=0, must-revalidate'


@pytest.mark.django_db
def test_has_public_cache_control_when_unauthenticated(client: Client):
    response = client.get(DIGESTS_URL,
                          **{'ACCEPT': settings.DIGESTS_CONTENT_TYPE})
    assert response.status_code == 200
    assert response['cache-control'] == 'public, max-age=300, ' \
                                        'stale-while-revalidate=300, ' \
                                        'stale-if-error=86400'
