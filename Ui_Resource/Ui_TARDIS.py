# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\zhurp 2\program\python\TARDIS\Ui_Resource\TARDIS.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1006, 653)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        Dialog.setFont(font)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(10, 0, 991, 641))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayoutWidget = QtWidgets.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 20, 981, 611))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.SourceChosser = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.SourceChosser.setMinimumSize(QtCore.QSize(110, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SourceChosser.setFont(font)
        self.SourceChosser.setStyleSheet("border-radius: 5px")
        self.SourceChosser.setEditable(False)
        self.SourceChosser.setFrame(False)
        self.SourceChosser.setObjectName("SourceChosser")
        self.SourceChosser.addItem("")
        self.SourceChosser.addItem("")
        self.gridLayout.addWidget(self.SourceChosser, 0, 3, 1, 1)
        self.SearchButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.SearchButton.setStyleSheet("background: none;\n"
"border: none")
        self.SearchButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("e:\\zhurp 2\\program\\python\\TARDIS\\Ui_Resource\\../Pic_Resource/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("e:\\zhurp 2\\program\\python\\TARDIS\\Ui_Resource\\../Pic_Resource/search_on.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.SearchButton.setIcon(icon)
        self.SearchButton.setIconSize(QtCore.QSize(35, 35))
        self.SearchButton.setObjectName("SearchButton")
        self.gridLayout.addWidget(self.SearchButton, 0, 4, 1, 1)
        self.LoadingLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.LoadingLabel.setText("")
        self.LoadingLabel.setObjectName("LoadingLabel")
        self.gridLayout.addWidget(self.LoadingLabel, 0, 5, 1, 2)
        self.WordInput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.WordInput.setEnabled(True)
        self.WordInput.setMinimumSize(QtCore.QSize(150, 30))
        self.WordInput.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.WordInput.setFont(font)
        self.WordInput.setStyleSheet("border:5px;\n"
"border-radius:15px")
        self.WordInput.setText("")
        self.WordInput.setObjectName("WordInput")
        self.gridLayout.addWidget(self.WordInput, 0, 2, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.gridLayoutWidget)
        self.scrollArea.setStyleSheet("border: none;")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 979, 553))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setStyleSheet("border:none")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 971, 643))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.ResultGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.ResultGridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.ResultGridLayout.setContentsMargins(10, 0, 0, 600)
        self.ResultGridLayout.setObjectName("ResultGridLayout")
        spacerItem = QtWidgets.QSpacerItem(250, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.ResultGridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ResultGridLayout.addItem(spacerItem1, 0, 1, 1, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 8)
        spacerItem2 = QtWidgets.QSpacerItem(280, 50, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 2)
        self.CloseButton = QtWidgets.QPushButton(self.frame)
        self.CloseButton.setGeometry(QtCore.QRect(960, 0, 15, 15))
        self.CloseButton.setMinimumSize(QtCore.QSize(10, 10))
        self.CloseButton.setStyleSheet("border:none;\n"
"border-radius: 7px;\n"
"background-color: rgb(255, 47, 102);")
        self.CloseButton.setText("")
        self.CloseButton.setObjectName("CloseButton")
        self.MinimizeButton = QtWidgets.QPushButton(self.frame)
        self.MinimizeButton.setGeometry(QtCore.QRect(940, 0, 15, 15))
        self.MinimizeButton.setMinimumSize(QtCore.QSize(10, 10))
        self.MinimizeButton.setStyleSheet("border:none;\n"
"border-radius: 7px;\n"
"background-color: rgb(116, 255, 139);")
        self.MinimizeButton.setText("")
        self.MinimizeButton.setObjectName("MinimizeButton")

        self.retranslateUi(Dialog)
        self.SourceChosser.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "TARDIS"))
        self.SourceChosser.setCurrentText(_translate("Dialog", "dictionary.com"))
        self.SourceChosser.setItemText(0, _translate("Dialog", "dictionary.com"))
        self.SourceChosser.setItemText(1, _translate("Dialog", "Merriam-Webster"))
        self.WordInput.setPlaceholderText(_translate("Dialog", "input word"))
