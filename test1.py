import sys
from PyQt4 import QtCore, QtGui
from gui import Ui_MainWindow
import cv2
import numpy as np

#------------------------------------------------------------------------ Static


#--------------------------------------------------------------------- Functions
def processImage(image,colormin,colormax):
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #Convert to HSV image
    hsvImage = cv2.medianBlur(hsvImage, 3) #blur image to reduce noise
    colorThreshed = cv2.inRange(hsvImage,colormin,colormax) #threshold image
    return colorThreshed


#-------------------------------------------------------------------- Form Class
class MyForm(QtGui.QMainWindow):
    #Constructor
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Create Video Object
        cv2.namedWindow('Video')
        device = 0
        self.video = cv2.VideoCapture(device)     
        
        #Set up timer
        self.ctimer = QtCore.QTimer()

        #Slider Bars signal connectors
        QtCore.QObject.connect(self.ui.horizontalSlider, QtCore.SIGNAL("sliderMoved(int)"),self.updateLabels)
        QtCore.QObject.connect(self.ui.horizontalSlider_2, QtCore.SIGNAL("sliderMoved(int)"),self.updateLabels)
        QtCore.QObject.connect(self.ui.horizontalSlider_3, QtCore.SIGNAL("sliderMoved(int)"),self.updateLabels)
        QtCore.QObject.connect(self.ui.horizontalSlider_4, QtCore.SIGNAL("sliderMoved(int)"),self.updateLabels)
        QtCore.QObject.connect(self.ui.horizontalSlider_5, QtCore.SIGNAL("sliderMoved(int)"),self.updateLabels)
        QtCore.QObject.connect(self.ui.horizontalSlider_6, QtCore.SIGNAL("sliderMoved(int)"),self.updateLabels)
        
        #Timer signal
        QtCore.QObject.connect(self.ctimer,QtCore.SIGNAL("timeout()"),self.tick)
        
        #Timer start
        self.ctimer.start(1)

    #Label Updates Signal Callback
    def updateLabels(self):
        self.ui.label.setText(str(self.ui.horizontalSlider.value()))
        self.ui.label_2.setText(str(self.ui.horizontalSlider_2.value()))
        self.ui.label_3.setText(str(self.ui.horizontalSlider_3.value()))
        self.ui.label_4.setText(str(self.ui.horizontalSlider_4.value()))
        self.ui.label_5.setText(str(self.ui.horizontalSlider_5.value()))
        self.ui.label_6.setText(str(self.ui.horizontalSlider_6.value()))
        self.updateThresh()
        
    def updateThresh(self):
        colormin,colormax = self.getColors()
        minStr = "Threshold minimum: " + str(colormin[0]) + ", " + str(colormin[1]) + ", " + str(colormin[2])
        maxStr = "Threshold maximum: " + str(colormax[0]) + ", " + str(colormax[1]) + ", " + str(colormax[2])
        self.ui.label_7.setText(minStr)
        self.ui.label_8.setText(maxStr)
        
    #Timer tick
    def tick(self):
        self.updateLabels()
        _,frame = self.video.read()
        colormin,colormax = self.getColors()
        checked = self.ui.checkBox.checkState()
        if not checked:
            cv2.imshow('Video', frame)
        else:
            image = processImage(frame,colormin,colormax)
            cv2.imshow('Video', image)
        
    #Get Colors from Ui
    def getColors(self):
        #Get values from form
        hmin = np.amax([0,self.ui.horizontalSlider.value()-(self.ui.horizontalSlider_6.value()/2)])
        hmax = np.amin([360,self.ui.horizontalSlider.value()+(self.ui.horizontalSlider_6.value()/2)])
        smin = self.ui.horizontalSlider_2.value()
        smax = self.ui.horizontalSlider_3.value()
        vmin = self.ui.horizontalSlider_4.value()
        vmax = self.ui.horizontalSlider_5.value()
        #Create colors and return them
        cmin = np.array([hmin,smin,vmin],np.uint8)
        cmax = np.array([hmax,smax,vmax],np.uint8)
        return cmin,cmax        
    
        
#-------------------------------------------------------------------------- Main
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())