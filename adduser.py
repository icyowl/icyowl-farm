import os
import configparser
from pymongo import MongoClient
from werkzeug.security import generate_password_hash


config = configparser.ConfigParser()
config.read(os.path.abspath('instance/config.ini'))
uri = config['DEV']['DB_URI']  # DEV(net) or PROD(local)

client = MongoClient(uri)
# db = client['test_db']
db = client['farm']

if 0:
    username = 'Matt'
    password = 'mockturtle'
    pw_hash = generate_password_hash(password)

    usr = {'username': username, 'password': pw_hash}
    db.users.insert_one(usr)

    print(list(db.users.find())[-1])
else:
    print('if 0 ..')
    