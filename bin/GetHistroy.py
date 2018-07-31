from utils import RedisConn


class RedisData(object):

    def __init__(self):
        self.redis = RedisConn.RedisConn('127.0.0.1', 6379)
        self.hash_map = 'deploy'

    def save_data(self, hash_map_key, data):
        self.redis.redis_conn().hset(self.hash_map, hash_map_key, data)
        print("保存redis成功")

    def get_data(self, time):
        if self.redis.redis_conn().hget(self.hash_map, time) is not None:
            return self.redis.redis_conn().hget(self.hash_map, time)
        else:
            return None
