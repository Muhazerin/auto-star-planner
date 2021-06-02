from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot

from ui import selectCourseYear
from datasource import source


class CourseYearDialog(QDialog, selectCourseYear.Ui_Dialog):
    def __init__(self):
        super(CourseYearDialog, self).__init__()
        self.setupUi(self)

        self.btnBack.clicked.connect(self.close)

    # Checks if course_year_key and course_year_value is valid and tries to execute the dialog box
    @pyqtSlot()
    def run(self):
        if type(source.course_year_key) is list and type(source.course_year_value) is list:
            self.qlistCourseYear.clear()
            self.qlistCourseYear.addItems(source.course_year_value)
            self.exec()
        else:
            if type(source.course_year_key) is str:
                QMessageBox.critical(self, self.windowTitle(),
                                     f'Unable to get the course year from NTU Website\n{source.course_year_key}')
            else:
                QMessageBox.critical(self, self.windowTitle(),
                                     f'Unable to get the course year from NTU Website\n{source.course_year_value}')
