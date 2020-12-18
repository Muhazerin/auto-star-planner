# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\filterSubjectsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_filterSubjectsDialog(object):
    def setupUi(self, filterSubjectsDialog):
        filterSubjectsDialog.setObjectName("filterSubjectsDialog")
        filterSubjectsDialog.setEnabled(False)
        filterSubjectsDialog.resize(187, 55)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        filterSubjectsDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/planner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        filterSubjectsDialog.setWindowIcon(icon)
        self.dialogFormLayout = QtWidgets.QFormLayout(filterSubjectsDialog)
        self.dialogFormLayout.setObjectName("dialogFormLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clearFilterBtn = QtWidgets.QPushButton(filterSubjectsDialog)
        self.clearFilterBtn.setEnabled(False)
        self.clearFilterBtn.setObjectName("clearFilterBtn")
        self.horizontalLayout.addWidget(self.clearFilterBtn)
        self.applyFilterBtn = QtWidgets.QPushButton(filterSubjectsDialog)
        self.applyFilterBtn.setObjectName("applyFilterBtn")
        self.horizontalLayout.addWidget(self.applyFilterBtn)
        self.dialogFormLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.dialogFormLayout.setItem(1, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.filterTypeLbl = QtWidgets.QLabel(filterSubjectsDialog)
        self.filterTypeLbl.setObjectName("filterTypeLbl")
        self.dialogFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.filterTypeLbl)
        self.filterTypeComboBox = QtWidgets.QComboBox(filterSubjectsDialog)
        self.filterTypeComboBox.setObjectName("filterTypeComboBox")
        self.filterTypeComboBox.addItem("")
        self.filterTypeComboBox.addItem("")
        self.dialogFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.filterTypeComboBox)

        self.retranslateUi(filterSubjectsDialog)
        QtCore.QMetaObject.connectSlotsByName(filterSubjectsDialog)

    def retranslateUi(self, filterSubjectsDialog):
        _translate = QtCore.QCoreApplication.translate
        filterSubjectsDialog.setWindowTitle(_translate("filterSubjectsDialog", "Filter Subjects"))
        self.clearFilterBtn.setText(_translate("filterSubjectsDialog", "Clear Filter"))
        self.applyFilterBtn.setText(_translate("filterSubjectsDialog", "Apply Filter"))
        self.filterTypeLbl.setText(_translate("filterSubjectsDialog", "Filter Type: "))
        self.filterTypeComboBox.setItemText(0, _translate("filterSubjectsDialog", "Blacklist"))
        self.filterTypeComboBox.setItemText(1, _translate("filterSubjectsDialog", "Whitelist"))
import ui.res.resources_rc
