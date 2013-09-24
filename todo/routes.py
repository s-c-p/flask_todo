import datetime
from flask import request, session, jsonify, json, make_response
from todo.models import TodoMemo, User

def init_routes(app):
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

            if username is not None:
                user = User.query.filter_by(username=username).first()
                return jsonify(user=json.dumps(user, default=to_json))

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
            if memo_id is None:
                memos = TodoMemo.query.filter_by(user_id=user_id).all()

                response = make_response(json.dumps(memos, default=to_json))
                response.headers['Content-Type'] = 'application/json'
                return response

            else:
                return 'a single memo of user'

        def add_memo():
            todo_memo = TodoMemo(user_id, request.form['memo'])
            todo_memo.save()
            return jsonify(todo_memo_id=todo_memo.id)

        def delete_memo():
            todo_memo = TodoMemo.query.filter_by(id=memo_id).first()

            if todo_memo is not None:
                todo_memo.delete()
                return jsonify(status=0)
            else:
                return jsonify(status=-1)

        def update_memo():
            todo_memo = TodoMemo.query.filter_by(id=memo_id).first()

            if todo_memo is not None:
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
        if python_object is None:
            return None
        return "{0} {1}".format(python_object.strftime("%Y-%m-%d"),
                                python_object.strftime("%H:%M:%S"))
