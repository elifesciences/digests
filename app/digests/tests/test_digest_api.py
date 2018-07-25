from django.test.client import Client
import pytest


@pytest.mark.django_db
def test_can_get_article_list_xml(client: Client):
    response = client.get('/digests')
    assert response.status_code == 200
