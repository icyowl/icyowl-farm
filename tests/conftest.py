import pytest
from farm import create_app


@pytest.fixture
def app():
    test_config = {'TESTING': True}
    app = create_app(test_config)
    return app


@pytest.fixture
def client(app):
    return app.test_client()
    # yield test_client
    # test_client.delete()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)