from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
import copy

from ui import selectModules
from datasource import source


class SelectModulesDialog(QDialog, selectModules.Ui_Dialog):
    def __init__(self):
        super(SelectModulesDialog, self).__init__()
        self.setupUi(self)
        self.__selected_modules = []
        self.__selected_indexes = []

        self.btnBack.clicked.connect(self.close)
        self.comboBoxCourseYear.currentIndexChanged.connect(self.comboBoxCourseYear_currentIndexChanged)
        self.btnAdd.clicked.connect(self.btnAdd_clicked)

    # Checks if course_year_key and course_year_value is valid and tries to execute the dialog box
    @pyqtSlot()
    def run(self):
        if type(source.course_year_key) is list and type(source.course_year_value) is list:
            self.comboBoxCourseYear.clear()
            self.comboBoxCourseYear.addItems(source.course_year_value)
            self.qListSelectedModules.clear()
            self.qListModuleList.clear()
            self.btnSave.setEnabled(False)
            self.exec()
        else:
            if type(source.course_year_key) is str:
                QMessageBox.critical(self, self.windowTitle(),
                                     f'Unable to get the course year from NTU Website\n{source.course_year_key}')
            else:
                QMessageBox.critical(self, self.windowTitle(),
                                     f'Unable to get the course year from NTU Website\n{source.course_year_value}')

    # Function to run when comboBoxCourseYear index changes
    @pyqtSlot()
    def comboBoxCourseYear_currentIndexChanged(self):
        # Clear the qListModuleList
        self.qListModuleList.clear()
        # If index gives valid key and index is more than -1
        if source.course_year_key[self.comboBoxCourseYear.currentIndex()] and \
                self.comboBoxCourseYear.currentIndex() > -1:
            # Load the modules using the valid key
            source.load_modules(source.course_year_key[self.comboBoxCourseYear.currentIndex()])
            # Check if the modules loaded are in a list and are valid
            if type(source.modules) is list and source.modules:
                # Add the modules to qListModuleList ui
                self.qListModuleList.addItems(source.modules)
                # Informs the user the process is complete
                QMessageBox.information(self, self.windowTitle(),
                                        f'Finished retrieving modules from NTU Website')
            else:
                QMessageBox.critical(self, self.windowTitle(),
                                     f'Unable to get the modules from NTU Website\n{source.modules}')

    # Function to run when btnAdd is clicked
    @pyqtSlot()
    def btnAdd_clicked(self):
        # Check if user has selected an item in qListModuleList and that item is not inside qListSelectedModules
        if self.qListModuleList.currentRow() > -1 and \
                len(self.qListSelectedModules.findItems(source.modules[self.qListModuleList.currentRow()],
                                                        Qt.MatchExactly)) < 1:
            # Add the item in qListSelectedModules
            self.qListSelectedModules.addItem(source.modules[self.qListModuleList.currentRow()])
            # Create a copy of the module and index info and store it in the respective "selected" list
            self.__selected_modules.append(copy.copy(source.modules[self.qListModuleList.currentRow()]))
            self.__selected_indexes.append(copy.copy(source.indexes[self.qListModuleList.currentRow()]))
        # Clear the selection in qListModuleList
        self.qListModuleList.setCurrentRow(-1)
