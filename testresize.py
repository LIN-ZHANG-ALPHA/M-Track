from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtNetwork import *

#import all of our resizer classes
from pyqtresizer import *

(Ui_MyFormClass, QMainWindow) = uic.loadUiType('test.ui')

class MainWindowClass (QMainWindow):
    """MyFormClass inherits QMainWindow"""

    def __init__ (self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        self.ui = Ui_MyFormClass()
        self.ui.setupUi(self)

        #build our resizer class as self.resize
        self.resize=slResizer(self.ui)

        self.connect(self.ui.pushButton_3, SIGNAL("clicked()"), self.chpage)
        
    def chpage(self):
        self.ui.stackedWidget_2.setCurrentIndex(0)
        #any time that a stacked widget is changed we should refresh the resize
        #because even though everything is resized sometimes it does not display 
        #correctly
        self.resize.refresh()

    def resizeEvent(self, ev):
        #when a resize event occurs at all we need to resize
        self.resize.refresh()

    def changeEvent(self, ev):
        if ev.type()==105:
          #on a maximize screen event we need to resize
          self.resize.refresh()

 #----------------------------------------------End--------------------------------------------------

if __name__ == "__main__":

    import sys
    app = QApplication(sys.argv)
    form = MainWindowClass()
    form.show()
    app.exec_()

