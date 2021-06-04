# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\selectModules.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1108, 483)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblCourseYear = QtWidgets.QLabel(Dialog)
        self.lblCourseYear.setObjectName("lblCourseYear")
        self.horizontalLayout.addWidget(self.lblCourseYear)
        self.comboBoxCourseYear = QtWidgets.QComboBox(Dialog)
        self.comboBoxCourseYear.setObjectName("comboBoxCourseYear")
        self.horizontalLayout.addWidget(self.comboBoxCourseYear)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2)
        self.qListModuleList = QtWidgets.QListWidget(Dialog)
        self.qListModuleList.setMinimumSize(QtCore.QSize(512, 384))
        self.qListModuleList.setObjectName("qListModuleList")
        self.verticalLayout_6.addWidget(self.qListModuleList)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.btnAdd = QtWidgets.QPushButton(Dialog)
        self.btnAdd.setObjectName("btnAdd")
        self.verticalLayout_5.addWidget(self.btnAdd)
        self.btnRemove = QtWidgets.QPushButton(Dialog)
        self.btnRemove.setObjectName("btnRemove")
        self.verticalLayout_5.addWidget(self.btnRemove)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_7.addWidget(self.label_3)
        self.qListSelectedModules = QtWidgets.QListWidget(Dialog)
        self.qListSelectedModules.setMinimumSize(QtCore.QSize(512, 384))
        self.qListSelectedModules.setObjectName("qListSelectedModules")
        self.verticalLayout_7.addWidget(self.qListSelectedModules)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnBack = QtWidgets.QPushButton(Dialog)
        self.btnBack.setObjectName("btnBack")
        self.horizontalLayout_2.addWidget(self.btnBack)
        self.btnSave = QtWidgets.QPushButton(Dialog)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_2.addWidget(self.btnSave)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Module Selection"))
        self.label.setText(_translate("Dialog", "Please select your modules"))
        self.lblCourseYear.setText(_translate("Dialog", "Course Year:"))
        self.label_2.setText(_translate("Dialog", "Module List"))
        self.btnAdd.setText(_translate("Dialog", "Add"))
        self.btnRemove.setText(_translate("Dialog", "Remove"))
        self.label_3.setText(_translate("Dialog", "Selected Modules"))
        self.btnBack.setText(_translate("Dialog", "Back"))
        self.btnSave.setText(_translate("Dialog", "Save"))
