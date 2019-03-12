# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-03-12 17:00:52
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-12 18:08:22
import sys;
import os;
import re;
import json;

def checkFilePath(filePath):
	if re.search("\w+\.py$", filePath):
		return True;
	return False;

# 获取所有文件列表
def getFileList(path):
	fileList = [];
	fileNameList = [];
	def checkAllFile(dirPath):
		for file in os.listdir(dirPath):
			isCanImport = False;
			filePath = os.path.join(dirPath, file);
			if os.path.isdir(filePath):
				checkAllFile(filePath);
				isCanImport = True;
			elif checkFilePath(filePath):
				fileList.append(filePath);
				isCanImport = True;
			if isCanImport:
				# 获取文件名
				result = re.match("(\w+)(\.py)?$", file);
				if result and (result.group(1) not in fileNameList):
					fileNameList.append(result.group(1));
	if os.path.isdir(path):
		checkAllFile(path);
	return fileList, fileNameList

# 获取所有文件列表中import的模块名
def getImportMapByFileList(fileList, excludeLists = []):
	importList = [];
	def checkImportList(file):
		with open(file, "rb") as f:
			for line in f.readlines():
				line = line.decode("utf-8", "ignore");
				result = re.match("^from (\w+)\.?.*import.*", line);
				if result and not checkKeyInExcludeLists(result.group(1), excludeLists) and (result.group(1) not in importList):
					importList.append(result.group(1));
				else:
					result = re.match("^import (\w+)\.?.*", line);
					if result and not checkKeyInExcludeLists(result.group(1), excludeLists) and (result.group(1) not in importList):
						importList.append(result.group(1));
			f.close();
	for filePath in fileList:
		checkImportList(filePath);
	return importList;

# 检测key值是否在排除列表中
def checkKeyInExcludeLists(key, excludeLists = []):
	for excludeMap in excludeLists:
		if key in excludeMap:
			return True;
	return False;

# 获取所有文件列表中import的模块名
def getImportList(path, excludeLists = []):
	fileList, fileNameList = getFileList(path);
	excludeLists.append(fileNameList);
	return getImportMapByFileList(fileList, excludeLists);

# 过滤import的模块
def filterImportList(importList = [], filterList = []):
	filteredList = [];
	for i in range(len(importList)-1, -1, -1):
		importKey = importList[i];
		if importKey in filterList:
			importList.pop(i);
			filteredList.append(importKey);
	return filteredList, importList;

# 扩展import的模块
def expandImportList(importList = [], expandList = []):
	expandedList = [];
	for importKey in expandList:
		if importKey not in importList:
			importList.append(importKey);
			expandedList.append(importKey);
	return expandedList, importList;

# 校验import的模块
def verifyImportList(importList = []):
	unImportList = [];
	for i in range(len(importList)-1, -1, -1):
		importKey = importList[i];
		try:
			__import__(importKey);
		except Exception as e:
			print(e);
			importList.pop(i);
			unImportList.append(importKey);
	return unImportList, importList;

def writeJsonFile(filePath, data):
	with open(filePath, "w") as f:
		f.write(json.dumps(data, indent=4));
		f.close();

def readJsonFile(filePath):
	data = {};
	with open(filePath, "rb") as f:
		data = json.loads(f.read().decode("utf-8", "ignore"));
		f.close();
	return data;


if __name__ == '__main__':
	cwd = os.getcwd();
	searchPath, targetPath = cwd, cwd;
	if len(sys.argv) > 1:
		searchPath = sys.argv[1];
	if len(sys.argv) > 2:
		targetPath = sys.argv[2];
	# 过滤文件名列表
	excludeList = ["TemplateWindowUI", "TemplateDialogUI", "TemplateViewUI"];
	# 获取import的模块名列表
	ipList = getImportList(searchPath, excludeLists = [excludeList]);
	# 过滤模块名
	filterList = ["wx", "grpc", "google"];
	filterImportList(ipList, filterList = filterList);
	# 添加模块名
	expandList = ["wxPython", "grpcio", "protobuf", "grpcio-tools"];
	expandImportList(ipList, expandList = expandList);
	# 校验import的模块
	# verifyImportList(ipList);
	# 写入Json文件
	writeJsonFile(targetPath + "\\importList.json", ipList);
	
	# importMap = readJsonFile(searchPath + "\\json\\importMap.json");