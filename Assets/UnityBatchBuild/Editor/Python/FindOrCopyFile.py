#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import os
import sys

from Util import find_file, copy_file


def gen_parser():
    parser = argparse.ArgumentParser(description="Find Or Copy File")

    # 要复制的文件或还有目标文件的目录
    parser.add_argument("--FileOrDir", dest="FileOrDir", required=True, help="File Or Dir")

    # 复制到的目录
    parser.add_argument("--TargetDir", dest="TargetDir", required=True, help="Target Dir")

    # 目标文件的部分名称如 .ipa,
    # 在FileOrDir为文件时,可不指定
    parser.add_argument("--SubName", dest="SubName", help="Sub Name")
    return parser


# 复制指定文件,或在目录中查找指定文件再复制
def main():
    parser = gen_parser()
    args = parser.parse_args()

    copyFile = args.FileOrDir

    if os.path.isdir(args.FileOrDir):
        if args.SubName is None:
            sys.stderr.write("main find file in dir,but no SubName\n\n")
            sys.exit(1)

        file = find_file(args.FileOrDir, args.SubName)
        if file == "":
            sys.stderr.write("main not find file %s in %s \n\n" % ( args.SubName, args.FileOrDir))
            sys.exit(1)
        else:
            copyFile = file

    if not os.path.isfile(copyFile):
        sys.stderr.write("main not file %s\n\n" % copyFile)
        sys.exit(1)

    if os.path.isfile(args.TargetDir):
        sys.stderr.write("main Target Dir is file %s\n\n" % args.TargetDir)
        sys.exit(1)

    isOK, error = copy_file(args.TargetDir, copyFile)
    if not isOK:
        sys.stderr.write("main copy file error : %s \n\n" % error)
        sys.exit(1)


if __name__ == '__main__':
    main()
