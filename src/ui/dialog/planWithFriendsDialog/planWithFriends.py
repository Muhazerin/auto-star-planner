from ui.dialog.planWithFriendsDialog import (planWithFriendsDialog, addRemoveSubjects, friendPlanner)
from ui.dialog.planWithFriendsDialog.model import (potentialPlanCopy, friends)
from model import potentialPlan

from PyQt5.QtWidgets import (QDialog, QMessageBox)
from PyQt5.QtCore import (pyqtSlot, pyqtSignal)

# TODO: Error handling

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
            # Each subject contains all the available indexes
            self.__collatedSubjectListWithFilteredIndexDict = {}    # "course code": "set of indexes"
            # Each subject contains the common indexes among everyone
            self.__collatedSubjectListWithCommonIndex = {}
            # Each subject contains the indexes to be removed
            self.__toBeRemovedIndex = {}

            # initialize friendList and relevant dialogs
            self.__friendList = []
            self.__addRemoveSubjectsDialog = addRemoveSubjects.Dialog()
            self.__friendPlannerDialog = friendPlanner.Dialog()

            # Setup the ui and connect the addFriendBtn and newFriendSignal signal and slot
            self.setupUi(self)
            self.addFriendBtn.clicked.connect(self.addFriendBtnClicked)
            self.__addRemoveSubjectsDialog.newFriendSignal.connect(self.plan)

            # Connect the signals and slots for various ui
            self.friendListWidget.currentRowChanged.connect(self.friendListWidgetRowChanged)
            self.viewFriendPlanBtn.clicked.connect(self.viewFriendPlanBtnClicked)
            self.viewFriendPlan.connect(self.__friendPlannerDialog.viewFriendPlanEmitted)
            self.deleteFriendBtn.clicked.connect(self.deleteFriendBtnClicked)
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
    # 1: It adds new friend to friendList and the potentialPlanInst to friendPotentialPlanList and friendPotentialPlanListCopy
    # 2: Collate the filtered index and common index
    # 3: Fill the toBeRemoved dict based on 2
    # 4: Filter user's and friends plan based on 4
    # 5: Reflect the changes for user to mainWindow
    @pyqtSlot(friends.Friend, potentialPlan.PotentialPlan)
    def plan(self, newFriend, friendPotentialPlan):
        try:
            # Step 1
            self.__friendList.append(newFriend)
            self.__friendPotentialPlanList.append(potentialPlanCopy.PotentialPlanCopy(friendPotentialPlan))
            self.__friendPotentialPlanListCopy.append(potentialPlanCopy.PotentialPlanCopy(friendPotentialPlan))
            self.friendListWidget.addItem(newFriend.name)

            # Step 2
            self.collateFilterIndex(self.__friendList[-1].name, self.__friendPotentialPlanList[-1])

            # Step 3
            for key in self.__collatedSubjectListWithFilteredIndexDict:
                self.__toBeRemovedIndex[key] = self.__collatedSubjectListWithFilteredIndexDict[key].symmetric_difference(self.__collatedSubjectListWithCommonIndex[key])

            # Step 4
            self.removePotentialPlan(self.__userPotentialPlan)
            for tempFriendPotentialPlan in self.__friendPotentialPlanList:
                self.removePotentialPlan(tempFriendPotentialPlan)

            # Step 5
            self.reflectTheChanges()
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::plan()\nError msg: {err}')

    # Based on the toBeRemovedIndex, get the index to be removed from potentialPlan
    # After that, pop the potentialPlan
    def removePotentialPlan(self, potentialPlanInst):
        try:
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

                    # Change the set into sorted list in descending order
                    sortedTempPlanIndexToBeRemoved = sorted(tempPlanIndexToBeRemoved, reverse=True)

                    # Pop the list
                    for i in sortedTempPlanIndexToBeRemoved:
                        potentialPlanInst.potentialPlan.pop(i)
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::removePotentialPlan()\nError msg: {err}')

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

    # Called everytime the user clicks the deleteFriendBtn
    @pyqtSlot()
    def deleteFriendBtnClicked(self):
        try:
            # Pop the item from friendList, friendPotentialPlanList, and friendPotentialPlanListCopy
            self.__friendList.pop(self.friendListWidget.currentRow())
            self.__friendPotentialPlanList.pop(self.friendListWidget.currentRow())
            self.__friendPotentialPlanListCopy.pop(self.friendListWidget.currentRow())

            # Remove the friend from the friendListWidget adn clear the selection
            self.friendListWidget.takeItem(self.friendListWidget.currentRow())
            self.friendListWidget.setCurrentRow(-1)

            # Reset the collatedDicts and toBeRemovedIndex
            self.__collatedSubjectListWithFilteredIndexDict.clear()
            self.__collatedSubjectListWithCommonIndex.clear()
            self.__toBeRemovedIndex.clear()

            # Reset userPotentialPlan and collatedDicts
            self.__userPotentialPlan = potentialPlanCopy.PotentialPlanCopy(self.__userPotentialPlanCopy)
            self.collateFilterIndex('user', self.__userPotentialPlan)

            # Based on the friendList, do Step 2, 3, and 4
            if self.__friendList:
                # Redo the collateFilterIndex for every friend
                for i in range(len(self.__friendPotentialPlanList)):
                    self.__friendPotentialPlanList[i] = potentialPlanCopy.PotentialPlanCopy(self.__friendPotentialPlanListCopy[i])
                    self.collateFilterIndex(self.__friendList[i].name, self.__friendPotentialPlanList[i])

                # Step 3 in the plan()
                for key in self.__collatedSubjectListWithFilteredIndexDict:
                    self.__toBeRemovedIndex[key] = self.__collatedSubjectListWithFilteredIndexDict[key].symmetric_difference(self.__collatedSubjectListWithCommonIndex[key])

                # Step 4
                self.removePotentialPlan(self.__userPotentialPlan)
                for tempFriendPotentialPlan in self.__friendPotentialPlanList:
                    self.removePotentialPlan(tempFriendPotentialPlan)

            # Reflect the changes in userPotentialPlan to mainWindow
            self.reflectTheChanges()
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::deleteFriendBtnClicked()\nError msg: {err}')

    # Reflect the changes to mainWindow through the observer pattern
    def reflectTheChanges(self):
        try:
            self.__mainPotentialPlan.whoMadeTheChange = self.getWindowName()
            self.__mainPotentialPlan.potentialPlan = self.__userPotentialPlan.potentialPlan
            self.__mainPotentialPlan.subjectList = self.__userPotentialPlan.subjectList
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::reflectTheChanges()\nError msg: {err}')

    # Collate the FilterIndex and CommonIndex and add it to their respective dicts
    def collateFilterIndex(self, name, tempPotentialPlan):
        try:
            # Loop through the subjectList
            # j = subjectIndex
            for j in range(len(tempPotentialPlan.subjectList)):
                # Create a set var: tempSet
                tempSet = set()
                # Loop through the subject in potentialPlan and add the indexNo to tempSet
                for i in range(len(tempPotentialPlan.potentialPlan)):
                    tempSet.add(tempPotentialPlan.potentialPlan[i][j].indexNo)

                # Depending whether the subject exist in the collatedDict, make changes or create a key for the dict
                if tempPotentialPlan.subjectList[j].courseCode in self.__collatedSubjectListWithFilteredIndexDict:
                    tempResult = self.__collatedSubjectListWithFilteredIndexDict[tempPotentialPlan.subjectList[j].courseCode].union(tempSet)
                    self.__collatedSubjectListWithFilteredIndexDict[tempPotentialPlan.subjectList[j].courseCode] = tempResult
                    tempResult = self.__collatedSubjectListWithCommonIndex[tempPotentialPlan.subjectList[j].courseCode].intersection(tempSet)
                    self.__collatedSubjectListWithCommonIndex[tempPotentialPlan.subjectList[j].courseCode] = tempResult
                else:
                    self.__collatedSubjectListWithFilteredIndexDict[tempPotentialPlan.subjectList[j].courseCode] = tempSet
                    self.__collatedSubjectListWithCommonIndex[tempPotentialPlan.subjectList[j].courseCode] = tempSet
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::collateFilterIndex()\nError msg: {err}')

    # Called everytime there's changes to mainPotentialPlan
    def updatePlan(self):
        try:
            if self.__mainPotentialPlan.whoMadeTheChange == 'Add/Remove Subjects':
                self.setEnabled(True)

                # Reset the all the lists and dicts and ui
                self.__friendList.clear()
                self.__friendPotentialPlanList.clear()
                self.__friendPotentialPlanListCopy.clear()
                self.__collatedSubjectListWithFilteredIndexDict.clear()
                self.__collatedSubjectListWithCommonIndex.clear()
                self.__toBeRemovedIndex.clear()
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