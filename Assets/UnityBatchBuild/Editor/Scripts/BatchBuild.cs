using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;

#if UNITY_2018_1_OR_NEWER
using UnityEditor.Build.Reporting;
#endif

public static class BatchBuild
{
    /// <summary>
    /// 批处理启动函数
    /// </summary>
    public static void Build()
    {
        var args = GetArgs();

        foreach (var pair in args)
        {
            Debug.LogFormat("args input {0} : {1}", pair.Key, pair.Value);
        }

        string saveFile;
        if (!args.TryGetValue("SaveFile", out saveFile))
        {
            Debug.LogError("BatchBuild Build() saveFile error");
            EditorApplication.Exit(-1);
            return;
        }


        var isDebug = false;
        string isDebugStr;
        if (args.TryGetValue("Debug", out isDebugStr))
        {
            isDebug = 0 == string.Compare(isDebugStr, "true", StringComparison.OrdinalIgnoreCase);
        }

        Debug.Log("BatchBuild Build() IsDebug:" + isDebug);

        var buildOptions = isDebug ? BuildOptions.Development | BuildOptions.ConnectWithProfiler : BuildOptions.None;

        if (EditorUserBuildSettings.activeBuildTarget == BuildTarget.Android)
        {
            SetAndroidPass(args);
        }


        var report = BuildPipeline.BuildPlayer(EditorBuildSettings.scenes, saveFile, EditorUserBuildSettings.activeBuildTarget, buildOptions);
#if UNITY_2018_1_OR_NEWER
        if (report.summary.result != BuildResult.Succeeded && report.summary.result != BuildResult.Cancelled)
        {
            Debug.LogError("BatchBuild Build() error");
            EditorApplication.Exit(-1);
        }

#else
        if (!string.IsNullOrEmpty(report))
        {
            Debug.LogError("BatchBuild Build() error:" + report);
            EditorApplication.Exit(-1);
        }
#endif
    }


    private static void SetAndroidPass(Dictionary<string, string> args)
    {
        string keyFileStr;
        if (args.TryGetValue("KeyFile", out keyFileStr))
        {
            if (!File.Exists(keyFileStr))
            {
                Debug.LogError("BatchBuild SetAndroidPass() keyFile Not Exists");
                return;
            }
        }

        PlayerSettings.Android.keystoreName = keyFileStr;


        string keyPassStr;
        args.TryGetValue("KeyPass", out keyPassStr);
        PlayerSettings.Android.keystorePass = keyPassStr;


        string aliasName;
        args.TryGetValue("AliasName", out aliasName);
        PlayerSettings.Android.keyaliasName = aliasName;


        string aliasPass;
        args.TryGetValue("AliasPass", out aliasPass);
        PlayerSettings.Android.keyaliasPass = aliasPass;
    }


    private static Dictionary<string, string> GetArgs()
    {
        var args = new Dictionary<string, string>();

        foreach (var arg in Environment.GetCommandLineArgs())
        {
            var strings = arg.Split(new[] {'~'}, StringSplitOptions.RemoveEmptyEntries);
            if (strings.Length == 2)
            {
                args.Add(strings[0], strings[1]);
            }
        }

        return args;
    }
}