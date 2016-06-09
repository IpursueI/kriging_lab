#-*- coding:utf-8 -*-

import numpy
import csv
from pykrige.ok3d import OrdinaryKriging3D

__doc__ = """Code by 黄澎江
pengjianghuang@163.com

Dependencies:
    PyKrige
    numpy
    scipy
    matplotlib

Classes:
    kriging: 支持三维的普通克里金插值

References:
    https://github.com/bsmurphy/PyKrige
"""

class Kriging:
    """对pykrige库进行封装

    封装PyKrige中的OrdinaryKriging3D类中的功能，提供更易用的插值接口，
    可以将整个待插值空间当作一个长方体,xLen,yLen,zLen分别为长宽高

    Attributes:
        inputFile: 一个csv文件，文件内容为已知的传感器坐标和温湿度的值，
            文件有若干行，每行文件包括5列(x,y,z,temperature,humidity),
            每行代表一个传感器，x,y,z是该传感器的空间坐标，temperature，
            humidity分别表示该传感器所测量到的温湿度值

        outputFile: 一个csv文件，用于保存待插值点的插值结果，文件格式和
            inputFile一样

        xLen: 待插值空间的长度
        yLen: 待插值空间的宽度
        zLen: 待插值空间的高度
        xStep: 因为待插入的传感器点是离散分布的，这表示x轴每个待插入传感器
            之间的距离，即步长
        yStep: y轴的步长
        zStep: z轴的步长
    """
    def __init__(self, inputFile, outputFile, xLen, yLen, zLen, xStep, yStep, zStep):
        """初始化类，并读入参数，参数含义如上文注释所示
        """

        self.inputFile = inputFile
        self.outputFile = outputFile
        self.xLen = xLen
        self.yLen = yLen
        self.zLen = zLen
        self.xStep = xStep
        self.yStep = yStep
        self.zStep = zStep

    def readCsv(self):
        """从filePath中读取传感器数据

        Returns:
            numpy.array(data): 从文件中读取的传感器数据，并将其转化为numpy中array的形式
        """

        csvfile = file(self.inputFile, 'rb')
        reader = csv.reader(csvfile)
        tempData = [line for line in reader]

        data = []
        for eachRow in tempData:
            data.append([float(item) for item in eachRow])

        return numpy.array(data)

    def calculate(self, data):
        """进行插值计算，并将结果写入到输出文件当中

        Args: 
            data: 已知的传感器数据，即readCsv所返回的数据
        """
        gridx = numpy.arange(0.0, self.xLen, self.xStep)
        gridy = numpy.arange(0.0, self.yLen, self.yStep)
        gridz = numpy.arange(0.0, self.zLen, self.zStep)

        gridPos = []
        for x in gridx:
            for y in gridy:
                for z in gridz:
                    gridPos.append([x,y,z])

        gridPos = numpy.array(gridPos)

        #对温度进行插值,k3dTemp为插值结果
        ok3dTemp = OrdinaryKriging3D(data[:, 0], data[:, 1], data[:, 2], data[:, 3],variogram_model='spherical')
        k3dTemp, ss3dTemp = ok3dTemp.execute('points', gridPos[:,0], gridPos[:,1], gridPos[:,2])
        
        #对湿度进行差值,k2dHum为插值结果
        ok3dHum = OrdinaryKriging3D(data[:, 0], data[:, 1], data[:, 2], data[:, 4],variogram_model='spherical')
        k3dHum, ss3dHum = ok3dHum.execute('points', gridPos[:,0], gridPos[:,1], gridPos[:,2])

        #用finalData存储最终插值结果
        finalData = []
        for idx in range(len(gridPos)):
            rowData = []
            rowData.append(gridPos[idx][0])
            rowData.append(gridPos[idx][1])
            rowData.append(gridPos[idx][2])
            rowData.append(k3dTemp[idx])
            rowData.append(k3dHum[idx])

            finalData.append(rowData)

        #将插值结果和传感器坐标保存到文件
        csvfile = file(self.outputFile, 'w')
        writer = csv.writer(csvfile)
        writer.writerows(finalData)
        csvfile.close()
            
        print 'write result successfully !'

    def run(self):
        """调用calculate以及readCsv进行计算
        """
        self.calculate(self.readCsv())


if __name__ == "__main__":
    #Kriging类使用样例
    solution = Kriging("input.csv","output.csv",1800, 920, 550, 300, 200, 100)
    solution.run()