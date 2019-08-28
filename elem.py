from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Elements(QWidget):
    windowX = 800
    windowY = 240
    window_Height = 300
    window_Width = 400

    class Clicklabel(QLabel):
        clicked = pyqtSignal()
        def __init__(self, parent):
            QLabel.__init__(self, parent)

        def mousePressEvent(self, event):
            self.clicked.emit()

    def point(self,posString,QWidget):
        if posString == "topRight":
            pos = QPoint(self.window_Width - QWidget.minimumSizeHint().width(),0)
        if posString == "bottomMiddle":
            pos = QPoint(self.window_Width/2 - QWidget.minimumSizeHint().width()/2,)
        if posString == "bottomLeft":
            pos = QPoint(0,self.window_Height-QWidget.minimumSizeHint().height()*2)
        return pos

    def button(self):
        self.cr = self.Clicklabel(self)
        self.crPixmap_og = QPixmap('assets\\CR_Icon.png')
        self.crPixmap = self.crPixmap_og.scaled(40,40)
        self.cr.setPixmap(self.crPixmap)
        self.cr.move(self.point("topRight",self.cr))
        self.cr.show()
