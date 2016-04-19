#!/usr/bin/python
#coding=utf-8

__doc__ = '''
本文件主要涉及传感器的选择策略
'''

import random
import fileIO.readCsv

class tactics:
	def __init__(self):
		pass
		
	#根据传入的传感器个数，随机挑选传感器
	def randomTactic(self, total = 34, number=10):
		listSlice =  random.sample(range(0,total), number)
		listSlice.sort()
		return listSlice

	#给出固定的传感器序列
	def fixedTactic(self, listc):
		return listc
		
if __name__ == '__main__':
	tac = tactics()
	print tac.randomTactic()
	
