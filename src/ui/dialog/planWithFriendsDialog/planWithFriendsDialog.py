# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\planWithFriendsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_planWithFriendsDialog(object):
    def setupUi(self, planWithFriendsDialog):
        planWithFriendsDialog.setObjectName("planWithFriendsDialog")
        planWithFriendsDialog.setEnabled(False)
        planWithFriendsDialog.resize(598, 229)
        planWithFriendsDialog.setMinimumSize(QtCore.QSize(598, 229))
        planWithFriendsDialog.setMaximumSize(QtCore.QSize(598, 229))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/planner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        planWithFriendsDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(planWithFriendsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.friendListWidget = QtWidgets.QListWidget(planWithFriendsDialog)
        self.friendListWidget.setObjectName("friendListWidget")
        self.horizontalLayout_2.addWidget(self.friendListWidget)
        self.viewFriendPlanBtn = QtWidgets.QPushButton(planWithFriendsDialog)
        self.viewFriendPlanBtn.setEnabled(False)
        self.viewFriendPlanBtn.setObjectName("viewFriendPlanBtn")
        self.horizontalLayout_2.addWidget(self.viewFriendPlanBtn)
        self.deleteFriendBtn = QtWidgets.QPushButton(planWithFriendsDialog)
        self.deleteFriendBtn.setEnabled(False)
        self.deleteFriendBtn.setObjectName("deleteFriendBtn")
        self.horizontalLayout_2.addWidget(self.deleteFriendBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.addFriendBtn = QtWidgets.QPushButton(planWithFriendsDialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.addFriendBtn.setFont(font)
        self.addFriendBtn.setObjectName("addFriendBtn")
        self.verticalLayout.addWidget(self.addFriendBtn)

        self.retranslateUi(planWithFriendsDialog)
        QtCore.QMetaObject.connectSlotsByName(planWithFriendsDialog)

    def retranslateUi(self, planWithFriendsDialog):
        _translate = QtCore.QCoreApplication.translate
        planWithFriendsDialog.setWindowTitle(_translate("planWithFriendsDialog", "Plan with Friends"))
        self.viewFriendPlanBtn.setText(_translate("planWithFriendsDialog", "View Friend\'s Plan"))
        self.deleteFriendBtn.setText(_translate("planWithFriendsDialog", "Delete Friend"))
        self.addFriendBtn.setText(_translate("planWithFriendsDialog", "Add Friend"))
import ui.res.resources_rc
