import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from Ui_TARDIS import *
from LookForWord import *
import time

class SearchWordWorker(QtCore.QObject) :
    '''
    搜索单词的类
    '''
    # 搜索完成的信号
    SearchDone = QtCore.pyqtSignal(list)
    SearchFail = QtCore.pyqtSignal()
    def SearchWord(self,word) :
        NewSearcher = WordSearcher('dictionary.com')
        SearchResult = NewSearcher.search(word)
        NewParser = HTMLParser('dictionary.com')
        try :
            WordList = NewParser.parse(SearchResult)
            self.SearchDone.emit(WordList)
        except :
            self.SearchFail.emit()
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
        self.worker.SearchFail.connect(self.SearchFail)
        #多线程开始信号连接
        self.StartSearch.connect(self.worker.SearchWord)
        #按钮信号连接
        self.SearchButton.clicked.connect(self.load)

    def SearchComplete(self,WordList) :
        '''
        结果显示
        '''
        self.LoadingLabel.setText('')
        
        for i in reversed(range(self.ResultGridLayout.count())) :
            self.ResultGridLayout.itemAt(i).widget().deleteLater()

        CountRow = 0
        for i in range(len(WordList)) :
            word = WordList[i]
            self.ResultLabel = QtWidgets.QLabel(self.gridLayoutWidget)
            self.ResultLabel.setMinimumSize(QtCore.QSize(200, 30))
            self.ResultLabel.setFont(QtGui.QFont("Segoe UI",15))
            self.ResultLabel.setText(word.spelling)
            self.ResultGridLayout.addWidget(self.ResultLabel, CountRow, 0, 1, 1)
            if word.phonetic :
                self.ResultLabel = QtWidgets.QLabel(self.gridLayoutWidget)
                self.ResultLabel.setMinimumSize(QtCore.QSize(200, 30))
                self.ResultLabel.setFont(QtGui.QFont("Segoe UI",15))
                self.ResultLabel.setText(word.phonetic)
                self.ResultGridLayout.addWidget(self.ResultLabel, CountRow, 1, 1, 1)
            CountRow += 1    
            
            for j in range(len(word.definitions)) :
                def_ = word.definitions[j]
                self.ResultLabel = QtWidgets.QLabel(self.gridLayoutWidget)
                self.ResultLabel.setMinimumSize(QtCore.QSize(200, 30))
                self.ResultLabel.setWordWrap(True)
                self.ResultLabel.setFont(QtGui.QFont('Segoe UI',9))
                self.ResultLabel.setText(def_.get_def())
                self.ResultGridLayout.addWidget(self.ResultLabel, CountRow, 0, 1, 2)
                CountRow += 1
        
        self.scrollAreaWidgetContents.setLayout(self.ResultGridLayout)

    def SearchFail(self) :
        self.LoadingLabel.setText('No Result Found')
    def load(self) :
        self.StartSearch.emit(self.WordInput.text())
        self.LoadingLabel.setText('Loading...')




if __name__ == '__main__' :
    app = QtWidgets.QApplication(sys.argv)
    window = T_Ui()
    window.show()
    sys.exit(app.exec_())


