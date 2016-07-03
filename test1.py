
import sys
import cv2
import time
import math
import os
import numpy as np
import subprocess
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QFileDialog, QLabel
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QDialog):

    def __init__(self, parent=None):
        super(Ui_Form, self).__init__(parent)
        self.setObjectName(_fromUtf8("Form"))
        self.resize(761, 637)
        self.pushButton = QtGui.QPushButton()
        self.pushButton.setGeometry(QtCore.QRect(0, 550, 201, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.connect(self.pushButton, QtCore.SIGNAL("released()"), self.get_output1_statement)

        self.tableWidget = QtGui.QTableWidget()
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 741, 551))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,     QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(50)
        self.tableWidget.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("name"))
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.pushButton)
        self.setLayout(layout)
        for i in range(1, 5):
            self.tableWidget.setHorizontalHeaderItem(i,     QtGui.QTableWidgetItem("column_{0}".format(i)))
        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "button1", None))

    def get_output1_statement(self):
        self.tableWidget.clearContents()

        self.tableWidget.setItem(0,0,QtGui.QTableWidgetItem("add some data"))

app = QtGui.QApplication(sys.argv)
form = Ui_Form()
form.show()
app.exec_()
