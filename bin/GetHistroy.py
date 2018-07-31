from utils import RedisConn


class RedisData(object):

    def __init__(self):
        self.redis = RedisConn.RedisConn('127.0.0.1', 6379)

    def save_data(self, hash_map, hash_map_key, data):
        try:
            self.redis.redis_conn().hset(hash_map, hash_map_key, data)
            print("保存redis成功")
        except Exception as e:
            print("".format(e))

    def get_data(self, hash_map, time):
        temp = self.redis.redis_conn().hget(hash_map, time)
        if temp is not None:
            return temp
        else:
            return None
