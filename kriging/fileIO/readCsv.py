#!/usr/bin/python
#coding=utf-8

__doc__ = ''' 从data文件夹中的csv读取数据，一共有34个csv文件，
每个csv中的数据除了尾部部分数据有差别外，其他数据
大致一样，每次读取数据取共同部分即可。
'''
import os,sys
import csv


class readCsv:
	'''读取csv文件'''
	def __init__(self, path):
		'''path 为csv文件所在目录'''
		self.dirPath = path
		self.fileList = self.getFileName(path)
		
	#用于初始化时读取所有csv的文件名
	def getFileName(self, path):
		fileList = os.listdir(path)
		return [os.path.join(self.dirPath, item) for item in fileList]
	
	#根据文件名，每个文件的起始行，步长，读取文件数据
	def getFileData(self, step = 10, startRow=2):
		totalData = [];
		for item in self.fileList:
			csvfile = file(item, 'rb')
			reader = csv.reader(csvfile)
			tmpData = [line for line in reader]
			fileLen = len(tmpData)
			
			#根据文件名获取传感器编号
			fileName = os.path.basename(item)
			sensorNum = fileName[fileName.find('-')+1 : fileName.find('.')]
			
			#根据起始行和步长提取出文件中的数据，文件格式为  [传感器编号，温度，湿度]
			fileData = [[sensorNum, tmpData[i][2], tmpData[i][3]] for i in range(startRow, fileLen, step)]
			totalData.append(fileData[0])
		return totalData
		
			
if __name__ == "__main__":
	rd = readCsv('/home/captain/文档/code/python/labWork/kriging/data');
	print rd.getFileData()
