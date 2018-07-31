from bin import Deploy, GetHistroy
import logging
import getpass
import yaml

if __name__ == '__main__':

    Deploy.logger()
    while True:
        time = input("请输入回滚版本的日期:")
        redis = GetHistroy.RedisData()
        if redis.get_data(time) is not None:
            data = yaml.load(redis.get_data(time))
            for values in data.values():
                temp1 = values.get('serverType')
                temp2 = values.get('ip')
                temp3 = values.get('remotePath')
                logging.error("将要回滚的服务清单:IP地址:%s,服务类型:%s" % (temp2, temp1))
            username = input("请输入用户名:")
            password = getpass.getpass()
            for KEY in data.keys():
                b = Deploy.Param(data.get(KEY), user=username, passwd=password)
            break
        else:
            print('输入日期版本不存在')
            continue
    logging.error('done')
