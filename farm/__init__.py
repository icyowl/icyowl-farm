import os
from flask import Flask, render_template, redirect, url_for, session
from .auth import login_required
import configparser


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    
    config = configparser.ConfigParser()
    config.read(os.path.abspath(os.path.join(app.instance_path, 'config.ini')))

    app.config.from_mapping(
        SECRET_KEY = 'dev',
        MONGO_URI = config['PROD']['DB_URI']  # DEV or PROD
    )
 
    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile('config.ini', silent=True)
        pass
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from farm.db import mongo, init_db
    init_db(app)

    from farm import auth
    app.register_blueprint(auth.bp)

    from farm import sidebar
    app.register_blueprint(sidebar.bp)

    from farm import fields
    app.register_blueprint(fields.bp)

    from farm import species
    app.register_blueprint(species.bp)

    from farm import variety
    app.register_blueprint(variety.bp)

    from farm import growth
    app.register_blueprint(growth.bp)

    from farm import records
    app.register_blueprint(records.bp)

    from farm import document
    app.register_blueprint(document.bp)

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return 'Page Not Found', 404

    return app