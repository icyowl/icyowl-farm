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
    work = RadioField('work', choices=[(0, '播種'), (1, '定植')])


def set_title(dt: datetime, i: int):
    dt_s = dt.strftime('%Y/%m/%d')
    work = '定植' if i else '播種'
    return ' '.join((dt_s, work))


@bp.route('/create/<id>/<variety>', methods=['GET', 'POST'])
@login_required
def create(id, variety):
    form = GrowthForm()
    if request.method == 'POST':
        dt = form.date.data
        dt_s = dt.strftime('%Y/%m/%d')
        i = int(form.work.data)
        s = '定植' if i else '播種'
        title = ' '.join((dt_s, s))
        data = {
            'parent': id,
            'title': title
            }
        dao.create_growth(data)
        return redirect(url_for('index'))

    return render_template('forms/growth.html', form=form, variety=variety)

@bp.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    found = dao.read_growth(id)
    title = found['title']
    dt_s, s = title.split()
    date = datetime.strptime(dt_s, '%Y/%m/%d').date()
    work = 1 if s == '定植' else 0
    form = GrowthForm()
    if request.method == 'POST':
        dt = form.date.data
        i = int(form.work.data)
        title = set_title(dt, i)
        found['title'] = title
        dao.update_growth(id, found)
        return redirect(url_for('index'))
    return render_template('forms/growth.html', 
                                form=form,
                                date=date, 
                                work=work
                            )


@bp.route('/records/<id>', methods=['GET', 'POST'])
@login_required
def growth_records(id):
    found = dao.read_growth(id)
    growth = found['title']
    parent = found['parent']
    variety = dao.get_variety(parent)
    records = dao.get_records(id)
    for x in records:
        print(x['title'])
    return render_template('growth-records.html',
                                id=id,
                                variety=variety,
                                growth=growth,
                                records=records
                            )