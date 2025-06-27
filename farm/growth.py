from flask import Blueprint, redirect, render_template, request, url_for
from farm.auth import login_required

from flask_wtf import FlaskForm
# from wtforms import StringField, IntegerField
from wtforms.fields import DateField, RadioField
from datetime import datetime
from bson.objectid import ObjectId

from farm.db import Dao
dao = Dao()

bp = Blueprint('growth', __name__, url_prefix='/growth')

class GrowthForm(FlaskForm):
    date = DateField('Date')
    work = RadioField('work', choices=[(0, '播種'), (1, '植付'), (2, '定植')])


def set_title(dt: datetime, i: int):
    dt_s = dt.strftime('%Y/%m/%d')
    s = ['播種', '植付', '定植'][i]
    return ' '.join((dt_s, s))


@bp.route('/create/<id>/<variety>', methods=['GET', 'POST'])
@login_required
def create(id, variety):
    form = GrowthForm()
    if request.method == 'POST':
        dt = form.date.data
        i = int(form.work.data)
        title = set_title(dt, i)
        _id = str(ObjectId())
        data = {
            '_id': _id,
            'parent': id,
            'title': title
            }
        dao.create_growth(data)
        return redirect(url_for('growth.growth_records', id=_id))

    return render_template('forms/growth.html', form=form, variety=variety)

@bp.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    found = dao.read_growth(id)
    parent = found['parent']
    variety = dao.get_variety(parent)
    title = found['title']
    dt_s, s = title.split()
    date = datetime.strptime(dt_s, '%Y/%m/%d').date()
    i = ['播種', '植付', '定植'].index(s)
    form = GrowthForm()
    if request.method == 'POST':
        dt = form.date.data
        i = int(form.work.data)
        title = set_title(dt, i)
        found['title'] = title
        dao.update_growth(id, found)
        return redirect(url_for('index'))
    return render_template('forms/growth.html',
                                id=id,
                                variety=variety,
                                form=form,
                                date=date, 
                                work=i
                            )


@bp.route('/records/<id>', methods=['GET', 'POST'])
@login_required
def growth_records(id):
    found = dao.read_growth(id)
    growth = found['title']
    parent = found['parent']
    variety = dao.get_variety(parent)
    records = dao.get_records(id)
    return render_template('records.html',
                                id=id,
                                variety=variety,
                                growth=growth,
                                records=records
                            )


@bp.route('/delete/<id>')
@login_required
def delete(id):
    dao.delete_growth(id)
    return redirect(url_for('index'))