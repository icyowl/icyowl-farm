from flask import Blueprint, redirect, render_template, request, url_for
from farm.auth import login_required

# from flask_wtf import FlaskForm
# # from wtforms import StringField, IntegerField
# from wtforms.fields import DateField, RadioField
# from datetime import datetime
from bson.objectid import ObjectId

from farm.db import Dao
dao = Dao()

bp = Blueprint('fields', __name__, url_prefix='/fields')


@bp.route('/docs/<idx>/', methods=['GET', 'POST'])
@login_required
def docs(idx):
    return render_template('fields.html', idx=idx)