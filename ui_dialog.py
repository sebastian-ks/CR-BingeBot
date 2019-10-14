import sys
import os
from functools import partial
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tkinter import *
from tkinter import filedialog
from functools import partial
import main
import elem

class Ui_Dialog(main.Driver):
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
        #for wid in self.episodeWidgets:
        #    wid.clicked.connect(partial(self.hover,wid))

    def hover(self,wid):
        wid.setStyleSheet("background-color: white;")

    def goTo(self,url):
        elem.destination = url
        self.setupDriver()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    sys.exit(app.exec_())
