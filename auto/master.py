#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import git
import re
from ftplib import FTP


def git_master(dir_repo, commit_msg, root_path):
    repo = git.Repo(root_path + dir_repo)
    print('>> start git...')
    try:
        repo.git.pull()
    except Exception as e:
        print(e)
    else:
        if repo.is_dirty():
            status = repo.git.status()
            regex = re.compile("modified:\s\s\s(.*?)\n").findall(status)
            repo.git.add('-u')
            repo.git.commit('-m', commit_msg)
            repo.git.push()
            print('>> git push finished.')
            return regex
        else:
            print('>> No modified files.')
            print('****************************** end')
            print(' ')


def ftp_connect(host, port, username, password):
    f = FTP()
    f.connect(host, port)
    f.login(username, password)
    return f


def upload_file(f, remote_path, local_path):
    buf_size = 1024
    fp = open(local_path, 'rb')
    f.storbinary('STOR ' + remote_path, fp, buf_size)
    fp.close()


def batch_git_upload(dirname_list, commit, cluster):
    for dirname in dirname_list:
        print('********** ' + dirname + ' ********** running')
        files_list = git_master(dirname, commit, path)
        if files_list:
            for py in files_list:
                remote = cluster + dirname + '/' + py
                local = path + dirname + '/' + py
                try:
                    upload_file(ftp, remote, local)
                    print('>> ' + py + ' ———— ftp upload success.')
                except Exception as e:
                    print('     ⬇️⬇️⬇️ { Error } ⬇️⬇️⬇️')
                    print(py + ' 上传失败，请手动上传到ftp')
                    print('报错： ' + str(e))
                    print('remote_path: ' + remote)
                    print('local_path: ' + local)
                    print('     ⬆️⬆️⬆️ { Error } ⬆️⬆️⬆️')
            print('********** ' + dirname + ' ********** end')
            print(' ')


if __name__ == "__main__":
    # todo 项目文件夹要设置可写入权限(非常重要)
    ftp = ftp_connect("118.24.18.235", 21, "bing", "JWrWbBT3WccKzGZD")
    path = '/Users/bing/PycharmProjects/auto_git/auto_git/'
    dirname_list = ['UDIWJS4L', 'V2UFJ8SH9']
    commit_msg = 'this is a test'
    site_cluster = '' + '/'
    batch_git_upload(dirname_list, commit_msg, site_cluster)

