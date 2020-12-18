from ui.dialog.addRemoveSubjectsDialog import addRemoveSubjectsDialog
from PyQt5.QtWidgets import (QDialog, QMessageBox)
from datasource import datasource
from model import (course, index)
import sys

# TODO: BUG FOUND!! I add a subject in SCSE Year 4 list.
#  When I go to SCSE Year 3 list, I can add the same subject

class Dialog(QDialog, addRemoveSubjectsDialog.Ui_AddRemoveSubject):
    def __init__(self, mainPotentialPlan):
        super(Dialog, self).__init__()
        self.__mainPotentialPlan = mainPotentialPlan
        self.__addedSubjectsList = []
        self.setupUi(self)

        self.__dayDict = {
            "MON":0,
            "TUE":1,
            "WED":2,
            "THU":3,
            "FRI":4,
            "SAT":5,
        }
        self.__timeDict = {
            "0800":0,
            "0830":1,
            "0900":2,
            "0930":3,
            "1000":4,
            "1030":5,
            "1100":6,
            "1130":7,
            "1200":8,
            "1230":9,
            "1300":10,
            "1330":11,
            "1400":12,
            "1430":13,
            "1500":14,
            "1530":15,
            "1600":16,
            "1630":17,
            "1700":18,
            "1730":19,
            "1800":20,
            "1830":21,
            "1900":22,
            "1930":23,
            "2000":24,
            "2030":25,
            "2100":26,
            "2130":27,
            "2200":28,
            "2230":29,
            "2300":30,
        }

        self.__potentialPlan = []
        self.__dayTime = []
        self.__dayTimeEvenOdd = []
        for i in range(0, 31):
            self.__dayTime.append([0] * 6)
            self.__dayTimeEvenOdd.append(["NIL"] * 6)     # NIL, A = All week, E = Even week, O = Odd Week, EO = Even and Odd Week

        self.__courseYear = datasource.loadCourseYears()
        self.loadCourseYears()
        self.courseYearComboBox.currentTextChanged.connect(self.loadSubjectListWidget)

        self.subjectListWidget.itemPressed.connect(self.clearAddedSubjectListAndRemoveButton)
        self.addedSubjectListWidget.itemPressed.connect(self.clearSubjectListAndAddButton)

        self.subjectListWidget.currentRowChanged.connect(self.setAddBtn)
        self.addBtn.clicked.connect(self.addBtnClicked)

        self.removeBtn.clicked.connect(self.removeBtnClicked)

        self.planBtn.clicked.connect(self.planBtnClicked)

    # Load the course year into the courseYearComboBox ui
    def loadCourseYears(self):
        if type(self.__courseYear) is not dict:
            # Raise an error
            QMessageBox.critical(self, self.getWindowName(), f'Error msg: {self.__courseYear}')
            sys.exit(1)
        else:
            for courseYear in self.__courseYear.values():
                self.courseYearComboBox.addItem(courseYear)

    # Load the list of subjects into subjectListWidget ui
    # Called everytime when user change courseYearComboBox text
    def loadSubjectListWidget(self, currentText):
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
                print(type(self.__subjectList))
                QMessageBox.critical(self, self.getWindowName(), f'Error Msg: {self.__subjectList}')
                sys.exit(1)
            else:
                for subject in self.__subjectList:
                    self.subjectListWidget.addItem(f'{subject.courseCode}: {subject.courseName}')
                self.subjectListWidget.setMinimumWidth(self.subjectListWidget.sizeHintForColumn(0))
            QMessageBox.information(self, self.getWindowName(), f'Finished loading subjects for {currentText}')

    # Returns the self.__courseYear key according to the value
    def getCourseYearKey(self, val):
        for key, value in self.__courseYear.items():
            if value == val:
                return key

    # Disable the remove button and clear focus in addedSubjectListWidget
    # Called everytime an item is pressed in subjectListWidget
    def clearAddedSubjectListAndRemoveButton(self):
        # These 2 ui symbolically forms a pair
        self.removeBtn.setEnabled(False)
        self.addedSubjectListWidget.setCurrentRow(-1)

    # Disable the add button and clear focus in subjectListWidget
    # Enable the remove button
    # Called everytime an item is pressed in addedSubjectListWidget
    def clearSubjectListAndAddButton(self):
        self.addBtn.setEnabled(False)
        self.subjectListWidget.setCurrentRow(-1)
        self.removeBtn.setEnabled(True)

    # Enable/disable the add button
    # currentRow: Int = subjectListWidget current row
    # Called everytime when user changes selection in subjectListWidget ui
    def setAddBtn(self, currentRow):
        if currentRow > -1:
            if self.__subjectList[currentRow].courseType == course.courseType.ONLINE:
                # Disable the add button if the course is an online course
                self.addBtn.setEnabled(False)
            elif len(self.__addedSubjectsList) == 0:
                # Enable the add button if self.__addedSubjectList is empty
                self.addBtn.setEnabled(True)
            else:
                # Check whether the subject exist in the addedSubjectListWidget
                # If exist, disable the addBtn. If not, enable the addBtn
                for addedSubject in self.__addedSubjectsList:
                    if self.__subjectList[currentRow] == addedSubject:
                        self.addBtn.setEnabled(False)
                        return
                self.addBtn.setEnabled(True)

    # Performs the necessary logic when the add button is clicked
    # Called everytime the add button is clicked
    def addBtnClicked(self):
        self.addBtn.setEnabled(False)
        # add the subject to addedSubjectsList
        self.__addedSubjectsList.append(self.__subjectList[self.subjectListWidget.currentRow()])
        # update the ui by adding the name to the list
        self.addedSubjectListWidget.addItem(f'{self.__subjectList[self.subjectListWidget.currentRow()].courseCode}: {self.__subjectList[self.subjectListWidget.currentRow()].courseName}')
        # adjust the ui width accordingly
        self.addedSubjectListWidget.setMinimumWidth(self.addedSubjectListWidget.sizeHintForColumn(0))
        # Enable the plan button
        self.planBtn.setEnabled(True)

    # Remove the selected course from self.__addedSubjectsList
    # Update the list widget and remove btn accordingly
    # Called everytime the remove button is clicked
    def removeBtnClicked(self):
        self.__addedSubjectsList.remove(self.__addedSubjectsList[self.addedSubjectListWidget.currentRow()])
        self.addedSubjectListWidget.takeItem(self.addedSubjectListWidget.currentRow())
        self.removeBtn.setEnabled(False)
        if (len(self.__addedSubjectsList) == 0):
            self.planBtn.setEnabled(False)
        # I need to call this as the list will pick the next item(if have).
        # So, I call this to clear the focus after removing an item
        self.addedSubjectListWidget.setCurrentRow(-1)

    # Plan my semester in 3 simple steps
    # 1. Create an index graph.
    # 2. Do a DFS and keep track potential index in a list. Add said list to mainPotentialPlan if 
    #    len(tempList) = len(self.__addedSubjectList)
    # 3. self.__mainPotentialPlan.potentialPlan = tempList
    def planBtnClicked(self):
        self.__potentialPlan.clear()
        self.clearIndexGraph()
        self.createIndexGraph()
        self.dfsMain()
        if len(self.__potentialPlan) > 0:
            self.__mainPotentialPlan.whoMadeTheChange = self.getWindowName()
            self.__mainPotentialPlan.potentialPlan = self.__potentialPlan
            self.__mainPotentialPlan.subjectList = self.__addedSubjectsList
            self.done(0)
        else:
            QMessageBox.critical(self, self.getWindowName(), "Unable to plan the semester with these setup")

    # Clear the index graph to eliminate some error
    def clearIndexGraph(self):
        for subject in self.__addedSubjectsList:
            for tempIndex in subject.indexList:
                tempIndex.next = None

    # Create an index graph
    # All the index of 1 course points to all indexes of another course
    def createIndexGraph(self):
        for i in range(len(self.__addedSubjectsList) - 1):
            for currSubjectIndex in self.__addedSubjectsList[i].indexList:
                currSubjectIndex.next = self.__addedSubjectsList[i+1].indexList


    # These next few functions are all for planning the potential plans

    # The algorithm to find the potential plans is simple
    # From the indexGraph, do a DFS
    # Only save the plans that have the same length as self.__addedSubjectList
    # plan contains the list of possible index the user can take
    def dfsMain(self):
        tempPlan = []
        for tempIndex in self.__addedSubjectsList[0].indexList:
            self.tempMarkDayTime(tempIndex)
            tempPlan.append(tempIndex)
            self.dfs(tempIndex, tempPlan)
            tempPlan.remove(tempIndex)
            self.unmarkDayTime(tempIndex)

    def dfs(self, tempIndex, tempPlan):
        if len(tempPlan) == len(self.__addedSubjectsList):
            self.__potentialPlan.append(tempPlan.copy())
        else:
            for nextTempIndex in tempIndex.next:
                clash = False
                for nextTempIndexInfo in nextTempIndex.indexInfoList:
                    if nextTempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LAB:
                        clash = self.gotClashForLab(self.getDayIndex(nextTempIndexInfo.day), self.getTimeRangeIndex(nextTempIndexInfo.time), nextTempIndexInfo.remarks)
                        if clash:
                            break
                    else:
                        clash = self.gotClash(self.getDayIndex(nextTempIndexInfo.day), self.getTimeRangeIndex(nextTempIndexInfo.time))
                        if clash:
                            break
                if not clash:
                    self.tempMarkDayTime(nextTempIndex)
                    tempPlan.append(nextTempIndex)
                    self.dfs(nextTempIndex, tempPlan)
                    tempPlan.remove(nextTempIndex)
                    self.unmarkDayTime(nextTempIndex)

    # Check whether there is a clash when adding this specific index
    def gotClashForLab(self, col, timeRange, remarks):
        for row in range(timeRange[0], timeRange[1]):
            if not remarks and self.__dayTimeEvenOdd[row][col] != 'NIL': # Some lab have no remarks so I assume it's all week
                return True
            elif remarks == 'Even' and (self.__dayTimeEvenOdd[row][col] == 'A' or self.__dayTimeEvenOdd[row][col] == 'E' or self.__dayTimeEvenOdd[row][col] == 'EO'):
                return True
            elif remarks == 'Odd' and (self.__dayTimeEvenOdd[row][col] == 'A' or self.__dayTimeEvenOdd[row][col] == 'O' or self.__dayTimeEvenOdd[row][col] == 'EO'):
                return True
        return False

    # Check whether there's a general clash when adding this specific index
    def gotClash(self, col, timeRange):
        for row in range(timeRange[0], timeRange[1]):
            if self.__dayTime[row][col] == 1:
                return True
        return False

    # Temporarily mark the day time
    def tempMarkDayTime(self, tempIndex):
        for tempIndexInfo in tempIndex.indexInfoList:
            if tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LAB:
                self.tempMarkDayTimeForLab(self.getDayIndex(tempIndexInfo.day), self.getTimeRangeIndex(tempIndexInfo.time), tempIndexInfo.remarks)
            else:
                # For non-lab, i assume it is all week
                timeRange = self.getTimeRangeIndex(tempIndexInfo.time)
                for row in range(timeRange[0], timeRange[1]):
                    self.__dayTime[row][self.getDayIndex(tempIndexInfo.day)] = 1
                    self.__dayTimeEvenOdd[row][self.getDayIndex(tempIndexInfo.day)] = 'A'

    # Temporarily mark the day time for lab
    def tempMarkDayTimeForLab(self, col, timeRange, remarks):
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
                if (remarks == 'Even' and self.__dayTimeEvenOdd[row][col] == 'O') or (remarks == 'Odd' and self.__dayTimeEvenOdd[row][col] == 'E'):
                    self.__dayTimeEvenOdd[row][col] = 'EO'
    
    # Unmark the temporary marked day time
    def unmarkDayTime(self, tempIndex):
        for tempIndexInfo in tempIndex.indexInfoList:
            if tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LAB:
                self.unmarkDayTimeForLab(self.getDayIndex(tempIndexInfo.day), self.getTimeRangeIndex(tempIndexInfo.time), tempIndexInfo.remarks)
            else:
                timeRange = self.getTimeRangeIndex(tempIndexInfo.time)
                for row in range(timeRange[0], timeRange[1]):
                    self.__dayTime[row][self.getDayIndex(tempIndexInfo.day)] = 0
                    self.__dayTimeEvenOdd[row][self.getDayIndex(tempIndexInfo.day)] = 'NIL'

    # Unmark the temporary marked day time for lab
    def unmarkDayTimeForLab(self, col, timeRange, remarks):
        for row in range(timeRange[0], timeRange[1]):
            if (remarks == 'Even' and self.__dayTimeEvenOdd[row][col] == 'EO'):
                self.__dayTimeEvenOdd[row][col] = 'O'
            elif (remarks == 'Odd' and self.__dayTimeEvenOdd[row][col] == 'EO'):
                self.__dayTimeEvenOdd[row][col] = 'E'
            else:
                self.__dayTimeEvenOdd[row][col] = 'NIL'
                self.__dayTime[row][col] = 0

    # Get the index based on the day
    def getDayIndex(self, day):
        return self.__dayDict.get(day)

    # Get the range index based on the time
    def getTimeRangeIndex(self, time):
        return [self.__timeDict.get(time.split('-')[0]), self.__timeDict.get(time.split('-')[1])]

    # The many potential plan functions end here

    def updatePlan(self):
        pass

    def getWindowName(self):
        return "Add/Remove Subjects"