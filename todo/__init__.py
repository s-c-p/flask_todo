from flask import Flask
from todo import log_config
from todo.models import init_db
from todo.routes import init_routes


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename, silent=True)
    app.logger.addHandler(log_config.create_log_file_handler(
                            app.config.get('LOG_PATH')))
    init_db(app)
    init_routes(app)
    return app



app = create_app('config.cfg')
