#!/usr/bin/python
#-*- coding:utf-8 -*-

import os,sys
import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import warnings

class drawValue:
    '''将数据分析后的结果进行可视化展示'''
    def __init__(self, errorResultFilePath, eachNum, startRow = 1):

        #选择字体，否则无法显示中文，在ubuntu中字体查看可以使用命令'fc-list :lang=zh'
        #以下是unbuntu字体配置
        #zhfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc') 
        #以下是windows字体配置
        self.zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')
        warnings.filterwarnings("ignore")

        csvfile = file(errorResultFilePath, 'rb')
        reader = csv.reader(csvfile)
        self.data = [line for line in reader]
        self.fileName = errorResultFilePath
        self.eachNum = eachNum
        self.startRow = startRow
        self.totalPic = (len(self.data)-startRow) / eachNum

    def drawValueBars(self, barIndex):

        startIdx = self.startRow
        startIdx = startIdx + barIndex*self.eachNum
        x = np.array(range(self.eachNum))
        sensorNumber = []
        tempRawValue = []
        tempKrigingValue = []
        humRawValue = []
        humKrigingValue = []

        for idx in range(startIdx, startIdx+self.eachNum):
            sensorNumber.append(self.data[idx][0])
            tempRawValue.append(self.data[idx][4])
            tempKrigingValue.append(self.data[idx][5])
            humRawValue.append(self.data[idx][6])
            humKrigingValue.append(self.data[idx][7])

        plt.style.use('ggplot')
        fig, axes = plt.subplots(ncols=1, nrows=2, sharex=True)
        ax1, ax2 = axes.ravel()

        # bar graphs
        y1 = np.array(tempRawValue)
        y2 = np.array(tempKrigingValue)
        width = 0.25
        tempRaw = ax1.bar(x, y1, width)
        tempKriging = ax1.bar(x + width, y2, width, color=plt.rcParams['axes.color_cycle'][2])
        ax1.set_xticks(x + width)
        ax1.set_xticklabels(sensorNumber, rotation = 45)
        ax1.legend([tempRaw, tempKriging], [u'传感器原始温度',u'传感器插值温度'],prop=self.zhfont)
        ax1.set_title(u'温度', fontproperties = self.zhfont)
        ax1.set_xlabel(u'传感器编号', fontproperties = self.zhfont)
        ax1.set_ylabel(u'温度值', fontproperties = self.zhfont)

        
        y3 = np.array(humRawValue)
        y4 = np.array(humKrigingValue)
        width = 0.25
        humRaw = ax2.bar(x, y3, width)
        humKriging = ax2.bar(x + width, y4, width, color=plt.rcParams['axes.color_cycle'][2])
        ax2.set_xticks(x + width)
        ax2.set_xticklabels(sensorNumber, rotation = 45)
        ax2.legend([humRaw, humKriging], [u'传感器原始湿度',u'传感器插值湿度'],prop=self.zhfont)
        ax2.set_title(u'湿度', fontproperties = self.zhfont)
        ax2.set_xlabel(u'传感器编号', fontproperties = self.zhfont)
        ax2.set_ylabel(u'湿度值', fontproperties = self.zhfont)

        plt.show()

            
if __name__ == "__main__":
    drawer = drawValue('E:/code/python/kriging_lab/kriging/data/result/result0.csv',34-10)
    drawer.drawValueBars(30)