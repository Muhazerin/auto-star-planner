from bs4 import BeautifulSoup
import sys, os
import importlib

from ui.mainwindow import window
from model import (potentialPlan, index)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QAction, QLabel, QMessageBox)

class Window(QMainWindow, window.Ui_MainWindow):
    # Initialize some variables
    # Initialize mainPotentialPlan and set itself as an observer
    # Setup the ui and load the dialogs
    def __init__(self):
        try:
            super(Window, self).__init__()
            self.importedDialogObjectList = []   # Holds the imported dialog objects
            self.qActionList = []                # Holds the qActions
            self.__dayDict = {
                "MON": 0,
                "TUE": 1,
                "WED": 2,
                "THU": 3,
                "FRI": 4,
                "SAT": 5,
            }               # Dictionary to translate day into respective index
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
            }              # Dictionary to translate the time into respective index

            self.mainPotentialPlan = potentialPlan.PotentialPlan()  # This class contains all the possible plans
            self.mainPotentialPlan.addObserver(self)                # Add itself as observer so this runs updatePlan()

            # Setup the UI
            self.setupUi(self)
            self.overviewLbl.hide()
            self.planSpinBox.valueChanged.connect(self.onPlanValueChanged)

            # Loads all the extension
            self.loadDialogs()
        except Exception as err:
            self.showErrorMsg(f'Mainwindow::__init__()\nError msg: {err}')

    # Called everytime the value in planSpinBox changed
    # Set the overviewLbl to its appropriate text
    # Updates the table to show the appropriate timetable
    def onPlanValueChanged(self, newValue):
        try:
            text = ''
            for i in range(len(self.mainPotentialPlan.subjectList)):
                text += f'{self.mainPotentialPlan.subjectList[i].courseCode}: {self.mainPotentialPlan.potentialPlan[self.planSpinBox.value() - 1][i].indexNo}          '
            self.overviewLbl.setText(text)
            self.overviewLbl.show()
            self.updateTable(newValue)
        except Exception as err:
            self.show(f'MainWindow::onPlanValueChanged()\nError msg: {err}')

    # Called everytime the app runs
    # Load the extensions
    def loadDialogs(self):
        try:
            # Clear the current imported dialog list
            # and qAction list
            self.importedDialogObjectList.clear()
            self.qActionList.clear()

            # Create a QMenu object
            self.menuExtension = QMenu(self.menubar)
            self.menuExtension.setObjectName("menuExtension")
            self.menuExtension.setTitle("Extensions")

            # Dynamically import the modules and add the object to importedDialogObjectList
            # After importing the modules, add a QAction to QMenu object
            # The qAction tells qt how to open the dialog
            for folder in os.listdir(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))+"/dialog"):
                self.importedDialogObjectList.append(importlib.import_module(f'ui.dialog.{folder}.{folder[:-6]}').Dialog(self.mainPotentialPlan))
                self.mainPotentialPlan.addObserver(self.importedDialogObjectList[-1])

                self.qActionList.append(QAction(self))
                self.qActionList[-1].setObjectName("action_"+folder)
                self.qActionList[-1].setText(self.importedDialogObjectList[-1].getWindowName())
                self.qActionList[-1].triggered.connect(self.importedDialogObjectList[-1].exec)
                self.menuExtension.addAction(self.qActionList[-1])
            if len(self.importedDialogObjectList) > 0:    # if there's imported modules
                # Add the QMenu to the menubar
                self.menubar.addAction(self.menuExtension.menuAction())
        except Exception as err:
            self.showErrorMsg(f"MainWindow::loadDialogs()\nError msg: {err}")

    # Called everytime there's changes in the mainPotentialPlan
    def updatePlan(self):
        try:
            # Setup the ui for planSpinBox and totalPlanLbl
            self.planSpinBox.setMinimum(1)
            self.planSpinBox.setValue(1)    # This should call the onPlanValueChanged function
            self.onPlanValueChanged(1)      # But it will not be called if the value change from 1 to 1 (different plan)
            self.planSpinBox.setMaximum(len(self.mainPotentialPlan.potentialPlan))
            self.planSpinBox.setEnabled(True)
            self.totalPlanLbl.setText(f'{len(self.mainPotentialPlan.potentialPlan)}')
        except Exception as err:
            self.showErrorMsg(f'MainWindow::updatePlan()\nError msg: {err}')

    # Update to the appropriate timetable based on the currentPlanNumber
    def updateTable(self, currentPlanNumber):
        try:
            self.plannerTable.clearContents()   # Clears the current table
            # Loop through the index of the plan
            # Get the info (LEC, TUT, LAB, etc)
            # Set the appropriate color code and info to the table
            for i in range(len(self.mainPotentialPlan.potentialPlan[currentPlanNumber - 1])):
                for tempIndexInfo in self.mainPotentialPlan.potentialPlan[currentPlanNumber - 1][i].indexInfoList:
                    timeRange = self.getTimeRangeIndex(tempIndexInfo.time)
                    if tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LEC:
                        for row in range(timeRange[0], timeRange[1]):
                            self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day), self.getInfoLabel(tempIndexInfo.indexInfoType, f'{self.mainPotentialPlan.subjectList[i].courseCode} LEC'))
                    elif tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.TUT:
                        for row in range(timeRange[0], timeRange[1]):
                            self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day), self.getInfoLabel(tempIndexInfo.indexInfoType, f'{self.mainPotentialPlan.subjectList[i].courseCode} TUT'))
                    elif tempIndexInfo.indexInfoType == index.typeIndexInfoEnum.LAB:
                        for row in range(timeRange[0], timeRange[1]):
                            if (self.plannerTable.cellWidget(row, self.getDayIndex(tempIndexInfo.day))):  # if there's some value existing in that cell
                                text = self.plannerTable.cellWidget(row, self.getDayIndex(tempIndexInfo.day)).text()
                                text += f"\n{self.mainPotentialPlan.subjectList[i].courseCode} LAB {tempIndexInfo.remarks}"
                                self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day), self.getInfoLabel(tempIndexInfo.indexInfoType, text))
                            else:
                                if not tempIndexInfo.remarks:
                                    self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day), self.getInfoLabel(tempIndexInfo.indexInfoType, f"{self.mainPotentialPlan.subjectList[i].courseCode} LAB All Week"))
                                else:
                                    self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day), self.getInfoLabel(tempIndexInfo.indexInfoType, f"{self.mainPotentialPlan.subjectList[i].courseCode} LAB {tempIndexInfo.remarks}"))
                    else: # For other indexInfoType like SEM, etc
                        for row in range(timeRange[0], timeRange[1]):
                            self.plannerTable.setCellWidget(row, self.getDayIndex(tempIndexInfo.day), self.getInfoLabel(tempIndexInfo.indexInfoType, f'{self.mainPotentialPlan.subjectList[i].courseCode} OTHERS'))
        except Exception as err:
            self.showErrorMsg(f'MainWindow::updateTable()\nError msg: {err}')

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

    # Show the error message in QMessageBox
    def showErrorMsg(self, errorMsg):
        QMessageBox.critical(self, self.windowTitle(), errorMsg)
    
def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())