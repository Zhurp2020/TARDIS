from MainProgram import *

if __name__ == '__main__' :
    app = QtWidgets.QApplication(sys.argv)
    window = T_Ui()
    window.show()
    sys.exit(app.exec_())