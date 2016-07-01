#  InfoDialog.py
#  This file is part of the mTrack program
#  Created by Sheldon Reeves on 6/24/15.
#  Email: sheldonreeves316@gmail.com
#  Language: Python 3.4
#  OpenCV Version: 3.0.0

from PyQt4.QtGui import QWidget, QMessageBox

#   Class InfoDialog:
#       Purpose: Redefine QWidget class for displaying info messages
#       Created by Sheldon Reeves on 6/24/15.
#       Language: Python 3.4

class InfoDialog(QWidget):

    def __init__(self):
        #super().__init__()
        super(InfoDialog, self).__init__()

    def infoDialog(self,message):
        QMessageBox.information(self,'Message',message,QMessageBox.Ok)
