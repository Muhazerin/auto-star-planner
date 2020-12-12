from ui.dialog.addCoursesDialog import addCourses
from model.index import (Index, typeIndexInfoEnum)

from PyQt5.QtCore import (pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import (QDialog, QMessageBox)

class AddCourses(QDialog, addCourses.Ui_dialog):    
    lecInfo = pyqtSignal(int, list, str)
    donePlanning = pyqtSignal()
    def __init__(self):
        super(AddCourses, self).__init__()
        self.courseList = []
        self.selectedCourse = []
        self.colDict = {
            "MON":0,
            "TUE":1,
            "WED":2,
            "THU":3,
            "FRI":4,
            "SAT":5,
        }
        self.dayTimeRowDict = {
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
        self.potentialPlan = []

        self.dayTime = []
        self.dayTimeEvenOdd = []
        for i in range(0, 31):
            self.dayTime.append([0] * 6)
            self.dayTimeEvenOdd.append(["NIL"] * 6)     # NIL, A = All week, E = Even week, O = Odd Week, EO = Even and Odd Week, MDP = MDP

        self.setupUi(self)
        self.planBtn.pressed.connect(self.check)

    def check(self):
        if self.planBtn.text() == "Check":
            self.selectedCourse.clear()
            addCourseList = self.coursesTxtEdit.toPlainText().upper().split()
            for course in addCourseList:
                valid = False
                if not valid:
                    for course2 in self.courseList:
                        if course == course2.courseCode:
                            self.selectedCourse.append(course2)
                            valid = True
                            break
                if not valid:
                    culprit = course
                    break
            
            if not valid:
                QMessageBox.critical(self, "Add Course", f"{culprit} is not found in class schedule")
                self.hide()
            else:
                self.planBtn.setText("Plan")
                QMessageBox.information(self, "Add Course", "Check OK!\nPress the plan button")
        else:
            self.planBtn.setText("Check")
            self.plan()

    def plan(self):
        self.potentialPlan.clear()
        print("Plan my semester...")
        # Step 1: Check for clashing lectures (Future update: Check which course lecture clash with which)
        if not (self.setLecTimeOnArray()):
            QMessageBox.critical(self, "Add Course", "Unable to plan the semester with these course setup.\nThere are clashing lectures.")
            self.hide()
            return

        # Step 2: Remove all the course indexes that clashes with the set course lecture
        if not (self.removeClashingCourseIndexes()):
            QMessageBox.critical(self, "Add Course", "Unable to plan the semester with these course setup.\nThere's a course with 0 index after removing index clashing with lectures")
            self.hide()
            return

        # Step 3: Create index graph
        self.createIndexGraph()
        
        # Step 4: Do DFS to gather the potential plans
        self.dfsMain()
        if self.potentialPlan:
            print(f"There are {len(self.potentialPlan)} potential plan(s)")
            QMessageBox.information(self, "Add Courses", f"There are {len(self.potentialPlan)} potential plan(s)")
            
            # Do this code at the end after got valid plan(s) to set the lecture timings
            for course in self.selectedCourse:
                for lecTiming in course.getLecTiming():
                    self.lecInfo.emit(self.getColIndex(lecTiming[0]), self.getRowRangeIndex(lecTiming[1]), f"{course.courseCode} Lec")
        else:
            QMessageBox.critical(self, "Add Courses", "Unable to plan the semester with these course setup")
            self.hide()
            return
        # clear the dayTime and dayTimeEvenOdd after finishing
        self.dayTime = []
        self.dayTimeEvenOdd = []
        for i in range(0, 31):
            self.dayTime.append([0] * 6)
            self.dayTimeEvenOdd.append(["NIL"] * 6)
        self.hide()
        self.donePlanning.emit()

    def createIndexGraph(self):
        for i in range(len(self.selectedCourse) - 1):
           for index in self.selectedCourse[i].indexList:
               index.next = self.selectedCourse[i+1].indexList   

    def dfsMain(self):
        tempPlan = []
        for index in self.selectedCourse[0].indexList:
            self.tempMarkDayTime(index)
            tempPlan.append(index)
            self.dfs(index, tempPlan)
            tempPlan.remove(index)
            self.unmarkDayTime(index)

    def dfs(self, index, tempPlan):
        if len(tempPlan) == len(self.selectedCourse):
            self.potentialPlan.append(tempPlan.copy())
        else:
            # some course only have tut while some have both tut and lab.
            # i need to check if that index have slot. mean check all the indexInfo does not clash
            for nextIndex in index.next:
                clash = False
                for nextIndexInfo in nextIndex.indexInfoList:
                    if nextIndexInfo.indexInfoType == typeIndexInfoEnum.TUT:
                        if (self.gotClash(self.getColIndex(nextIndexInfo.day), self.getRowRangeIndex(nextIndexInfo.time))):
                            clash = True
                            break
                    else:   # currently, if not tut, then it means lab. this is a possible area of update
                        if (self.gotClashForLab(self.getColIndex(nextIndexInfo.day), self.getRowRangeIndex(nextIndexInfo.time), nextIndexInfo.remarks)):
                            clash = True
                            break
                if not clash:   # if there's no clash, do dfs
                    self.tempMarkDayTime(nextIndex)
                    tempPlan.append(nextIndex)
                    self.dfs(nextIndex, tempPlan)
                    tempPlan.remove(nextIndex)
                    self.unmarkDayTime(nextIndex)

    def tempMarkDayTime(self, index):
        for indexInfo in index.indexInfoList:
            if indexInfo.indexInfoType == typeIndexInfoEnum.TUT:
                self.setOnArray(self.getColIndex(indexInfo.day), self.getRowRangeIndex(indexInfo.time))
            else:
                self.setOnArrayForLab(self.getColIndex(indexInfo.day), self.getRowRangeIndex(indexInfo.time), indexInfo.remarks)
    
    def unmarkDayTime(self, index):
        for indexInfo in index.indexInfoList:
            if indexInfo.indexInfoType == typeIndexInfoEnum.TUT:
                self.unsetArray(self.getColIndex(indexInfo.day), self.getRowRangeIndex(indexInfo.time))
            else:
                self.unsetArrayForLab(self.getColIndex(indexInfo.day), self.getRowRangeIndex(indexInfo.time), indexInfo.remarks)

    def unsetArray(self, col, rowRange):
        for row in range(rowRange[0], rowRange[1]):
            self.dayTime[row][col] = 0
            self.dayTimeEvenOdd[row][col] = "NIL"

    def getColIndex(self, day):
        return self.colDict.get(day)

    def getRowRangeIndex(self, time):
        timeList = time.split("-")
        startEnd = [self.dayTimeRowDict.get(timeList[0]), self.dayTimeRowDict.get(timeList[1])]
        return startEnd

    def setOnArray(self, col, rowRange):
        ableToSet = True
        for row in range(rowRange[0], rowRange[1]):
            if self.dayTime[row][col] == 0:
                self.dayTime[row][col] = 1
                self.dayTimeEvenOdd[row][col] = "A"
            else:
                ableToSet = False
                break
        return ableToSet

    def unsetArrayForLab(self, col, rowRange, remarks):
        for row in range(rowRange[0], rowRange[1]):
            if (remarks == "Even" and self.dayTimeEvenOdd[row][col] == "EO"):
                self.dayTimeEvenOdd[row][col] = "O"
            elif (remarks == "Odd" and self.dayTimeEvenOdd[row][col] == "EO"):
                self.dayTimeEvenOdd[row][col] = "E"
            else:
                self.dayTimeEvenOdd[row][col] = "NIL"
                self.dayTime[row][col] = 0

    def setOnArrayForLab(self, col, rowRange, remarks):
        ableToSet = True
        for row in range(rowRange[0], rowRange[1]):
            if self.dayTime[row][col] == 0:
                self.dayTime[row][col] = 1
                if remarks == "Even":
                    self.dayTimeEvenOdd[row][col] = "E"
                elif remarks == "Odd":
                    self.dayTimeEvenOdd[row][col] = "O"
                else:
                    self.dayTimeEvenOdd[row][col] = "MDP"
            else:   # something is occupying that slot. need to check
                if self.dayTimeEvenOdd[row][col] == "A":
                    ableToSet = False
                    break
                elif (remarks == "Even" and self.dayTimeEvenOdd[row][col] == "O") or (remarks == "Odd" and self.dayTimeEvenOdd[row][col] == "E"):
                    self.dayTimeEvenOdd[row][col] = "EO"
                else:
                    ableToSet = False
                    break
        return ableToSet

    # translate the time {MON, 0800 - 0830} to dayTime[][]
    def setLecTimeOnArray(self):
        for course in self.selectedCourse:
            for lecTiming in course.getLecTiming():
                if not (self.setOnArray(self.getColIndex(lecTiming[0]), self.getRowRangeIndex(lecTiming[1]))):
                    return False
        return True

    # removing course indexes that clashes with lecture timing
    def removeClashingCourseIndexes(self):
        for course in self.selectedCourse:
            tempIndexList = []
            for index in course.indexList:  # a course may have multiple indexes. indexes are like different classes
                for indexInfo in index.indexInfoList:   # an index may have tutorial and lab. those are indexInfo
                    if (self.gotClash(self.getColIndex(indexInfo.getTiming()[0]), self.getRowRangeIndex(indexInfo.getTiming()[1]))):
                        tempIndexList.append(index)
                        break
            # remove the clashing index from the course
            for tempIndex in tempIndexList:
                course.indexList.remove(tempIndex)
            # check the current indexList size
            if len(course.indexList) == 0:
                return False
        return True               

    def gotClashForLab(self, col, rowRange, remarks):
        for row in range(rowRange[0], rowRange[1]):
            if remarks == "Even" and (self.dayTimeEvenOdd[row][col] == "A" or self.dayTimeEvenOdd[row][col] == "E" or self.dayTimeEvenOdd[row][col] == "EO"):
                return True
            elif remarks == "Odd" and (self.dayTimeEvenOdd[row][col] == "A" or self.dayTimeEvenOdd[row][col] == "O" or self.dayTimeEvenOdd[row][col] == "EO"):
                return True
            elif remarks == "MDP" and self.dayTime[row][col] == 1:
                return True
        return False

    def gotClash(self, col, rowRange):
        for row in range(rowRange[0], rowRange[1]):
            if self.dayTime[row][col] == 1:
                return True
        return False