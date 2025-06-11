from flask import Blueprint, redirect, render_template, request, url_for
from farm.auth import login_required

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.fields import RadioField


# from bson.objectid import ObjectId
from farm.db import Dao
dao = Dao()

bp = Blueprint('species', __name__, url_prefix='/species')


class SpeciesForm(FlaskForm):
    field = RadioField('Field', choices=[(0, 'Crop'), (1, 'Vegetable'), (2, 'Other')])
    family = StringField('Family')
    species = StringField('Species')
    sort_no = IntegerField('Sort No')


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = SpeciesForm()
    if request.method == 'POST':
        sort_no = str((int(form.field.data) + 1) * 100 + int(form.sort_no.data))
        data = {
            'field': form.field.data,
            'family': form.family.data,
            'species': form.species.data,
            'sort_no': sort_no,
            }
        dao.create_species(data)
        return redirect(url_for('index'))

    return render_template('forms/species.html', form=form)


@bp.route('/update/<string:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    form = SpeciesForm()
    found = dao.read_species(id)
    field = found['field']
    species = found['species']
    family = found['family']
    sort_no = found['sort_no']
    if request.method == 'POST':
        found['field'] = form.field.data
        found['family'] = form.family.data
        found['species'] = form.species.data
        found['sort_no'] = form.sort_no.data
        dao.update_species(id, found) 
        return redirect(url_for('index'))

    return render_template('forms/species.html', 
                                form=form,
                                id=id,
                                field=field,
                                family=family, 
                                species=species,
                                sort_no=sort_no
                            )

@bp.route('/delete/<id>')
@login_required
def delete(id):
    dao.delete_species(id)
    return redirect(url_for('index'))