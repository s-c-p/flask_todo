import datetime
from flask import request, session, jsonify, json, make_response
from todo import app
from todo.models import TodoMemo, User
from todo import memo


class ResultType:
    REGISTER_SECCESS = 'success'
    USER_EXIST_ERROR = 'user_exist_error'
    USERNAME_IS_NONE_ERROR = 'user_is_none_error'
    PASSWORD_IS_NONE_ERRPR = 'password_is_none_error'

    GET_USER_SECCESS = 'success'
    GET_USER_NO_DATA = 'get_user_no_data'

    LOGIN_SECCESS = 'success'
    LOGIN_PASSWORD_ERROR = 'login_password_error'
    LOGIN_NO_USER_DATA = 'login_no_user_data'

    GET_MEMOS_SECCESS = 'success'
    GET_MEMOS_NO_USER_DATA = 'get_memos_no_user_data'

    ADD_MEMO_SECCESS = 'success'
    ADD_MEMO_NO_USER_DATA = 'add_memo_no_user_data'

    UPDATE_MEMO_SECCESS = 'success'
    UPDATE_MEMO_NO_USER_DATA = 'update_memo_no_user_data'
    UPDATE_MEMO_NO_MEMO_DATA = 'update_memo_no_memeo_data'


@app.route('/todo/')
def index():
    return app.send_static_file('index.html')


@app.route('/todo/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.form['username']).first()

    if user:
        if request.form['password'] != user.password:
            return jsonify(result=ResultType.LOGIN_PASSWORD_ERROR)

        else:
            session['username'] = user.username
            session['user_id'] = user.id
            session['logged_in'] = True

            return jsonify(result=ResultType.LOGIN_SECCESS, user_id=user.id,
                           username=user.username)
    else:
        return jsonify(result=ResultType.LOGIN_NO_USER_DATA)


@app.route('/todo/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return jsonify(return_code=0)


@app.route('/todo/users/', methods=['GET', 'POST'])
@app.route('/todo/users/<username>', methods=['GET', 'DELETE'])
def users(username=None):
    """
    The users fuction provide three user's action
    user action :
        1.get user data,
        2.regist user,
        3.delete user
    """

    if request.method == 'GET':

        if username is None:
            return jsonify(result=ResultType.GET_USER_NO_DATA)

        user = User.query.filter(User.username == username).first()

        if user:
            result = {}
            result['result'] = ResultType.GET_USER_SECCESS
            result['user'] = user

            response = make_response(json.dumps(result, default=to_json))
            response.headers['Content-Type'] = 'application/json'
            return response

        else:
            return jsonify(result=ResultType.GET_USER_NO_DATA)

    elif request.method == 'POST':

        if request.form['username'] is None or request.form['username'] == '':
            return jsonify(result=ResultType.USERNAME_IS_NONE_ERROR)

        if request.form['password'] is None or request.form['password'] == '':
            return jsonify(result=ResultType.PASSWORD_IS_NONE_ERRPR)

        user = User.query.filter(
            User.username == request.form['username']).first()

        if user:
            return jsonify(result=ResultType.USER_EXIST_ERROR)

        user = User(request.form['username'], request.form['password'])
        user.save()
        return jsonify(result=ResultType.REGISTER_SECCESS)

    elif request.method == 'DELETE':

        if username:
            user = User.query.filter(User.username == username).first()

            if user:
                user.delete()
                return jsonify(status=0)
            else:
                return jsonify(status=-1)
        else:
            return jsonify(status=-1)


@app.route('/todo/user/<user_id>/memos/', methods=['GET', 'POST'])
@app.route('/todo/user/<user_id>/memos/<memo_id>', methods=['GET', 'PUT', 'DELETE'])
def memos(user_id=None, memo_id=None):
    """
    The memos fuction provide four memos's action
    memos action :  1.get memos data,
                    2.add_memo,
                    3.delete_memo,
                    4.update_memo
    """

    def get_memos():
        user = User.query.filter(User.id == user_id).first()

        if user is None:
            return jsonify(result=ResultType.GET_MEMOS_NO_USER_DATA)

        if memo_id:
            return 'a single memo of user'

        else:
            memos = memo.get_memos(user_id)
            result = {}
            result['result'] = ResultType.GET_MEMOS_SECCESS
            result['memos'] = memos

            response = make_response(json.dumps(result, default=to_json))
            response.headers['Content-Type'] = 'application/json'
            return response

    def add_memo():
        user = User.query.filter(User.id == user_id).first()

        if  user:
            new_memo = memo.add_memo(user_id, request.form['memo'])

            result = {}
            result['result'] = ResultType.ADD_MEMO_SECCESS
            result['memo'] = new_memo
            response = make_response(json.dumps(result, default=to_json))
            response.headers['Content-Type'] = 'application/json'
            return response

        else:
            return jsonify(result=ResultType.ADD_MEMO_NO_USER_DATA)



    def delete_memo():

        if memo.delete_memo(user_id, memo_id):
            return jsonify(status=0)
        else:
            return jsonify(status=-1)

    def update_memo():
        user = User.query.filter(User.id == user_id).first()

        if user is None:
            return jsonify(result=ResultType.UPDATE_MEMO_NO_USER_DATA)

        todo_memo = memo.update_memo(user_id, memo_id,
                                     request.form['memo'],
                                     request.form['state'])

        if todo_memo:
            result = {}
            result['result'] = ResultType.UPDATE_MEMO_SECCESS
            result['memo'] = todo_memo
            response = make_response(json.dumps(result, default=to_json))
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            return jsonify(result=ResultType.UPDATE_MEMO_NO_MEMO_DATA)

    if request.method == 'GET':
        return get_memos()

    elif request.method == 'POST':
        return add_memo()

    elif request.method == 'DELETE':
        return delete_memo()

    elif request.method == 'PUT':
        return update_memo()


def to_json(python_object):
    if isinstance(python_object, TodoMemo):
        return {
            'id': python_object.id,
            'user_id': python_object.user_id,
            'memo': python_object.memo,
            'state': python_object.state,
            'create_date': python_object.create_date
        }

    if isinstance(python_object, User):
        return {
            'id': python_object.id,
            'username': python_object.username,
            'password': python_object.password
        }

    if isinstance(python_object, datetime.date):
        if python_object:
            return "{0} {1}".format(python_object.strftime("%Y-%m-%d"),
                                    python_object.strftime("%H:%M:%S"))
        else:
            return None
