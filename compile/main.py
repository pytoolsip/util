# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-05-10 12:29:30
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-10 14:26:29
import os,json,shutil,re,zipfile;
import compileall;

def getJsonConfig():
    config = {};
    with open("config.json", "rb") as f:
        config = json.loads(f.read().decode("utf-8", "ignore"));
    return config;

# 拷贝工程
def copyProject(sPath, tPath):
	if not os.path.exists(tPath):
		os.makedirs(tPath);
	for name in os.listdir(sPath):
		# 过滤git文件
		if re.search("^\.git.*", os.path.basename(name)):
			continue;
		# 拼接地址
		srcPath = os.path.join(sPath, name);
		targetPath = os.path.join(tPath, name);
		if os.path.basename(name) in ["assets", "common"]:
			copyProject(srcPath, targetPath);
			continue;
		if os.path.isfile(srcPath):
			shutil.copyfile(srcPath, targetPath);
		else:
			shutil.copytree(srcPath, targetPath);

def copyDir(srcDir, targetDir):
	tdPath = os.path.join(targetDir, "PyToolsIP");
	copyProject(srcDir, tdPath);
	return tdPath;

def compileDir(dirPath, isRemoveOri):
	compileall.compile_dir(dirPath);
	if isRemoveOri:
		# 移动dirPath下__pycache__里的文件，并移除py文件
		for root, dirs, files in os.walk(dirPath):
			for path in dirs:
				if os.path.basename(path) != "__pycache__":
					continue;
				pycachePath = os.path.join(root,path);
				for name in os.listdir(pycachePath):
					fPath = os.path.join(pycachePath,name);
					if os.path.isfile(fPath):
						# 重命名文件
						mtObj = re.match("^(.*)\..*(\..*)$", name);
						if mtObj:
							newName = "".join(mtObj.groups());
							newFPath = os.path.join(pycachePath,newName);
							os.rename(fPath, newFPath);
							fPath = newFPath;
						# 移动文件
						shutil.move(fPath, os.path.join(pycachePath, ".."));
				# 删除__pycache__文件夹
				shutil.rmtree(pycachePath);
			for name in files:
				if name.endswith(".py"):
					os.remove(os.path.join(root,name));

def zipTargetPath(tDir):
    tPath = os.path.join(tDir, "PyToolsIP");
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
    ppd = os.path.abspath(cfg["py_project_dir"]);
    pptd = os.path.abspath(cfg["py_project_target_dir"]);
    # 拷贝工程文件
    tdPath = copyDir(ppd, pptd);
    # 编译文件
    compileDir(tdPath, cfg.get("is_remove_original", True));
    # 打成zip包
    zipTargetPath(pptd);