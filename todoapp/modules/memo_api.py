from flask.views import MethodView
from flask import request, jsonify, json, current_app
from todoapp.database import TodoMemo, DAOManager


class MemoAPI(MethodView):

    def get(self, user_id):
        if user_id is None:
            return 'a list of users'

        else:
            memos = DAOManager.get_todo_memos(user_id)

            return jsonify(memos=json.dumps(
                           [json.dumps(memo.serialize) for memo in memos]))

    def post(self):
        # create a new memo
        todoMemo = TodoMemo(request.form['user_id'], request.form['memo'])
        DAOManager.add_todo_memo(todoMemo.user_id, todoMemo.memo)

        return jsonify(status=0)

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass
