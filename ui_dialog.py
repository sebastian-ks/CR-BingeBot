import sys
import os
from functools import partial
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tkinter import *
from tkinter import filedialog
from functools import partial
import driver
from elem import Elements

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
            wid.entered.connect(partial(self.hover,wid,"in"))
            wid.left.connect(partial(self.hover,wid,"out"))
        for dl in self.delbtns:
            dl.clicked.connect(partial(self.remove,self.delbtns.index(dl)))
        self.forward.clicked.connect(partial(self.scroll,"forward"))
        self.back.clicked.connect(partial(self.scroll,"back"))


    def scroll(self,dir):
        if dir is "back":
            if Elements.page > 0:
                Elements.page -= 1
                self.updateWidgets(self.mainPlane)
        else:
            file = open("progress.txt", "r")
            episodes = file.readlines()
            if len(episodes) > Elements.page*3+3:
                Elements.page += 1
                self.updateWidgets(self.mainPlane)


    def remove(self,id):
        toremove = Elements.page*3+id
        file = open("progress.txt", "r+")
        episodes = file.readlines()
        del episodes[toremove]
        file.close()
        os.remove("progress.txt")
        open("progress.txt", "a+").writelines(episodes)
        self.updateWidgets(self.mainPlane)

    def hover(self,obj,mouseState):
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
