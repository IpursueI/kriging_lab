#!/usr/bin/python
#coding=utf-8

__doc__ = ''' 根据插值后的数据计算误差
'''
import os,sys
import csv

class analysis:
	def __init__(self, inputFile):
		self.inputFile = inputFile
		
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
		
if __name__ == '__main__':
	an = analysis('/home/captain/文档/code/python/labWork/kriging/data/result/result.csv')
	print an.getTempAbsoluteError()
	print an.getTempRelativeError()
	print an.getHumAbsoluteError()
	print an.getHumRelativeError()
