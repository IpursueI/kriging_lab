#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
sys.path.append("..")
import numpy
from pickTactics.tactics import tactics
from fileIO.readCsv import readCsv
from fileIO.writeCsv import writeCsv
from pykrige.ok3d import OrdinaryKriging3D

__doc__ = '''用于kriging的计算'''

class calculate:
	def __init__(self, inputPath, outputFile, selectedList, unSelectedList, totalSensorDataNum):
		
		reader = readCsv(inputPath)
		self.writer = writeCsv(outputFile)
		self.selectedList = selectedList
		self.unSelectedList = unSelectedList
		self.sensorPosData = reader.getSensorPos()
		self.sensorRawData = reader.getSensorData(totalSensorDataNum)
		
	def createData(self, rawData, selectedList):
		#对原始数据根据selectedList进行拆分，并对坐标进行整合
		calData = []
		for selectedItem in selectedList:
			colData = []
			for valData in rawData[selectedItem]:
				#将坐标和温湿度进行拼接
				rowData = list(self.sensorPosData[selectedItem]) + list(valData)
				colData.append(rowData)				
			calData.append(colData)
		
		calPos = []
		#找出未选中的传感器坐标
		for unSelectedItem in self.unSelectedList:
			calPos.append(list(self.sensorPosData[unSelectedItem]))
			
		return calData,calPos
		
	def calculateData(self, calData, calPos):
		colLen = [len(item) for item in calData]
		minColLen = min(colLen)
		
		#分别求出x，y，z的列表
		gridx = []
		gridy = []
		gridz = []
		for idx in range(3):
			for item in calPos:
				if idx == 0:
					gridx.append(item[idx])
				elif idx == 1:
					gridy.append(item[idx])
				elif idx == 2:
					gridz.append(item[idx])
		
		gridx = numpy.array([float(i) for i in gridx])
		gridy = numpy.array([float(i) for i in gridy])
		gridz = numpy.array([float(i) for i in gridz])
		
		for rowIdx in range(minColLen):
			eachRow = []
			for colItem in calData:
				eachRow.append(colItem[rowIdx])
			
			#将字符串类型转化为float
			eachRowFloat = []
			for row in eachRow:
				eachRowFloat.append([float(element) for element in row])
			
			#print eachRowFloat
			data = numpy.array(eachRowFloat)
			
			self.doCalculateData(data, gridx, gridy, gridz, rowIdx)
			
	def doCalculateData(self, data, gridx, gridy, gridz, rowIdx):
		#对温度进行插值
		ok3dTemp = OrdinaryKriging3D(data[:, 0], data[:, 1], data[:, 2], data[:, 3],variogram_model='spherical')
		k3dTemp, ss3dTemp = ok3dTemp.execute('points', gridx, gridy, gridz)
		
		#对湿度进行差值
		ok3dHum = OrdinaryKriging3D(data[:, 0], data[:, 1], data[:, 2], data[:, 4],variogram_model='spherical')
		k3dHum, ss3dHum = ok3dHum.execute('points', gridx, gridy, gridz)
		
		#最后保存的数据，包括传感器编号，对应的x，y，z坐标，原始值，差值测量值
		finalData = []
		for idx in range(len(self.unSelectedList)):
			rowData = []
			rowData.append(self.unSelectedList[idx])
			rowData.append(self.sensorPosData[self.unSelectedList[idx]][0])
			rowData.append(self.sensorPosData[self.unSelectedList[idx]][1])
			rowData.append(self.sensorPosData[self.unSelectedList[idx]][2])
			rowData.append(self.sensorRawData[self.unSelectedList[idx]][rowIdx][0])  #温度
			rowData.append(str(k3dTemp[idx]))
			rowData.append(self.sensorRawData[self.unSelectedList[idx]][rowIdx][1])  #湿度
			rowData.append(str(k3dHum[idx]))
			
			finalData.append(rowData)
		
		self.writer.writeResult(finalData)
		
	def run(self):
		calData, calPos = self.createData(self.sensorRawData, self.selectedList)
		self.calculateData(calData, calPos)
		self.writer.close()
		print 'Calculate successfully !'
	
if __name__ == '__main__':
	
	tac = tactics()
	selectedList, unSelectedList = tac.randomTactic(10)
	cal = calculate('E:/code/python/kriging_lab/kriging/data',
	'E:/code/python/kriging_lab/kriging/data/result/result.csv',
	selectedList, unSelectedList,10)
	cal.run()
