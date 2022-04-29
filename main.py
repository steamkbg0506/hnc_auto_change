from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, qApp, QDialog, \
    QVBoxLayout, QPushButton, QLabel, QScrollArea
import webbrowser
import multiprocessing
import subprocess
import time
import sys

def check_hwp():
    while True:
        result = subprocess.check_output("ps -ef", shell=True)
        if "hwp".encode('utf-8') in result:
            print("hwp is running")
            q.put(True)
        else:
            print("not running")
            q.put(False)
        time.sleep(1)

def changeSettings():
    while True:
        if q.get() == True:
            subprocess.check_output("gsettings set org.freedesktop.ibus.engine.hangul use-event-forwarding false", shell=True)
        elif q.get() == False:
            subprocess.check_output("gsettings set org.freedesktop.ibus.engine.hangul use-event-forwarding true", shell=True)
        time.sleep(0.5)

def killCheck():
    checkhwp.terminate()
    changeSetting.terminate()
    checkhwp.join()
    changeSetting.join()
    qApp.quit()

class HelpWindow(QDialog):

    helpText = """
HncHangul Auto iBus Behavior Switcher 도움말
    
이 프로그램은 리눅스에서 한컴오피스 한글을 사용할 때 한글 모드에서 한글 입력이
제대로 되지 않는 문제를 해결하는 설정을 다른 프로그램과 충돌을 일으키지 않고
조정하기 위해 만들어졌습니다.
   
사용 방법:
1. 이 프로그램이 메모리에 상주해 있는 동안 \"hwp\" 바이너리가 실행되는
  것을 감지하면 자동으로 org.freedesktop.ibus.engine.hangul
  use-event-forwarding을(를) false로 변경합니다.
  
2. 이 프로그램이 메모리에 상주해 있는 동안 \"hwp\" 바이너리가 실행되지 않는다는
  것을 감지하면 자동으로 org.freedesktop.ibus.engine.hangul use-event
  -forwarding을(를) true로 변경합니다. 이는 Google Chrome등의 프로그램에서
  스페이스 삽입 오류를 방지하기 위해 일어납니다.
      
3. 이 프로그램은 시작할 때 자동으로 org.freedesktop.ibus.engine.hangul use-event
  -forwarding을(를) true로 변경합니다.
      
  자세한 내용은 개발자의 GitHub에서 알아보실 수 있습니다.
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("HncHangul Auto iBus Behavior Switcher Help")
        self.setGeometry(480, 320, 480, 320)
        self.setFixedSize(480, 320)
        layout = QVBoxLayout()
        layout.addStretch(1)
        scrollArea = QScrollArea()

        TitleLabel = QLabel('HncHangul Auto iBus Behavior Switcher 도움말', self)
        TitleLabel.setAlignment(Qt.AlignCenter)
        font1 = TitleLabel.font()
        font1.setBold(True)
        font1.setPointSize(15)
        TitleLabel.setFont(font1)

        explanationLabel = QLabel(self.helpText, self)
        explanationLabel.setAlignment(Qt.AlignCenter)
        font2 = explanationLabel.font()
        font2.setPointSize(9)
        explanationLabel.setFont(font2)

        scrollArea.setWidget(explanationLabel)

        btnLink = QPushButton("개발자 Github 확인하기")
        btnLink.clicked.connect(self.onLinkButtonClicked)

        btnOK = QPushButton("확인")
        btnOK.clicked.connect(self.onOKButtonClicked)

        layout.addWidget(TitleLabel)
        layout.addWidget(scrollArea)
        layout.addWidget(btnLink)
        layout.addWidget(btnOK)
        layout.addStretch(1)
        self.setLayout(layout)

    def onOKButtonClicked(self):
        self.accept()

    def onLinkButtonClicked(self):
        webbrowser.open("https://github.com/steamkbg0506/hnc_auto_change")

    def showModal(self):
        mw.show()
        return super().exec_()

class MainWindow(QMainWindow):
    def helpWindow(self):
        win = HelpWindow()
        win.showModal()
        mw.hide()

    def exitprog(self):
        killCheck()

    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle("HncHangul Auto iBus Behavior Switcher")
        self.setGeometry(0, 0, 0, 0)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("image.jpg"))

        quit_action = QAction("종료", self)
        help_action = QAction("도움말", self)
        quit_action.triggered.connect(self.exitprog)
        help_action.triggered.connect(self.helpWindow)
        tray_menu = QMenu()
        tray_menu.addAction(help_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()





if __name__ == "__main__":
    q = multiprocessing.Queue()
    checkhwp = multiprocessing.Process(target=check_hwp)
    changeSetting = multiprocessing.Process(target=changeSettings)
    checkhwp.start()
    changeSetting.start()
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())


