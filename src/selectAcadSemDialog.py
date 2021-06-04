from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot

from ui import selectAcadSem
from datasource import source
from selectModulesDialog import SelectModulesDialog


class SelectAcadSemDialog(QDialog, selectAcadSem.Ui_Dialog):
    def __init__(self):
        super(SelectAcadSemDialog, self).__init__()
        self.setupUi(self)

        self.__select_module_dialog = SelectModulesDialog()

        self.btnNext.clicked.connect(self.btnNext_clicked)
        self.btnNext.clicked.connect(self.__select_module_dialog.run)

    # Checks if able to load acad sem before executing this dialog box
    @pyqtSlot()
    def run(self):
        if not source.acad_sem_dict:
            source.load_acad_sem()
        if type(source.acad_sem_dict) is dict:
            self.comboBoxAcadSem.addItems(source.acad_sem_dict.values())
            self.exec()
        else:
            QMessageBox.critical(self, self.windowTitle(),
                                 f'Unable to get academic semester from NTU Website.\n{source.acad_sem_dict}')

    # Checks if chosen_acad_sem is different and load_course_year from NTU website
    @pyqtSlot()
    def btnNext_clicked(self):
        if source.chosen_acad_sem != self.comboBoxAcadSem.currentText():
            source.chosen_acad_sem = self.comboBoxAcadSem.currentText()
            source.load_course_year(
                list(source.acad_sem_dict.keys())[self.comboBoxAcadSem.currentIndex()]
            )