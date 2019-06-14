# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-06-13 10:30:15
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-06-13 12:27:24
import os, sys;
import json,zipfile,shutil;

def unzipFile(sPath, tPath):
	zf = zipfile.ZipFile(sPath, "r");
	for f in zf.namelist():
		zf.extract(f, tPath);
	zf.close();

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

def main():
	client_zip = "";
	ptip_exe = "";
	py_zip = "";
	version = "";
	target_dir = "";

	target_path = os.path.join(target_dir, "PyToolsIP", ".".join(version.split(".")[:-1]));
	target_pro_path = os.path.join(target_path, "xxx"); # f"PyToolsIP-v{version}"

	# 创建目标文件夹
	if not os.path.exists(target_dir):
		os.makedirs(target_dir);
	if not os.path.exists(target_path):
		os.makedirs(target_path);
	if not os.path.exists(target_pro_path):
		os.makedirs(target_pro_path);

	# 解压client_zip
	unzipFile(client_zip, target_pro_path);

	# 将pytoolsip.exe复制到target_pro_path
	shutil.copyfile(ptip_exe, os.path.join(target_pro_path, os.path.basename(ptip_exe)));

	# 将py_zip解压到$target_pro_path/include
	unzipFile(py_zip, os.path.join(target_pro_path, "include"));

	# 打成zip包
	zipTargetPath(target_pro_path);

if __name__ == '__main__':
	# main();
	pass;