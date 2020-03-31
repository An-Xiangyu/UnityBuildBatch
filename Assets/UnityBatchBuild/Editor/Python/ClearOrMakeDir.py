#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import sys
import os

from Util import clear_dir


def gen_parser():
    parser = argparse.ArgumentParser(description="Clear Or MakeDir")
    # 生成目录
    parser.add_argument("--TargetDir", dest="TargetDir", required=True, help="Target Dir")
    return parser


# 生成指定目录,如果已存在则清除其子文件或子文件夹
def main():
    parser = gen_parser()
    args = parser.parse_args()

    if os.path.isfile(args.TargetDir):
        sys.stderr.write("main TargetDir is file: %s \n\n" % args.TargetDir)
        sys.exit(1)

    if os.path.exists(args.TargetDir):
        clear_dir(args.TargetDir)
    else:
        os.makedirs(args.TargetDir)


if __name__ == '__main__':
    main()
