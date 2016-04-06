#!/usr/bin/python
#coding=utf-8

__doc__ = ''' 从data文件夹中的csv读取数据，一共有34个csv文件，
每个csv中的数据除了尾部部分数据有差别外，其他数据
大致一样，每次读取数据取共同部分即可。
'''
import os,sys
import csv


class readCsv:
	'''读取csv文件'''
	def __init__(self, path):
		'''path 为csv文件所在目录'''
		self.fileList = self.getFileName(path)
	def getFileName(self, path):
		fileList = os.listdir(path)
		return fileList
	def printTest(self):
		for item in self.fileList:
			print item
			
if __name__ == "__main__":
	rd = readCsv('/home/captain/文档/code/python/labWork/kriging/data');
	rd.printTest()
