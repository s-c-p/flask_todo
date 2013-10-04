from werkzeug.contrib.cache import RedisCache


class CustomRedisCache(RedisCache):
    """
        add hashes commands
        1. hget
        2. hset
        3. hgetall
        4. hdel
    """

    def __init__(self, host='localhost', port=6379, password=None,
                 db=0, default_timeout=300, key_prefix=None):

        super().__init__(host, port, password, db, default_timeout, key_prefix)
        self._client = super().__dict__['_client']
        self.key_prefix = super().__dict__['key_prefix']
        self.load_object = super().load_object

    def hget(self, key, field):
        return super().load_object(self._client.hget(self.key_prefix + key, field))

    def hset(self, key, field, value):
        dump = super().dump_object(value)
        self._client.hsetnx(self.key_prefix + key, field, dump)

    def hgetall(self, key):
        result_data = self._client.hgetall(self.key_prefix + key)

        return {key : self.load_object(value) for key, value in result_data.items()}

    def hdel(self, key, *fields):
        return self._client.hdel(key, *fields)
