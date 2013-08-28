from todo.sesto import Sesto
from todo.modules import init_db, MemoAPI


def create_app(config_filename):
    sesto_app = Sesto(__name__)
    sesto_app.config.from_pyfile(config_filename, silent=True)
    sesto_app.init_logger()
    init_db(sesto_app)
    sesto_app.register_api(MemoAPI, 'memo_api', '/memos/', pk='user_id')
    return sesto_app

app = create_app('config.cfg')

import todo.views.login_views
