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
        Dialog.resize(685, 444)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        Dialog.setFont(font)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(40, 0, 611, 511))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayoutWidget = QtWidgets.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 20, 601, 401))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.gridLayoutWidget)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 597, 368))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 591, 621))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.ResultGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.ResultGridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.ResultGridLayout.setContentsMargins(0, 0, 0, 600)
        self.ResultGridLayout.setObjectName("ResultGridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultGridLayout.addItem(spacerItem, 0, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultGridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultGridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultGridLayout.addItem(spacerItem3, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultGridLayout.addItem(spacerItem4, 0, 5, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultGridLayout.addItem(spacerItem5, 0, 6, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultGridLayout.addItem(spacerItem6, 0, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 5)
        self.SearchButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.SearchButton.setObjectName("SearchButton")
        self.gridLayout.addWidget(self.SearchButton, 0, 4, 1, 1)
        self.WordInput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.WordInput.setMinimumSize(QtCore.QSize(100, 0))
        self.WordInput.setText("")
        self.WordInput.setObjectName("WordInput")
        self.gridLayout.addWidget(self.WordInput, 0, 0, 1, 1)
        self.LoadingLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.LoadingLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.LoadingLabel.setLineWidth(1)
        self.LoadingLabel.setText("")
        self.LoadingLabel.setObjectName("LoadingLabel")
        self.gridLayout.addWidget(self.LoadingLabel, 0, 3, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(180, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 0, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "TARDIS"))
        self.SearchButton.setText(_translate("Dialog", "Search"))
        self.WordInput.setPlaceholderText(_translate("Dialog", "input word"))
