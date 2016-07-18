#!/usr/bin/python
#  MTrack.py
#  This file is part of the M-Track program
#  For support and questions, please email Annalisa Scimemi (scimemia@gmail.com)
#  Language: Python 2.7
#  OpenCV Version: 3.0

from PyQt4.QtGui import QWidget, QMessageBox

#   Class InfoDialog:
#       Purpose: Redefine QWidget class for displaying info messages

class InfoDialog(QWidget):

    def __init__(self):
        #super().__init__()
        super(InfoDialog, self).__init__()

    def infoDialog(self,message):
        QMessageBox.information(self,'Message',message,QMessageBox.Ok)
