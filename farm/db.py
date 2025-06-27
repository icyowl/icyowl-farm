from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from farm.models import Species, Variety, Growth, Records, Document

mongo = PyMongo()

def init_db(app):  # app.config["MONGO_URI"] は app.py 側で設定
    mongo.init_app(app)


class Dao:
    def __init__(self):
        pass

    # Species
    def create_species(self, data):
        d = Species(**data).to_mongo()  # validation
        mongo.db.species.insert_one(d)

    def read_species(self, id):
        return mongo.db.species.find_one({'_id': ObjectId(id)})

    def update_species(self, id, data):
        doc = Species.from_mongo(data) # validation
        d = doc.model_dump()
        _ = d.pop('id')
        mongo.db.species.update_one({'_id': ObjectId(id)}, {'$set': d})

    def delete_species(self, id):
        mongo.db.species.delete_one({'_id': ObjectId(id)})

    def count_variety(self, id):
        return mongo.db.variety.count_documents({'parent': {'$eq': id}})

    # Variety
    def create_variety(self, data):
        d = Variety(**data).to_mongo()  # validation
        mongo.db.variety.insert_one(d)

    def read_variety(self, id):
        return mongo.db.variety.find_one({'_id': ObjectId(id)})

    def update_variety(self, id, data):
        doc = Variety.from_mongo(data) # validation
        d = doc.model_dump()
        _ = d.pop('id')
        mongo.db.variety.update_one({'_id': ObjectId(id)}, {'$set': d})

    def delete_variety(self, id):
        mongo.db.variety.delete_one({'_id': ObjectId(id)})

    def get_field_index(self, id: str) -> int:
        d = self.read_variety(id)
        parent = d['parent']
        s = mongo.db.species.find_one({'_id': ObjectId(parent)})
        return s['field']

    def get_field_index_by_species_id(self, id: str):
        s = self.read_species(id)
        return s['field']


    def count_growth(self, id):
        return mongo.db.growth.count_documents({'parent': {'$eq': id}})


    # Growth
    def create_growth(self, data):
        d = Growth(**data).to_mongo()  # validation
        mongo.db.growth.insert_one(d)

    def read_growth(self, id):
        return mongo.db.growth.find_one({'_id': ObjectId(id)})

    def update_growth(self, id, data):
        doc = Growth.from_mongo(data) # validation
        d = doc.model_dump()
        _ = d.pop('id')
        mongo.db.growth.update_one({'_id': ObjectId(id)}, {'$set': d})

    def delete_growth(self, id):
        mongo.db.records.delete_many({'parent': id})
        mongo.db.growth.delete_one({'_id': ObjectId(id)})

    # 
    def get_variety(self, id: str):
        d = mongo.db.variety.find_one({'_id': ObjectId(id)}, {'_id': 0, 'variety': 1})
        return d['variety']
    
    def get_variety_and_growth(self, id: str):
        d = mongo.db.growth.find_one({'_id': ObjectId(id)}, {'_id': 0, 'parent': 1, 'title': 1})
        variety = self.get_variety(d['parent'])
        growth = d['title']
        return variety, growth

    def get_records(self, id: str):
        cur = mongo.db.records.find({'parent': id}).sort({'date': 1})
        return list(cur)

    # Records
    def create_record(self, data):
        dic = Records(**data).to_mongo()  # validation
        mongo.db.records.insert_one(dic)

    def read_record(self, id: str):
        return mongo.db.records.find_one({'_id': ObjectId(id)})

    def update_record(self, id, data):
        # doc = Records.from_mongo(data) # validation
        mongo.db.records.update_one({'_id': ObjectId(id)}, {'$set': data})

    def  delete_record(self, id):
        mongo.db.records.delete_one({'_id': ObjectId(id)})

    # document
    def create_document(self, data):
        d = Document(**data).to_mongo()
        mongo.db.document.insert_one(d)

    def read_document(self, parent_id):
        return mongo.db.document.find_one({'parent': parent_id})

    def update_document(self, id, data):
        mongo.db.document.update_one({'_id': ObjectId(id)}, {'$set': data})
