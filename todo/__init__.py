from todo.sesto import Sesto
from todo.modules import db, MemoAPI


def create_app(config_filename):
    sesto_app = Sesto(__name__)
    sesto_app.config.from_pyfile(config_filename, silent=True)
    sesto_app.init_logger()
    init_db(sesto_app)
    pluggable_views_setting(sesto_app)
    return sesto_app

def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

def pluggable_views_setting(app):
    view_func = MemoAPI.as_view('memo_api')
    app.add_url_rule('/user/<int:user_id>/memos/', defaults={'memo_id': None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule('/user/<int:user_id>/memos/', view_func=view_func,
                     methods=['POST',])
    app.add_url_rule('/user/<int:user_id>/memos/<int:memo_id>', view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

app = create_app('config.cfg')

import todo.views.login_views
