# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-05-10 12:29:30
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-10 14:26:29
import os,json,shutil;
import compileall;

def getJsonConfig():
    config = {};
    with open("config.json", "rb") as f:
        config = json.loads(f.read().decode("utf-8", "ignore"));
    return config;

def copyDir(srcDir, targetDir):
    tdPath = os.path.join(targetDir, os.path.basename(srcDir));
    shutil.copytree(srcDir, tdPath);
    return tdPath;

def compileDir(dirPath, isRemoveOri):
	compileall.compile_dir(dirPath);
	if isRemoveOri:
		for root, dirs, files in os.walk(dirPath):
			for name in files:
				if name.endswith(".py"):
					os.remove(os.path.join(root,name));

if __name__ == '__main__':
    # 加载配置
    cfg = getJsonConfig();
    # 转换路径
    ppd = os.path.abspath(cfg["py_project_dir"]);
    pptd = os.path.abspath(cfg["py_project_target_dir"]);
    # 拷贝工程文件
    tdPath = copyDir(ppd, pptd);
    # 编译文件
    compileDir(tdPath, cfg.get("is_remove_original", True));