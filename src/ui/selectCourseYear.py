# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\selectCourseYear.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(588, 248)
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
        self.qlistCourseYear = QtWidgets.QListWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qlistCourseYear.sizePolicy().hasHeightForWidth())
        self.qlistCourseYear.setSizePolicy(sizePolicy)
        self.qlistCourseYear.setMinimumSize(QtCore.QSize(512, 384))
        self.qlistCourseYear.setObjectName("qlistCourseYear")
        self.horizontalLayout.addWidget(self.qlistCourseYear)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnBack = QtWidgets.QPushButton(Dialog)
        self.btnBack.setObjectName("btnBack")
        self.horizontalLayout_2.addWidget(self.btnBack)
        self.btnNext = QtWidgets.QPushButton(Dialog)
        self.btnNext.setObjectName("btnNext")
        self.horizontalLayout_2.addWidget(self.btnNext)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Course Year Selection"))
        self.label.setText(_translate("Dialog", "Please select a course year"))
        self.lblCourseYear.setText(_translate("Dialog", "Course Year:"))
        self.btnBack.setText(_translate("Dialog", "Back"))
        self.btnNext.setText(_translate("Dialog", "Next"))