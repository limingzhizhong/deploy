import hashlib
import logging


def CallMD5(filename):
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


def checkMD5(ssh, from_path, to_path):
    cmd = "md5sum %s|cut -d ' ' -f1" % to_path
    to_md5 = ssh.exe(cmd).strip()
    from_md5 = CallMD5(from_path)
    if to_md5 == from_md5:
        logging.error("update %s 路径%s 成功" % (ssh.host, to_path))
    else:
        logging.error("update %s 路径%s 失败" % (ssh.host, to_path))
