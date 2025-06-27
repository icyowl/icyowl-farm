from flask import Blueprint, request, current_app, render_template, session, url_for, redirect
from farm.db import mongo


bp = Blueprint('sidebar', __name__, url_prefix=None)


@bp.route('/crop')
def crop():
    session['field'] = 0
    return redirect(url_for('fields.docs', idx=0))

@bp.route('/vegetable')
def vegetable():
    session['field'] = 1
    return redirect(url_for('fields.docs', idx=1))

@bp.route('/other')
def other():
    session['field'] = 2
    return redirect(url_for('fields.docs', idx=2))

@bp.app_context_processor
def inject_page():
    if 'field' in session:
        cursor = mongo.db.species.aggregate([
            {
                '$match': {'field': session['field']}
            },
            { 
                '$sort' : { 'sort_no': 1 }
            },
            {
                '$project': {
                    '_id': { '$toString': '$_id' },
                    'field': 1,
                    'species': 1,
                    }
            },
            {
                '$lookup': {
                    'from': 'variety',
                    'let': { 'id': '$_id'},
                    'pipeline': [

                        {
                            '$match': {'$expr': {'$eq': ['$parent', '$$id']}}
                        },
                        {
                            '$project': {'_id': { '$toString': '$_id' },'variety': 1}
                        },
                        {
                            '$lookup': {
                                'from': 'growth',
                                'let': { 'id': '$_id'},
                                'pipeline': [
                                    {
                                        '$match': {'$expr': {'$eq': ['$parent', '$$id']}}
                                    },
                                    {
                                        '$project': {'_id': { '$toString': '$_id' }, 'title': 1}
                                    }
                                ],
                                'as': 'children'
                            }
                        }

                    ],
                    'as': 'children'
                }
            },
        ])

        # for x in cursor:
        #     print(x)
        return {'items': list(cursor)}
    else:
        return {}

# cursor = col.find(filter, {'_id': 1, 'species': 1}).sort({'sort_key': 1})
# items = []
# for doc in cursor:
#     children = col.find({'parent': doc['_id']}).sort({'sort_key': 1})
#     varieties = []
#     for child in children:
#         variety_id = str(child['_id'])
#         variety = child['variety']
#         growths = child['growths']
#         varieties.append((variety_id, variety, growths))
#     doc['id'] = str(doc.pop('_id'))
#     doc['varieties'] = varieties
#     # print(doc)
#     items.append(doc)
# return {'items': items}