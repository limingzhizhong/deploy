import redis


class RedisConn(object):

    def __init__(self, host, port, password=''):
        self.host = host
        self.port = port
        self.password = password

    def redis_conn(self):
        return redis.Redis(host=self.host, port=self.port, password=self.password, decode_responses=True)


"""
def start():
    data = LoadFile.read_file('./serverConfig.yml')
    redis_conn = RedisConn(host='127.0.0.1', port=16789)
    for key in data.keys():
        for i in data.get(key).keys():
            redis_conn.redis_conn().hset(key, i, data.get(key).get(i))
"""
