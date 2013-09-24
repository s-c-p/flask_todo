from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from todo import log_config


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename, silent=True)
    app.logger.addHandler(log_config.create_log_file_handler(
                            app.config.get('LOG_PATH')))
    init_db(app)
    return app

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

app = create_app('config.cfg')

import todo.routes
