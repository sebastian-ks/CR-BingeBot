from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Elements(QWidget):
    windowX = 800
    windowY = 240
    window_Height = 400
    window_Width = 500
    destination = ""    # should be in a global var module but unecessary for just one
    topBarHeight = 60
    bottomBarHeight = 40
    episodeWidgets = []

    class Clicklabel(QLabel):
        clicked = pyqtSignal()
        def __init__(self, parent):
            QLabel.__init__(self, parent)

        def mousePressEvent(self, event):
            self.clicked.emit()

    class ClickWidget(QWidget):
        clicked = pyqtSignal()
        entered = pyqtSignal()
        left = pyqtSignal()

        def __init__(self, parent):
            QWidget.__init__(self, parent)

        def mousePressEvent(self, event):
            self.clicked.emit()

        def enterEvent(self, event):
            self.entered.emit()

        def leaveEvent(self, event):
            self.left.emit()

    def point(self,posString,QWidget):
        if posString == "topRight":
            pos = QPoint(self.window_Width - QWidget.minimumSizeHint().width(),0)
        if posString == "bottomMiddle":
            pos = QPoint(self.window_Width/2 - QWidget.minimumSizeHint().width()/2,)
        if posString == "bottomLeft":
            pos = QPoint(0,self.window_Height-QWidget.minimumSizeHint().height()*2)
        return pos

    def setup(self):

        #widgets
        self.topBar = QWidget(self)
        self.topBar.setGeometry(QRect(0, 0, self.window_Width, self.topBarHeight))
        self.topBar.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(199, 021, 133, 255));\n"
"border-color: black;\n"
"border: 4px solid;")

        self.mainPlane = QWidget(self)
        self.mainPlane.setGeometry(QRect(0, self.topBarHeight, self.window_Width, self.window_Height-self.topBarHeight-self.bottomBarHeight))
        self.mainPlane.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(077,077,077,255));")

        self.bottomBar = QWidget(self)
        self.bottomBar.setGeometry(QRect(0, self.window_Height-self.bottomBarHeight, self.window_Width, self.bottomBarHeight))
        self.bottomBar.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(030,030,030,255));\n"
"border-color: black;\n"
"border: 2px solid;")

        mainPlaneThird = (self.window_Height-self.topBarHeight-self.bottomBarHeight)/3

        for i in range(3):
            self.episodeWidgets.append(self.ClickWidget(self.mainPlane))

        for wid in self.episodeWidgets:
            i = self.episodeWidgets.index(wid)
            wid.setGeometry(QRect(0,i*(mainPlaneThird+2), self.window_Width, mainPlaneThird))
            wid.setAttribute(Qt.WA_StyledBackground)
            wid.setStyleSheet("background-color: none;")



        #buttons
        self.cr = self.Clicklabel(self)
        self.crPixmap_og = QPixmap('assets\\CR_Icon.png')
        self.crPixmap = self.crPixmap_og.scaled(40,40)
        self.cr.setPixmap(self.crPixmap)
        self.cr.move(self.window_Width-120,10)
        self.cr.show()

        self.settings = self.Clicklabel(self)
        self.setPixmap_og = QPixmap('assets\\Gear.png')
        self.setPixmap = self.setPixmap_og.scaled(40,40)
        self.settings.setPixmap(self.setPixmap)
        self.settings.move(self.window_Width-60,10)
        self.settings.show()
