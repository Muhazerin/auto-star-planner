from ui.dialog.planWithFriendsDialog import addRemoveSubjectsDialog

from PyQt5.QtWidgets import (QDialog, QMessageBox)

class Dialog(QDialog, addRemoveSubjectsDialog.Ui_AddRemoveSubject):
    def __init__(self):
        try:
            super(Dialog, self).__init__()
            self.setupUi(self)
        except Exception as err:
            self.showErrorMsg(err)

    def showErrorMsg(self, errorMsg):
        QMessageBox.critical(self, self.getWindowName(), errorMsg)

    def getWindowName(self):
        return 'Add/Remove Subjects (Plan with Friends)'