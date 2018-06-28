def put_files():
    for KEY in data.keys():
        b = Param(data.get(KEY))
        for index in range(len(b.hosts)):
            host = b.hosts[index].split(':')[0]
            port = int(b.hosts[index].split(':')[1])
            ssh = SFTP.MySSH(host=host, port=port, username=user, password=passwd)
            for keys in b.updateFile.keys():
                if b.type == 'hz':
                    for i in range(len(b.remotePath)):
                        from_path = b.localPath + b.updateFile.get(keys)
                        to_path = b.remotePath[i] + 'lib/' + b.updateFile.get(keys)
                        # print("正在拷贝 %s" % b.type)
                        ssh.sftp_put(from_path, to_path)
                        cmd = "md5sum %s|cut -d ' ' -f1" % to_path
                        to_md5 = ssh.exe(cmd).strip()
                        from_md5 = self.__CalcMD5(from_path)
                        # print(to_md5 == from_md5)
                        if to_md5 == from_md5:
                            continue
                            # print("主机%s拷贝成功：%s " % (host, b.updateFile.get(keys)))
                        else:
                            print("主机%s上传文件%smd5不正确！！！！" % (host, b.updateFile.get(keys)))

                else:
                    if keys != 'extensions':
                        for i in range(len(b.remotePath)):
                            from_path = b.localPath + b.updateFile.get(keys)
                            to_path = b.remotePath[i] + 'extensions/' + b.type + '/' + b.updateFile.get(keys)
                            # print("正在拷贝 %s" % b.type)
                            ssh.sftp_put(from_path, to_path)
                            cmd = "md5sum %s|cut -d ' ' -f1" % to_path
                            to_md5 = ssh.exe(cmd).strip()
                            from_md5 = CalcMD5(from_path)
                            # print(to_md5 == from_md5)
                            if to_md5 == from_md5:
                                continue
                                # print("主机%s拷贝成功：%s " % (host, b.updateFile.get(keys)))
                            else:
                                print("主机%s上传文件%smd5不正确！！！！" % (host, b.updateFile.get(keys)))
                    else:
                        if keys != 'yml':
                            for i in range(len(b.remotePath)):
                                from_path = b.localPath + b.updateFile.get(keys)
                                to_path = b.remotePath[i] + 'extensions/__lib__/' + b.updateFile.get(keys)
                                # print("正在拷贝 %s" % b.updateFile.get(keys))
                                ssh.sftp_put(from_path, to_path)
                                cmd = "md5sum %s|cut -d ' ' -f1" % to_path
                                to_md5 = ssh.exe(cmd).strip()
                                from_md5 = CalcMD5(from_path)
                                if to_md5 == from_md5:
                                    continue
                                    # print("主机%s拷贝成功：%s " % (host, b.updateFile.get(keys)))
                                else:
                                    print("主机%s上传文件%smd5不正确！！！！" % (host, b.updateFile.get(keys)))
                        else:
                            for i in range(len(b.remotePath)):
                                from_path = b.localPath + b.updateFile.get(keys)
                                to_path = b.remotePath[i] + b.updateFile.get(keys)
                                # print("正在拷贝 %s" % b.updateFile.get(keys))
                                ssh.sftp_put(from_path, to_path)
                                cmd = "md5sum %s|cut -d ' ' -f1" % to_path
                                to_md5 = ssh.exe(cmd).strip()
                                from_md5 = CalcMD5(from_path)
                                if to_md5 == from_md5:
                                    continue
                                    # print("主机%s拷贝成功：%s " % (host, b.updateFile.get(keys)))
                                else:
                                    print("主机%s上传文件%smd5不正确！！！！" % (host, b.updateFile.get(keys)))
