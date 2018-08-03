from typing import Dict, List

import pytest

from digests.models import Digest, PUBLISHED


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-01 00:00:00')
def test_can_create_digest(preview_digest: Digest,
                           digest_json: Dict,
                           digest_image_json: Dict,
                           digest_content_json: List[Dict],
                           digest_related_content_json: List[Dict],
                           digest_subjects_json: List[Dict]):
    digest = preview_digest
    assert digest
    assert digest.id == '2'
    assert digest.title == 'Neighborhood watch'
    assert digest.published == "2018-07-06T09:06:01Z"
    assert str(digest.updated) == '2018-01-01 00:00:00+00:00'
    assert digest.content == digest_content_json
    assert digest.image == digest_image_json
    assert digest.relatedContent == digest_related_content_json
    assert digest.stage == 'preview'
    assert digest.subjects == digest_subjects_json
    assert digest.impactStatement == digest_json['impactStatement']


@pytest.mark.django_db
def test_can_set_stage_to_published(preview_digest: Digest):
    preview_digest.stage = PUBLISHED
    preview_digest.save()
    assert preview_digest.stage == PUBLISHED
