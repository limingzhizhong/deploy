import redis
import yaml


class RedisConn(object):

    def __init__(self, host, port, password=''):
        self.host = host
        self.port = port
        self.password = password

    def redis_conn(self):
        return redis.Redis(host=self.host, port=self.port, password=self.password, decode_responses=True)


def read_file(file):
    try:
        with open(file, 'r') as f:
            return yaml.load(f)
    except Exception as e:
        print("", e)
    exit()


def start():
    data = read_file('./serverConfig.yml')
    redis_conn = RedisConn(host='127.0.0.1', port=16789)
    for key in data.keys():
        for i in data.get(key).keys():
            redis_conn.redis_conn().hset(key, i, data.get(key).get(i))
