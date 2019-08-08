# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-08-08 17:50:27
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-08-08 19:14:23
import os, re;

# 根据文件夹，获取内容
def writeContentByFile(path, file):
	with open(path, "r", encoding = "utf-8") as f:
		for line in f.readlines():
			mtObj = re.match("^from (.*) import \*.*#\s*local", line);
			if mtObj:
				writeContentByFile(mtObj.group(1).strip()+".py", file);
			elif not re.match("^#.*", line):
				file.write(line);

# 合并文件内容，并输出到指定文件
def merge(srcFile, tgtFile):
	with open(tgtFile, "w+", encoding = "utf-8") as f:
		writeContentByFile(srcFile, f);

# 打包文件
def pack(tgtFile):
	code = os.system(f"pyInstaller -F -w {tgtFile} --distpath=./dist");
	if code != 0:
		raise Exception(f"Pack failed! [code:{code}]");

if __name__ == '__main__':
	tgtPath = "installer.py"; # 目标文件路径
	if os.path.exists("main.py"):
		merge("main.py", tgtPath);
		pack(tgtPath);