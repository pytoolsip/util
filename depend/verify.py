import os, json, subprocess;

# 获取依赖模块表
def getDependMap():
    with open("dependMap.json", "rb") as f:
        return json.load(f);
    return {};

# 保存依赖模块表
def saveDependMap(dependMap):
    with open("dependMap.json", "w") as f:
        json.dump(dependMap, f);

# 获取工具依赖模块列表
def getToolDepends(toolName):
    modList = [];
    with open("depend.mod", "r") as f:
        for line in f.readlines():
            mod = line.strip();
            if mod not in modList:
                modList.append(mod);
    return modList;

# 安装模块
def installMod(mod):
    print(f"Pip install {mod} ...");
    # if subprocess.call(f"pip install {mod}") != 0:
    #     print(f"Pip install {mod} failed!");
    #     return False;
    # return True;

# 卸载模块
def uninstallMod(mod):
    print(f"Pip uninstall {mod} ...");
    # if subprocess.call(f"pip uninstall {mod}") != 0:
    #     print(f"Pip uninstall {mod} failed!");
    #     return False;
    # return True;

# 新增工具
def addTool():
    dependMap = getDependMap();
    modList = getToolDepends("");
    for mod in modList:
        if mod not in dependMap:
            if installMod(mod):
                dependMap[mod] = 1;
        else:
            dependMap[mod] += 1;
    saveDependMap(dependMap);

# 移除工具
def removeTool():
    dependMap = getDependMap();
    modList = getToolDepends("");
    for mod in modList:
        if mod in dependMap:
            dependMap[mod] -= 1;
        if dependMap[mod] <= 0:
            if uninstallMod(mod):
                dependMap.pop(mod);
    saveDependMap(dependMap);

if __name__ == '__main__':
    removeTool()
    