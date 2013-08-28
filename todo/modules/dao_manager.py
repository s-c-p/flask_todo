from todo.modules import TodoMemo


class DAOManager(object):

    """DAOManager controll all database access"""

    def __init__(self, arg):
        super(DAOManager, self).__init__()
        self.arg = arg

    def get_todo_memos(user_id=None):
        return TodoMemo.query.filter_by(user_id=user_id).all()

    def add_todo_memo(user_id, memo):
        todo_memo = TodoMemo(user_id, memo)
        todo_memo.save()

    def del_todo_memo(memo_id):
        pass

    def update_todo_memo(memo_id):
        pass
