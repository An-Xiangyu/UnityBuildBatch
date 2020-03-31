#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import os
import sys

from Util import do_command, find_file, get_split_part, find_dir


def gen_parser():
    parser = argparse.ArgumentParser(description="Zip Sym File")
    # 有ipa包的文件夹
    parser.add_argument("--BuildDir", dest="BuildDir", required=True, help="Build Dir has ipa")

    # 有符号文件的目录
    parser.add_argument("--SymRoot", dest="SymRoot", required=True, help="Xcode dSYM Path")

    # 符号压缩文件路径脚本
    parser.add_argument("--SaveTemplate", dest="SaveTemplate", required=True, help="SaveTemplate")
    return parser


# zip ios 符号文件
# Jenkins xCode 插件旧版本才需要此脚本
# 因为Bugly上传符号表需要版本号,因此需要先解析ipa包名的版本号,再与SaveTemplate合成最终路径
def main():
    parser = gen_parser()
    args = parser.parse_args()

    if not os.path.isdir(args.BuildDir):
        sys.stderr.write("main not a dir: %s \n\n" % args.BuildDir)
        sys.exit(1)

    ipaPath = find_file(args.BuildDir, ".ipa")
    if ipaPath == "":
        sys.stderr.write("main no ipa in dir: %s \n\n" % args.BuildDir)
        sys.exit(1)

    version = get_split_part(ipaPath, 1)
    if version == "":
        sys.stderr.write("main not a ipa: %s \n\n" % ipaPath)
        sys.exit(1)

    savePath = args.SaveTemplate % version

    # Xcode新版本插件会打包符号文件到输出目录,不用压缩了
    if os.path.isfile(savePath):
        sys.exit(0)

    symPath = args.SymRoot
    if not os.path.isdir(args.SymRoot):
        sys.stderr.write("main SymRoot is not dir: %s \n\n" % args.SymRoot)
        sys.exit(1)

    else:
        endStr = ".app.dSYM"
        if not args.SymRoot.endswith(endStr):
            findDir = find_dir(args.SymRoot, endStr)
            if findDir == "":
                sys.stderr.write("main no dSYM in dir: %s \n\n" % args.SymRoot)
                sys.exit(1)
            else:
                symPath = findDir

    command = ["ditto", "-c", "-k", "--keepParent", "-rsrc", symPath, savePath ]

    print("Final Command:", command, "\n\n")
    isOK, error = do_command(command)

    if not isOK:
        sys.stderr.write("main zip dSYM error: %s \n\n" % error)
        sys.exit(1)


if __name__ == '__main__':
    main()
