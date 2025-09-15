from flask import Blueprint, redirect, render_template, request, url_for, flash
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


def new_document(id: str, species: str, variety: str):
    data = {
        'parent': id,
        'species': species,
        'variety': variety,
        'document': ''
    }
    dao.create_document(data)


@bp.route('/create/<id>/<species>', methods=['GET', 'POST'])
@login_required
def create(id, species):
    form = VarietyForm()
    # id = request.args.get('id')
    # species = request.args.get('species')
    if request.method == 'POST':
        _id = str(ObjectId())
        variety = form.variety.data
        data = {
            '_id': _id,
            'parent': id,
            'variety': variety,
            'sort_no': form.sort_no.data,
            }
        dao.create_variety(data)

        new_document(_id, species, variety)
        # data_ = {
        #     'parent': _id,
        #     'species': species,
        #     'variety': variety,
        #     'document': ''
        # }
        # dao.create_document(data_)
        
        idx = dao.get_field_index_by_species_id(id)
        return redirect(url_for('fields.docs', idx=idx))

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
        idx = dao.get_field_index(id) 
        return redirect(url_for('fields.documents', idx=idx))
    return render_template('forms/variety.html', 
                                        form=form,
                                        id=id,
                                        variety=variety, 
                                        sort_no=sort_no
                                        )

@bp.route('/delete/<id>')
@login_required
def delete(id):
    count = dao.count_growth(id)
    if not count:
        dao.delete_variety(id)
        idx = dao.get_field_index_by_species_id(id)
        return redirect(url_for('fields.docs', idx=idx))
    else:
        flash('Please remove the child documents first')
        found = dao.read_variety(id)
        variety = found['variety']
        sort_no = found['sort_no']
        form = VarietyForm()
    return render_template('forms/variety.html', 
                                        form=form,
                                        id=id,
                                        variety=variety, 
                                        sort_no=sort_no
                                        )