import sys
from PyQt5 import QtWidgets, QtCore
from Ui_TARDIS import *
from LookForWord import *
import time

class SearchWordWorker(QtCore.QObject) :
    '''
    搜索单词的类
    '''
    # 搜索完成的信号
    SearchDone = QtCore.pyqtSignal(list)
    def SearchWord(self,word) :
        NewSearcher = WordSearcher('dictionary.com')
        SearchResult = NewSearcher.search(word)
        NewParser = HTMLParser('dictionary.com')
        WordList = NewParser.parse(SearchResult)
        self.SearchDone.emit(WordList)
class T_Ui(QtWidgets.QWidget, Ui_Dialog):
    StartSearch = QtCore.pyqtSignal(str)
    def __init__(self):
        #父类ui初始化
        super(T_Ui, self).__init__()
        self.setupUi(self)
        #多线程初始化
        thread = QtCore.QThread(self)
        thread.start()
        self.worker = SearchWordWorker()
        self.worker.moveToThread(thread)
        #完成信号连接
        self.worker.SearchDone.connect(self.SearchComplete)
        #多线程开始信号连接
        self.StartSearch.connect(self.worker.SearchWord)
        #按钮信号连接
        self.SearchButton.clicked.connect(self.load)
    def SearchComplete(self,WordList) :
        self.LoadingLabel.setText('')
        self.ResultText.setText(''.join([i.get_def() for i in WordList[0]]))
    def load(self) :
        self.StartSearch.emit(self.WordInput.text())
        self.LoadingLabel.setText('Loading...')



if __name__ == '__main__' :
    app = QtWidgets.QApplication(sys.argv)
    window = T_Ui()
    window.show()
    sys.exit(app.exec_())


