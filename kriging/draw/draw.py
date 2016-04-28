#!/usr/bin/python
#coding=utf-8

__doc__ = ''' 将插值后的数据保存到csv当中
'''
import os,sys
import csv
import numpy as np
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
		
	
	def drawBars():
		for i in range(self.totalPic):
			pass
		
	def __del__(self):
		self.csvfile.close()
			
if __name__ == "__main__":
	drawer = draw('/home/captain/文档/code/python/labWork/kriging/data/result/errorResult.csv', 24)
