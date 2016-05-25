#!/usr/bin/python
#-*- coding:utf-8 -*-

__doc__ = ''' 根据插值后的数据计算误差，并将结果保存
'''
import os,sys
import csv

class analysis:
	def __init__(self, inputFile, outputFile, ratingOutputFile, totalSensorNum, selectedSensorNum):
		self.inputFile = inputFile
		self.outputFile = outputFile
		self.ratingOutputFile = ratingOutputFile
		self.totalSensorNum = totalSensorNum
		self.selectedSensorNum = selectedSensorNum

		
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

	#获得温度方差
	def getTempVar(self):
		res = 0
		for item in self.tempAbsoluteError:
			res += item*item
		return res/len(self.tempAbsoluteError)


	#获得湿度方差
	def getHumVar(self):
		res = 0
		for item in self.humAbsoluteError:
			res += item*item
		return res/len(self.humAbsoluteError)
	
	#对每个传感器都计算绝对误差和相对误差，并记录到文件
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
			
		print 'write errorResultFile successfully !'

	#对每组数据，数据元素个数为(34-x)，参数errorList是一个误差列表
	def writeErrorRatingResult(self, error):
		restSensorNum = self.totalSensorNum - self.selectedSensorNum
		counts = len(self.tempRelativeError) / restSensorNum
		results = []

		for i in range(counts):
			tempCount = 0
			humCount = 0
			for j in range(restSensorNum):
				if(self.tempRelativeError[i*restSensorNum+j] <= error):
					tempCount += 1
				if(self.humRelativeError[i*restSensorNum+j] <= error):
					humCount += 1
			results.append([restSensorNum, tempCount, float(tempCount)/restSensorNum, humCount, float(humCount)/restSensorNum])


		csvfile = file(self.ratingOutputFile, 'w')
		writer = csv.writer(csvfile)
		writer.writerow(['总插传感器个数','满足温度误差的传感器个数', '满足温度误差的传感器所占百分比',
			'满足湿度误差的传感器个数', '满足湿度误差的传感器所占百分比'])

		writer.writerows(results)
		csvfile.close()

		print 'write errorRatingResultFile successfully !'
		
if __name__ == '__main__':
	an = analysis('E:/code/python/kriging_lab/kriging/data/result/result.csv', 
	'E:/code/python/kriging_lab/kriging/data/result/errorResult.csv',
	'E:/code/python/kriging_lab/kriging/data/result/errorRatingResult.csv', 34, 10)
	#print an.getTempAbsoluteError()
	#print an.getTempRelativeError()
	#print an.getHumAbsoluteError()
	#print an.getHumRelativeError()
	#an.writeErrorResult()
	#an.writeErrorRatingResult(0.05)
	print an.getTempVar()
	print an.getHumVar()
