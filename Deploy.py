import yaml
import SFTP
import getpass
import hashlib


def read_file(loadfile):
    with open(loadfile, 'r') as f:
        return yaml.load(f)


class Param(object):

    def __init__(self, values):
        self.hosts = None
        self.localPath = None
        self.updateFile = None
        self.remotePath = None
        self.server = None
        self.type = None
        self.port = None
        self.values = values
        self.__get_host()
        self.basic = 'basic-core-1.0-SNAPSHOT.jar'
        self.services = 'services-1.0-SNAPSHOT.jar'

    def __get_host(self):
        self.type = self.values.get('type')
        self.hosts = self.values.get('ip')
        self.remotePath = self.values.get('remotePath')
        self.updateFile = self.values.get('updateFile')
        self.localPath = self.values.get('localPath')


def put_files():
    for KEY in data.keys():
        b = Param(data.get(KEY))
        for index in range(len(b.hosts)):
            host = b.hosts[index].split(':')[0]
            port = int(b.hosts[index].split(':')[1])
            print(port)
            ssh = SFTP.MySSH(host=host, port=port, username=user, password=passwd)
            for keys in b.updateFile.keys():
                if b.type == 'hz':
                    for i in range(len(b.remotePath)):
                        from_path = b.localPath + b.updateFile.get(keys)
                        to_path = b.remotePath[i] + 'lib/' + b.updateFile.get(keys)
                        print("正在拷贝 %s" % b.type)
                        ssh.sftp_put(from_path, to_path)
                        cmd = "md5sum %s|cut -d ' ' -f1" % to_path
                        to_md5 = ssh.exe(cmd).strip()
                        from_md5 = CalcMD5(from_path)
                        # print(to_md5 == from_md5)
                        if to_md5 == from_md5:
                            print("主机%s拷贝成功：%s " % (host, b.updateFile.get(keys)))
                        else:
                            print("主机%s上传文件%smd5不正确！！！！" % (host, b.updateFile.get(keys)))
                else:
                    if keys == 'basic':
                        for i in range(len(b.remotePath)):
                            from_path = b.localPath + b.updateFile.get(keys)
                            to_path = b.remotePath[i] + 'extensions/__lib__/' + b.updateFile.get(keys)
                            print("正在拷贝 %s" % b.type)
                            ssh.sftp_put(from_path, to_path)
                            cmd = "md5sum %s|cut -d ' ' -f1" % to_path
                            to_md5 = ssh.exe(cmd).strip()
                            from_md5 = CalcMD5(from_path)
                            # print(to_md5 == from_md5)
                            if to_md5 == from_md5:
                                print("主机%s拷贝成功：%s " % (host, b.updateFile.get(keys)))
                            else:
                                print("主机%s上传文件%smd5不正确！！！！" % (host, b.updateFile.get(keys)))
                    else:
                        for i in range(len(b.remotePath)):
                            from_path = b.localPath + b.updateFile.get(keys)
                            to_path = b.remotePath[i] + 'extensions/' + b.type + '/' + b.updateFile.get(keys)
                            print("正在拷贝 %s" % b.updateFile.get(keys))
                            ssh.sftp_put(from_path, to_path)
                            cmd = "md5sum %s|cut -d ' ' -f1" % to_path
                            to_md5 = ssh.exe(cmd).strip()
                            from_md5 = CalcMD5(from_path)
                            if to_md5 == from_md5:
                                print("主机%s拷贝成功：%s " % (host, b.updateFile.get(keys)))
                            else:
                                print("主机%s上传文件%smd5不正确！！！！" % (host, b.updateFile.get(keys)))


def CalcMD5(filename):
    """
        获取文件md5, 用来检验文件传输完整性
    """
    try:
        with open(filename, 'rb') as f:
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            hash = md5obj.hexdigest()
            return hash
    except Exception as e:
        print("本地文件不存在 %s" % e)


if "__main__" == __name__:
    loadfile = '/Users/admin/Documents/deploy/deploy.yaml'
    data = read_file(loadfile)
    user = input('请输入服务器名字: ')
    passwd = getpass.getpass()
    print(user)
    print(passwd)
    put_files()
