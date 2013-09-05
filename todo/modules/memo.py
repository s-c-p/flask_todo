import datetime
from flask.views import MethodView
from flask import request, jsonify, json, current_app
from flask import make_response
from todo.modules import db


class TodoMemo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    memo = db.Column(db.String(50))
    state = db.Column(db.String(50))
    create_date = db.Column(db.DateTime)

    def __init__(self, user_id, memo, state='incomplete',
                 create_date=datetime.datetime.today()):
        self.user_id = user_id
        self.memo = memo
        self.state = state
        self.create_date = create_date

    def __repr__(self):
        return '<TodoMemo %r>' % self.memo

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def dump_datetime(self, value):
        """Deserialize datetime object into string form for JSON processing."""
        if value is None:
            return None
        return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'memo': self.memo,
            'state': self.state,
            'create_date': self.dump_datetime(self.create_date)
        }


class MemoAPI(MethodView):

    def get(self, user_id, memo_id):
        if memo_id is None:
            memos = TodoMemo.query.filter_by(user_id=user_id).all()

            response = make_response(json.dumps(memos, default=to_json))
            response.headers['Content-Type'] = 'application/json'
            return response
            #return jsonify(memos=json.dumps(
            #               [json.dumps(memo.serialize) for memo in memos]))

        else:
            return 'a single memo of user'

    def post(self, user_id):
        todo_memo = TodoMemo(user_id, request.form['memo'])
        todo_memo.save()
        return jsonify(todo_memo_id=todo_memo.id)

    def delete(self, user_id, memo_id):
        todo_memo = TodoMemo.query.filter_by(id=memo_id).first()

        if todo_memo is not None:
            todo_memo.delete()
            return jsonify(status=0)
        else:
            return jsonify(status=-1)

    def put(self, user_id, memo_id):
        todo_memo = TodoMemo.query.filter_by(id=memo_id).first()

        if todo_memo is not None:
            todo_memo.memo = request.form['memo']
            todo_memo.save()
            return jsonify(memo=json.dumps(todo_memo.serialize))
        else:
            return jsonify(memo=None)


def to_json(python_object):

    if isinstance(python_object, TodoMemo):
        return {
            'id': python_object.id,
            'user_id': python_object.user_id,
            'memo': python_object.memo,
            'state': python_object.state,
            'create_date': python_object.create_date
        }

    if isinstance(python_object, datetime.date):
        if python_object is None:
            return None
        return "{0} {1}".format(python_object.strftime("%Y-%m-%d"),
                                python_object.strftime("%H:%M:%S"))

