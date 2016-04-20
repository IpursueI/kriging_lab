#!/usr/bin/python
#coding=utf-8

import sys
sys.path.append("..")


import numpy
from pickTactics.tactics import tactics
from fileIO.readCsv import readCsv
from pykrige.ok3d import OrdinaryKriging3D

__doc__ = '''用于kriging的计算'''

class calculate:
	def __init__(self, path):
		
		tac = tactics()
		reader = readCsv(path)
		self.selectedList = tac.randomTactic()
		self.sensorPosData = reader.getSensorPos()
		self.allSensorNum = tac.getAllSensorNum()
		self.sensorRawData = reader.getSensorData()
		
	def createData(self, rawData, selectedList, allSensorNum):
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
		#找出未选中的传感器节点编号
		unSelectedList = [item for item in allSensorNum if item not in selectedList]
		for unSelectedItem in unSelectedList:
			calPos.append(list(self.sensorPosData[unSelectedItem]))
			
		return calData,calPos
		
		
	def doCalculateData(self, data, gridx, gridy, gridz):
		ok3d = OrdinaryKriging3D(data[:, 0], data[:, 1], data[:, 2], data[:, 3],variogram_model='spherical')
		k3d, ss3d = ok3d.execute('points', gridx, gridy, gridz)
		
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
		gridx = numpy.array(gridx)
		gridy = numpy.array(gridy)
		gridz = numpy.array(gridz)
		
		for rowIdx in range(minColLen):
			eachRow = []
			for colItem in calData:
				eachRow.append(colItem[rowIdx])
				
			data = numpy.array(eachRow)
			
			self.doCalculateData(data, gridx, gridy, gridz)
		
		
	def analysisData(self):
		pass
	
if __name__ == '__main__':
	cal = calculate('/home/captain/文档/code/python/labWork/kriging/data')
	calData, calPos = cal.createData(cal.sensorRawData, cal.selectedList, cal.allSensorNum)
	print calData
