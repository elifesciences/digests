

def test_can_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response['cache-control'] == 'must-revalidate, no-cache, ' \
                                        'no-store, private'
