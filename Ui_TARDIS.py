# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\zhurp 2\program\python\TARDIS\TARDIS.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(554, 508)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        Dialog.setFont(font)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(40, 0, 511, 511))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayoutWidget = QtWidgets.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 461, 461))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.SearchButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.SearchButton.setObjectName("SearchButton")
        self.gridLayout.addWidget(self.SearchButton, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(180, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.WordInput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.WordInput.setMinimumSize(QtCore.QSize(150, 0))
        self.WordInput.setText("")
        self.WordInput.setObjectName("WordInput")
        self.gridLayout.addWidget(self.WordInput, 0, 0, 1, 1)
        self.LoadingLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.LoadingLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.LoadingLabel.setLineWidth(1)
        self.LoadingLabel.setText("")
        self.LoadingLabel.setObjectName("LoadingLabel")
        self.gridLayout.addWidget(self.LoadingLabel, 0, 2, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.gridLayoutWidget)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 457, 428))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 441, 431))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.ResultGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.ResultGridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.ResultGridLayout.setContentsMargins(0, 0, 0, 0)
        self.ResultGridLayout.setObjectName("ResultGridLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "TARDIS"))
        self.SearchButton.setText(_translate("Dialog", "Search"))
        self.WordInput.setPlaceholderText(_translate("Dialog", "input word"))
