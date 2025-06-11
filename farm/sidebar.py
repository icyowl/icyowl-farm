from flask import Blueprint, request, current_app, render_template, session, url_for, redirect
from farm.db import mongo


bp = Blueprint('sidebar', __name__, url_prefix=None)


@bp.route('/crop')
def crop():
    session['field'] = 0
    return redirect(url_for('index'))

@bp.route('/vegetable')
def vegetable():
    session['field'] = 1
    return redirect(url_for('index'))

@bp.route('/other')
def other():
    session['field'] = 2
    return redirect(url_for('index'))

@bp.app_context_processor
def inject_page():
    if 'field' in session:
        # query = {'field': session['field']}
        query = {'field': 1}
        projection = {'_id': 1, 'species': 1}
        species = mongo.db.species.find(query, projection).sort({'sort_no': 1})
        items = []
        for s in species:
            s['id'] = str(s.pop('_id'))
            query = {'parent': s['id']}
            projection = {'_id': 1, 'variety': 1}
            varieties = mongo.db.variety.find(query, projection).sort({'sort_no': 1})
            children = []
            for v in varieties:
                v['id'] = str(v.pop('_id'))
                query = {'parent': v['id']}
                projection = {'_id': 1, 'title': 1}
                growths = mongo.db.growth.find(query, projection).sort({'title': 1})
                g_children = []
                for g in growths:
                    g['id'] = str(g.pop('_id'))
                    g_children.append(g)
                v['children'] = g_children
                children.append(v)
            s['children'] = children
            # print(s)
            items.append(s)
        return {'items': items}
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