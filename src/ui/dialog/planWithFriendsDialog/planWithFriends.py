from ui.dialog.planWithFriendsDialog import (planWithFriendsDialog, addRemoveSubjects, friendPlanner)
from ui.dialog.planWithFriendsDialog.model import (potentialPlanCopy, friends)
from model import potentialPlan

from PyQt5.QtWidgets import (QDialog, QMessageBox)
from PyQt5.QtCore import (pyqtSlot, pyqtSignal)

class Dialog(QDialog, planWithFriendsDialog.Ui_planWithFriendsDialog):
    viewFriendPlan = pyqtSignal(friends.Friend, potentialPlanCopy.PotentialPlanCopy)
    def __init__(self, mainPotentialPlan):
        try:
            super(Dialog, self).__init__()
            # This is to reflect the changes to mainwindow
            self.__mainPotentialPlan = mainPotentialPlan
            # This is to hold the user's potential plan
            # I need 2 copies. 1 to do the changing and 1 to reset when user delete other friends
            self.__userPotentialPlan = None
            self.__userPotentialPlanCopy = None

            # To do the changing and reset when the user delete other friends
            self.__friendPotentialPlanList = []
            self.__friendPotentialPlanListCopy = []

            # To do the filtering via the common subjects
            # Will eventually hold the indexes to be removed for each subjects
            self.__collatedSubjectListWithFilteredIndexList = {}    # "course code": "set of indexes"
            self.__collatedSubjectListWithCommonIndex = {}
            self.__toBeRemovedIndex = {}

            # To find who has common subjects together --> "course code": "['user', 'friend#1 name', 'friend#2 name']"
            self.__subjectOccurence = {}

            self.__friendList = []
            self.__addRemoveSubjectsDialog = addRemoveSubjects.Dialog()
            self.__friendPlannerDialog = friendPlanner.Dialog()

            self.setupUi(self)
            self.addFriendBtn.clicked.connect(self.addFriendBtnClicked)
            self.__addRemoveSubjectsDialog.newFriendSignal.connect(self.plan)

            self.friendListWidget.currentRowChanged.connect(self.friendListWidgetRowChanged)
            self.viewFriendPlanBtn.clicked.connect(self.viewFriendPlanBtnClicked)
            self.viewFriendPlan.connect(self.__friendPlannerDialog.viewFriendPlanEmitted)
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::__init__():\nError msg: {err}')

    # Called everytime addFriendBtn is clicked
    # Opens the dialog for the user to add friend and their subjects
    @pyqtSlot()
    def addFriendBtnClicked(self):
        try:
            self.__addRemoveSubjectsDialog.resetUi()
            self.__addRemoveSubjectsDialog.exec()
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::addFriendBtnClicked()\nError msg: {err}')

    # How the planWithFriends works:
    # 1: It adds new friend to friendList

    @pyqtSlot(friends.Friend, potentialPlan.PotentialPlan)
    def plan(self, newFriend, friendPotentialPlan):
        # Add newFriend to friendList
        self.__friendList.append(newFriend)
        self.__friendPotentialPlanList.append(potentialPlanCopy.PotentialPlanCopy(friendPotentialPlan))
        self.__friendPotentialPlanListCopy.append(potentialPlanCopy.PotentialPlanCopy(friendPotentialPlan))
        self.friendListWidget.addItem(newFriend.name)

        # Collate the filtered index
        self.collateFilterIndex(self.__friendList[-1].name, self.__friendPotentialPlanList[-1])

        # Fill the toBeRemoved dict based on the collatedSubjectListWithFilteredIndexList and collatedSubjectListWithCommonIndex
        for key in self.__collatedSubjectListWithFilteredIndexList:
            self.__toBeRemovedIndex[key] = self.__collatedSubjectListWithFilteredIndexList[key].symmetric_difference(self.__collatedSubjectListWithCommonIndex[key])

        # Remove user's plan that have those indexes
        self.removePotentialPlan(self.__userPotentialPlan)
        # Remove friends plan that have those indexes
        for tempFriendPotentialPlan in self.__friendPotentialPlanList:
            self.removePotentialPlan(tempFriendPotentialPlan)

        # Reflect the changes to mainWindow
        self.__mainPotentialPlan.whoMadeTheChange = self.getWindowName()
        self.__mainPotentialPlan.potentialPlan = self.__userPotentialPlan.potentialPlan
        self.__mainPotentialPlan.subjectList = self.__userPotentialPlan.subjectList

    def removePotentialPlan(self, potentialPlanInst):
        for subjectIndex in range(len(potentialPlanInst.subjectList)):
            # This contains the indexes to be removed for a specific subject
            indexesToBeRemovedSet = self.__toBeRemovedIndex[potentialPlanInst.subjectList[subjectIndex].courseCode]
            # This will contains the index in the potentialPlan that is to be removed later
            tempPlanIndexToBeRemoved = set()
            if indexesToBeRemovedSet:
                # Get the index to be removed
                for i in range(len(potentialPlanInst.potentialPlan)):
                    if potentialPlanInst.potentialPlan[i][subjectIndex].indexNo in indexesToBeRemovedSet:
                        tempPlanIndexToBeRemoved.add(i)

                sortedTempPlanIndexToBeRemoved = sorted(tempPlanIndexToBeRemoved, reverse=True)
                for i in sortedTempPlanIndexToBeRemoved:
                    potentialPlanInst.potentialPlan.pop(i)

    # Called everytime the selected row in the friendListWidget changes
    # Enable the viewFriendPlanBtn and deleteFriendBtn
    @pyqtSlot(int)
    def friendListWidgetRowChanged(self, currentRow):
        try:
            if currentRow > -1:
                self.viewFriendPlanBtn.setEnabled(True)
                self.deleteFriendBtn.setEnabled(True)
            else:
                self.viewFriendPlanBtn.setEnabled(False)
                self.deleteFriendBtn.setEnabled(False)
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::friendListWidgetRowChanged()\nError msg: {err}')

    # Called everytime the user clicks the viewFriendPlanBtn
    # Send signal to friendPlanner
    # Clears the selection in the friendListWidget
    @pyqtSlot()
    def viewFriendPlanBtnClicked(self):
        try:
            self.viewFriendPlan.emit(self.__friendList[self.friendListWidget.currentRow()],
                                     self.__friendPotentialPlanList[self.friendListWidget.currentRow()])
            self.friendListWidget.setCurrentRow(-1)
            self.__friendPlannerDialog.exec()
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::viewFriendPlanBtnClicked()\nError msg: {err}')

    def collateFilterIndex(self, name, tempPotentialPlan):
        try:
            for j in range(len(tempPotentialPlan.subjectList)):
                tempSet = set()
                for i in range(len(tempPotentialPlan.potentialPlan)):
                    tempSet.add(tempPotentialPlan.potentialPlan[i][j].indexNo)

                if tempPotentialPlan.subjectList[j].courseCode in self.__collatedSubjectListWithFilteredIndexList:
                    self.__subjectOccurence[tempPotentialPlan.subjectList[j].courseCode].append(name)
                    tempResult = self.__collatedSubjectListWithFilteredIndexList[tempPotentialPlan.subjectList[j].courseCode].union(tempSet)
                    self.__collatedSubjectListWithFilteredIndexList[tempPotentialPlan.subjectList[j].courseCode] = tempResult
                    tempResult = self.__collatedSubjectListWithCommonIndex[tempPotentialPlan.subjectList[j].courseCode].intersection(tempSet)
                    self.__collatedSubjectListWithCommonIndex[tempPotentialPlan.subjectList[j].courseCode] = tempResult
                else:
                    self.__subjectOccurence[tempPotentialPlan.subjectList[j].courseCode] = [name]
                    self.__collatedSubjectListWithFilteredIndexList[tempPotentialPlan.subjectList[j].courseCode] = tempSet
                    self.__collatedSubjectListWithCommonIndex[tempPotentialPlan.subjectList[j].courseCode] = tempSet
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::collateFilterIndex()\nError msg: {err}')

    def updatePlan(self):
        try:
            if self.__mainPotentialPlan.whoMadeTheChange == 'Add/Remove Subjects':
                self.setEnabled(True)

                # Reset the all the lists and dicts and ui
                self.__friendList.clear()
                self.__friendPotentialPlanList.clear()
                self.__friendPotentialPlanListCopy.clear()
                self.__collatedSubjectListWithFilteredIndexList.clear()
                self.__toBeRemovedIndex.clear()
                self.__subjectOccurence.clear()
                self.friendListWidget.clear()
                self.viewFriendPlanBtn.setEnabled(False)
                self.deleteFriendBtn.setEnabled(False)

                self.__userPotentialPlan = potentialPlanCopy.PotentialPlanCopy(self.__mainPotentialPlan)
                self.__userPotentialPlanCopy = potentialPlanCopy.PotentialPlanCopy(self.__mainPotentialPlan)
                self.collateFilterIndex('user', self.__userPotentialPlan)
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::updatePlan()\nError msg: {err}')

    def showErrorMsg(self, errorMsg):
        QMessageBox.critical(self, self.getWindowName(), errorMsg)

    def getWindowName(self):
        return 'Plan with Friends'