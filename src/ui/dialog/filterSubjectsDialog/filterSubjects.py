from ui.dialog.filterSubjectsDialog import (filterSubjectsDialog, potentialPlanCopy)

from PyQt5.QtWidgets import (QDialog, QLabel, QComboBox, QMessageBox)

class Dialog(QDialog, filterSubjectsDialog.Ui_filterSubjectsDialog):
    def __init__(self, mainPotentialPlan):
        try:
            super(Dialog, self).__init__()

            # This is the class i used to talk back to mainwindow via observer pattern
            self.__mainPotentialPlan = mainPotentialPlan

            # This is a copy of the mainPotentialPlan, for the apply filter and clear filter
            self.__mainPotentialPlanCopy = None

            self.__comboBoxList = []
            self.__tempFilteredPlan = []
            self.setupUi(self)
            self.applyFilterBtn.clicked.connect(self.applyFilterBtnClicked)
            self.clearFilterBtn.clicked.connect(self.clearFilterBtnClicked)
        except Exception as err:
            self.showErrorMsg(f'filterSubjects::__init__()\nError msg: {err}')

    # Called everytime the applyFilterBtn is clicked
    # Tries to filter the plan based on the filter
    def applyFilterBtnClicked(self):
        try:
            tempPlanList = []
            self.clearFilterBtn.setEnabled(True)
            gotFilter = False
            first = True

            # Check if the user have set any filter
            # By checking the comboBox currentIndex
            for i in range(len(self.__comboBoxList)):
                if self.__comboBoxList[i].currentIndex() != 0:
                    # Tries to filter the plan if there is a filter set
                    gotFilter = True
                    if first:
                        first = False
                        tempPlanList = self.filterPlan(i, self.__comboBoxList[i].currentText(), self.__mainPotentialPlanCopy.potentialPlan)
                    else:
                        tempPlanList = self.filterPlan(i, self.__comboBoxList[i].currentText(), tempPlanList)

            # If the user tried to filter but the result of that filter does not gives a valid plan
            if len(tempPlanList) == 0 and gotFilter:
                QMessageBox.critical(self, self.getWindowName(), 'Unable to plan with the current filter')
                return

            # If there is no filter applied and the user pressed the apply button
            if not gotFilter:
                tempPlanList = self.__mainPotentialPlanCopy.potentialPlan
                self.clearFilterBtn.setEnabled(False)

            # Apply the changes to the mainwindow
            self.__mainPotentialPlan.potentialPlan = tempPlanList
            self.__mainPotentialPlan.whoMadeTheChange = self.getWindowName()
            self.__mainPotentialPlan.subjectList = self.__mainPotentialPlanCopy.subjectList
            self.done(0)
        except Exception as err:
            self.showErrorMsg(f'filterSubjects::applyFilterBtnClicked()\nError msg: {err}')

    # Loop through tempPlanList and retrieve the plan with the indexNo
    # I use tempPlanList as so the user can apply the filter to more than 1 subjects
    # First filter is based on mainPotentialPlanCopy. This produces another list: tempPlanList
    # Second filter onwards is based on the tempPlanList
    def filterPlan(self, subjectIndex, indexNo, tempPlanList):
        try:
            tempPlanList2 = []
            for tempPlan in tempPlanList:
                if tempPlan[subjectIndex].indexNo == indexNo:
                    tempPlanList2.append(tempPlan.copy())
            return tempPlanList2
        except Exception as err:
            self.showErrorMsg(f'filterSubjects::filterPlan()\nError msg: {err}')

    # Called everytime the user clicks the clearFilterBtn
    def clearFilterBtnClicked(self):
        try:
            # Reset the apply and filter btn ui
            self.applyFilterBtn.setEnabled(True)
            self.clearFilterBtn.setEnabled(False)

            # Reset the comboBox ui
            for i in range(len(self.__mainPotentialPlanCopy.subjectList)):
                self.__comboBoxList[i].clear()
                self.__comboBoxList[i].addItem('Choose an index')
                for tempPlan in self.__mainPotentialPlanCopy.potentialPlan:
                    if self.__comboBoxList[i].findText(str(tempPlan[i].indexNo)) == -1:
                        self.__comboBoxList[i].addItem(str(tempPlan[i].indexNo))

            # Reflect the changes to mainWindow
            self.__mainPotentialPlan.whoMadeTheChange = self.getWindowName()
            self.__mainPotentialPlan.potentialPlan = self.__mainPotentialPlanCopy.potentialPlan
            self.__mainPotentialPlan.subjectList = self.__mainPotentialPlanCopy.subjectList
        except Exception as err:
            self.showErrorMsg(f'filterSubjects::clearFilterBtnClicked()\nError msg: {err}')

    # Called everytime there's changes to mainPotentialPlan
    # However, this dialog only cares when Add/Remove Subjects make the changes
    # Tries to show the appropriate ui(comboBox) based on the plan
    def updatePlan(self):
        try:
            if self.__mainPotentialPlan.whoMadeTheChange == 'Add/Remove Subjects':
                self.setEnabled(True)
                self.resetUi()
                self.__mainPotentialPlanCopy = potentialPlanCopy.PotentialPlanCopy(self.__mainPotentialPlan)
                self.__comboBoxList.clear()
                for i in range(len(self.__mainPotentialPlanCopy.subjectList)):
                    self.__comboBoxList.append(self.createComboBox(i, self.__mainPotentialPlanCopy.potentialPlan))
                    self.dialogFormLayout.insertRow(i, QLabel(str(self.__mainPotentialPlanCopy.subjectList[i].courseCode)+': '), self.__comboBoxList[-1])
        except Exception as err:
            self.showErrorMsg(f'filterSubjects::updatePlan()\nError msg: {err}')

    # Reset the ui to the default state (the dialog with 2 buttons(applyFilterBtn and clearFilterBtn))
    def resetUi(self):
        try:
            for i in range(self.dialogFormLayout.rowCount() - 1):
                self.dialogFormLayout.removeRow(0)
        except Exception as err:
            self.showErrorMsg(f'filterSubjects::resetUi()\nError msg: {err}')

    # Create the combo box for updatePlan function
    def createComboBox(self, subjectIndex, tempPlanList):
        try:
            tempComboBox = QComboBox(self)
            tempComboBox.addItem("Choose an index")
            for i in range(len(tempPlanList)):
                if tempComboBox.findText(str(tempPlanList[i][subjectIndex].indexNo)) == -1:
                    # The text does not exist in the combo box so add it to the comboBox
                    tempComboBox.addItem(str(tempPlanList[i][subjectIndex].indexNo))
            return tempComboBox
        except Exception as err:
            self.showErrorMsg(f'filterSubjects::createComboBox()\nError msg: {err}')

    def showErrorMsg(self, errorMsg):
        QMessageBox.critical(self, self.getWindowName(), errorMsg)

    def getWindowName(self):
        return 'Filter Subject'