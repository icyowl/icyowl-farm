from flask import template_rendered
from farm.sidebar import inject_page


def test_crop(client, auth):
    auth.login()
    response = client.get(f'/crop')
    assert response.headers["Location"] == '/'
    with client.session_transaction() as session:
        assert session['field'] == 0


def test_vegetable(client, auth):
    auth.login()
    response = client.get(f'/vegetable')
    assert response.headers["Location"] == '/'
    with client.session_transaction() as session:
        assert session['field'] == 1


def test_other(client, auth):
    auth.login()
    response = client.get(f'/other')
    assert response.headers["Location"] == '/'
    with client.session_transaction() as session:
        assert session['field'] == 2


def test_context_processor(client, auth, app):
    auth.login()
    response = client.get(f'/crop')
    assert response.headers["Location"] == '/'
    # Flaskのsignalでテンプレートレンダリングを監視
    recorded = {}
    def record(sender, template, context, **extra):
        recorded['context'] = context

    with template_rendered.connected_to(record, app):
        response = client.get('/')
        print(recorded['context']['items'])  # .[{'species': 'ライムギ', 'id': '681b65ed44a08736933c6f93'}]


# def test_inject_page(client, auth, app):
#     auth.login()
#     response = client.get(f'/vegetable')
#     with client.session_transaction() as session:
#         assert session['field'] == 1
#         with app.test_request_context('/vegetable', method='GET'):
#             res = inject_page()
#             print(res)  # -> {}





    

