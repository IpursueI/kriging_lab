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
        pickRes.append(tac.fixedTactic([1,7,8,13,15,17,22,24,31,32]))
        #随机挑选
        for i in range(10):
            pickRes.append(tac.randomTactic(10))

        return pickRes

    def cal(self, valueResultFile, selectedList, unSelectedList, totalSensorDataNum):
        """对输入数据进行插值计算，并保存文件，再对文件数据分析求出温湿度方差，并返回

        Args:
            valueResultFile: 保存的文件名
            selectedList: 挑选出来的传感器点
            unSelectedList: 未被挑选的传感器点
            totalSensorDataNum: 根据不同的时间挑选出来的传感器数据组数

        Return:
            an.getTempVar(): 温度方差
            an.getHumVar(): 湿度方差
        """
        #利用kriging对所选的数据进行计算
        caler = calculate(self.inputFile, valueResultFile, selectedList, unSelectedList, totalSensorDataNum)
        tempVar,humVar =  caler.run()

        #把计算方差的功能继承到calculate模块中，避免重复读文件计算方差，所以下面三行可以去掉
        #将analysis中没有使用到的文件赋值为空字符串
        #an = analysis(valueResultFile,"","", self.totalSensorNum, self.pickSensorNum)
        #print an.getTempVar(),an.getHumVar()
        return tempVar,humVar

    def writeVar(self, variance, varianceFile):
        #采用追加的模式把每次的方差数据都保存下来
        csvfile = file(varianceFile, 'a+')  
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