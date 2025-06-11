from flask import Blueprint, redirect, render_template, request, url_for
from farm.auth import login_required

from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, DateTimeLocalField
# from wtforms.fields import DateTimeField, RadioField
from datetime import datetime
from bson.objectid import ObjectId

import base64
import io 
from PIL import Image

from farm.db import Dao
dao = Dao()

bp = Blueprint('records', __name__, url_prefix='/records')

class RecordsForm(FlaskForm):
    date = DateTimeLocalField('Date')
    title = StringField('Title')
    description = StringField('Desc')


def encode_and_resize(file = None) -> str:
    '''usage
    file = request.files['uploadFile']
    b64_img = encode_and_resize(file)
    '''
    encoded = ''
    if file:
        img = file.read()
        if img:
            img_pil = Image.open(io.BytesIO(img))
            img_resize = img_pil.resize((350, 263), Image.LANCZOS)
            img_io = io.BytesIO()
            img_resize.save(img_io, format="JPEG")
            jpeg_bytes = img_io.getvalue()
            encoded = base64.b64encode(jpeg_bytes).decode('utf-8')

    return encoded

@bp.route('/create/<id>/', methods=['GET', 'POST'])  # growth_id
def create(id):
    form = RecordsForm()
    variety, growth = dao.get_variety_and_growth(id)
    if request.method == 'POST':
        file = request.files['uploadFile']
        # encoded = ''
        # if file:
        #     img = file.read()
        #     if img:
        #         encoded = base64.b64encode(img).decode('utf-8')
        encoded = encode_and_resize(file)
        data = {
            'parent': id,
            'date': form.date.data,
            'title': form.title.data,
            'description': form.description.data,
            'image': encoded
        }
        dao.create_record(data)

        return redirect(url_for('growth.growth_records', id=id))
    return render_template('forms/records.html', form=form, variety=variety, growth=growth)


@bp.route('/update/<id>/', methods=['GET', 'POST'])  # record_id
def update(id):
    doc = dao.read_record(id)
    growth_id = doc['parent']
    variety, growth = dao.get_variety_and_growth(growth_id)
    date = doc['date']
    title = doc['title']
    description = doc['description']
    form = RecordsForm()
    if request.method == 'POST':
        data = {
            # 'parent': growth_id,
            'date': form.date.data,
            'title': form.title.data,
            'description': form.description.data
        }
        file = request.files['uploadFile']
        if file:
            encoded = encode_and_resize(file)
            data['image'] = encoded
        dao.update_record(id, data)
        return redirect(url_for('growth.growth_records', id=growth_id))

    return render_template('forms/records.html',
                                form=form,
                                id=id,
                                variety=variety,
                                growth=growth,
                                date=date,
                                title=title,
                                description=description
                            )
