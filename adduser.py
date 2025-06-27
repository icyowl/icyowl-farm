import os
import configparser
from pymongo import MongoClient
from werkzeug.security import generate_password_hash


config = configparser.ConfigParser()
config.read(os.path.abspath('instance/config.ini'))
uri = config['PROD']['DB_URI']  # DEV or PROD

client = MongoClient(uri)
# db = client['test_db']
db = client['farm']

if 0:
    username = 'Alice'
    password = 'mockturtle'
    pw_hash = generate_password_hash(password)

    usr = {'username': username, 'password': pw_hash}
    db.users.insert_one(usr)

    print(list(db.users.find())[-1])
    