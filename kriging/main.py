#!/usr/bin/python
#-*- coding:utf-8 -*-

from pickTactics.tactics import tactics
from calculate.calculate import calculate
from analysis.analysis import analysis
from draw.drawError import drawError
from draw.drawErrorRating import drawErrorRating

class process:
    def __init__(self, inputFile, valueResultFile, errorResultFile, errorRatingResultFile):
        self.inputFile = inputFile
        self.valueResultFile = valueResultFile
        self.errorResultFile = errorResultFile
        self.errorRatingResultFile = errorRatingResultFile

    def run(self, needTacticsAndCalculate, needAnalysis, needDrawError, needDrawErrorRating):

        #所有传感器个数，以及所需挑选的传感器个数
        totalSensorNum = 34
        pickSensorNum = 10
        #每个传感器有很多数据，挑选取其中多少个数据，可以将其值设为很大的值，默认会设置为文件中数据个数的最大值
        totalSensorDataNum = 50

        if needTacticsAndCalculate:
            #对传感器的挑选策略进行选择
            
            tac = tactics()
            selectedList, unSelectedList = tac.randomTactic(pickSensorNum)

            #利用kriging对所选的数据进行计算
            caler = calculate(self.inputFile, self.valueResultFile, selectedList, unSelectedList, totalSensorDataNum)
            caler.run()

        if needAnalysis:
            #对计算结果进行误差分析，并保存
            an = analysis(self.valueResultFile, self.errorResultFile, self.errorRatingResultFile, totalSensorNum, pickSensorNum)
            an.writeErrorResult()
            an.writeErrorRatingResult(0.05)

        if needDrawError:
            #对计算结果进行可视化展示
            drawer = drawError(self.errorResultFile, totalSensorNum-pickSensorNum)
            drawer.drawValueBars(10)

        if needDrawErrorRating:
            drawer = drawErrorRating(self.errorRatingResultFile)
            drawer.drawErrorRatingPie()

if __name__ == '__main__':
    processor = process('E:/code/python/kriging_lab/kriging/data',
    'E:/code/python/kriging_lab/kriging/data/result/result.csv',
    'E:/code/python/kriging_lab/kriging/data/result/errorResult.csv',
    'E:/code/python/kriging_lab/kriging/data/result/errorRatingResult.csv')

    #processor.run(True, True, True, True)

    #有时当只需看绘制结果时无需重新计算
    processor.run(False, False, True, False)