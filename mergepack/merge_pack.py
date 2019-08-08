# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-08-08 17:50:27
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-08-08 19:28:01
import os, re;

# 导入过滤
importMap = [];

# 根据文件夹，获取内容
def writeContentByFile(path, file):
	with open(path, "r", encoding = "utf-8") as f:
		for line in f.readlines():
			mt = re.match("^from (.*) import \*.*#\s*local", line);
			if mt:
				writeContentByFile(mt.group(1).strip()+".py", file);
			elif not re.match("^#.*", line):
				mt1 = re.match("^.*(import \w+).*", line);
				if mt1:
					ip = mt1.group(1);
					if ip in importMap:
						continue;
					importMap.append(ip);
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
		# pack(tgtPath);