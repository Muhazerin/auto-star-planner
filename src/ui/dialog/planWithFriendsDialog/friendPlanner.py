from ui.dialog.planWithFriendsDialog import plannerDialog
from ui.dialog.planWithFriendsDialog.model import (potentialPlanCopy, friends)
from model import index

from PyQt5.QtWidgets import (QDialog, QMessageBox, QLabel)
from PyQt5.QtCore import pyqtSlot

class Dialog(QDialog, plannerDialog.Ui_plannerTableDialog):
    def __init__(self):
        try:
            super(Dialog, self).__init__()
            self.__friendPotentialPlan = None
            self.__friend = None

            self.__dayDict = {
                "MON": 0,
                "TUE": 1,
                "WED": 2,
                "THU": 3,
                "FRI": 4,
                "SAT": 5,
            }  # Dictionary to translate day into respective index
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
            }  # Dictionary to translate the time into respective index

            self.setupUi(self)
            self.planSpinBox.valueChanged.connect(self.onPlanSpinBoxValueChanged)
        except Exception as err:
            self.showErrorMsg(f'friendPlanner::__init__()\nError msg: {err}')

    @pyqtSlot(int)
    def onPlanSpinBoxValueChanged(self, newValue):
        try:
            text = ''
            for i in range(len(self.__friendPotentialPlan.subjectList)):
                text += f'{self.__friendPotentialPlan.subjectList[i].courseCode}: {self.__friendPotentialPlan.potentialPlan[newValue - 1][i].indexNo}          '
            self.overviewLbl.setText(text)
            self.overviewLbl.show()
            self.updateTable(newValue)
        except Exception as err:
            self.showErrorMsg(f'friendPlanner::onPlanSpinBoxValueChanged()\nError msg: {err}')

    def updateTable(self, currentPlanNumber):
        try:
            self.plannerTable.clearContents()
            # Loop through the index of the plan
            # Get the info (LEC, TUT, LAB, etc)
            # Set the appropriate color code and info to the table
            for i in range(len(self.__friendPotentialPlan.potentialPlan[currentPlanNumber - 1])):
                for tempIndexInfo in self.__friendPotentialPlan.potentialPlan[currentPlanNumber - 1][i].indexInfoList:
                    timeRange = self.getTimeRangeIndex(tempIndexInfo.time)
                    if tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LEC:
                        for row in range(timeRange[0], timeRange[1]):
                            self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day),
                                                            self.getInfoLabel(tempIndexInfo.indexInfoType,
                                                                              f'{self.__friendPotentialPlan.subjectList[i].courseCode} LEC'))
                    elif tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.TUT:
                        for row in range(timeRange[0], timeRange[1]):
                            self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day),
                                                            self.getInfoLabel(tempIndexInfo.indexInfoType,
                                                                              f'{self.__friendPotentialPlan.subjectList[i].courseCode} TUT'))
                    elif tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LAB:
                        for row in range(timeRange[0], timeRange[1]):
                            if (self.plannerTable.cellWidget(row, self.getDayIndex(
                                    tempIndexInfo.day))):  # if there's some value existing in that cell
                                text = self.plannerTable.cellWidget(row, self.getDayIndex(tempIndexInfo.day)).text()
                                text += f"\n{self.__friendPotentialPlan.subjectList[i].courseCode} LAB {tempIndexInfo.remarks}"
                                self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day),
                                                                self.getInfoLabel(tempIndexInfo.indexInfoType, text))
                            else:
                                if not tempIndexInfo.remarks:
                                    self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day),
                                                                    self.getInfoLabel(tempIndexInfo.indexInfoType,
                                                                                      f"{self.__friendPotentialPlan.subjectList[i].courseCode} LAB All Week"))
                                else:
                                    self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day),
                                                                    self.getInfoLabel(tempIndexInfo.indexInfoType,
                                                                                      f"{self.__friendPotentialPlan.subjectList[i].courseCode} LAB {tempIndexInfo.remarks}"))
                    else:  # For other indexInfoType like SEM, etc
                        for row in range(timeRange[0], timeRange[1]):
                            self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day),
                                                            self.getInfoLabel(tempIndexInfo.indexInfoType,
                                                                              f'{self.__friendPotentialPlan.subjectList[i].courseCode} OTHERS'))
        except Exception as err:
            self.showErrorMsg(f'friendPlanner::updateTable()\nError msg: {err}')

    # Returns the tempLabel for the timetable
    def getInfoLabel(self, indexInfoType, text):
        tempLabel = QLabel(text)
        if indexInfoType == index.typeIndexInfoEnum.LEC:
            tempLabel.setStyleSheet("background-color: lightskyblue; font-family: Arial; font-size: 22px")
        elif indexInfoType == index.typeIndexInfoEnum.TUT:
            tempLabel.setStyleSheet("background-color: springgreen; font-family: Arial; font-size: 22px")
        elif indexInfoType == index.typeIndexInfoEnum.LAB:
            tempLabel.setStyleSheet("background-color: salmon; font-family: Arial; font-size: 22px")
        else:
            tempLabel.setStyleSheet("background-color: lightcoral; font-family: Arial; font-size: 22px")
        return tempLabel

    # Get the index based on the day
    def getDayIndex(self, day):
        return self.__dayDict.get(day)

    # Get the range index based on the time
    def getTimeRangeIndex(self, time):
        return [self.__timeDict.get(time.split('-')[0]), self.__timeDict.get(time.split('-')[1])]

    @pyqtSlot(friends.Friend, potentialPlanCopy.PotentialPlanCopy)
    def viewFriendPlanEmitted(self, friend, friendPotentialPlan):
        self.__friend = friend
        self.__friendPotentialPlan = friendPotentialPlan
        self.setWindowTitle(f'{self.__friend.name}\'s Planner')
        self.planSpinBox.setMinimum(1)
        self.planSpinBox.setMaximum(len(self.__friendPotentialPlan.potentialPlan))
        self.totalPlanLbl.setText(f'{len(self.__friendPotentialPlan.potentialPlan)}')
        self.planSpinBox.setEnabled(True)
        self.planSpinBox.setValue(1)
        self.onPlanSpinBoxValueChanged(1)

    def showErrorMsg(self, errorMsg):
        QMessageBox.critical(self, self.getWindowName(), errorMsg)

    def getWindowName(self):
        return 'Friend\'s Planner'