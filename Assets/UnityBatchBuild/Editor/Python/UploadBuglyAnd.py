#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import zipfile

from Util import do_command, clear_dir, find_file, remove_file_container_str, remove_dir, get_split_part


def gen_parser():
    parser = argparse.ArgumentParser(description="Upload Bugly Android")
    # 含有IL2Cpp符号文件的文件夹
    parser.add_argument("--SymDir", dest="SymDir", required=True, help="IL2Cpp Sym Dir")

    # Bugly 分配的AppID
    parser.add_argument("--AppID", dest="AppID", required=True, help="AppID")

    # Bugly分配的AppKey
    parser.add_argument("--AppKey", dest="AppKey", required=True, help="AppKey")

    # Bugly工具如 buglySymbolAndroid.jar
    parser.add_argument("--BuglyToolFile", dest="BuglyToolFile", required=True, help="PackageVersion")
    return parser


# 上传安卓版Bugly符号文件
def main():
    parser = gen_parser()
    args = parser.parse_args()

    if not os.path.isdir(args.SymDir):
        sys.stderr.write("main NoExist SymDir: %s \n\n" % args.SymDir)
        sys.exit(1)

    symZip = find_file(args.SymDir, ".symbols.zip")
    if symZip == "":
        sys.stderr.write("main NoExist SymFile in Dir: %s \n\n" % args.SymDir)
        sys.exit(1)

    version = get_split_part(symZip, 1)
    if version == "":
        sys.stderr.write("main not a symFile: %s \n\n" % symZip)
        sys.exit(1)

    extractRoot = args.SymDir + "/temp"
    remove_dir(extractRoot)

    zip = zipfile.ZipFile(symZip, 'r')

    extractFiles = ["libunity.sym.so", "libil2cpp.sym"]
    for name in zip.namelist():
        for extractFile in extractFiles:
            if name.endswith(extractFile):
                zip.extract(name, extractRoot)

    zip.close()

    command = ["java", "-jar", args.BuglyToolFile, "-i", extractRoot, "-u", "-id",
               args.AppID, "-key", args.AppKey, "-version", version]

    print("Final Command:", command, "\n\n")
    isOK, error = do_command(command)

    # 清理临时解压文件夹和bugly生成的符号文件
    remove_dir(extractRoot)
    remove_file_container_str(args.SymDir, "buglySymbol_")

    if not isOK:
        sys.stderr.write("main upload bugly error: %s \n\n" % error)
        sys.exit(1)


if __name__ == '__main__':
    main()
