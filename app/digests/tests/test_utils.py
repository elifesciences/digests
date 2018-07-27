import pytest

from digests.utils import get_schema_name


@pytest.mark.parametrize('content_type, schema_name', [
    ('application/vnd.elife.digest+json; version=1', 'digest.v1.json'),
    ('application/vnd.elife.digest+json; version=2', 'digest.v2.json'),
    ('application/vnd.elife.digest+json; version=3', 'digest.v3.json'),
    ('application/vnd.elife.digest+json', 'digest.v1.json'),
])
def test_can_get_schema_name(content_type: str, schema_name: str):
    assert get_schema_name(content_type) == schema_name
