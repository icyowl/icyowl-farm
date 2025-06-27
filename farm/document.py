from flask import Blueprint, redirect, render_template, request, url_for
from farm.auth import login_required
import markdown

from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import InputRequired
from bson.objectid import ObjectId

bp = Blueprint('document', __name__, url_prefix='/document')

from farm.db import Dao
dao = Dao()

class documentForm(FlaskForm):
    document = TextAreaField('document', validators=[InputRequired()])

# @bp.route('/create/<id>', methods=['GET', 'POST'])
# @login_required
# def create(id):
#     form = documentForm()
#     return render_template('forms/document.html', form=form)

@bp.route('/read/<parent_id>', methods=['GET', 'POST'])
@login_required
def read(parent_id):
    # species = request.args.get('species')
    variety = request.args.get('variety')
    found = dao.read_document(parent_id)
    text = found['document']
    md = markdown.markdown(text)

    return render_template('document.html', 
                                parent_id=parent_id, 
                                variety=variety, 
                                md=md
                            )

@bp.route('/update/<parent_id>', methods=['GET', 'POST'])
@login_required
def update(parent_id):
    form = documentForm()
    found = dao.read_document(parent_id)
    variety = found['variety']
    text = found['document']
    if request.method == 'POST':
        id = str(found['_id'])
        text = form.document.data
        found['document'] = text
        dao.update_document(id, found)
        md = markdown.markdown(text)
        return redirect(url_for('document.read', parent_id=parent_id, variety=variety)) 
    return render_template('forms/document.html',
                                form=form,
                                variety=variety,
                                document=text
                            )

