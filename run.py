import sys
from PyQt5 import QtWidgets
from Ui_TARDIS import *
from LookForWord import *
import time

class FindWord(QtCore.QObject) :
    result_ready = QtCore.pyqtSignal(str)
    def SearchWord(self,word) :
        words = ParWordDic_com(word)
        text = ''
        for defs in words :
            for i in defs :
                text += i.get_def()
        self.result_ready.emit(text)
class T_Ui(QtWidgets.QWidget, Ui_Dialog):
    StartFind = QtCore.pyqtSignal(str)
    def __init__(self):
        super(T_Ui, self).__init__()
        self.setupUi(self)
        
        thread = QtCore.QThread(self)
        thread.start()
        self.finder = FindWord()
        self.finder.moveToThread(thread)
        self.finder.result_ready.connect(self.SearchComplete)

        self.pushButton.clicked.connect(self.load)
        self.StartFind.connect(self.finder.SearchWord)
    def SearchComplete(self,text) :
        self.LoadingLabel.setText('')
        self.label.setText(text)
    def load(self) :
        self.StartFind.emit(self.lineEdit.text())
        self.LoadingLabel.setText('加载中...')



if __name__ == '__main__' :
    app = QtWidgets.QApplication(sys.argv)
    window = T_Ui()
    window.show()
    sys.exit(app.exec_())


