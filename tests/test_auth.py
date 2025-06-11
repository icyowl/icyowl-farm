import pytest
from flask import g, session


def test_login(client, auth):
    assert client.get('auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_load_logged_in_user(client, auth):
    auth.login()
    with client:
        client.get('/')  # inside of request context
        assert 'user_id' in session
        assert g.user['username'] == 'test'


def test_logout(client, auth):
    auth.login()
    auth.logout()
    with client:
        client.get('/')
        assert not 'user_id' in session
        assert g.user is None


def test_login_required(client):
    with client:
        client.get('/')
        msg = session['_flashes'][0]
        assert msg == ('message', 'Please log in to access this page.')

