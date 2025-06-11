from farm.models import PyObjectId, Species
from farm.db import mongo
import pytest


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


def test_Species(setup):
    data = {
        'field': 0, 
        'family': 'test-poaceae', 
        'species': 'test-wheat',
        'sort_key': 1
    }
    res = Species(**data)
    print(res)
    assert res.id is None
    doc = mongo.db.species.find_one({'family': 'test-poaceae'})
    res = Species.from_mongo(doc)
    d = res.model_dump()
    d.pop('id')
    print(d)