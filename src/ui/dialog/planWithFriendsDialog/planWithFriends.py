from ui.dialog.planWithFriendsDialog import (planWithFriendsDialog, addRemoveSubjects)
from ui.dialog.planWithFriendsDialog.model import (potentialPlanCopy, friends)

from PyQt5.QtWidgets import (QDialog, QMessageBox)

class Dialog(QDialog, planWithFriendsDialog.Ui_planWithFriendsDialog):
    def __init__(self, mainPotentialPlan):
        try:
            super(Dialog, self).__init__()
            # This is to reflect the changes to mainwindow
            self.__mainPotentialPlan = mainPotentialPlan
            # This is to hold the user's potential plan
            self.__mainPotentialPlanCopy = None

            self.__friendList = []
            self.__addRemoveSubjects = addRemoveSubjects.Dialog()

            self.setupUi(self)
            self.addFriendBtn.clicked.connect(self.addFriendBtnClicked)
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::__init__():\nError msg: {err}')

    def addFriendBtnClicked(self):
        self.__addRemoveSubjects.exec()

    def updatePlan(self):
        try:
            if self.__mainPotentialPlan.whoMadeTheChange == 'Add/Remove Subjects':
                self.setEnabled(True)
                self.__mainPotentialPlanCopy = potentialPlanCopy.PotentialPlanCopy(self.__mainPotentialPlan)
        except Exception as err:
            self.showErrorMsg(f'planWithFriends::updatePlan()\nError msg: {err}')

    def showErrorMsg(self, errorMsg):
        QMessageBox.critical(self, self.getWindowName(), errorMsg)

    def getWindowName(self):
        return 'Plan with Friends'