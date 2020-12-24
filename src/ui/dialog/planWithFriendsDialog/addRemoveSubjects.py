from ui.dialog.planWithFriendsDialog import addRemoveSubjectsDialog
from ui.dialog.planWithFriendsDialog.model import friends
from datasource import datasource
from model import (course, index)

import sys
from PyQt5.QtWidgets import (QDialog, QMessageBox)
from PyQt5.QtCore import (pyqtSlot, pyqtSignal)

class Dialog(QDialog, addRemoveSubjectsDialog.Ui_AddRemoveSubject):
    newFriendSignal = pyqtSignal(friends.Friend)
    def __init__(self):
        try:
            super(Dialog, self).__init__()
            self.__subjectList = []
            self.__addedSubjectsList = []
            self.__dayDict = {
                "MON": 0,
                "TUE": 1,
                "WED": 2,
                "THU": 3,
                "FRI": 4,
                "SAT": 5,
            }  # Dictionary to translate day to index
            self.__timeDict = {
                "0800": 0,
                "0830": 1,
                "0900": 2,
                "0930": 3,
                "1000": 4,
                "1030": 5,
                "1100": 6,
                "1130": 7,
                "1200": 8,
                "1230": 9,
                "1300": 10,
                "1330": 11,
                "1400": 12,
                "1430": 13,
                "1500": 14,
                "1530": 15,
                "1600": 16,
                "1630": 17,
                "1700": 18,
                "1730": 19,
                "1800": 20,
                "1830": 21,
                "1900": 22,
                "1930": 23,
                "2000": 24,
                "2030": 25,
                "2100": 26,
                "2130": 27,
                "2200": 28,
                "2230": 29,
                "2300": 30,
            }  # Dictionary to translate time to index

            self.setupUi(self)

            # Connect the signal textEdited of nameLineEdit to the appropriate slot
            self.nameLineEdit.textEdited.connect(self.nameLineEditTextEdited)

            # Load the course years and store the information into a variable
            # Load the courseYears into the ui
            self.__courseYear = datasource.loadCourseYears()
            self.loadCourseYears()
            self.courseYearComboBox.currentTextChanged.connect(self.loadSubjectListWidget)

            # Set the signal and slot pair for subjectListWidget and addedSubjectListWidget
            self.subjectListWidget.itemPressed.connect(self.clearAddedSubjectListAndRemoveButton)
            self.addedSubjectListWidget.itemPressed.connect(self.clearSubjectListAndAddButton)

            # Set the signal slot to check to prevent user from adding duplicate course
            self.subjectListWidget.currentRowChanged.connect(self.setAddBtn)

            # Set the signal and slot for add and remove btn pair
            self.addBtn.clicked.connect(self.addBtnClicked)
            self.removeBtn.clicked.connect(self.removeBtnClicked)

            self.submitBtn.clicked.connect(self.submitBtnClicked)
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::__init__()\nError msg: {err}')

    # Called everytime when the text self.nameLineEdit is edited
    # Depending on the currentText, enable or disable the submitBtn
    @pyqtSlot(str)
    def nameLineEditTextEdited(self, currentText):
        try:
            self.submitBtn.setEnabled(False)
            if currentText and self.__addedSubjectsList:
                self.submitBtn.setEnabled(True)
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::nameLineEditTextEdited()\nError msg: {err}')

    # Load the course year into the courseYearComboBox ui
    # If the result from the datasource.loadCourseYears() is not a dict, raise an error
    def loadCourseYears(self):
        try:
            if type(self.__courseYear) is not dict:
                self.showErrorMsg(f'datasource::loadCourseYears()\n{self.__courseYear}')
                sys.exit(1)
            else:
                for courseYear in self.__courseYear.values():
                    self.courseYearComboBox.addItem(courseYear)
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriend)::loadCourseYears()\nError msg: {err}')

    # Load the list of subjects into subjectListWidget ui
    # Called everytime when user change courseYearComboBox text
    @pyqtSlot(str)
    def loadSubjectListWidget(self, currentText):
        try:
            # Clear the subjectListWidget and disable the add, remove btn everytime this function is called
            # This function is only called when user choose a different course year option
            self.subjectListWidget.clear()
            self.addBtn.setEnabled(False)
            self.removeBtn.setEnabled(False)

            # There are a 2 cases we have to consider
            # Invalid string(either blank, contains ' ', or starts with '-'), we ignore
            # Valid string, loadSubjects and add the subjects to the list widget
            if currentText and currentText != ' ' and currentText[0] != '-':
                self.__subjectList = datasource.loadSubjects(self.getCourseYearKey(currentText))
                if type(self.__subjectList) is not list:
                    # Raise an error
                    self.showErrorMsg(f'dataSource::loadSubjects()\n{self.__subjectList}')
                    sys.exit(1)
                else:
                    for subject in self.__subjectList:
                        self.subjectListWidget.addItem(f'{subject.courseCode}: {subject.courseName}')
                    self.subjectListWidget.setMinimumWidth(self.subjectListWidget.sizeHintForColumn(0))
                QMessageBox.information(self, self.getWindowName(), f'Finished loading subjects for {currentText}')
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::loadSubjectListWidget()\nError msg: {err}')

    # Returns the self.__courseYear key according to the value
    def getCourseYearKey(self, val):
        for key, value in self.__courseYear.items():
            if value == val:
                return key

    # Disable the remove button and clear focus in addedSubjectListWidget
    # Called everytime an item is pressed in subjectListWidget
    @pyqtSlot()
    def clearAddedSubjectListAndRemoveButton(self):
        # These 2 ui symbolically forms a pair
        self.removeBtn.setEnabled(False)
        self.addedSubjectListWidget.setCurrentRow(-1)

    # Disable the add button and clear focus in subjectListWidget
    # Enable the remove button
    # Called everytime an item is pressed in addedSubjectListWidget
    @pyqtSlot()
    def clearSubjectListAndAddButton(self):
        self.addBtn.setEnabled(False)
        self.subjectListWidget.setCurrentRow(-1)
        self.removeBtn.setEnabled(True)

    # Enable/disable the add button based on the item in currentRow of subjectListWidget
    # Called everytime when user changes selection in subjectListWidget ui
    @pyqtSlot(int)
    def setAddBtn(self, currentRow):
        try:
            if currentRow > -1:
                if self.__subjectList[currentRow].courseType == course.courseType.ONLINE:
                    # Disable the add button if the course is an online course
                    self.addBtn.setEnabled(False)
                elif len(self.__addedSubjectsList) == 0:
                    # Enable the add button if self.__addedSubjectsList is empty
                    self.addBtn.setEnabled(True)
                else:
                    # Check whether the subject exist in the addedSubjectListWidget
                    # If exist, disable the addBtn. If not, enable the addBtn
                    for addedSubject in self.__addedSubjectsList:
                        if self.__subjectList[currentRow].courseCode == addedSubject.courseCode:
                            self.addBtn.setEnabled(False)
                            return
                    self.addBtn.setEnabled(True)
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::setAddBtn()\nError msg: {err}')

    # Performs the necessary logic when the add button is clicked
    # Called everytime the add button is clicked
    @pyqtSlot()
    def addBtnClicked(self):
        try:
            self.addBtn.setEnabled(False)
            # add the subject to addedSubjectsList
            self.__addedSubjectsList.append(self.__subjectList[self.subjectListWidget.currentRow()])
            # update the ui by adding the name to the list
            self.addedSubjectListWidget.addItem(
                f'{self.__subjectList[self.subjectListWidget.currentRow()].courseCode}: {self.__subjectList[self.subjectListWidget.currentRow()].courseName}')
            # adjust the ui width accordingly
            self.addedSubjectListWidget.setMinimumWidth(self.addedSubjectListWidget.sizeHintForColumn(0))
            # Enable the plan button
            if self.nameLineEdit.text():
                self.submitBtn.setEnabled(True)
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::addBtnCllicked()\nError msg: {err}')

    # Remove the selected course from self.__addedSubjectsList
    # Update the list widget and remove btn accordingly
    # Called everytime the remove button is clicked
    @pyqtSlot()
    def removeBtnClicked(self):
        try:
            self.__addedSubjectsList.remove(self.__addedSubjectsList[self.addedSubjectListWidget.currentRow()])
            self.addedSubjectListWidget.takeItem(self.addedSubjectListWidget.currentRow())
            self.removeBtn.setEnabled(False)
            if (len(self.__addedSubjectsList) == 0):
                self.submitBtn.setEnabled(False)
            # I need to call this as the list will pick the next item(if have).
            # So, I call this to clear the focus after removing an item
            self.addedSubjectListWidget.setCurrentRow(-1)
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::removeBtnClicked()\nError msg: {err}')

    # Called everytime submitBtn is clicked
    # Emit newFriendSignal
    # Close this dialog
    @pyqtSlot()
    def submitBtnClicked(self):
        self.newFriendSignal.emit(friends.Friend(self.nameLineEdit.text(), self.__addedSubjectsList))
        self.done(0)

    # Reset the ui to its default state
    # Default state: empty nameLineEdit, courseYearComboBox is at index 0,
    # addedSubjectListWidget is empty, and submitBtn is disabled
    def resetUi(self):
        self.nameLineEdit.clear()
        self.courseYearComboBox.setCurrentIndex(0)
        self.addedSubjectListWidget.clear()
        self.submitBtn.setEnabled(False)

    def showErrorMsg(self, errorMsg):
        QMessageBox.critical(self, self.getWindowName(), errorMsg)

    def getWindowName(self):
        return 'Add/Remove Subjects (Plan with Friends)'