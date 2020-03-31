#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import os
import sys


from Util import do_command, find_file


def gen_parser():
    parser = argparse.ArgumentParser(description="Upload Fir")
    # fir.im平台生成Token
    parser.add_argument("--Token", dest="Token", required=True, help="Fir Token")
    # 安装包所在目录
    parser.add_argument("--TargetDir", dest="TargetDir", required=True, help="Package Dir or Pakcage Dir Root")
    # 安装包平台, Android或iOS
    parser.add_argument("--BuildTarget", dest="BuildTarget", required=True, help="BuildTarget Android or iOS")

    # 上传注释
    parser.add_argument("--Note", dest="Note", required=True, help="Show Note")
    return parser


# 上传到Fir发布平台
def main():
    parser = gen_parser()
    args = parser.parse_args()

    if not os.path.isdir(args.TargetDir):
        sys.stderr.write("main NoExist TargetDir: %s \n\n" % args.TargetDir)
        sys.exit(1)

    if args.BuildTarget.lower() == "android":
        fileExt = ".apk"
    elif args.BuildTarget.lower() == "ios":
        fileExt = ".ipa"
    else:
        sys.stderr.write("main error BuildTarget: %s \n\n" % args.BuildTarget)
        sys.exit(1)

    packagePath = find_file(args.TargetDir, fileExt)
    if packagePath == "":
        sys.stderr.write("main not package file in dir: %s \n\n" % args.TargetDir)
        sys.exit(1)

    tokenCmd = "--token=" + args.Token
    changelog = "--changelog=" + args.Note
    command = ["fir", "publish", tokenCmd, packagePath, changelog]
    print("Final Command:", command, "\n\n")

    isOK, error = do_command(command)

    if not isOK:
        sys.stderr.write("main Upload Fir error: %s \n\n" % error)
        sys.exit(1)


if __name__ == '__main__':
    main()
