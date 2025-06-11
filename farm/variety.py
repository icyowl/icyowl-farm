from flask import Blueprint, redirect, render_template, request, url_for
from farm.auth import login_required

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from bson.objectid import ObjectId

from farm.db import Dao
dao = Dao()

bp = Blueprint('variety', __name__, url_prefix='/variety')


class VarietyForm(FlaskForm):
    variety = StringField('Variety')
    sort_no = IntegerField('Sort No')


@bp.route('/create/<id>/<species>', methods=['GET', 'POST'])
@login_required
def create(id, species):
    form = VarietyForm()
    # id = request.args.get('id')
    # species = request.args.get('species')
    if request.method == 'POST':
        data = {
            'parent': id,
            'variety': form.variety.data,
            'sort_no': form.sort_no.data,
            }
        dao.create_variety(data)
        return redirect(url_for('index'))

    return render_template('forms/variety.html', form=form, species=species)


@bp.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = VarietyForm()
    found = dao.read_variety(id)
    variety = found['variety']
    sort_no = found['sort_no']
    if request.method == 'POST':
        found['variety'] = form.variety.data
        found['sort_no'] = form.sort_no.data
        dao.update_variety(id, found) 
        return redirect(url_for('index'))
    return render_template('forms/variety.html', 
                                        form=form, 
                                        variety=variety, 
                                        sort_no=sort_no
                                        )