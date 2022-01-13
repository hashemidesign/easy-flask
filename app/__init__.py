import logging
import os
from logging.handlers import RotatingFileHandler

import toml
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
base_dir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    # configure the application
    app.config.from_file('../config.toml', toml.load)
    app.config['UPLOAD_PATH'] = os.path.join(base_dir, 'uploads')
    # initialize modules
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # register blueprints
    from app.console import console
    from app.web.public import pub
    from app.web.admin import admin
    from app.api import api
    app.register_blueprint(console)
    app.register_blueprint(pub)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(api, url_prefix='/api')

    # save error log in logs/
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('easy-flask')

    return app
