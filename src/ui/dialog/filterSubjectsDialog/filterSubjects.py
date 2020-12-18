from ui.dialog.filterSubjectsDialog import (filterSubjectsDialog, potentialPlanCopy)

from PyQt5.QtWidgets import (QDialog, QLabel, QComboBox, QMessageBox)

class Dialog(QDialog, filterSubjectsDialog.Ui_filterSubjectsDialog):
    def __init__(self, mainPotentialPlan):
        super(Dialog, self).__init__()

        # This is the class i used to talk back to mainwindow via observer pattern
        self.__mainPotentialPlan = mainPotentialPlan

        # This is a copy of the mainPotentialPlan, for the apply filter and clear filter
        self.__mainPotentialPlanCopy = None

        self.__comboBoxList = []
        self.setupUi(self)
        self.applyFilterBtn.clicked.connect(self.applyFilterBtnClicked)
        self.clearFilterBtn.clicked.connect(self.clearFilterBtnClicked)

    def applyFilterBtnClicked(self):
        self.filterTypeComboBox.setEnabled(False)
        for comboBox in self.__comboBoxList:
            comboBox.setEnabled(False)
        self.applyFilterBtn.setEnabled(False)
        self.clearFilterBtn.setEnabled(True)
        self.applyFilter()

    def applyFilter(self):
        subjectIndex = self.getSubjectIndex()
        tempPlanList = []
        if self.filterTypeComboBox.currentText() == 'Blacklist':
            if self.__comboBoxList[subjectIndex].count() == 2:
                QMessageBox.critical(self, self.getWindowName(), "Dude! This is the only index.\nRemove the subject la")
                return
            for tempPlan in self.__mainPotentialPlanCopy.potentialPlan:
                if tempPlan[subjectIndex].indexNo != self.__comboBoxList[subjectIndex].currentText():
                    tempPlanList.append(tempPlan.copy())
        else:
            for tempPlan in self.__mainPotentialPlanCopy.potentialPlan:
                if tempPlan[subjectIndex].indexNo == self.__comboBoxList[subjectIndex].currentText():
                    tempPlanList.append(tempPlan.copy())
        self.__mainPotentialPlan.whoMadeTheChange = self.getWindowName()
        self.__mainPotentialPlan.subjectList = self.__mainPotentialPlanCopy.subjectList
        self.__mainPotentialPlan.potentialPlan = tempPlanList
        self.done(0)

    # Returns the index from self.__comboList where the current index != 0
    # Returns -1 if invalid
    def getSubjectIndex(self):
        for i in range(len(self.__comboBoxList)):
            if self.__comboBoxList[i].currentIndex() != 0:
                return i
        return -1

    def clearFilterBtnClicked(self):
        self.filterTypeComboBox.setEnabled(True)
        for comboBox in self.__comboBoxList:
            comboBox.setEnabled(True)
        self.applyFilterBtn.setEnabled(True)
        self.clearFilterBtn.setEnabled(False)

        self.resetUi()
        self.__comboBoxList.clear()
        for i in range(len(self.__mainPotentialPlanCopy.subjectList)):
            self.__comboBoxList.append(self.createComboBox(i))
            self.__comboBoxList[-1].currentIndexChanged.connect(self.comboBoxIndexChanged)
            self.dialogFormLayout.insertRow(i + 1, QLabel(str(self.__mainPotentialPlanCopy.subjectList[i].courseCode) + ': '), self.__comboBoxList[-1])
        self.__mainPotentialPlan.whoMadeTheChange = self.getWindowName()
        self.__mainPotentialPlan.potentialPlan = self.__mainPotentialPlanCopy.potentialPlan
        self.__mainPotentialPlan.subjectList = self.__mainPotentialPlanCopy.subjectList


    def updatePlan(self):
        if self.__mainPotentialPlan.whoMadeTheChange == 'Add/Remove Subjects':
            self.setEnabled(True)
            self.resetUi()
            self.__mainPotentialPlanCopy = potentialPlanCopy.PotentialPlanCopy(self.__mainPotentialPlan)
            self.__comboBoxList.clear()
            for i in range(len(self.__mainPotentialPlanCopy.subjectList)):
                self.__comboBoxList.append(self.createComboBox(i))
                self.__comboBoxList[-1].currentIndexChanged.connect(self.comboBoxIndexChanged)
                self.dialogFormLayout.insertRow(i+1, QLabel(str(self.__mainPotentialPlanCopy.subjectList[i].courseCode)+': '), self.__comboBoxList[-1])

    # SLOT: Called when any comboBox in self.__comboBoxList change index
    def comboBoxIndexChanged(self, currentIndex):
        if currentIndex != 0:
            for comboBox in self.__comboBoxList:
                if comboBox.currentIndex() == 0:
                    comboBox.setEnabled(False)
        else:
            for comboBox in self.__comboBoxList:
                comboBox.setEnabled(True)

    # Reset the ui to the default state
    def resetUi(self):
        for i in range(self.dialogFormLayout.rowCount() - 2):
            self.dialogFormLayout.removeRow(1)

    # Create the combo box for updatePlan function
    def createComboBox(self, subjectIndex):
        tempComboBox = QComboBox(self)
        tempComboBox.addItem("Choose an index")
        for i in range(len(self.__mainPotentialPlanCopy.potentialPlan)):
            if tempComboBox.findText(str(self.__mainPotentialPlanCopy.potentialPlan[i][subjectIndex].indexNo)) == -1:
                # The text does not exist in the combo box
                tempComboBox.addItem(str(self.__mainPotentialPlanCopy.potentialPlan[i][subjectIndex].indexNo))
        return tempComboBox

    def getWindowName(self):
        return 'Filter Subject'