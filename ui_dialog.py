import sys
import os
from functools import partial
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from PyQt5.QObject import QIODevice
from tkinter import *
from tkinter import filedialog
from functools import partial
import driver
import subprocess
from elem import Elements
from general import Methods

class Ui_Dialog(driver.Driver):
    x = __import__('elem').Elements.windowX
    y = __import__('elem').Elements.windowY
    w = __import__('elem').Elements.window_Width
    h = __import__('elem').Elements.window_Height

    def __init__(self):
        super().__init__()
        self.setupUi()


    def setupUi(self):
        self.setGeometry(self.x,self.y,self.w,self.h)
        self.setWindowTitle("Crunchyroll Binge Bot")
        self.events()
        self.show()


    def events(self):
        self.cr.clicked.connect(partial(self.goTo,"https://www.crunchyroll.com"))
        for wid in self.activeEpisodes:
            i = self.activeEpisodes.index(wid)
            wid.clicked.connect(partial(self.chooseDestination,i))
            wid.entered.connect(partial(self.hover,wid,"in"))
            wid.left.connect(partial(self.hover,wid,"out"))
        for dl in self.delbtns:
            dl.clicked.connect(partial(self.remove,self.delbtns.index(dl)))
        self.forward.clicked.connect(partial(self.scroll,"forward"))
        self.forward.entered.connect(partial(self.hover,self.forward,"in"))
        self.forward.left.connect(partial(self.hover,self.forward,"out"))
        self.back.clicked.connect(partial(self.scroll,"back"))
        self.back.entered.connect(partial(self.hover,self.back,"in"))
        self.back.left.connect(partial(self.hover,self.back,"out"))
        self.erase.entered.connect(partial(self.hover,self.erase,"in"))
        self.erase.left.connect(partial(self.hover,self.erase,"out"))
        self.erase.clicked.connect(self.erasefunc)

    def scroll(self,dir):
        if dir is "back":
            if Elements.page > 0:
                if Elements.page is 1:
                    self.hover(self.back,"out")
                Elements.page -= 1
                self.updateWidgets(self.mainPlane)
        else:
            file = open("progress.txt", "r")
            episodes = file.readlines()
            if len(episodes) > Elements.page*3+3:
                if (len(episodes) - (Elements.page*3+3)) < 4:
                    self.hover(self.forward,"out")
                Elements.page += 1
                self.updateWidgets(self.mainPlane)

    def chooseDestination(self,id):
        des = Elements.page*3 +id
        file = open("progress.txt", "r+")
        episodes = list(reversed(file.readlines()))
        file.close()
        self.goTo(Methods.url(episodes[des]))

    def remove(self,id):
        toremove = Elements.page*3+id
        file = open("progress.txt", "r+")
        episodes = list(reversed(file.readlines()))
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
            self.updateWidgets(self.mainPlane)

    def hover(self,obj,mouseState):
        file = open("progress.txt", "r")
        episodes = file.readlines()
        file.close()
        if obj is self.forward:
            if len(episodes) > Elements.page*3+3:
                if mouseState is "in":
                    obj.setPixmap(self.fwPixmap2)
                elif mouseState is "out":
                    obj.setPixmap(self.fwPixmap)
            else:
                obj.setPixmap(self.fwPixmap)
            return
        elif obj is self.back:
            if Elements.page > 0:
                if mouseState is "in":
                    obj.setPixmap(self.bkPixmap2)
                elif mouseState is "out":
                    obj.setPixmap(self.bkPixmap)
            else:
                obj.setPixmap(self.bkPixmap)
            return

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
        Elements.destination = url
        self.setupDriver()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    sys.exit(app.exec_())
