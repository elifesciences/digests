from typing import Dict

from django.conf import settings
from django.test.client import Client
import pytest

from digests.models import Digest

DIGESTS_URL = '/digests'


@pytest.mark.django_db
def test_can_filter_by_article_id(can_preview_header: Dict,
                                  client: Client,
                                  preview_digest: Digest,
                                  digest_json: Dict,
                                  digest_related_content_json: Dict):
    article_id = digest_related_content_json[0]['id']
    response = client.get(f'{DIGESTS_URL}?article={article_id}',
                          **{'ACCEPT': settings.DIGEST_CONTENT_TYPE},
                          **can_preview_header)
    assert response.data['total'] == 1
    assert response.data['items'][0]['id'] == preview_digest.id
    assert response.data['items'][0]['relatedContent'][0]['id'] == article_id


@pytest.mark.django_db
def test_will_return_empty_if_article_id_not_found(can_preview_header: Dict,
                                                   client: Client,
                                                   preview_digest: Digest,
                                                   digest_json: Dict):
    article_id = '123456'
    response = client.get(f'{DIGESTS_URL}?article={article_id}',
                          **{'ACCEPT': settings.DIGEST_CONTENT_TYPE},
                          **can_preview_header)
    assert response.data['total'] == 0


@pytest.mark.django_db
def test_will_find_by_article_id_if_not_first_item(can_preview_header: Dict,
                                                   client: Client,
                                                   preview_digest: Digest,
                                                   multiple_related_content_json: Dict):
    preview_digest.relatedContent = multiple_related_content_json
    preview_digest.save()

    article_id = multiple_related_content_json[1]['id']
    response = client.get(f'{DIGESTS_URL}?article={article_id}',
                          **{'ACCEPT': settings.DIGEST_CONTENT_TYPE},
                          **can_preview_header)
    assert response.data['total'] == 1
    assert response.data['items'][0]['id'] == preview_digest.id
    assert response.data['items'][0]['relatedContent'][1]['id'] == article_id
