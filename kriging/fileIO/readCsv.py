#!/usr/bin/python
#-*- coding:utf-8 -*-

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
		return [os.path.join(self.dirPath, item) for item in fileList if item != 'pos' and item != 'result']  #把pos和result目录排除掉
	
	#根据文件名，每个文件的起始行，步长，读取文件数据
	#设置步长的原因是因为相邻的多个数据中温度和湿度的数值几乎不变，可以省略掉一些数值避免重复计算
	#total表示选取数据的个数
	def getSensorData(self, totalNum, step = 10, startRow=2):
		totalData = {};
		for item in self.fileList:
			csvfile = file(item, 'rb')
			reader = csv.reader(csvfile)
			tmpData = [line for line in reader]
			
			#每个文件的末尾含有一些无用数据，因此删除一些
			fileLen = len(tmpData)-4

			#取totalNum和fileLen/10的最小值，防止所给的totalNum超出总的数据量
			totalNum = min(totalNum, fileLen/10)
			
			#根据文件名获取传感器编号
			fileName = os.path.basename(item)
			sensorNum = fileName[fileName.find('-')+1 : fileName.find('.')]
			
			#根据起始行和步长提取出文件中的数据，文件格式为  [传感器编号，温度，湿度]
			fileData = [(tmpData[i][2], tmpData[i][3]) for i in range(startRow, fileLen, step)]

			#当传感器数据太多时，可以控制取出传感器数据的个数
			totalData[sensorNum] = fileData[:totalNum]
		return totalData
	
	#获取传感器坐标，文件格式是，传感器编号，x坐标，y坐标，z坐标
	def getSensorPos(self):
		posData = {}
		posFile = os.path.join(self.dirPath, 'pos/pos.csv')
		with open(posFile) as f:
			fCsv = csv.reader(f)
			for row in fCsv:
				posData[row[0]] = (row[1], row[2],row[3])
			return posData
		
			
if __name__ == "__main__":
	rd = readCsv('E:/code/python/kriging_lab/kriging/data')
	print rd.getSensorData(2)
