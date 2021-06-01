from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot

from ui import selectAcadSem

import datasource


class SelectAcadSemDialog(QDialog, selectAcadSem.Ui_Dialog):
    def __init__(self):
        super(SelectAcadSemDialog, self).__init__()
        self.setupUi(self)
        self.__acad_sem = None
        self.btnNext.clicked.connect(self.btnNextClicked)

    @pyqtSlot()
    def run(self):
        self.__acad_sem = datasource.load_course_year()
        if self.__acad_sem:
            self.comboBoxAcadSem.addItems(self.__acad_sem.values())
        self.exec()

    @pyqtSlot()
    def btnNextClicked(self):
        if self.__acad_sem:
            print(list(self.__acad_sem.keys())[self.comboBoxAcadSem.currentIndex()])
