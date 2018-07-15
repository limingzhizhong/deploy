import yaml
import SFTP
import getpass
import hashlib
import datetime
import sys
import logging


def logger():
    logging.basicConfig(
        filename="update.log",
        level=logging.ERROR,
        format="%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p"
    )


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
        self.update_hz()
        self.update_game()
        self.update_web()

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
            for keys in self.updateFile.keys():
                if self.type == 'hz':
                    for index in range(len(self.hosts)):
                        ssh = SFTP.MySSH(
                            host=self.hosts[index].split(':')[0],
                            port=int(self.hosts[index].split(':')[1]),
                            username=self.username,
                            password=self.password
                        )
                        for i in range(len(self.remotePath)):
                            from_path = self.localPath + self.updateFile.get(keys)
                            to_path = self.remotePath[i] + 'lib/' + self.updateFile.get(keys)
                            ssh.sftp_put(from_path, to_path)
                            self.__checkMD5(ssh, from_path, to_path)
                else:
                    continue

    def update_game(self):
        """
        升级游戏
        """
        if self.type == 'game':
            for keys in self.updateFile.keys():
                if self.type == 'game':
                    for index in range(len(self.hosts)):
                        ssh = SFTP.MySSH(
                            host=self.hosts[index].split(':')[0],
                            port=int(self.hosts[index].split(':')[1]),
                            username=self.username,
                            password=self.password
                        )
                        if keys != 'extensions' and keys != 'yml':
                            for i in range(len(self.remotePath)):
                                from_path = self.localPath + self.updateFile.get(keys)
                                to_path = self.remotePath[i] + 'extensions/__lib__/' + self.updateFile.get(keys)
                                ssh.sftp_put(from_path, to_path)
                                self.__checkMD5(ssh, from_path, to_path)
                        else:
                            if keys != 'yml':
                                for i in range(len(self.remotePath)):
                                    from_path = self.localPath + self.updateFile.get(keys)
                                    to_path = self.remotePath[
                                                  i] + 'extensions/' + self.serverType + '/' + self.updateFile.get(
                                        keys)
                                    ssh.sftp_put(from_path, to_path)
                                    self.__checkMD5(ssh, from_path, to_path)
                            else:
                                for i in range(len(self.remotePath)):
                                    from_path = self.localPath + self.updateFile.get(keys)
                                    to_path = self.remotePath[i] + self.updateFile.get(keys)
                                    ssh.sftp_put(from_path, to_path)
                                    self.__checkMD5(ssh, from_path, to_path)

    def update_web(self):
        """
        升级web
        """
        if self.type == 'web':
            for index in range(len(self.hosts)):
                ssh = SFTP.MySSH(
                    host=self.hosts[index].split(':')[0],
                    port=int(self.hosts[index].split(':')[1]),
                    username=self.username,
                    password=self.password
                )
                for keys in self.updateFile.keys():
                    if keys != 'zip':
                        """
                        非全包更新扩展
                        """
                        continue
                    else:
                        for i in range(len(self.remotePath)):
                            cmd = "mv  %s %s" % (
                                self.remotePath[i] + self.serverType + self.updateFile.get(keys),
                                self.remotePath[i] + datetime.date.today().strftime('%Y-%m-%d') + '.zip'
                            )
                            ssh.exe(cmd)
                            from_path = self.localPath + self.updateFile.get(keys)
                            to_path = self.remotePath[i] + self.updateFile.get(keys)
                            ssh.sftp_put(from_path, to_path)
                            self.__checkMD5(ssh, from_path, to_path)
                            cmd = "cd %s" % self.remotePath[i]
                            ssh.exe(cmd)
                            cmd = "zip %s" % self.updateFile.get(keys)
                            ssh.exe(cmd)
                            cmd = "\cp -r /root/conf/* %sWEB-INF/class/conf/*" % self.remotePath[i]
                            ssh.exe(cmd)

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
            logging.error("本地文件%s不存在 %s" % (filename, e))

    def __checkMD5(self, ssh, from_path, to_path):

        cmd = "md5sum %s|cut -d ' ' -f1" % to_path
        to_md5 = ssh.exe(cmd).strip()
        from_md5 = self.__CallMD5(from_path)
        if to_md5 == from_md5:
            logging.error("update %s 路径%s 成功" % (ssh.host, to_path))
        else:
            logging.error("update %s 路径%s 失败" % (ssh.host, to_path))


if "__main__" == __name__:
    if len(sys.argv) < 2:
        print("请跟上yml文件路径")
    else:
        logger()
        data = read_file(sys.argv[1])
        username = input("请输入用户名:")
        password = getpass.getpass()
        for KEY in data.keys():
            b = Param(data.get(KEY), user=username, passwd=password)
