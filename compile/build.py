# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-05-10 12:29:30
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-10 13:28:46
import os,json;
import compileall;

def getJsonConfig():
    config = {};
    with open("config.json", "rb") as f:
        config = json.loads(f.read().decode("utf-8", "ignore"));
    return config;

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
    # 编译文件
    compileDir(ppd, cfg.get("is_remove_original", True));