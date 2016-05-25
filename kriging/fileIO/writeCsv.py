#!/usr/bin/python
#-*- coding:utf-8 -*-

__doc__ = ''' 将插值后的数据保存到csv当中
'''
import os,sys
import csv


class writeCsv:
	'''读取csv文件'''
	def __init__(self, path):
		self.fileName = path
		self.csvfile = file(path, 'w')
		self.writer = csv.writer(self.csvfile)
		self.writer.writerow(['传感器编号','x坐标(cm)','y坐标(cm)','z坐标(cm)','原始温度','插值温度','原始湿度','插值湿度'])
		
	def writeResult(self, resultData):
		self.writer.writerows(resultData)
	
	def close(self):
		self.csvfile.close()
			
if __name__ == "__main__":
	wc = writeCsv('E:/code/python/kriging_lab/kriging/data/result/test.csv')
	data = [['1','2','3','4'],['5','6','7','8']]
	wc.writeResult(data)
