#!/usr/bin/python
#-*- coding:utf-8 -*-

__doc__ = ''' 将插值后的数据保存到csv当中
'''
import os,sys
import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import warnings

class drawError:
	'''将数据分析后的结果进行可视化展示'''
	def __init__(self, errorResultFilePath, eachNum, startRow = 1):

		#选择字体，否则无法显示中文，在ubuntu中字体查看可以使用命令'fc-list :lang=zh'
		#以下是unbuntu字体配置
		#zhfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc') 
		#以下是windows字体配置
		self.zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')
		warnings.filterwarnings("ignore")

		csvfile = file(errorResultFilePath, 'rb')
		reader = csv.reader(csvfile)
		self.data = [line for line in reader]
		self.fileName = errorResultFilePath
		self.eachNum = eachNum
		self.startRow = startRow
		self.totalPic = (len(self.data)-startRow) / eachNum

	
	def drawTempErrorBars(self, barIndex):
		#一共有很多组数据，用barIndex来指定绘制第几个

		startIdx = self.startRow
		startIdx = startIdx + barIndex*self.eachNum
		x = range(self.eachNum)
		tempAbsError = []
		tempReError = []
		humAbsError = []
		humReError = []
		sensorNumber = []
		for idx in range(startIdx, startIdx+self.eachNum):
			sensorNumber.append(self.data[idx][0])
			tempAbsError.append(self.data[idx][8])
			humAbsError.append(self.data[idx][9])
			tempReError.append(self.data[idx][10])
			humReError.append(self.data[idx][11])
			
		#print tempAbsError
		#调整图片大小
		plt.style.use('ggplot')
		plt.figure(figsize=(18,8), dpi=80)

		plt.subplot(1,2,1)
		plt.bar(x, tempAbsError)
		plt.title(u'温度绝对误差', fontproperties = self.zhfont)
		plt.xticks(np.arange(self.eachNum), sensorNumber, rotation=45)
		plt.xlabel(u'传感器编号', fontproperties = self.zhfont)
		plt.ylabel(u'温度绝对误差值', fontproperties = self.zhfont)

		plt.subplot(1,2,2)
		plt.bar(x, tempReError)
		plt.title(u'温度相对误差', fontproperties = self.zhfont)
		plt.xticks(np.arange(self.eachNum), sensorNumber, rotation=45)
		plt.xlabel(u'传感器编号', fontproperties = self.zhfont)
		plt.ylabel(u'温度相对误差值', fontproperties = self.zhfont)

		plt.show()

	def drawHumErrorBars(self, barIndex):
		startIdx = self.startRow
		startIdx = startIdx + barIndex*self.eachNum
		x = range(self.eachNum)
		humAbsError = []
		humReError = []
		sensorNumber = []
		for idx in range(startIdx, startIdx+self.eachNum):
			sensorNumber.append(self.data[idx][0])
			humAbsError.append(self.data[idx][9])
			humReError.append(self.data[idx][11])
			

		plt.style.use('ggplot')
		plt.figure(figsize=(18,8), dpi=80)

		plt.subplot(1,2,1)
		plt.bar(x, humAbsError)
		plt.title(u'湿度绝对误差', fontproperties = self.zhfont)
		plt.xticks(np.arange(self.eachNum), sensorNumber, rotation=45)
		plt.xlabel(u'传感器编号', fontproperties = self.zhfont)
		plt.ylabel(u'湿度绝对误差值', fontproperties = self.zhfont)
		
		plt.subplot(1,2,2)
		plt.bar(x, humReError)
		plt.title(u'湿度相对误差', fontproperties = self.zhfont)
		plt.xticks(np.arange(self.eachNum), sensorNumber, rotation=45)
		plt.xlabel(u'传感器编号', fontproperties = self.zhfont)
		plt.ylabel(u'湿度相对误差值', fontproperties = self.zhfont)
		
		plt.show()

			
if __name__ == "__main__":
	drawer = drawError('E:/code/python/kriging_lab/kriging/data/result/errorResult.csv',24)
	#drawer.drawTempErrorBars(0)
	#drawer.drawHumErrorBars(0)
