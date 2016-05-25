#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
sys.path.append("..")
from pickTactics.tactics import tactics
from calculate.calculate import calculate
from analysis.analysis import analysis
from draw.drawError import drawError
from draw.drawErrorRating import drawErrorRating

class process:
    """控制整体运行流程，对其他模块进行调用。

    调用的模块涉及tactics,calculate,analysis,drawError,drawErrorRating

    Attributes:
        inputFile: 传感器原始数据文件夹路径
        valueResultFile:  经过插值后所得结果，保存的路径名
        errorResultFile:  根据插值后的结果，经过误差计算，保存的路径名
        errorRatingResultFile:  根据误差结果，进一步进行比例分析，保存的路径名
    """

    def __init__(self, inputFile, valueResultFile, errorResultFile, errorRatingResultFile):
        self.inputFile = inputFile
        self.valueResultFile = valueResultFile
        self.errorResultFile = errorResultFile
        self.errorRatingResultFile = errorRatingResultFile

    def run(self, needTacticsAndCalculate, needAnalysis, needDrawError, needDrawErrorRating, 
                pickSensorNum, totalSensorDataNum, error, valueBarIdx,totalSensorNum=34):
        """对整个模块的运行流程进行控制

        对每个流程使用一个bool值进行控制，bool值为真时，才执行该模块

        Args:
            needTacticsAndCalculate: 是否要运行tactics模块和calculate模块
            needAnalysis: 是否要运行分析模块
            needDrawError: 是否要运行drawError模块
            needDrawErrorRating: 是否要运行drawErrorRating模块
            pickSensorNum: 挑选出来用做插值基准点的个数
            totalSensorDataNum: 根据原始数据的csv， 每一时刻都能取得一组数据，这里这个值代表挑选出来的数据组数
            error: 绘制误差饼状图的时候需要提供一个误差值
            valueBarIdx: 由于有多组数据，这里有totalSensorDataNum个，数据太多如果同时绘制，不变查看，可以指定编号进行绘制展示
            totalSensorNum: 所有传感器的个数，这里一共有34个
        """

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
            an.writeErrorRatingResult(error)

        if needDrawError:
            #对计算结果进行可视化展示
            drawer = drawError(self.errorResultFile, totalSensorNum-pickSensorNum)
            drawer.drawValueBars(valueBarIdx)

        if needDrawErrorRating:
            drawer = drawErrorRating(self.errorRatingResultFile)
            drawer.drawErrorRatingPie()

if __name__ == '__main__':
    processor = process('E:/code/python/kriging_lab/kriging/data',
    'E:/code/python/kriging_lab/kriging/data/result/result.csv',
    'E:/code/python/kriging_lab/kriging/data/result/errorResult.csv',
    'E:/code/python/kriging_lab/kriging/data/result/errorRatingResult.csv')

    #processor.run(True, True, True, True, 14, 50, 0.05, 10)

    #有时当只需看绘制结果时无需重新计算
    processor.run(False, False, True, True, 14, 50, 0.05, 10)