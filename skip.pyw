import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Skip(QWidget):
    x = 1920-260
    y = 980
    w = 260
    h = 50

    countdown = 5
    left = countdown

    def __init__(self):
        super().__init__()
        self.setupWindow()
        self.start_timer()

    def setupWindow(self):
        self.setGeometry(self.x,self.y,self.w,self.h)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.show()
        self.setWindowOpacity(0.7)
        self.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(077,077,077,255));
        """)
        self.timerL = QLabel(self)
        self.timerL.move(85,15)
        self.timerL.setStyleSheet("background-color: none;")
        self.timerL.show()
        self.cancel = QPushButton(self)
        self.cancel.setText("Cancel")
        self.cancel.move(5,10)
        self.cancel.setStyleSheet("""
            color: white;
            font: bold 18px;
        """)
        self.cancel.clicked.connect(self.cancelSkip)
        self.cancel.show()
        self.timer = QTimer(self)

    def timer_label(self):
        self.timerL.setText("<font face='roboto' size=5 color='white'><b>Next Episode in: "+str(self.left)+"</b></font>")
        self.timerL.adjustSize()

    def start_timer(self):
        self.left = self.countdown
        self.timer.timeout.connect(self.next)
        self.timer.start(1000)
        self.timer_label()

    def next(self):
        self.left -= 1
        self.timer_label()
        if self.left == 0:
            self.timer.stop()
            open("temp","w")
            self.setWindowFlags() #so main window doesn't freeze
            self.close()

    def cancelSkip(self):
        self.timer.stop()
        open("temp_cancel","w")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    skip = Skip()
    sys.exit(app.exec_())
