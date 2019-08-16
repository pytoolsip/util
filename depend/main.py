import os, json, subprocess;

# 获取依赖模块表
def getDependMap():
    with open("dependMap.json", "rb") as f:
        return json.load(f);
    return {};

# 获取已安装模块
def getInstalledMods():
    modList = [];
    ret = subprocess.check_output("pip freeze");
    for line in ret.decode().split("\n"):
        line = line.strip();
        if line:
            modList.append(line.split("==")[0]);
    return modList;

# 获取未安装模块
def getUninstalledMods():
    modList = getInstalledMods(); # 获取已安装模块
    unInstallMods = [];
    for mod in getDependMap():
        if mod not in modList:
            unInstallMods.append(mod);
    return unInstallMods;

# 安装模块
def installMods(mods):
    failedMods = [];
    for mod in mods:
        if subprocess.call(f"pip install {mod}") != 0:
            failedMods.append(mod);
    return failedMods;

if __name__ == '__main__':
    # 获取未安装模块
    unInstallMods = getUninstalledMods();

    # 打印未安装模块名称
    print("UnInstallMods:", unInstallMods)

    # # 安装未安装模块
    # failedMods = installMods(unInstallMods);
    # if len(failedMods) > 0:
    #     print(f"Pip install {failedMods} failed!");
    