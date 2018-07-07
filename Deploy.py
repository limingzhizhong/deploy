import yaml
import SFTP
import getpass
import hashlib
import datetime
import sys


def read_file(file):
    try:
        with open(file, 'r') as f:
            return yaml.load(f)
    except Exception as e:
        print("", e)
        exit()


class Param(object):

    def __init__(self, values, user, passwd) -> object:
        """
        :param values:
        :param user:
        :param passwd:
        hosts: 主机列别
        localPath: 本地文件路径
        remotePath: 需要更新的服务器文件路径
        updateFile: 需要更新的文件
        serverType: 游戏服务器类型
        type: 需要更新的类型
        """
        self.host = None
        self.username = user
        self.password = passwd
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
        #self.update_web()

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
        if self.type == 'hz':
            for self.keys in self.updateFile.keys():
                if self.type == 'hz':
                    for self.index in range(len(self.hosts)):
                        self.ssh = SFTP.MySSH(
                            host=self.hosts[self.index].split(':')[0],
                            port=int(self.hosts[self.index].split(':')[1]),
                            username=self.username,
                            password=self.password
                        )
                        for self.i in range(len(self.remotePath)):
                            self.from_path = self.localPath + self.updateFile.get(self.keys)
                            self.to_path = self.remotePath[self.i] + 'lib/' + self.updateFile.get(self.keys)
                            self.ssh.sftp_put(self.from_path, self.to_path)
                            self.__checkMD5()
                else:
                    continue

    def update_game(self):
        """
        升级游戏
        """
        if self.type == 'game':
            for self.keys in self.updateFile.keys():
                if self.type == 'game' and self.keys != 'extensions' and self.keys != 'yml':
                    for self.index in range(len(self.hosts)):
                        self.ssh = SFTP.MySSH(
                            host=self.hosts[self.index].split(':')[0],
                            port=int(self.hosts[self.index].split(':')[1]),
                            username=self.username,
                            password=self.password
                        )
                        for self.i in range(len(self.remotePath)):
                            self.from_path = self.localPath + self.updateFile.get(self.keys)
                            self.to_path = self.remotePath[self.i] + 'extensions/__lib__/' + \
                                           self.updateFile.get(self.keys)
                            self.ssh.sftp_put(self.from_path, self.to_path)
                            self.__checkMD5()
                else:
                    if self.keys != 'yml':
                        for self.i in range(len(self.remotePath)):
                            self.from_path = self.localPath + self.updateFile.get(self.keys)
                            self.to_path = self.remotePath[
                                               self.i] + 'extensions/' + self.serverType + '/' + self.updateFile.get(
                                self.keys)
                            self.ssh.sftp_put(self.from_path, self.to_path)
                            self.__checkMD5()
                    else:
                        for self.i in range(len(self.remotePath)):
                            self.from_path = self.localPath + self.updateFile.get(self.keys)
                            self.to_path = self.remotePath[self.i] + self.updateFile.get(self.keys)
                            self.ssh.sftp_put(self.from_path, self.to_path)
                            self.__checkMD5()

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
                for self.keys in self.updateFile.keys():
                    if self.keys != 'zip':
                        """
                        非全包更新扩展
                        """
                        continue
                    else:
                        for self.i in range(len(self.remotePath)):
                            self.cmd = "zip -r %s %s" % (
                                self.remotePath[self.i] + datetime.date.today().strftime('%Y-%m-%d') + '.zip',
                                self.remotePath[self.i] + self.serverType + '/')
                            self.ssh.exe(self.cmd)
                            self.from_path = self.localPath + self.updateFile.get(self.keys)
                            self.to_path = self.remotePath[self.i] + self.updateFile.get(self.keys)
                            self.ssh.sftp_put(self.from_path, self.to_path)
                            self.__checkMD5()


    def update_brnn(self):
        """
        升级游戏，百人牛牛
        """
        if self.type == 'hz' and self.serverType == 'baiRen':
            for self.index in range(len(self.hosts)):
                self.ssh = SFTP.MySSH(
                    host=self.hosts[self.index].split(':')[0],
                    port=int(self.hosts[self.index].split(':')[1]),
                    username=self.username,
                    password=self.password
                )
                for self.keys in self.updateFile.keys():
                    if self.keys == 'baisc':
                        for self.i in self.remotePath.keys():
                            if self.i == 'master':
                                self.to_path = self.remotePath.get(self.i) + 'lib/' + self.updateFile.get(self.keys)
                                self.from_path = self.localPath + self.updateFile.get(self.keys)
                                self.ssh.sftp_put(self.from_path, self.to_path)
                                self.__checkMD5()
                            else:
                                if self.i == 'slave':
                                    self.to_path = self.remotePath.get(
                                        self.i) + 'extension/__lib__/' + self.updateFile.get(
                                        self.keys)
                                    self.from_path = self.localPath + self.remotePath.get(self.keys)
                                    self.ssh.sftp_put(self.from_path, self.to_path)
                                    self.__checkMD5()
                    else:
                        if self.keys == 'extensions':
                            self.to_path = self.remotePath.get('slave') + 'lib/' + self.updateFile.get(self.keys)
                            self.from_path = self.localPath + self.updateFile.get(self.keys)
                            self.ssh.sftp_put(self.from_path, self.to_path)
                            self.__checkMD5()
                        else:
                            if self.keys == 'yml':
                                self.to_path = self.remotePath.get('slave') + self.updateFile.get(self.keys)
                                self.from_path = self.localPath + self.updateFile.get(self.keys)
                                self.ssh.sftp_put(self.from_path, self.to_path)
                                self.__checkMD5()
                            else:
                                self.to_path = self.remotePath.get('slave') + self.updateFile.get(self.keys)
                                self.from_path = self.localPath + self.updateFile.get(self.keys)

    def update_worldcup(self):

        if self.type == 'game' and self.serverType == 'worldcup':
            for self.index in range(len(self.hosts)):
                self.ssh = SFTP.MySSH(
                    host=self.hosts[self.index].split(':')[0],
                    port=int(self.hosts[self.index].split(':')[1]),
                    username=self.username,
                    password=self.password
                )

    @staticmethod
    def __CallMD5(filename):
        """
            获取文件md5, 用来检验文件传输完整性
        """
        try:
            with open(filename, 'rb') as f:
                md5obj = hashlib.md5()
                md5obj.update(f.read())
                hashes = md5obj.hexdigest()
                return hashes
        except Exception as e:
            print("本地文件%s不存在 %s" % (filename, e))

    def __checkMD5(self):

        self.cmd = "md5sum %s|cut -d ' ' -f1" % self.to_path
        self.to_md5 = self.ssh.exe(self.cmd).strip()
        self.from_md5 = self.__CallMD5(self.from_path)
        if self.to_md5 == self.from_md5:
            print(
                "update成功: %s %s %s %s" % (self.hosts[self.index].split(':')[0], self.type,
                                           self.serverType, self.to_path))
        else:
            print("主机%s上传文件%smd5不正确！！！！" % (self.hosts[self.index], self.updateFile.get(self.keys)))


if "__main__" == __name__:
    loadfile = sys.argv[1]
    data = read_file(loadfile)
    username = input("请输入用户名:")
    password = getpass.getpass()
    for KEY in data.keys():
        b = Param(data.get(KEY), user=username, passwd=password)
