#  MTrack.py
#  This file is part of the M-Track program
#  For support and questions, please email Annalisa Scimemi (scimemia@gmail.com)
#  Language: Python 2.7
#  OpenCV Version: 3.0


import cv2
from PyQt4 import QtGui
from PyQt4.QtGui import QLabel

#   Class RoiLabel:
#       Purpose: Redefine QLabel class for displaying color selector image


class ColorLabel(QLabel):
    def __init__(self):
        super(ColorLabel, self).__init__()

    def display_image(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(img.data,img.shape[1], img.shape[0],img.shape[1]*3, QtGui.QImage.Format_RGB888)
        p1 = QtGui.QPixmap.fromImage(qimg)
        self.setPixmap(p1)


