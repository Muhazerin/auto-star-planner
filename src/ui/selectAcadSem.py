# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\selectAcadSem.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(175, 76)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.hlAcadSem = QtWidgets.QHBoxLayout()
        self.hlAcadSem.setObjectName("hlAcadSem")
        self.lblAcadSem = QtWidgets.QLabel(Dialog)
        self.lblAcadSem.setObjectName("lblAcadSem")
        self.hlAcadSem.addWidget(self.lblAcadSem)
        self.comboBoxAcadSem = QtWidgets.QComboBox(Dialog)
        self.comboBoxAcadSem.setObjectName("comboBoxAcadSem")
        self.hlAcadSem.addWidget(self.comboBoxAcadSem)
        self.verticalLayout.addLayout(self.hlAcadSem)
        self.hlBtn = QtWidgets.QHBoxLayout()
        self.hlBtn.setObjectName("hlBtn")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlBtn.addItem(spacerItem)
        self.btnNext = QtWidgets.QPushButton(Dialog)
        self.btnNext.setObjectName("btnNext")
        self.hlBtn.addWidget(self.btnNext)
        self.verticalLayout.addLayout(self.hlBtn)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Academic Semester Selection"))
        self.label_2.setText(_translate("Dialog", "Please select an academic semester"))
        self.lblAcadSem.setText(_translate("Dialog", "Academic Semester:"))
        self.btnNext.setText(_translate("Dialog", "Next"))
