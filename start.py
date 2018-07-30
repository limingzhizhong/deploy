import Deploy
import logging
from utils import LoadFile
import GetHistroy
import sys
import getpass


if __name__ == '__main__':

    if len(sys.argv) < 1:
        print("请跟上yml文件路径")
    else:
        Deploy.logger()
        data = LoadFile.read_file('./yml/test.yml')
        redis = GetHistroy.RedisData()
        redis.save_data(data)
        for values in data.values():
            temp1 = values.get('serverType')
            temp2 = values.get('ip')
            temp3 = values.get('remotePath')
            logging.error("将要更新的服务清单:IP地址:%s,服务类型:%s" % (temp2, temp1))
        username = input("请输入用户名:")
        password = getpass.getpass()
        for KEY in data.keys():
            b = Deploy.Param(data.get(KEY), user=username, passwd=password)