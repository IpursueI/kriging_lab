#!/usr/bin/python
#-*- coding:utf-8 -*-

import csv
import sys
sys.path.append("..")
from pickTactics.tactics import tactics
from calculate.calculate import calculate
from analysis.analysis import analysis
from draw.drawError import drawError
from draw.drawErrorRating import drawErrorRating

class process:
    """控制整体运行流程，对其他模块进行调用。

    调用的模块涉及tactics,calculate,analysis

    Attributes:
        inputFile: 传感器原始数据文件夹路径
        valueResultFile:  经过插值后所得结果，保存的路径名
    """

    def __init__(self, inputFile, pickSensorNum, totalSensorNum):
        self.inputFile = inputFile
        self.pickSensorNum = pickSensorNum
        self.totalSensorNum = totalSensorNum

    def pickSensor(self):
        pickRes = []
        tac = tactics()
        #人工挑选
        pickRes.append(tac.fixedTactic([0,5,10,15,28,29,30,31,32,33]))
        #随机挑选
        for i in range(10):
            pickRes.append(tac.randomTactic(10))

        return pickRes

    def cal(self, valueResultFile, selectedList, unSelectedList, totalSensorDataNum):

        #利用kriging对所选的数据进行计算
        caler = calculate(self.inputFile, valueResultFile, selectedList, unSelectedList, totalSensorDataNum)
        caler.run()

        #将analysis中没有使用到的文件赋值为空字符串
        an = analysis(valueResultFile,"","", self.totalSensorNum, self.pickSensorNum)
        return an.getTempVar(),an.getHumVar()

    def writeVar(self, variance, varianceFile):
        csvfile = file(varianceFile, 'w')
        writer = csv.writer(csvfile)
        resultData = []

        for item in variance:
            tmp = []
            for i in range(2):
                for j in item[i]:
                    tmp.append(j)
            resultData.append(tmp)

        writer.writerows(resultData)
        csvfile.close()

    def run(self, varianceFile):
        baseFileName = 'E:/code/python/kriging_lab/kriging/data/result/result'
        variance = []
        pickRes = self.pickSensor()
        for idx in range(len(pickRes)):
            tmpFileName = baseFileName+str(idx)+'.csv'
            tmp = []
            tmp.append(pickRes[idx][0])
            tmp.append(self.cal(tmpFileName, pickRes[idx][0], pickRes[idx][1], 100))
            variance.append(tmp)

        #保存方差
        self.writeVar(variance, varianceFile)


if __name__ == '__main__':
    processor = process('E:/code/python/kriging_lab/kriging/data',10, 34)
    processor.run('E:/code/python/kriging_lab/kriging/data/result/variance.csv')