from todo import app
from todo.flask_redis_cache import CustomRedisCache
from todo.models import TodoMemo


cache = CustomRedisCache()


def get_memos(user_id):
    """
        First, get memos from cache, if memos is None, then get memos from
        mariaDB.
        When memos is not None, then save it into cache.

        cache variable format:
        name : 'user:<user_id>:memo'
        key : memo_id

    """

    app.logger.debug('user_id : {0}'.format(user_id))
    cache_key_name = 'user:{0}:memo'.format(user_id)

    hmemos = cache.hgetall(cache_key_name)
    app.logger.debug('first redis hmemos : {0}'.format(hmemos))
    if hmemos:
        return [value for key, value in hmemos.items()]

    memos = TodoMemo.query.filter(TodoMemo.user_id == user_id).all()
    if memos is None:
        return memos

    for memo in memos:
        cache.hset(cache_key_name, memo.id, memo)

    app.logger.debug(
        'after redis memos : {0}'.format(cache.hgetall(cache_key_name)))
    return memos


def add_memo():
    pass


def delete_memo(user_id, memo_id):
    """
        First, delete memo from mariaDB, and then delete memo from cache.

        result:
        True  : delete success
        False : no memo data in mariaDB
    """

    todo_memo = TodoMemo.query.filter(TodoMemo.id == memo_id).first()

    if todo_memo is None:
        return False

    todo_memo.delete()

    # remove memo from cache
    app.logger.debug('user_id : {0}'.format(user_id))
    cache_key_name = 'user:{0}:memo'.format(user_id)
    cache.hdel(cache_key_name, memo_id)

    return True

def update_memo():
    pass
