from bs4 import BeautifulSoup

import sys, os
from ui.mainwindow import window

from PyQt5.QtCore import (pyqtSignal, pyqtSlot)
from PyQt5.QtGui import (QFont, QTextCharFormat)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QMessageBox, QLabel)

class Window(QMainWindow, window.Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.courseList = []
        self.lastPlanSpinBoxValue = None
        self.currentPlanSpinBoxValue = None

        self.setupUi(self)
        self.overviewLbl.hide()
        self.planSpinBox.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())