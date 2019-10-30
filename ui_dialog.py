import sys
import os
import shutil
from functools import partial
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from PyQt5.QObject import QIODevice
from tkinter import *
from tkinter import filedialog
from functools import partial
from driver import Driver
import subprocess
import elem
import skip
from general import Methods
import time
import mouse

class Ui_Dialog(elem.Elements):
    x = __import__('elem').Elements.windowX
    y = __import__('elem').Elements.windowY
    w = __import__('elem').Elements.window_Width
    h = __import__('elem').Elements.window_Height
    inEpisode = False


    def __init__(self):
        super().__init__()
        self.setup(self.w,self.h)
        self.setupUi()


    def setupUi(self):
        self.setGeometry(self.x,self.y,self.w,self.h)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.offset = self.pos()
        self.events()
        self.show()


    def events(self):#partial(self.goTo,"https://www.crunchyroll.com")
        self.cr.clicked.connect(partial(self.goTo,"https://www.crunchyroll.com"))
        self.quit.clicked.connect(self.close)
        for wid in self.activeEpisodes:
            i = self.activeEpisodes.index(wid)
            wid.clicked.connect(partial(self.chooseDestination,i))
            wid.entered.connect(partial(self.hover,wid,"in"))
            wid.left.connect(partial(self.hover,wid,"out"))
        for dl in self.delbtns:
            dl.clicked.connect(partial(self.remove,self.delbtns.index(dl)))
            dl.entered.connect(partial(self.hover,dl,"in"))
            dl.left.connect(partial(self.hover,dl,"out"))
        self.forward.clicked.connect(partial(self.scroll,"forward"))
        self.forward.entered.connect(partial(self.hover,self.forward,"in"))
        self.forward.left.connect(partial(self.hover,self.forward,"out"))
        self.back.clicked.connect(partial(self.scroll,"back"))
        self.back.entered.connect(partial(self.hover,self.back,"in"))
        self.back.left.connect(partial(self.hover,self.back,"out"))
        self.erase.entered.connect(partial(self.hover,self.erase,"in"))
        self.erase.left.connect(partial(self.hover,self.erase,"out"))
        self.erase.clicked.connect(self.erasefunc)
        self.settings.clicked.connect(self.openSettings)
        self.settings.entered.connect(partial(self.hover,self.settings,"in"))
        self.settings.left.connect(partial(self.hover,self.settings,"out"))
        self.mini.clicked.connect(partial(self.setWindowState,Qt.WindowMinimized))

    #def exitApp(self):
    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if not self.inEpisode:
            xx = event.globalX()
            yy = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(xx-x_w,yy-y_w)

    def skippi(self):
        self.inEpisode = True
        os.system("pythonw skip.pyw")


    def scroll(self,dir):
        if dir is "back":
            if self.page > 0:
                if self.page is 1:
                    self.hover(self.back,"out")
                self.page -= 1
                self.updateWidgets(self.mainPlane)
        else:
            file = open("progress.txt", "r")
            episodes = file.readlines()
            if len(episodes) > self.page*3+3:
                if (len(episodes) - (self.page*3+3)) < 4:
                    self.hover(self.forward,"out")
                self.page += 1
                self.updateWidgets(self.mainPlane)

    def chooseDestination(self,id):
        des = self.page*3 +id
        file = open("progress.txt", "r+")
        episodes = list(reversed(file.readlines()))
        file.close()
        self.goTo(Methods.url(episodes[des]))

    def remove(self,id):
        toremove = self.page*3+id
        file = open("progress.txt", "r+")
        episodes = list(reversed(file.readlines()))
        os.remove("assets\\mugs\\"+Methods.getMugCode(episodes[toremove]))
        del episodes[toremove]
        file.close()
        os.remove("progress.txt")
        open("progress.txt", "a+").writelines(reversed(episodes))
        self.updateWidgets(self.mainPlane)

    def erasefunc(self):
        file = open("progress.txt", "r")
        episodes = file.readlines()
        file.close()
        if len(episodes) > 0:
            self.hover(self.erase,"out")
            open("progress.txt", "w").close()
            shutil.rmtree("assets\\mugs")
            self.updateWidgets(self.mainPlane)

    def changePixmap(self,obj,mouseState,pm1,pm2):
        if mouseState is "in":
            obj.setPixmap(pm2)
        elif mouseState is "out":
            obj.setPixmap(pm1)

    def hover(self,obj,mouseState):
        file = open("progress.txt", "r")
        episodes = file.readlines()
        file.close()
        if obj is self.forward:
            if len(episodes) > self.page*3+3:
                self.changePixmap(obj,mouseState,self.fwPixmap,self.fwPixmap2)
            else:
                obj.setPixmap(self.fwPixmap)
            return
        elif obj is self.back:
            if self.page > 0:
                self.changePixmap(obj,mouseState,self.bkPixmap,self.bkPixmap2)
            else:
                obj.setPixmap(self.bkPixmap)
            return

        if obj is self.settings:
            self.changePixmap(obj,mouseState,self.setPixmap,self.setPixmap2)

        if obj in self.delbtns:
            self.changePixmap(obj,mouseState,self.rmPixmap,self.rmPixmap2)

        if obj is self.erase and len(episodes) > 0:
            if mouseState is "in":
                obj.setText("<u><font face='roboto' color='#DCDCDC' size=5>Remove All</font></u>")
            elif mouseState is "out":
                obj.setText("<font face='roboto' color='#7F7F7F' size=5>Remove All</font>")

        if isinstance(obj, self.ClickWidget):
            if mouseState is "in":
                obj.setStyleSheet("background-color: rgba(255,255,255,75);")
            elif mouseState is "out":
                obj.setStyleSheet("background-color: none;")

    def goTo(self,url):
        self.inEpisode = True;
        Driver.setupDriver(url)

    def openSettings(self):
        st = Settings()

class Settings(Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupSUi()

    def setupSUi(self):
        x = super().pos().x() + self.w/1.5
        y = super().pos().y() + self.topBarHeight*2
        w = self.w/2
        h = self.h - self.bottomBarHeight
        self.setGeometry(x,y,w,h)
        self.setupSettings(w,h)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    sys.exit(app.exec_())
