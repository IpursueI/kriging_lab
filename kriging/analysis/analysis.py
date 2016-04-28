#!/usr/bin/python
#coding=utf-8

__doc__ = ''' 根据插值后的数据计算误差，并将结果保存
'''
import os,sys
import csv

class analysis:
	def __init__(self, inputFile, outputFile):
		self.inputFile = inputFile
		self.outputFile = outputFile
		
		
		#读取csv中的结果数据
		csvfile = file(self.inputFile, 'rb')
		reader = csv.reader(csvfile)
		tmpData = [line for line in reader]
		self.data = tmpData[1:]
		
		#温度的绝对误差
		self.tempAbsoluteError = [float(item[5]) - float(item[4]) for item in self.data]
		
		#温度的相对误差
		self.tempRelativeError = [ self.tempAbsoluteError[idx] / float(self.data[idx][4]) for idx in range(len(self.data))]
		
		#湿度的绝对误差
		self.humAbsoluteError = [float(item[7]) - float(item[6]) for item in self.data]
		
		#湿度的相对误差
		self.humRelativeError = [ self.humAbsoluteError[idx] / float(self.data[idx][6]) for idx in range(len(self.data))]
		
	#获取温度的绝对误差
	def getTempAbsoluteError(self):
		return self.tempAbsoluteError
	
	#获取温度的相对误差
	def getTempRelativeError(self):
		return self.tempRelativeError
			
	
	#获取湿度的绝对误差
	def getHumAbsoluteError(self):
		return self.humAbsoluteError
		
	#获取湿度的相对误差
	def getHumRelativeError(self):
		return self.humRelativeError
	
	
	def writeErrorResult(self):
		csvfile = file(self.outputFile, 'w')
		writer = csv.writer(csvfile)
		writer.writerow(['传感器编号','x坐标(cm)','y坐标(cm)','z坐标(cm)','原始温度','插值温度','原始湿度','插值湿度',
		'温度绝对误差','湿度绝对误差','温度相对误差','湿度相对误差'])
		resultData = []
		
		for idx in range(len(self.data)):
			rowData = self.data[idx]
			rowData.append(self.tempAbsoluteError[idx])
			rowData.append(self.humAbsoluteError[idx])
			rowData.append(self.tempRelativeError[idx])
			rowData.append(self.humRelativeError[idx])
			
			resultData.append(rowData)
			
		writer.writerows(resultData)
		csvfile.close()
			
			
		
if __name__ == '__main__':
	an = analysis('/home/captain/文档/code/python/labWork/kriging/data/result/result.csv', 
	'/home/captain/文档/code/python/labWork/kriging/data/result/errorResult.csv')
	#print an.getTempAbsoluteError()
	#print an.getTempRelativeError()
	#print an.getHumAbsoluteError()
	#print an.getHumRelativeError()
	an.writeErrorResult()
	print "write errorResult finished"
