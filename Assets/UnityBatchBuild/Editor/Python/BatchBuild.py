#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
import re
import sys

from Util import do_command


def gen_parser():
    parser = argparse.ArgumentParser(description="Unity Batch Script")
    # Unity编辑器路径
    parser.add_argument("--UnityPath", dest="UnityPath", required=True, help="Unity Path")
    # Unity工程路径
    parser.add_argument("--ProjectPath", dest="ProjectPath", required=True, help="Project Path")
    # UntiyLog输出路径
    parser.add_argument("--LogFile", dest="LogFile", required=True, help="Log File")

    # 生成安装包平台,Android或者iOS
    parser.add_argument("--BuildTarget", dest="BuildTarget", required=True, help="Build Target Android or iOS")

    # 给Unity脚本的参数,如是否调试,输出路径等, 以~号连接参数名与值, 空格分割多个参数
    # 以~号连接参数名与值, 空格分割多个参数
    # 如 SaveFile~d:\BuildOutput Debug~true(或false)
    parser.add_argument("--BuildArgs", dest="BuildArgs", required=True, help="Build Args")
    return parser

# 调用Unity打包脚本,参数如下
def main():
    parser = gen_parser()
    args = parser.parse_args()

    command = [args.UnityPath, "-batchmode", "-nographics", "-quit", "-logFile", args.LogFile, "-buildTarget",
               args.BuildTarget, "-projectPath", args.ProjectPath, "-executeMethod", "BatchBuild.Build"]
    unityArgs = re.split(' ', args.BuildArgs)
    finalCommand = command + unityArgs

    print("Final Command:", finalCommand, "\n\n")
    isOK, error = do_command(finalCommand)
    if not isOK:
        sys.stderr.write("main Build error: %s \n\n" % error)
        sys.exit(1)


if __name__ == '__main__':
    main()
