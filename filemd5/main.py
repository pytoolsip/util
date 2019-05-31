# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-05-30 11:58:59
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-31 11:15:57
import os;
import hashlib;
import json,zipfile,shutil;

maxBuf = 1024 * 16; # 单次获取md5的最大缓冲量

def getJsonConfig():
	config = {};
	with open("config.json", "rb") as f:
		config = json.loads(f.read().decode("utf-8", "ignore"));
	return config;

# 解压zip包
def unzipFile(sPath, tPath):
	zf = zipfile.ZipFile(sPath, "r");
	for f in zf.namelist():
		zf.extract(f, tPath);
	zf.close();

# 根据文件获取md5值
def getMd5ByFile(file, basePath = ""):
	filePath = os.path.join(basePath, file);
	if not os.path.isfile(filePath):
		return "";
	hm = hashlib.md5();
	with open(filePath, "rb") as f:
		buf = f.read(maxBuf);
		while buf:
			hm.update(buf);
			buf = f.read(maxBuf);
	return hm.hexdigest();

# 获取文件md5数据
def getFileMd5Map(tPath, filterList = []):
	fileMd5Map = {};
	for file in os.listdir(tPath):
		if file in filterList:
			continue;
		filePath = os.path.join(tPath, file);
		if os.path.isdir(filePath):
			for root, _, files in os.walk(filePath):
				for f in files:
					relPath = os.path.relpath(os.path.join(root, f), tPath).replace("\\", "/");
					fileMd5Map[relPath] = getMd5ByFile(relPath, basePath = tPath);
		else:
			relPath = os.path.relpath(filePath, tPath).replace("\\", "/");
			fileMd5Map[relPath] = getMd5ByFile(relPath, basePath = tPath);
	return fileMd5Map;

# 保存json文件
def saveJson(data, filePath):
	with open(filePath, "wb") as f:
		f.write(json.dumps(data, sort_keys = True, indent = 2, separators=(',', ':')).encode("utf-8"));

if __name__ == '__main__':
	# 加载配置
	cfg = getJsonConfig();
	srcPath = os.path.abspath(cfg["source_file"]);
	tarPath = os.path.abspath(cfg["target_path"]);
	filterList = cfg.get("filter_list", []); # 过滤数据
	tempPath = os.path.join(tarPath, "tempPath");
	# 解压文件
	unzipFile(srcPath, tempPath);
	# 保存json文件
	saveJson({
		"filterList" : filterList,
		"md5Map" : getFileMd5Map(tempPath, filterList), # 获取文件md5数据
	}, os.path.join(tarPath, "fileMd5Map.json"));
	# 删除临时文件
	shutil.rmtree(tempPath);