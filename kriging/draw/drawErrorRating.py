#!/usr/bin/python
#-*- coding:utf-8 -*-

__doc__ = ''' 将插值后的数据保存到csv当中
'''
import os,sys
import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class drawErrorRating:
    '''将数据分析后的结果进行可视化展示'''
    def __init__(self, errorRatingResultFilePath, startRow = 1):

        #选择字体，否则无法显示中文，在ubuntu中字体查看可以使用命令'fc-list :lang=zh'
        #以下是unbuntu字体配置
        #zhfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc') 
        #以下是windows字体配置
        self.zhfont = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

        csvfile = file(errorRatingResultFilePath, 'rb')
        reader = csv.reader(csvfile)
        self.data = [line for line in reader]
        self.fileName = errorRatingResultFilePath
        self.startRow = startRow

    
    def drawErrorRatingPie(self):
        startIdx = self.startRow
        ratingLevel = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        tempRatingCount = [0,0,0,0,0,0,0,0,0,0]
        humRatingCount = [0,0,0,0,0,0,0,0,0,0]
        for i in range(startIdx, len(self.data)):
            for j in range(len(ratingLevel)):
                if float(self.data[i][2]) >= ratingLevel[9-j]:
                    tempRatingCount[9-j] += 1
                    break

            for j in range(len(ratingLevel)):
                if float(self.data[i][4]) >= ratingLevel[9-j]:
                    humRatingCount[9-j] += 1
                    break
        dataLen = len(self.data)-self.startRow
        tempRatingCountRating = [float(item)/dataLen for item in tempRatingCount]
        humRatingCountRating = [float(item)/dataLen for item in humRatingCount]

        #print tempRatingCount
        #print tempRatingCountRating
        #print humRatingCountRating

        
        plt.style.use('ggplot')
        plt.figure(figsize=(18,8), dpi=80)

        plt.subplot(1,2,1)
        tempFracs = [int(item*100) for item in tempRatingCountRating]

        temp = [[i, tempFracs[i]] for i in range(len(tempFracs)) if tempFracs[i] != 0]
        tempLabels = [item[0] for item in temp]
        tempFracs = [item[1] for item in temp]

        
        colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','lightgreen',
                'cyan','plum','mistyrose','lightpink','tomato']
        #explode = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
          
        plt.pie(tempFracs, labels=tempLabels, colors=colors, autopct='%1.1f%%', shadow=True)
        plt.title(u'温度插值结果分布图', fontproperties = self.zhfont)

        plt.subplot(1,2,2)
        humFracs = [int(item*100) for item in humRatingCountRating]
        hum = [[i, humFracs[i]] for i in range(len(humFracs)) if humFracs[i] != 0]
        humLabels = [item[0] for item in hum]
        humFracs = [item[1] for item in hum]
          
        #explode=(0, 0.05, 0, 0)  
        plt.pie(humFracs, labels=humLabels, colors=colors, autopct='%1.1f%%', shadow=True)
        plt.title(u'湿度插值结果分布图', fontproperties = self.zhfont)
        plt.show()
        
            
if __name__ == "__main__":
    drawer = drawErrorRating('E:/code/python/kriging_lab/kriging/data/result/errorRatingResult.csv')
    drawer.drawErrorRatingPie()
