import sys
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from Ui_Resource.Ui_TARDIS import *
from functions.LookForWord import *
import time



StyleSheetDict = {
    'public':'border-radius: 12px;\n font: 25 15pt "Segoe UI";\n color: white;\n',
    'n.': 'background-color: #c93756;\n',
    'c.n.': 'background-color: #FF6666;\n',
    'u.n.': 'background-color: #CC3333;\n',
    'v.t.': 'background-color: #057748;\n',
    'v.i.': 'background-color: #00e500;\n',
    'v.': 'background-color: #0aa344;\n',
    'adj.':'background-color: #5cb3cc;\n',
    'adv.':'background-color: #134857;\n',
    'pron.':'background-color: #ec4e8a;\n',
    'prep.':'background-color: #a35c8f;\n',
    'conj.': 'background-color: #f04a3a;\n',
    'interj.':'background-color: #954416;\n',
    'art.':'background-color: #0f1423;\n',
    'abbr.':'background-color: #21373d\n',
    'phrase':'background-color: #19363B\n',
    'special':'color: #867e76;\n font:15pt "Segoe UI";\n'
}





class SearchWordWorker(QtCore.QObject) :
    '''
    搜索单词的类
    '''
    # 搜索完成的信号
    SearchDone = QtCore.pyqtSignal(list)
    SearchFail = QtCore.pyqtSignal()
    def SearchWord(self,word,source) :
        NewSearcher = WordSearcher(word,source)
        try :
            SearchResult = NewSearcher.SearchWord()
            self.SearchDone.emit(SearchResult)
        except NoSuchWord:
            self.SearchFail.emit()




class T_Ui(QtWidgets.QWidget, Ui_Dialog):
    StartSearch = QtCore.pyqtSignal(str,str)


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

        self.MinimizeButton.clicked.connect(self.showMinimized)
        self.CloseButton.clicked.connect(self.close)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)


    def CreateWordLabel(self,content,row,column=0) :
        self.WordLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.WordLabel.setText(content)
        self.WordLabel.setStyleSheet('font: 30pt "Times New Roman";')
        self.ResultGridLayout.addWidget(self.WordLabel, row,column,1,1)
    def CreatePosLabel(self,content,row) :
        self.PosLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.PosLabel.setText(content)
        self.PosLabel.setMaximumSize(70,24)
        self.PosLabel.setAlignment(Qt.Qt.AlignCenter)
        self.PosLabel.setStyleSheet(StyleSheetDict['public']+StyleSheetDict[content])
        self.ResultGridLayout.addWidget(self.PosLabel, row,0,1,1)
    def CreateDefLabel(self,content,row,RowSpan) :
        self.DefLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.DefLabel.setMinimumSize(650,20)
        self.DefLabel.setAlignment(Qt.Qt.AlignTop)
        self.DefLabel.setText(content)
        self.DefLabel.setStyleSheet('font: 15pt "Segoe UI";\n')
        self.DefLabel.setWordWrap(True)
        self.ResultGridLayout.addWidget(self.DefLabel, row,1,RowSpan,1)
    def CreateSpecialLabel(self,content,row) :
        self.SpecialLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.SpecialLabel.setText(content)
        self.SpecialLabel.setStyleSheet(StyleSheetDict['special'])
        self.SpecialLabel.setWordWrap(True)
        self.ResultGridLayout.addWidget(self.SpecialLabel, row,0,1,1)
    def CreateSplitLine(self,row):
        self.line = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line.setStyleSheet("background-color: black;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setMaximumSize(900,1)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.ResultGridLayout.addWidget(self.line, row,0,1,2)
    def CreateWordExampleLabel(self,content,row):
        self.ExampleLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ExampleLabel.setMinimumSize(900,20)
        self.ExampleLabel.setText(content)
        self.ExampleLabel.setStyleSheet('font: 15pt "Segoe UI";\n')
        self.ExampleLabel.setWordWrap(True)
        self.ResultGridLayout.addWidget(self.ExampleLabel, row,0,1,2)
    def ClearLayout(self) :
        try :
            for i in reversed(range(2,self.ResultGridLayout.count())) :
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
            self.CreateWordLabel(word.spelling,CountRow)
            if word.phonetic:
                self.CreateWordLabel(word.phonetic,CountRow,column=1)
            CountRow += 1

            for j in range(len(word.definitions)):
                def_ = word.definitions[j] 
                RightCountRow = CountRow
                if def_.PoS :
                    self.CreatePosLabel(def_.PoS,CountRow) 
                    CountRow += 1  
                for k in range(len(def_.special)) :
                    self.CreateSpecialLabel(def_.special[k],CountRow)
                    CountRow += 1
                if def_.phrase:
                    self.CreateSpecialLabel(def_.phrase,CountRow)
                    CountRow += 1    
                if def_.inflect:
                    self.CreateSpecialLabel('-'.join(def_.inflect),CountRow)
                    CountRow += 1
                self.CreateDefLabel(def_.content,RightCountRow,1) 
                RightCountRow += 1
                if def_.example:
                    self.CreateDefLabel('e.g.'+'\n'.join(def_.example),RightCountRow,1)
                    RightCountRow += 1
                CountRow = max(CountRow,RightCountRow)
                self.CreateSplitLine(CountRow)
                CountRow += 1
         
        ExampleList = ResultList[1]
        self.CreateWordLabel('Examples:',CountRow)
        CountRow += 1
        for i in range(len(ExampleList)) :
            self.CreateWordExampleLabel(ExampleList[i],CountRow)
            CountRow += 1

        self.scrollAreaWidgetContents.setLayout(self.ResultGridLayout)

        
    def SearchFail(self) :
        self.LoadingLabel.setText('No Result Found')
    def load(self) :
        self.StartSearch.emit(self.WordInput.text(),self.SourceChosser.currentText())
        self.LoadingLabel.setText('Loading...')



'''

    def mouseMoveEvent(self, e: Qt.QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: Qt.QMouseEvent):
        if e.button() == Qt.Qt.LeftButton:
            self._isTracking = True
            self._startPos = Qt.QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: Qt.QMouseEvent):
        if e.button() == Qt.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None
'''
