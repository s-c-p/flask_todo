from werkzeug.contrib.cache import RedisCache
from todo import app
from todo.models import TodoMemo


redis_cache = RedisCache()

def get_memos(user_id):
    """
        First, get memos from redis_cache, if memos is None, then get memos from
        mariaDB.
        When memos is not None, then save it into redis_cache.
    """
    app.logger.debug('user_id : {0}'.format(user_id))
    memos = redis_cache.get(user_id)
    app.logger.debug('first redis memos : {0}'.format(memos))
    if memos:
        return memos

    memos = TodoMemo.query.filter(TodoMemo.user_id==user_id).all()
    if memos is None:
        return memos

    redis_cache.set(user_id, memos)
    app.logger.debug('after redis memos : {0}'.format(redis_cache.get(user_id)))
    return memos

def add_memo():
    pass


def delete_memo(user_id, memo_id):
    """
        First, delete memo from mariaDB, and then delete memo from redis_cache
    """

    todo_memo = TodoMemo.query.filter(TodoMemo.id==memo_id).first()

    if todo_memo is None:
        return

    todo_memo.delete()

    # remove memo from redis_cache

    pass


def update_memo():
    pass
