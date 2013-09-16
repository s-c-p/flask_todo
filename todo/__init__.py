from flask import session, redirect, url_for, escape, request, json, jsonify, make_response, send_file
from todo.sesto import Sesto
from todo.modules import db, MemoAPI, User


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
    app.add_url_rule('/todo/user/<int:user_id>/memos/', defaults={'memo_id': None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule('/todo/user/<int:user_id>/memos/', view_func=view_func,
                     methods=['POST',])
    app.add_url_rule('/todo/user/<int:user_id>/memos/<int:memo_id>', view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

app = create_app('config.cfg')


@app.route('/todo/')
def index():
    return app.send_static_file('index.html')



@app.route('/todo/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user is None:
            return_code = 1
            error = 'Invalid username'
        elif request.form['password'] != user.password:
            return_code = 2
            error = 'Invalid password'
        else:
            session['username'] = user.username
            session['user_id'] = user.id
            session['logged_in'] = True
            return jsonify(return_code=0, user_id=user.id, username=user.username)

        return jsonify(return_code=return_code, error_dic=error)
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/todo/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return jsonify(return_code=0)


@app.route('/todo/users/', methods=['GET', 'POST'])
@app.route('/todo/users/<username>', methods=['GET', 'POST', 'DELETE'])
def users(username=None):

    if request.method == 'GET':

        if username is not None:
            user = User.query.filter_by(username=username).first()
            return jsonify(user=json.dumps(user.serialize))

        else:
            return jsonify(user=None)

    elif request.method == 'POST':

        if request.form['username'] is None or request.form['password'] is None:
            return jsonify(status=-1)

        user = User.query.filter_by(username=request.form['username']).first()

        if user is not None:
            return jsonify(status=-1)

        user = User(request.form['username'], request.form['password'])
        user.save()
        return jsonify(status=0)

    elif request.method == 'DELETE':

        if username is not None:
            user = User.query.filter_by(username=username).first()

            if user is not None:
                user.delete()
                return jsonify(status=0)
            else:
               return jsonify(status=-1)
        else:
            return jsonify(status=-1)

