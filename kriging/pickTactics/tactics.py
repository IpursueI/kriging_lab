#!/usr/bin/python
#-*- coding:utf-8 -*-

__doc__ = '''
本文件主要涉及传感器的选择策略
'''

import random

class tactics:
	def __init__(self):
		self.sensorNum = ['10728412','10728515','10728382','10728506','10728402','10728400','10728435','10728517','10728383',
		'10728534','10728432','10728401','10728391','10728437','10728525','10728399','10728518','10728442','10728527','10728390',
		'10728405','10728419','10728425','10728439','10728404','10728408','10728522','10728396','10728422','10728507','10728513',
		'10728387','10728385','10728519']
		
	def getAllSensorNum(self):
		return self.sensorNum
		
	#根据传入的传感器个数，随机挑选传感器
	def randomTactic(self, number, total = 34,):
		listSlice =  random.sample(range(0,total), number)
		listSlice.sort()
		selectedList = [self.sensorNum[i] for i in listSlice]
		unSelectedList = [item for item in self.sensorNum if item not in selectedList]
		return selectedList, unSelectedList

	#给出固定的传感器序列，列表取值范围时0-33
	def fixedTactic(self, listc):
		selectedList = [self.sensorNum[i] for i in listc]
		unSelectedList = [item for item in self.sensorNum if item not in selectedList]
		return selectedList, unSelectedList
		
if __name__ == '__main__':
	tac = tactics()
	#print tac.randomTactic()
	print tac.fixedTactic([33])
	
