from bs4 import BeautifulSoup
import sys, os
import importlib

from ui.mainwindow import window
from model import (potentialPlan, index)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QAction, QLabel)

class Window(QMainWindow, window.Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.courseList = []
        self.importedDialogObjectList = []
        self.qActionList = []
        self.lastPlanSpinBoxValue = None
        self.currentPlanSpinBoxValue = None
        self.mainPotentialPlan = potentialPlan.PotentialPlan()
        self.mainPotentialPlan.addObserver(self)

        self.setupUi(self)
        self.overviewLbl.hide()
        self.planSpinBox.valueChanged.connect(self.onPlanValueChanged)

        self.loadDialogs()

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

    def onPlanValueChanged(self, newValue):
        text = ''
        for i in range(len(self.mainPotentialPlan.subjectList)):
            # i = 0..total_number_of_added_subjects
            text += f'{self.mainPotentialPlan.subjectList[i].courseCode}: {self.mainPotentialPlan.potentialPlan[self.planSpinBox.value() - 1][i].indexNo}          '
        self.overviewLbl.setText(text)
        self.updateTable(newValue)

    def loadDialogs(self):
        try:
            # clear the current imported dialog list
            # and try to import the modules 
            self.importedDialogObjectList.clear()
            self.qActionList.clear()

            # Create a QMenu object
            self.menuFile = QMenu(self.menubar)
            self.menuFile.setObjectName("menuFile")
            self.menuFile.setTitle("File")

            # Dynamically import the modules and add the object to importedDialogObjectList
            # After importing the modules, add a QAction to QMenu object
            for folder in os.listdir(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))+"/dialog"):
                self.importedDialogObjectList.append(importlib.import_module(f'ui.dialog.{folder}.{folder[:-6]}').Dialog(self.mainPotentialPlan))
                self.mainPotentialPlan.addObserver(self.importedDialogObjectList[-1])
                self.qActionList.append(QAction(self))
                self.qActionList[-1].setObjectName("action_"+folder)
                self.qActionList[-1].setText(self.importedDialogObjectList[-1].getWindowName())
                self.qActionList[-1].triggered.connect(self.importedDialogObjectList[-1].exec)
                self.menuFile.addAction(self.qActionList[-1])
            if len(self.importedDialogObjectList) > 0:    # if there's imported modules
                # Add the QMenu to the menubar
                self.menubar.addAction(self.menuFile.menuAction())               
        except Exception as err:
            print(f"MainWindow::loadDialogs() Other error occured: {err}")
        
    def updatePlan(self):
        self.planSpinBox.setMinimum(1)
        self.planSpinBox.setValue(1)
        self.planSpinBox.setMaximum(len(self.mainPotentialPlan.potentialPlan))
        self.planSpinBox.setEnabled(True)
        self.totalPlanLbl.setText(f'{len(self.mainPotentialPlan.potentialPlan)}')
        text = ''
        for i in range(len(self.mainPotentialPlan.subjectList)):
            # i = 0..total_number_of_added_subjects
            text += f'{self.mainPotentialPlan.subjectList[i].courseCode}: {self.mainPotentialPlan.potentialPlan[self.planSpinBox.value() - 1][i].indexNo}          '
        self.overviewLbl.setText(text)
        self.overviewLbl.show()
        self.updateTable(self.planSpinBox.value())

    def updateTable(self, currentPlanNumber):
        self.plannerTable.clearContents()
        for i in range(len(self.mainPotentialPlan.potentialPlan[currentPlanNumber - 1])):
            for tempIndexInfo in self.mainPotentialPlan.potentialPlan[currentPlanNumber - 1][i].indexInfoList:
                timeRange = self.getTimeRangeIndex(tempIndexInfo.time)
                if tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LEC:
                    for row in range(timeRange[0], timeRange[1]):
                        tempLabel = QLabel(f'{self.mainPotentialPlan.subjectList[i].courseCode} LEC')
                        tempLabel.setStyleSheet("background-color: lightskyblue; font-family: Arial; font-size: 22px")
                        self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day), tempLabel)
                elif tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.TUT:
                    for row in range(timeRange[0], timeRange[1]):
                        tempLabel = QLabel(f'{self.mainPotentialPlan.subjectList[i].courseCode} TUT')
                        tempLabel.setStyleSheet("background-color: springgreen; font-family: Arial; font-size: 22px")
                        self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day), tempLabel)
                elif tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LAB:
                    for row in range(timeRange[0], timeRange[1]):
                        if (self.plannerTable.cellWidget(row, self.getDayIndex(tempIndexInfo.day))):  # if there's some value existing in that cell
                            text = self.plannerTable.cellWidget(row, self.getDayIndex(tempIndexInfo.day)).text()
                            text += f"\n{self.mainPotentialPlan.subjectList[i].courseCode} LAB {tempIndexInfo.remarks}"
                            tempLabel = QLabel(text)
                            tempLabel.setStyleSheet("background-color: salmon; font-family: Arial; font-size: 22px")
                            self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day), tempLabel)
                        else:
                            if not tempIndexInfo.remarks:
                                tempLabel = QLabel(f"{self.mainPotentialPlan.subjectList[i].courseCode} LAB All Week")
                            else:
                                tempLabel = QLabel(f"{self.mainPotentialPlan.subjectList[i].courseCode} LAB {tempIndexInfo.remarks}")
                            tempLabel.setStyleSheet("background-color: salmon; font-family: Arial; font-size: 22px")
                            self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day), tempLabel)
                else: # For other indexInfoType like SEM, etc
                    for row in range(timeRange[0], timeRange[1]):
                        tempLabel = QLabel(f'{self.mainPotentialPlan.subjectList[i].courseCode} OTHERS')
                        tempLabel.setStyleSheet("background-color: lightcoral; font-family: Arial; font-size: 22px")
                        self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day), tempLabel)

    # Get the index based on the day
    def getDayIndex(self, day):
        return self.__dayDict.get(day)

    # Get the range index based on the time
    def getTimeRangeIndex(self, time):
        return [self.__timeDict.get(time.split('-')[0]), self.__timeDict.get(time.split('-')[1])]
    
def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())