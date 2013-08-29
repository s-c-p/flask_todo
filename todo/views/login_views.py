from flask import session, redirect, url_for, escape, request, json, jsonify
from todo import app
from todo.modules import User


@app.route('/')
def index():
    if 'username' in session:
        return 'You were logged in %s' % escape(session['username'])
    return 'You were logged out'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user is None:
            error = 'Invalid username'
        elif request.form['password'] != user.password:
            error = 'Invalid password'
        else:
            session['username'] = request.form['username']
            session['logged_in'] = True
            return redirect(url_for('index'))

        return error
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/users/', methods=['GET', 'POST'])
@app.route('/users/<username>', methods=['GET', 'POST', 'DELETE'])
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
