#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
sys.path.append("..")
import numpy
import csv
from pickTactics.tactics import tactics
from fileIO.readCsv import readCsv
from fileIO.writeCsv import writeCsv
from pykrige.ok3d import OrdinaryKriging3D

__doc__ = '''用于kriging的计算'''

class calculate:
	"""进行kriging插值

	从原始传感器数据中挑选出一定量的数据进行插值,同时返回方差

	Attributes:
		selectedList: 挑选出来的传感器插值基准点的列表
		unSelectedList: 未挑选出来的传感器插值基准点的列表
		sensorPosData: 传感器位置数据
		sensorRawData: 传感器原始数据

	"""
	def __init__(self, inputPath, outputFile, selectedList, unSelectedList, totalSensorDataNum):
		
		reader = readCsv(inputPath)
		self.writer = writeCsv(outputFile)
		self.selectedList = selectedList
		self.unSelectedList = unSelectedList
		self.sensorPosData = reader.getSensorPos()
		self.sensorRawData = reader.getSensorData(totalSensorDataNum)
		
	def createData(self):
		"""根据selectedList和sensorRawData和sensorPosData,整合出最终的代插值数据

		Returns:
			calData: 挑选出来的被插值的温度值和湿度值，这里该值是一个三维列表
			calPos: 未挑选出来的被插值的传感器的坐标值
		"""
		calData = []
		for selectedItem in self.selectedList:
			colData = []
			for valData in self.sensorRawData[selectedItem]:
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
		"""对每一组传感器数据调用doCalculateData进行插值

		Args: 
			calData: 由createData所得到的传感器温湿度数据
			calPos: 由createData所得到的传感器位置数据

		"""
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
		
		tempVar = 0
		humVar = 0
		for rowIdx in range(minColLen):
			eachRow = []
			for colItem in calData:
				eachRow.append(colItem[rowIdx])
			
			#将字符串类型转化为float
			eachRowFloat = []
			for row in eachRow:
				eachRowFloat.append([float(element) for element in row])
			#print eachRow
			#print eachRowFloat
			data = numpy.array(eachRowFloat)
			#print data
			ttemp,thum = self.doCalculateData(data, gridx, gridy, gridz, rowIdx)

			tempVar += ttemp
			humVar += thum

		return tempVar/minColLen,humVar/minColLen
			
	def doCalculateData(self, data, gridx, gridy, gridz, rowIdx):
		"""调用库进行kriging插值

		Args:
			data: 供插值的传感器基准点数据
			gridx: 待插值的传感器x坐标
			gridy: 待插值的传感器y坐标
			gridz: 待插值的传感器z坐标
			rowIdx:
		"""
		#对温度进行插值
		ok3dTemp = OrdinaryKriging3D(data[:, 0], data[:, 1], data[:, 2], data[:, 3],variogram_model='spherical')
		#print data[:,1]
		#print gridx
		k3dTemp, ss3dTemp = ok3dTemp.execute('points', gridx, gridy, gridz)
		
		#对湿度进行差值
		ok3dHum = OrdinaryKriging3D(data[:, 0], data[:, 1], data[:, 2], data[:, 4],variogram_model='spherical')
		k3dHum, ss3dHum = ok3dHum.execute('points', gridx, gridy, gridz)
		
		#最后保存的数据，包括传感器编号，对应的x，y，z坐标，原始值，差值测量值
		finalData = []
		tempVar = 0
		humVar = 0
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
			
			originalTemp = float(self.sensorRawData[self.unSelectedList[idx]][rowIdx][0])
			originalHum = float(self.sensorRawData[self.unSelectedList[idx]][rowIdx][1])
			tempVar += (originalTemp-k3dTemp[idx])*(originalTemp-k3dTemp[idx])
			humVar += (originalHum-k3dHum[idx])*(originalHum-k3dHum[idx])
			finalData.append(rowData)
		

		self.writer.writeResult(finalData)

		return tempVar/len(self.unSelectedList),humVar/len(self.unSelectedList)

	def run(self):
		"""控制上面的函数运行，进行整体的运算

		Returns:
			tempVar: 温度方差
			humVar: 湿度方差
		"""
		calData, calPos = self.createData()
		tempVar,humVar = self.calculateData(calData, calPos)
		self.writer.close()
		print 'Calculate successfully !'
		return tempVar,humVar
	
if __name__ == '__main__':
	
	tac = tactics()
	selectedList, unSelectedList = tac.randomTactic(10)
	cal = calculate('E:/code/python/kriging_lab/kriging/data',
	'E:/code/python/kriging_lab/kriging/data/result/result.csv',
	selectedList, unSelectedList,10)
	print cal.run()
