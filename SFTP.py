import paramiko
import sys





class MySSH(object):
    """
    1、创建一个ssh对象，将host port 用户名密码初始化，port默认值为22，用户名默认为root，密码默认空
    2、创建ssh链接，并将目录确定到指定目录
    3、创建sftp链接，提供调用方法，put和get
    4、提供命令执行方法cmd
    5、关闭链接
    """

    def __init__(self, host, port=9300, username='', password=''):

        """
        :rtype: object
        :param host: 远程主机地址
        :param port: 远程主机端口
        :param username: 用户名
        :param password: 密码
        """

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssh = None
        self.sftp = None
        self.ssh_connect()

    @staticmethod
    def __callback(a, b):
        sys.stdout.write('Data Transmission %10d [%3.2f%%]\r' % (a, a * 100. / int(b)))
        sys.stdout.flush()

    def ssh_connect(self):
        try:
            # print("开始ssh连接远程主机%s" % self.host)
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host, self.port, username=self.username, password=self.password)
            stdin, stdout, stderr = self.ssh.exec_command('rm -f /home/GameServer*/logs/*')
            #print(stdout.readline())
            #print(u'连接SSH %s 成功...' % self.host)
        except Exception as e:
            print('ssh %s@%s:%s: %s' % (self.username, self.host, self.port, e))
            # exit()

    def sftp_put(self, from_path, to_path) -> object:

        try:
            # print("开始sftp连接远程主机%s" % self.host)
            self.t = paramiko.Transport((self.host, self.port))
            self.t.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.t)
            self.sftp.put(from_path, to_path, callback=self.__callback(10, 10))
            self.t.close()
            print("%s 上传成功" % self.host)

        except Exception as e:
            print('sftp %s@%s: %s' % (self.username, self.host, e))

    def sftp_get(self, from_path, to_path) -> object:

        try:
            # print("开始sftp连接远程主机%s" % self.host)
            self.t = paramiko.Transport((self.host, self.port))
            self.t.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.t)
            self.sftp.get(to_path, from_path)
            self.t.close()
            # print("%s 上传成功" % self.host)

        except Exception as e:
            print('sftp %s@%s: %s' % (self.username, self.host, e))

            # exit()

    def exe(self, cmd):
        '''''
            让远程服务器执行cmd
        '''
        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            self.a = stdout.readline()
            #if cmd.find('md5') == 0:
        except Exception as e:
            print("", e)
        return self.a

    def close(self):
        self.ssh.close()

    def __del__(self):
        self.close()
