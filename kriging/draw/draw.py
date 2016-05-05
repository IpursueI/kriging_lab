#!/usr/bin/python
#coding=utf-8

__doc__ = ''' 将插值后的数据保存到csv当中
'''
import os,sys
import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

class draw:
	'''将数据分析后的结果进行可视化展示'''
	def __init__(self, path, eachNum, startRow = 1):
		csvfile = file(path, 'rb')
		reader = csv.reader(csvfile)
		self.data = [line for line in reader]
		self.fileName = path
		self.eachNum = eachNum
		self.startRow = startRow
		self.totalPic = (len(self.data)-startRow) / eachNum
	
	def drawBars(self, barIndex):
		#选择字体，否则无法显示中文，在ubuntu中字体查看可以使用命令'fc-list :lang=zh'
		zhfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc') 
		startIdx = self.startRow
		for count in range(self.totalPic):
			startIdx = startIdx + count*self.eachNum
			x = range(self.eachNum)
			tempAbsError = []
			tempReError = []
			humAbsError = []
			humReError = []
			for idx in range(startIdx, startIdx+self.eachNum):
				tempAbsError.append(self.data[idx][8])
				humAbsError.append(self.data[idx][9])
				tempReError.append(self.data[idx][10])
				humReError.append(self.data[idx][11])
				
			print tempAbsError
			plt.subplot(2,2,1)
			plt.bar(x, tempAbsError, color = 'g')
			plt.title(u'温度绝对误差', fontproperties = zhfont)
			
			plt.subplot(2,2,2)
			plt.bar(x, tempReError, color = 'g')
			plt.title(u'温度相对误差', fontproperties = zhfont)
			
			plt.subplot(2,2,3)
			plt.bar(x, humAbsError, color = 'g')
			plt.title(u'湿度绝对误差', fontproperties = zhfont)
			
			plt.subplot(2,2,4)
			plt.bar(x, humReError, color = 'g')
			plt.title(u'湿度相对误差', fontproperties = zhfont)
			
			plt.show()
		
		
			
if __name__ == "__main__":
	drawer = draw('/home/captain/文档/code/python/labWork/kriging/data/result/errorResult.csv', 24)
	drawer.drawBars(0)
