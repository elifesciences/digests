from typing import Dict, List

import pytest

from digests.models import Digest, PUBLISHED


@pytest.mark.django_db
def test_can_create_digest(digest: Digest,
                           digest_json: Dict,
                           digest_image_json: Dict,
                           digest_content_json: List[Dict],
                           digest_related_content_json: List[Dict],
                           digest_subjects_json: List[Dict]):
    assert digest
    assert digest.id == '2'
    assert digest.title == 'Neighborhood watch'
    assert digest.published == "2018-07-06T09:06:01Z"
    assert digest.updated == "2018-07-06T16:23:24Z"
    assert digest.content == digest_content_json
    assert digest.image == digest_image_json
    assert digest.relatedContent == digest_related_content_json
    assert digest.stage == 'preview'
    assert digest.subjects == digest_subjects_json
    assert digest.impactStatement == digest_json['impactStatement']


@pytest.mark.django_db
def test_can_set_stage_to_published(digest: Digest):
    digest.stage = PUBLISHED
    digest.save()
    assert digest.stage == PUBLISHED
