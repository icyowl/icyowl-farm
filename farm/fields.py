from flask import Blueprint, redirect, render_template, request, url_for
from farm.auth import login_required

# from flask_wtf import FlaskForm
# # from wtforms import StringField, IntegerField
# from wtforms.fields import DateField, RadioField
# from datetime import datetime
from bson.objectid import ObjectId

from farm.db import Dao, mongo
dao = Dao()

bp = Blueprint('fields', __name__, url_prefix='/fields')


@bp.route('/documents/<idx>/', methods=['GET', 'POST'])
@login_required
def documents(idx):
    i = int(idx)
    docs = []
    cur = mongo.db.species.find({'field': i})
    for d in cur:
        s_id = d['_id']
        cu = mongo.db.variety.find({'parent': str(s_id)})
        for v in cu:
            v_id = v['_id']
            doc = mongo.db.document.find_one({'parent': str(v_id)})
            variety_id = str(v_id)
            variety = doc['variety']
            text = doc['document']
            # print(text.split('\r\n'))
            excerpt = text.split('\r\n')[0]
            docs.append((variety_id, variety, excerpt))
    return render_template('fields.html', idx=idx, docs=docs)