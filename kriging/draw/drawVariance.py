#!/usr/bin/python
#-*- coding:utf-8 -*-

import os,sys
import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import warnings

class drawVariance:
    """对每种选择策略的传感器温湿度方差进行绘制
    """
    def __init__(self, varFilePath, sensorNumber):

        #选择字体，否则无法显示中文，在ubuntu中字体查看可以使用命令'fc-list :lang=zh'
        #以下是unbuntu字体配置
        #zhfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc') 
        #以下是windows字体配置
        self.zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')
        warnings.filterwarnings("ignore")

        csvfile = file(varFilePath, 'rb')
        reader = csv.reader(csvfile)
        self.data = [line for line in reader]
        self.fileName = varFilePath
        self.sensorNumber = sensorNumber

    def drawVarBars(self, barIndex):
        """绘制方差柱状图
        """
        x = np.array(range(len(self.data)))
        tempVar = []
        humVar = []

        for idx in range(len(self.data)):
            tempVar.append(self.data[idx][self.sensorNumber])
            humVar.append(self.data[idx][self.sensorNumber+1])

        plt.style.use('ggplot')


        # bar graphs
        y1 = np.array(tempVar)
        y2 = np.array(humVar)
        width = 0.25
        tempVariance = plt.bar(x, y1, width)
        humVariance = plt.bar(x + width, y2, width, color=plt.rcParams['axes.color_cycle'][2])
        plt.xticks(x)
        plt.legend([tempVariance, humVariance], [u'温度方差',u'湿度方差'],prop=self.zhfont)
        plt.title(u'方差', fontproperties = self.zhfont)
        plt.xlabel(u'编号', fontproperties = self.zhfont)
        plt.ylabel(u'方差', fontproperties = self.zhfont)

        plt.show()

if __name__ == "__main__":
    drawer = drawVariance('E:/code/python/kriging_lab/kriging/data/result/variance.csv', 10)
    drawer.drawVarBars(0)
    #drawer.drawTempErrorBars(0)
    #drawer.drawHumErrorBars(0)
