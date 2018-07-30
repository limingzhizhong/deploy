import SFTP
import datetime
import logging
from utils import check


def logger():
    logging.basicConfig(
        filename="update.log",
        level=logging.ERROR,
        format="%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p"
    )


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
                        check.checkMD5(ssh, from_path, to_path)
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
                                check.checkMD5(ssh, from_path, to_path)
                        else:
                            if keys != 'yml':
                                for i in range(len(self.remotePath)):
                                    from_path = self.localPath + self.updateFile.get(keys)
                                    to_path = self.remotePath[
                                                  i] + 'extensions/' + self.serverType + '/' + self.updateFile.get(
                                        keys)
                                    ssh.sftp_put(from_path, to_path)
                                    check.checkMD5(ssh, from_path, to_path)
                            else:
                                for i in range(len(self.remotePath)):
                                    from_path = self.localPath + self.updateFile.get(keys)
                                    to_path = self.remotePath[i] + self.updateFile.get(keys)
                                    ssh.sftp_put(from_path, to_path)
                                    check.checkMD5(ssh, from_path, to_path)

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
                            from_path = self.localPath + self.updateFile.get(keys)
                            to_path = self.remotePath[i] + self.updateFile.get(keys)
                            cmd = "zip -r  %s %s" % (
                                self.remotePath[i] + datetime.date.today().strftime('%Y-%m-%d') + '.zip',
                                self.remotePath[i] + self.serverType
                            )
                            logging.info("开始备份文件：%s" % cmd)
                            ssh.exe(cmd)
                            cmd = "rm -fr %s" % self.remotePath[i] + self.serverType
                            logging.info("开始删除文件：%s" % cmd)
                            ssh.exe(cmd)
                            ssh.sftp_put(from_path, to_path)
                            check.checkMD5(ssh, from_path, to_path)
                            cmd = 'unzip -qo %s -d %s ' % (to_path, self.remotePath[i] + self.serverType)
                            logging.info("开始解压文件：%s" % cmd)
                            ssh.exe(cmd)
                            cmd = '\cp -r /root/conf/* %sWEB-INF/class/conf/*' % self.remotePath[i]
                            ssh.exe(cmd)
                            ssh.sftp_put('/home/update/lib/cache-api.yml',
                                         self.remotePath[i] + self.serverType + 'WEB-INF/class/cache-api.yml')
                            cmd = '\cp -r /root/cache-api.yml/* %sWEB-INF/class/' % self.remotePath[i]
                            ssh.exe(cmd)


