import datetime
from flask import request, session, jsonify, json, make_response
from todo import app
from todo.models import TodoMemo, User
from todo import memos_center


@app.route('/todo/')
def index():
    return app.send_static_file('index.html')

@app.route('/todo/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.form['username']).first()

    if user:
        if request.form['password'] != user.password:
            return_code = 2
            error = 'Invalid password'
        else:
            session['username'] = user.username
            session['user_id'] = user.id
            session['logged_in'] = True
            return jsonify(return_code=0, user_id=user.id, username=user.username)
    else:
        return_code = 1
        error = 'Invalid username'

    return jsonify(return_code=return_code, error_dic=error)

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

        if username:
            user = User.query.filter(User.username==username).first()
            return jsonify(user=json.dumps(user, default=to_json))

        else:
            return jsonify(user=None)

    elif request.method == 'POST':

        if request.form['username'] is None or request.form['password'] is None:
            return jsonify(status=-1)

        user = User.query.filter(User.username==request.form['username']).first()

        if user:
            return jsonify(status=-1)

        user = User(request.form['username'], request.form['password'])
        user.save()
        return jsonify(status=0)

    elif request.method == 'DELETE':

        if username:
            user = User.query.filter(User.username==username).first()

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
        if memo_id:
            return 'a single memo of user'

        else:
            memos = memos_center.get_memos(user_id)
            response = make_response(json.dumps(memos, default=to_json))
            response.headers['Content-Type'] = 'application/json'
            return response

    def add_memo():
        todo_memo = TodoMemo(user_id, request.form['memo'])
        todo_memo.save()
        return jsonify(todo_memo_id=todo_memo.id)

    def delete_memo():

        if memos_center.delete_memo(user_id, memo_id):
            return jsonify(status=0)
        else:
            return jsonify(status=-1)

    def update_memo():
        todo_memo = TodoMemo.query.filter(TodoMemo.id==memo_id).first()

        if todo_memo:
            todo_memo.memo = request.form['memo']
            todo_memo.state = request.form['state']
            todo_memo.save()
            return jsonify(memo=json.dumps(todo_memo, default=to_json))
        else:
            return jsonify(memo=None)

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

