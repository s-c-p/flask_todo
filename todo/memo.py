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

    cache_key_name = 'user:{0}:memo'.format(user_id)

    hmemos = cache.hgetall(cache_key_name)

    if hmemos:
        return [value for key, value in hmemos.items()]

    todo_memos = TodoMemo.query.filter(TodoMemo.user_id == user_id).all()
    if todo_memos is None:
        return todo_memos

    for todo_memo in todo_memos:
        cache.hset(cache_key_name, todo_memo.id, todo_memo)

    return todo_memos


def add_memo(user_id, memo_text):
    todo_memo = TodoMemo(user_id, memo_text)
    todo_memo.save()

    cache_key_name = 'user:{0}:memo'.format(user_id)
    cache.hset(cache_key_name, todo_memo.id, todo_memo)
    return todo_memo


def delete_memo(user_id, memo_id):
    """
        First, delete memo from mariaDB, and then delete memo from cache.

        return result:
        True  : delete success
        False : no memo data in mariaDB
    """

    todo_memo = TodoMemo.query.filter(TodoMemo.id == memo_id).first()

    if todo_memo is None:
        return False

    todo_memo.delete()

    # remove memo from cache
    cache_key_name = 'user:{0}:memo'.format(user_id)
    cache.hdel(cache_key_name, memo_id)

    return True

def update_memo(user_id, memo_id, memo_text, state):
    """
        First, update memo into mariaDB, and then update memo into cache

        return result:
        None : no memo data
        TodoMemo : new todo_memo
    """
    todo_memo = TodoMemo.query.filter(TodoMemo.id==memo_id).first()

    if todo_memo is None:
        return None

    todo_memo.memo = memo_text
    todo_memo.state = state
    todo_memo.save()

    #update memo into redis cache
    cache_key_name = 'user:{0}:memo'.format(user_id)
    cache.hset(cache_key_name, todo_memo.id, todo_memo)

    return todo_memo
