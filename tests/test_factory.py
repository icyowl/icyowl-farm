from farm import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_index(client):
    response = client.get('/')
    assert response.status_code == 302
    assert not response.data == b'Page Not Found'