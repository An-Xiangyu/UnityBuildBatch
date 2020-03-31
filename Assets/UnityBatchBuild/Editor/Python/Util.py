# -*- coding: utf-8 -*-
import os
import subprocess
import shutil


# import time


def do_command(cmd):
    # TODO 就是怎么执行,怎么知道错误,怎么不会阻塞运行?
    sub = subprocess.Popen(cmd)

    # todo 可以设置超时
    # while sub.poll() is None:
    #     time.sleep(0.1)

    retCode = sub.wait()
    if retCode != 0:
        return False, "DoCommand Error: %r" % cmd
    else:
        return True, ""


def clear_dir(target):
    for root, dirs, files in os.walk(target, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def find_file(dir, sub):
    for root, dirs, files in os.walk(dir):
        for name in files:
            if -1 != name.find(sub):
                return os.path.join(root, name)

    return ""


def find_dir(dir, sub):
    for root, dirs, files in os.walk(dir):
        for name in dirs:
            if -1 != name.find(sub):
                return os.path.join(root, name)

    return ""

def remove_file_container_str(dir, subStr):
    findPath = find_file(dir, subStr)
    if findPath != "":
        os.remove(findPath)


def remove_dir(dstDir):
    if os.path.isdir(dstDir):
        clear_dir(dstDir)
        os.rmdir(dstDir)


def get_split_part(filePath, versionIndex, splitStr="-"):
    """获取部分字符串"""

    dirName, fileName = os.path.split(filePath)
    parts = fileName.split(splitStr)

    if len(parts) < versionIndex:
        return ""

    return parts[versionIndex]


def copy_file(dstDir, file):
    """复制文件到指定目录"""

    if not os.path.isfile(file):
        return False, "copy file error no file: %s \n\n" % file

    if not os.path.exists(dstDir):
        os.makedirs(dstDir)

    shutil.copy(file, dstDir)
    return True, ""
