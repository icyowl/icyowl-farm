import pytest
from farm.db import mongo


@pytest.fixture
def setup(app):
    data = {
        'field': 0, 
        'family': 'test-poaceae', 
        'species': 'test-wheat',
        'sort_key': 1
    }
    mongo.db.species.insert_one(data)
    yield
    filter = {'family': 'test-poaceae'}
    if mongo.db.species.count_documents(filter):
        mongo.db.species.delete_many(filter)


def test_create_species(setup, client, auth, app):
    auth.login()
    assert client.get('/species/create').status_code == 200
    client.post('/species/create', data={
                                            'field': 0, 
                                            'family': 'test-poaceae', 
                                            'species': 'test-barley',
                                            'sort_key': 2
                                            })
    assert mongo.db.species.count_documents({'family': 'test-poaceae'}) == 2


def test_update_species(setup, client, auth, app):
    auth.login()
    doc = mongo.db.species.find_one({'species': 'test-wheat'})
    id = str(doc['_id'])
    assert client.get(f'/species/update/{id}').status_code == 200
    client.post(f'/species/update/{id}', data={
                                            'field': 0, 
                                            'family': 'test-poaceae', 
                                            'species': 'update-wheat',
                                            'sort_key': 1
                                            })
    filter = {'family': 'test-poaceae'}
    updated = mongo.db.species.find_one(filter, {'_id': 0, 'species': 1})
    assert mongo.db.species.count_documents(filter) == 1
    assert updated == {'species': 'update-wheat'}


def test_delete_species(setup, client, auth, app):
    auth.login()
    doc = mongo.db.species.find_one({'family': 'test-poaceae'})
    id = str(doc['_id'])
    response = client.get(f'/species/delete/{id}')
    assert response.headers["Location"] == '/'
    assert mongo.db.species.count_documents({'family': 'test-poaceae'}) == 0
