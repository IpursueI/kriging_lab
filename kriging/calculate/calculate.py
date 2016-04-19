#!/usr/bin/python
#coding=utf-8

import sys
sys.path.append("..")
import fileIO.readCsv
import pickTactics.tactics
import numpy
from pykrige.ok3d import OrdinaryKriging3D

__doc__ = '''用于kriging的计算'''

class calculate:
	def __init__(self):
		pass
	def createData(self, rawData, selectedList):
		pass
	def calculateData(self, filteredData, gridx, gridy, gridz):
		pass
	def analysisData(self):
		pass
	
if __name__ == '__main__':
	print 'ok'
