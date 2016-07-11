__author__ = 'linzhang'

# -*- coding: UTF8 -*-

import sys

from PyQt4 import QtGui

from Test.parent import Ui_MainWindow
from Test.child import Ui_Dialog


class MainClass(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainClass, self).__init__(parent)
        self.Ui = Ui_MainWindow()
        self.Ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())


        self.Ui.BtnOpenC.clicked.connect(self.Child)


    def Child(self):
        self.WChild = Ui_Dialog()
        self.Dialog = QtGui.QDialog(self)

        self.WChild.setupUi(self.Dialog)

        self.WChild.pushButtonOK.clicked.connect(self.GetLine)
        self.WChild.pushButtonCancel.clicked.connect(self.APPclose)
        self.Dialog.exec_()

    def GetLine(self):
        LineData=self.WChild.lineEdit.text()
        self.Ui.textEdit.setText(LineData)
        self.Dialog.close()

    def APPclose(self):
        self.Dialog.close()



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainApp = MainClass()
    MainApp.show()
    sys.exit(app.exec_())