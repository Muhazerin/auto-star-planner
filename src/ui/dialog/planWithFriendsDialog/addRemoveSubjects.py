from ui.dialog.planWithFriendsDialog import addRemoveSubjectsDialog
from ui.dialog.planWithFriendsDialog.model import friends
from datasource import datasource
from model import (course, index, potentialPlan)

import sys
from PyQt5.QtWidgets import (QDialog, QMessageBox)
from PyQt5.QtCore import (pyqtSlot, pyqtSignal)

class Dialog(QDialog, addRemoveSubjectsDialog.Ui_AddRemoveSubject):
    newFriendSignal = pyqtSignal(friends.Friend, potentialPlan.PotentialPlan)
    def __init__(self):
        try:
            super(Dialog, self).__init__()
            self.__subjectList = []

            self.__addedSubjectsList = []
            self.__potentialPlan = []

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

            self.__dayTime = []  # Used to temporarily mark dayTime for planning
            self.__dayTimeEvenOdd = []  # Used to temporarily mark dayTime for lab planning
            for i in range(0, 31):
                self.__dayTime.append([0] * 6)
                self.__dayTimeEvenOdd.append(
                    ["NIL"] * 6)  # NIL, A = All week, E = Even week, O = Odd Week, EO = Even and Odd Week

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
        try:
            tempPotentialPlan = potentialPlan.PotentialPlan()
            self.__potentialPlan.clear()
            self.createIndexGraph()

            self.dfsMain()

            # Check the potentialPlan
            if len(self.__potentialPlan) > 0:
                tempPotentialPlan.subjectList = self.__addedSubjectsList
                tempPotentialPlan.potentialPlan = self.__potentialPlan

                self.newFriendSignal.emit(friends.Friend(self.nameLineEdit.text(), self.__addedSubjectsList), tempPotentialPlan)
                self.done(0)
            else:
                self.show('Unable to plan your friend\'s semester with these setup')
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::submitBtnClicked()\nError msg: {err}')

    # Create an index graph
    # All the index of 1 course points to all indexes of another course
    def createIndexGraph(self):
        try:
            for i in range(len(self.__addedSubjectsList) - 1):
                for currSubjIndex in self.__addedSubjectsList[i].indexList:
                    currSubjIndex.next = self.__addedSubjectsList[i+1].indexList
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::createIndexGraph()\nError msg: {err}')

    # The algorithm to find the potential plans is simple
    # From the indexGraph, do a DFS
    # Only save the plans that have the same length as self.__addedSubjectList
    # plan contains the list of possible index the user can take
    def dfsMain(self):
        try:
            tempPlan = []
            for tempIndex in self.__addedSubjectsList[0].indexList:
                self.tempMarkDayTime(tempIndex)
                tempPlan.append(tempIndex)
                self.dfs(tempIndex, tempPlan)
                tempPlan.remove(tempIndex)
                self.unmarkDayTime(tempIndex)
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::dfsMain()\nError msg: {err}')

    def dfs(self, tempIndex, tempPlan):
        try:
            if len(tempPlan) == len(self.__addedSubjectsList):
                self.__potentialPlan.append(tempPlan.copy())
            else:
                for nextTempIndex in tempIndex.next:
                    clash = False
                    for nextTempIndexInfo in nextTempIndex.indexInfoList:
                        if nextTempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LAB:
                            clash = self.gotClashForLab(self.getDayIndex(nextTempIndexInfo.day),
                                                        self.getTimeRangeIndex(nextTempIndexInfo.time),
                                                        nextTempIndexInfo.remarks)
                            if clash:
                                break
                        else:
                            clash = self.gotClash(self.getDayIndex(nextTempIndexInfo.day),
                                                  self.getTimeRangeIndex(nextTempIndexInfo.time))
                            if clash:
                                break
                    if not clash:
                        self.tempMarkDayTime(nextTempIndex)
                        tempPlan.append(nextTempIndex)
                        self.dfs(nextTempIndex, tempPlan)
                        tempPlan.remove(nextTempIndex)
                        self.unmarkDayTime(nextTempIndex)
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::dfs()\nError msg: {err}')

    # Check whether there is a clash when adding this specific index
    def gotClashForLab(self, col, timeRange, remarks):
        try:
            for row in range(timeRange[0], timeRange[1]):
                if not remarks and self.__dayTimeEvenOdd[row][col] != 'NIL':  # Some lab have no remarks so I assume it's all week
                    return True
                elif remarks == 'Even' and (
                        self.__dayTimeEvenOdd[row][col] == 'A' or self.__dayTimeEvenOdd[row][col] == 'E' or
                        self.__dayTimeEvenOdd[row][col] == 'EO'):
                    return True
                elif remarks == 'Odd' and (
                        self.__dayTimeEvenOdd[row][col] == 'A' or self.__dayTimeEvenOdd[row][col] == 'O' or
                        self.__dayTimeEvenOdd[row][col] == 'EO'):
                    return True
            return False
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::gotClashForLab()\nError msg: {err}')

    # Check whether there's a general clash when adding this specific index
    def gotClash(self, col, timeRange):
        try:
            for row in range(timeRange[0], timeRange[1]):
                if self.__dayTime[row][col] == 1:
                    return True
            return False
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::gotClash()\nError msg: {err}')

    # Temporarily mark the day time
    def tempMarkDayTime(self, tempIndex):
        try:
            for tempIndexInfo in tempIndex.indexInfoList:
                if tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LAB:
                    self.tempMarkDayTimeForLab(self.getDayIndex(tempIndexInfo.day),
                                               self.getTimeRangeIndex(tempIndexInfo.time), tempIndexInfo.remarks)
                else:
                    # For non-lab, i assume it is all week
                    timeRange = self.getTimeRangeIndex(tempIndexInfo.time)
                    for row in range(timeRange[0], timeRange[1]):
                        self.__dayTime[row][self.getDayIndex(tempIndexInfo.day)] = 1
                        self.__dayTimeEvenOdd[row][self.getDayIndex(tempIndexInfo.day)] = 'A'
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::tempMarkDayTime()\nError msg: {err}')

    # Temporarily mark the day time for lab
    def tempMarkDayTimeForLab(self, col, timeRange, remarks):
        try:
            for row in range(timeRange[0], timeRange[1]):
                if self.__dayTime[row][col] == 0:
                    self.__dayTime[row][col] = 1
                    if remarks == 'Even':
                        self.__dayTimeEvenOdd[row][col] = 'E'
                    elif remarks == 'Odd':
                        self.__dayTimeEvenOdd[row][col] = 'O'
                    else:
                        self.__dayTimeEvenOdd[row][col] = 'A'
                else:
                    # Something is occupying this time slot. So, check the evenOdd
                    if (remarks == 'Even' and self.__dayTimeEvenOdd[row][col] == 'O') or (
                            remarks == 'Odd' and self.__dayTimeEvenOdd[row][col] == 'E'):
                        self.__dayTimeEvenOdd[row][col] = 'EO'
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::tempMarkDayTimeForLab()\nError msg: {err}')

    # Unmark the temporary marked day time
    def unmarkDayTime(self, tempIndex):
        try:
            for tempIndexInfo in tempIndex.indexInfoList:
                if tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LAB:
                    self.unmarkDayTimeForLab(self.getDayIndex(tempIndexInfo.day),
                                             self.getTimeRangeIndex(tempIndexInfo.time), tempIndexInfo.remarks)
                else:
                    timeRange = self.getTimeRangeIndex(tempIndexInfo.time)
                    for row in range(timeRange[0], timeRange[1]):
                        self.__dayTime[row][self.getDayIndex(tempIndexInfo.day)] = 0
                        self.__dayTimeEvenOdd[row][self.getDayIndex(tempIndexInfo.day)] = 'NIL'
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::unmarkDayTime()\nError msg: {err}')

    # Unmark the temporary marked day time for lab
    def unmarkDayTimeForLab(self, col, timeRange, remarks):
        try:
            for row in range(timeRange[0], timeRange[1]):
                if remarks == 'Even' and self.__dayTimeEvenOdd[row][col] == 'EO':
                    self.__dayTimeEvenOdd[row][col] = 'O'
                elif remarks == 'Odd' and self.__dayTimeEvenOdd[row][col] == 'EO':
                    self.__dayTimeEvenOdd[row][col] = 'E'
                else:
                    self.__dayTimeEvenOdd[row][col] = 'NIL'
                    self.__dayTime[row][col] = 0
        except Exception as err:
            self.showErrorMsg(f'addRemoveSubjects(planWithFriends)::unmarkDayTimeForLab()\nError msg: {err}')

    # Get the index based on the day
    def getDayIndex(self, day):
        return self.__dayDict.get(day)

    # Get the range index based on the time
    def getTimeRangeIndex(self, time):
        return [self.__timeDict.get(time.split('-')[0]), self.__timeDict.get(time.split('-')[1])]

    # Reset the ui to its default state
    # Default state: empty nameLineEdit, courseYearComboBox is at index 0,
    # addedSubjectListWidget is empty, and submitBtn is disabled
    def resetUi(self):
        self.nameLineEdit.clear()
        self.courseYearComboBox.setCurrentIndex(0)
        self.addedSubjectListWidget.clear()
        self.__addedSubjectsList.clear()
        self.submitBtn.setEnabled(False)

    def showErrorMsg(self, errorMsg):
        QMessageBox.critical(self, self.getWindowName(), errorMsg)

    def getWindowName(self):
        return 'Add/Remove Subjects (Plan with Friends)'