from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from general import Methods
import general
import os

class Elements(QWidget, general.Methods):
    windowX = 800
    windowY = 240
    window_Height = 400
    window_Width = 500
    topBarHeight = 55
    bottomBarHeight = 40
    mainPlaneThird = (window_Height-topBarHeight-bottomBarHeight)/3
    activeEpisodes = []
    delbtns = []
    episodeLabels = []
    mugs = []
    page = 0

    class Clicklabel(QLabel):
        clicked = pyqtSignal()
        entered = pyqtSignal()
        left = pyqtSignal()

        def __init__(self, parent):
            QLabel.__init__(self, parent)

        def mousePressEvent(self, event):
            self.clicked.emit()

        def enterEvent(self, event):
            self.entered.emit()

        def leaveEvent(self, event):
            self.left.emit()

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


    def updateWidgets(self,parent):
        if not os.path.isfile("settings"):
            s = open("settings", "w" )
            s.write("HK:None\nShortcut:False\nSkipTimer:True")
            s.close()
        Methods.getSettings()
        if not os.path.isfile("progress.txt"):#if progress file doesn't exist create it
            file = open("progress.txt", "a+" )
        else:
            file = open("progress.txt", "r" )
        Methods.manageMugs()
        episodes = list(reversed(file.readlines()))
        showsOnPage = episodes[(self.page*3):(self.page*3+3)]
        showCount = len(showsOnPage)
        for e in range(showCount):
            if len(self.activeEpisodes) < 3:
                self.activeEpisodes.append(self.ClickWidget(parent))
                self.episodeLabels.append(QLabel(self.activeEpisodes[len(self.activeEpisodes)-1]))
                self.mugs.append(QLabel(self.activeEpisodes[len(self.activeEpisodes)-1]))
                self.delbtns.append(self.Clicklabel(self.activeEpisodes[len(self.activeEpisodes)-1]))
        for wid in self.activeEpisodes[0:showCount]:
            i = self.activeEpisodes.index(wid)
            rowsInwid = 3
            #widgets
            wid.setGeometry(QRect(0,i*(self.mainPlaneThird+2), self.window_Width, self.mainPlaneThird))
            wid.setAttribute(Qt.WA_StyledBackground)
            wid.setStyleSheet("background-color: none;")
            wid.show()
            #labels
            self.episodeLabels[i].setText("<font color='white' size=5><b>" + Methods.print_series(showsOnPage[i]) + "</b></font><br><br>"
                                            +"<font color ='#EEEDED' size=4>"+Methods.print_season(showsOnPage[i]) + "<br>"
                                            +Methods.print_episodeTitle(showsOnPage[i])+"</font>")
            self.episodeLabels[i].move(self.window_Width/3+30,self.mainPlaneThird/6-(len(self.episodeLabels[i].text().split("<br>"))-3)*5)
            self.episodeLabels[i].setStyleSheet("background-color: none;")
            self.episodeLabels[i].show()
            #mugs
            mug_og = QPixmap('assets\\mugs\\'+Methods.getMugCode(showsOnPage[i]))
            self.mugs[i].setPixmap(mug_og)
            self.mugs[i].move(5,5)
            self.mugs[i].setStyleSheet("background-color: none;")
            self.mugs[i].show()
            #Deletion
            self.delbtns[i].move(self.window_Width-30,5)
            self.delbtns[i].setPixmap(self.rmPixmap)
            self.delbtns[i].setStyleSheet("background-color: none;")
            self.delbtns[i].show()

        diff = len(self.episodeLabels) - showCount
        if diff > 0: #hide Labels when there used to be 3 eWidgets but then <3
            for s in range(diff):
                self.episodeLabels[(s+1)*-1].hide()
                self.activeEpisodes[(s+1)*-1].hide()
                self.delbtns[(s+1)*-1].hide()


    def setup(self,w,h):
        self.topBar = QWidget(self)
        self.topBar.setGeometry(QRect(0, 0, w, self.topBarHeight))
        self.topBar.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 #5c14ea);\n"
"border-color: black;\n"
"border: 3px solid;")

        self.mainPlane = QWidget(self)
        self.mainPlane.setGeometry(QRect(0, self.topBarHeight, w, h-self.topBarHeight-self.bottomBarHeight))
        self.mainPlane.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(077,077,077,255));")

        self.bottomBar = QWidget(self)
        self.bottomBar.setGeometry(QRect(0, h-self.bottomBarHeight, w, self.bottomBarHeight))
        self.bottomBar.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(030,030,030,255));\n"
"border-color: black;\n"
"border: 2px solid;")

        self.rmPixmap_og = QPixmap('assets\\Cross.png')
        self.rmPixmap = self.rmPixmap_og.scaled(20,20)
        self.rmPixmap2_og = QPixmap('assets\\Crossw.png')
        self.rmPixmap2 = self.rmPixmap2_og.scaled(20,20)
        self.updateWidgets(self.mainPlane)


        #buttons
        self.cr = self.Clicklabel(self)
        self.crPixmap_og = QPixmap('assets\\CR_Icon.png')
        self.crPixmap = self.crPixmap_og.scaled(40,40)
        self.cr.setPixmap(self.crPixmap)
        self.cr.move(self.window_Width-200,7)
        self.cr.show()

        self.settings = self.Clicklabel(self)
        self.setPixmap_og = QPixmap('assets\\Gear.png')
        self.setPixmap2_og = QPixmap('assets\\Gearw.png')
        self.setPixmap = self.setPixmap_og.scaled(40,40)
        self.setPixmap2 = self.setPixmap2_og.scaled(40,40)
        self.settings.setPixmap(self.setPixmap)
        self.settings.move(self.window_Width-145,7)
        self.settings.show()

        self.quit = self.Clicklabel(self)
        self.quitPixmap = QPixmap('assets\\close-window.png').scaled(40,40)
        self.quit.setPixmap(self.quitPixmap)
        self.quit.move(self.window_Width-40,0)
        self.quit.show()

        self.mini = self.Clicklabel(self)
        self.miniPixmap = QPixmap('assets\\Minimize.png').scaled(30,30)
        self.mini.setPixmap(self.miniPixmap)
        self.mini.move(self.window_Width-66,4)
        self.mini.show()

        self.forward = self.Clicklabel(self)
        self.fwPixmap_og = QPixmap('assets\\ArrowRightgr.png')
        self.fwPixmap_og2 = QPixmap('assets\\ArrowRight.png')
        self.fwPixmap = self.fwPixmap_og.scaled(self.bottomBarHeight-10,self.bottomBarHeight-10)
        self.fwPixmap2 = self.fwPixmap_og2.scaled(self.bottomBarHeight-10,self.bottomBarHeight-10)
        self.forward.setPixmap(self.fwPixmap)
        self.forward.move(self.window_Width-self.bottomBarHeight,self.window_Height-self.bottomBarHeight+5)
        self.forward.show()

        self.back = self.Clicklabel(self)
        self.bkPixmap_og = QPixmap('assets\\ArrowLeftgr.png')
        self.bkPixmap_og2 = QPixmap('assets\\ArrowLeft.png')
        self.bkPixmap = self.bkPixmap_og.scaled(self.bottomBarHeight-10,self.bottomBarHeight-10)
        self.bkPixmap2 = self.bkPixmap_og2.scaled(self.bottomBarHeight-10,self.bottomBarHeight-10)
        self.back.setPixmap(self.bkPixmap)
        self.back.move(self.window_Width-self.bottomBarHeight*2,self.window_Height-self.bottomBarHeight+5)
        self.back.show()

        self.erase = self.Clicklabel(self.bottomBar)
        self.erase.setText("<font face='roboto' color='#7F7F7F' size=5>Remove All</font>")
        self.erase.setStyleSheet("background-color: none;")
        self.erase.move(5,5)
        self.erase.show()

    def setupSettings(self,w,h):
        self.erase.hide()
        self.mainPlane.setGeometry(QRect(0, 0, w, h-self.bottomBarHeight))
        self.bottomBar.setGeometry(QRect(0, h-self.bottomBarHeight, w, self.bottomBarHeight))

        self.save = QPushButton(self.bottomBar)
        self.save.move(w-55,7)
        self.save.setText("Save")
        self.save.setStyleSheet("""
            background: none;
            background-color = white;
            border-color: none;
            border-width: 2px;
            color: white;
            font: bold 18px;
        """)
        self.save.show()

        self.bullLabel = QLabel(self)
        self.bullLabel.move(5,10)
        self.bullLabel.setText(
        "<font color='white'><b>Hotkeys</b><br>"+
        "______________________"+"<br><br><br><br><br><br>"+
        "<b>Episodes & Skipping</b><br>"+
        "______________________"
        )
        self.bullLabel.setStyleSheet("""
            font-size: 18px;
        """)
        self.bullLabel.show()

        self.hotkeyDesc = QLabel(self)
        self.hotkeyDesc.move(5,80)
        self.hotkeyDesc.setText(
            "<font color='white' size=5>Skip Episode: </font>"+"<br><br>"+
            "<font size=4 color='#555555'><i>*Default is mouse right click</i></font>"
        )
        self.hotkeyDesc.show()

        self.hotkey = QLabel(self)
        self.hotkey.move(110,82)
        self.hotkey.setText(Methods.getHotkey())
        self.hotkey.setStyleSheet("""
            color: #555555;
            font-size: 14px;
        """)
        self.hotkey.show()

        self.change = QPushButton(self)
        self.change.move(155,80)
        self.change.setText("Change")
        self.change.setStyleSheet("""
            color: white;
            background-color: none;
            font-size: 16px;
            border: 2px outset;
            border-color: white;
            border-radius: 10px;
        """)
        self.change.show()

        self.default = QPushButton(self)
        self.default.move(215,80)
        self.default.setText(" * ")
        self.default.setStyleSheet("""
            color: white;
            background-color: none;
            font-size: 16px;
            border: 2px outset;
            border-color: white;
        """)
        self.default.show()

        self.timerPref = QCheckBox("Skip Timer",self)
        self.timerPref.move(5,230)
        if Methods.skipTimer:
            self.timerPref.setChecked(True)
        else:
            self.timerPref.setChecked(False)
        self.timerPref.setStyleSheet("""
            color: white;
            font-size: 16px;
        """)
        self.timerPref.show()

        self.nextShow = QCheckBox("Have Shortcut to next Episode",self)
        if not Methods.stne:
            self.nextShow.setChecked(False)
        else:
            self.nextShow.setChecked(True)
        self.nextShow.move(5,270)
        self.nextShow.setStyleSheet("""
            color: white;
            font-size: 16px;
        """)
        self.nextShow.show()
