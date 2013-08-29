from flask.views import MethodView
from flask import request, jsonify, json, current_app
from todo.modules import DAOManager, TodoMemo


class MemoAPI(MethodView):

    def get(self, user_id, memo_id):
        if memo_id is None:
            memos = DAOManager.get_todo_memos(user_id)

            return jsonify(memos=json.dumps(
                           [json.dumps(memo.serialize) for memo in memos]))

        else:
            return 'a single memo of user'

    def post(self, user_id):
        todoMemo = TodoMemo(user_id, request.form['memo'])
        DAOManager.add_todo_memo(todoMemo.user_id, todoMemo.memo)

        return jsonify(status=0)

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
