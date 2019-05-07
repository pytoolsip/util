#-*- coding:utf-8 -*-
import os,re;
import json,zipfile,shutil;

def getJsonConfig():
    config = {};
    with open("config.json", "rb") as f:
        config = json.loads(f.read().decode("utf-8", "ignore"));
    return config;

def unzipPyEmbed(sPath, tPath):
    zf = zipfile.ZipFile(sPath, "r");
    for f in zf.namelist():
        zf.extract(f, tPath);
    zf.close();

def runGetPip(tPath, fPath):
    os.system(" ".join(["cd /d", os.path.dirname(fPath)+"&"+os.path.join(tPath, "python.exe"), os.path.basename(fPath)]));
    pass;

def updatePyPth(tPath):
    for f in os.listdir(tPath):
        fPath = os.path.join(tPath, f);
        if os.path.isfile(fPath) and re.search("python\d*\._pth", f):
            with open(fPath, "a") as f:
                f.write("\nLib/site-packages");
                f.write("\nScripts");
    pass;

def pipInstallDepends(tPath, depends):
    for mod in depends:
        os.system(" ".join(["cd /d", tPath+"&python.exe", "-m pip install", mod]));
    pass;

def zipTargetPath(tPath):
    dirName = os.path.dirname(tPath);
    zf = zipfile.ZipFile(tPath+".zip", "w");
    for root, _, files in os.walk(tPath):
        # 去掉目标根路径，只对目标文件夹下边的文件进行压缩
        for f in files:
            absPath = os.path.join(root, f);
            zf.write(absPath, os.path.relpath(absPath, dirName));
    zf.close();
    shutil.rmtree(tPath);

if __name__ == '__main__':
    # 加载配置
    cfg = getJsonConfig();
    # 转换路径
    petp = os.path.abspath(cfg["py_embed_target_path"]);
    pezp = os.path.abspath(cfg["py_embed_zip_path"]);
    gppp = os.path.abspath(cfg["get_pip_py_path"]);
    tPath = os.path.join(petp, "python");
    # 下载压缩
    unzipPyEmbed(pezp, tPath);
    runGetPip(tPath, gppp);
    updatePyPth(tPath);
    pipInstallDepends(tPath, cfg["depend_modules"]);
    zipTargetPath(tPath);
