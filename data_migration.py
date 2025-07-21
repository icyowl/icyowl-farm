# from farm.models import Species, Variety, Growth, Records, Document
import configparser
import os
from pymongo import MongoClient


config = configparser.ConfigParser()
p = os.path.abspath(os.path.join('instance', 'config.ini'))
config.read(p)

uri = config['PROD']['DB_URI']
print(uri)
client = MongoClient(uri)

cur = client.farm.users.find()

uri = config['DEV']['DB_URI']
print(uri)
atlas = MongoClient(uri)

atlas.farm.users.insert_many(cur)
