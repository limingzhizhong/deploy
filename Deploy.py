import yaml
import SFTP
import getpass
import hashlib
import datetime


def read_file(loadfile):
    try:
        with open(loadfile, 'r') as f:
            return yaml.load(f)
    except Exception as e:
        print("", e)
        exit()


class Param(object):

    def __init__(self, values, username, password):
        """
        :param values:
        :param username:
        :param password:
        hosts: 主机列别
        localPath: 本地文件路径
        remotePath: 需要更新的服务器文件路径
        updateFile: 需要更新的文件
        serverType: 游戏服务器类型
        type: 需要更新的类型
        """
        self.username = username
        self.password = password
        self.hosts = None
        self.localPath = None
        self.updateFile = None
        self.remotePath = None
        self.type = None
        self.serverType = None
        self.values = values
        self.__get_host()
        self.from_path = None
        self.to_path = None
        self.cmd = None
        self.to_md5 = None
        self.from_md5 = None
        self.ssh = None
        self.update_hz()
        self.update_game()

    def __get_host(self):
        self.type = self.values.get('type')
        self.hosts = self.values.get('ip')
        self.remotePath = self.values.get('remotePath')
        self.updateFile = self.values.get('updateFile')
        self.localPath = self.values.get('localPath')
        self.serverType = self.values.get('serverType')

    def update_hz(self):
        """
        升级hz
        """
        for self.keys in self.updateFile.keys():
            if self.type == 'hz':
                for self.index in range(len(self.hosts)):
                    self.ssh = SFTP.MySSH(
                        host=self.hosts[self.index].split(':')[0],
                        port=self.hosts[self.index].split(':')[1],
                        username=self.username,
                        password=self.password
                    )
                    for self.i in range(len(self.remotePath)):
                        self.from_path = self.localPath + self.updateFile.get(self.keys)
                        self.to_path = self.remotePath[self.i] + 'lib/' + self.updateFile.get(self.keys)
                        self.ssh.sftp_put(self.from_path, self.to_path)
                        self.cmd = "md5sum %s|cut -d ' ' -f1" % self.to_path
                        self.to_md5 = self.ssh.exe(self.cmd)
                        self.from_md5 = self.__CallMD5(self.from_path)
                        if self.to_md5 == self.from_path:
                            continue
                        else:
                            print("主机%s上传文件%smd5不正确！！！！" % (self.hosts[self.index].split(':')[0],
                                                            self.updateFile.get(self.keys)))
            else:
                continue
    def update_game(self):
        """
        升级游戏
        """
        for self.keys in self.updateFile.keys():
            if self.type == 'game' and self.keys != 'extensions':
                for self.index in range(len(self.hosts)):
                    self.ssh = SFTP.MySSH(
                        host=self.hosts[self.index].split(':')[0],
                        port=int(self.hosts[self.index].split(':')[1]),
                        username=self.username,
                        password=self.password
                    )
                    for self.i in range(len(self.remotePath)):
                        self.from_path = self.localPath + self.updateFile.get(self.keys)
                        self.to_path = self.remotePath[self.i] + 'extensions/' + self.serverType + '/' + \
                                       self.updateFile.get(self.keys)
                        self.ssh.sftp_put(self.from_path, self.to_path)
                        self.cmd = "md5sum %s|cut -d ' ' -f1" % self.to_path
                        self.to_md5 = self.ssh.exe(self.cmd).strip()
                        self.from_md5 = self.__CallMD5(self.from_path)
                        if self.to_md5 == self.from_md5:
                            continue
                        else:
                            print("主机%s上传文件%smd5不正确！！！！" % (self.hosts[self.index].split(':')[0],
                                                            self.updateFile.get(self.keys)))
            else:
                continue

    def update_web(self):
        """
        升级web
        """
        if self.type == 'web':
            for self.index in range(len(self.hosts)):
                self.ssh = SFTP.MySSH(
                    host=self.hosts[self.index].split(':')[0],
                    port=int(self.hosts[self.index].split(':')[1]),
                    username=self.username,
                    password=self.password
                )
                self.cmd = "zip -r %s %s" % (datetime.date.today(), self.to_path.split('.')[0])
                self.ssh.sftp_put(self.from_path, self.to_path)
                self.to_md5 = self.ssh.exe(self.cmd).strip()
                self.from_md5 = self.__CallMD5(self.from_path)
                if self.to_md5 == self.from_md5:
                    continue
                else:
                    print("主机%s上传文件%smd5不正确！！！！" % (self.hosts[self.index].split(':')[0],
                                                    self.updateFile.get(self.keys)))
                self.cmd = "unzip %s" % self.to_path
                self.ssh.exe(self.cmd)

    def update_brnn(self):
        """

        """
        pass

    def update_worldcup(self):
        pass

    @staticmethod
    def __CallMD5(filename):
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
    loadfile = '/Users/admin/Documents/deploy/Deploy2.yml'
    data = read_file(loadfile)
    username = input("请输入用户名:")
    password = getpass.getpass()
    for KEY in data.keys():
        b = Param(data.get(KEY), username=username, password=password)
