#-*- coding:utf-8 -*-

import pygame,sys,Buttons
import csv
from pygame.locals import *

class drawLayout:
    def __init__(self, posPath, variancePath, selectedSensorNum):
        self.WINDOWWIDTH = 1250
        self.WINDOWHEIGHT = 800

        self.BOXSIZE = 40

        self.AQUA = (0, 255, 255)
        self.SILVER = (192, 192, 192)
        self.GRAY = (100, 100, 100)
        self.NAVYBLUE = ( 60, 60, 100)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = ( 0, 255, 0)
        self.BLUE = ( 0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 128, 0)
        self.PURPLE = (255, 0, 255)
        self.CYAN = ( 0, 255, 255)
        self.MYC = (107, 142, 35)

        self.BGCOLOR = self.NAVYBLUE

        self.sensorImg1 = pygame.image.load('sensor.png')

        self.sensorx = 10
        self.sensory = 10

        self.sensorPos = self.readSensorPos(posPath)
        self.variance = self.readVariance(variancePath, selectedSensorNum)

        self.FPS = 30 # frames per second setting
        self.fpsClock = pygame.time.Clock()

        self.BGIMAGE = pygame.image.load('background.jpg')
        

        

    def main(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('cave sensors layout')
        

        self.layoutCount = -1


        self.screen.fill(self.BGCOLOR)
        self.initDraw()
        self.drawSensorPos(False)

        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                        self.layoutCount -= 1
                        self.drawLayout()
                    elif self.Button2.pressed(pygame.mouse.get_pos()):
                        self.layoutCount += 1
                        self.drawLayout()
                    

            #最后进行绘制
            pygame.display.update()
            self.fpsClock.tick(self.FPS)


    def readSensorPos(self,filePath):
        csvfile = file(filePath, 'rb')
        reader = csv.reader(csvfile)
        data = [line for line in reader]
        sensorPos = {}
        for item in data:
            sensorPos[item[0]] = (float(item[1])*0.6, 1000*0.6-float(item[2])*0.6, int(item[4]))
        #print sensorPos
        return sensorPos


    def readVariance(self, filePath, selectedSensorNum):
        csvfile = file(filePath, 'rb')
        reader = csv.reader(csvfile)
        data = [line for line in reader]
        res = []
        for item in data:
            res.append([item[:selectedSensorNum], item[selectedSensorNum:]])
        return res

    def initDraw(self):
        # Use smoothscale() to stretch the background image to fit the entire window:
        self.BGIMAGE = pygame.transform.smoothscale(self.BGIMAGE, (self.WINDOWWIDTH, self.WINDOWHEIGHT))
        self.screen.blit(self.BGIMAGE, self.BGIMAGE.get_rect())

        pygame.draw.line(self.screen, self.GRAY, (0, 20), (600, 20), 15)
        pygame.draw.line(self.screen, self.GRAY, (600, 20), (600, 270), 15)
        pygame.draw.line(self.screen, self.GRAY, (600, 270), (700, 270), 15)
        pygame.draw.line(self.screen, self.GRAY, (700, 270), (700, 90), 15)
        pygame.draw.line(self.screen, self.GRAY, (700, 90), (1200, 90), 15)
        pygame.draw.line(self.screen, self.GRAY, (0, 20), (0, 650), 15)
        pygame.draw.line(self.screen, self.GRAY, (0, 650), (600, 650), 15)
        pygame.draw.line(self.screen, self.GRAY, (600, 650), (600, 480), 15)
        pygame.draw.line(self.screen, self.GRAY, (600, 480), (700, 480), 15)
        pygame.draw.line(self.screen, self.GRAY, (700, 480), (700, 590), 15)
        pygame.draw.line(self.screen, self.GRAY, (700, 590), (1200, 590), 15)

        self.Button1 = Buttons.Button()
        self.Button2 = Buttons.Button()
        #Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
        self.Button1.create_button(self.screen, (107,142,35), 550, 700, 80,    40,    0,        "pre", (255,255,255))
        self.Button2.create_button(self.screen, (107,142,35), 650, 700, 80,    40,    0,        "next", (255,255,255))

        

    #根据传感器位置进行绘制
    def drawSensorPos(self, drawSensorBar):
        sensorPos = ((0,900),(0,460),(191.1,460),(461.1,460),(737.1,460),(920,0),(1010,460),(1100,290),(1450,460),(1800,740),(1800,300))
        sensorNarrowPos = [[item[0]*0.6, 1000*0.6-item[1]*0.6] for item in sensorPos]
        for item in sensorNarrowPos:
            self.screen.blit(self.sensorImg1, (item[0], item[1]))
            if drawSensorBar == True:
                pygame.draw.rect(self.screen, self.SILVER, (item[0]+60,item[1]-30, 25, 100))



    def drawLayout(self):
        #self.screen.fill(self.BGCOLOR) #重新填充背景色，整个图形重新构建，就相当于把原先添加的传感器图片删除掉了！！！！！
        self.initDraw()
        self.drawSensorPos(True)

        if self.layoutCount < 0:
            self.layoutCount = 0
        elif self.layoutCount >= len(self.variance):
            self.layoutCount = len(self.variance)-1
        var = self.variance[self.layoutCount]
        for item in var[0]:
            #print item, self.sensorPos[item][2]
            if self.sensorPos[item][2] == 1:
                pygame.draw.rect(self.screen, self.ORANGE, (self.sensorPos[item][0]+60,self.sensorPos[item][1]+45, 25, 25))
            elif self.sensorPos[item][2] == 2:
                pygame.draw.rect(self.screen, self.BLUE, (self.sensorPos[item][0]+60,self.sensorPos[item][1]+20, 25, 25))
            elif self.sensorPos[item][2] == 3:
                pygame.draw.rect(self.screen, self.PURPLE, (self.sensorPos[item][0]+60,self.sensorPos[item][1]-5, 25, 25))
            elif self.sensorPos[item][2] == 4:
                pygame.draw.rect(self.screen, self.CYAN, (self.sensorPos[item][0]+60,self.sensorPos[item][1]-30, 25, 25))

        fontObj1 = pygame.font.Font('freesansbold.ttf', 25)
        fontObj2 = pygame.font.Font('freesansbold.ttf', 30)

        textSurfaceObj = fontObj1.render("temp var: %.2f"%(float(var[1][0])), True, self.WHITE)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (330, 150)
        self.screen.blit(textSurfaceObj, textRectObj)

        textSurfaceObj3 = fontObj1.render("hum var: %.2f"%(float(var[1][1])), True, self.WHITE)
        textRectObj3 = textSurfaceObj3.get_rect()
        textRectObj3.center = (330, 200)
        self.screen.blit(textSurfaceObj3, textRectObj3)



        textSurfaceObj2 = fontObj2.render("%d/%d" % (self.layoutCount+1, len(self.variance)), True, self.AQUA)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (330, 100)
        self.screen.blit(textSurfaceObj2, textRectObj2)

if __name__ == '__main__':
    drawer = drawLayout('E:/code/python/kriging_lab/kriging/data/pos/pos.csv',
        'E:/code/python/kriging_lab/kriging/data/result/variance.csv', 10)
    drawer.main()