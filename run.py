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
            ResultList = NewParser.parse(SearchResult)
            self.SearchDone.emit(ResultList)
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


    def CreateResultLabel(self,content,FontSize:int,position:tuple) :
        self.ResultLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ResultLabel.setMinimumSize(QtCore.QSize(40, 30))
        self.ResultLabel.setFont(QtGui.QFont("Segoe UI",FontSize))
        self.ResultLabel.setText(content)
        self.ResultLabel.setWordWrap(True)
        self.ResultGridLayout.addWidget(self.ResultLabel, *position)
    def ClearLayout(self) :
        try :
            for i in reversed(range(6,self.ResultGridLayout.count())) :
                self.ResultGridLayout.itemAt(i).widget().deleteLater()
        except :
            pass

    def SearchComplete(self,ResultList) :
        '''
        结果显示
        '''
        self.LoadingLabel.setText('')
        self.ClearLayout()
        
        WordList = ResultList[0]
        CountRow = 0
        for i in range(len(WordList)) :
            word = WordList[i]
            self.CreateResultLabel(word.spelling,20,(CountRow, 0, 1, 1))

            if word.phonetic :
                self.CreateResultLabel(word.phonetic,17,(CountRow, 1, 1, 1))
            CountRow += 1    
            
            for j in range(len(word.definitions)) :
                CountColumn = 1
                def_ = word.definitions[j]
                self.CreateResultLabel(def_.PoS,15,(CountRow, 0, 1, 1))

                for k in range(len(def_.special)) :
                    self.CreateResultLabel(def_.special[k],15,(CountRow, CountColumn, 1, 1))
                    CountColumn += 1
                CountRow += 1

                self.CreateResultLabel(def_.content,12,(CountRow, 0, 1, 7))
                CountRow += 1

                if def_.example :
                    self.CreateResultLabel('e.g.'+' '*2+def_.example,12,(CountRow, 0, 1, 6))
                CountRow += 1

        ExampleList = ResultList[1]
        self.CreateResultLabel('Examples:',15,(CountRow, 0, 1, 1))
        CountRow += 1
        for i in range(len(ExampleList)) :
            self.CreateResultLabel(ExampleList[i],12,(CountRow, 0, 1, 6))
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


