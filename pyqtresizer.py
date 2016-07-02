from PyQt4.QtCore import *

def logit(dat):
  rt=open("access.log","a")
  rt.write(dat+"\n")
  rt.close()

class slResizer(object):
    def __init__(self,ui):
        self.ui=ui
        self.ma=False
        self.slapObjects()

    def slapObjects(self):
        #record all object sizes as they currently are
        self.rsw=[]
        obj1= self.ui.__dict__
        objlist=obj1.values()
        self.wss=[]
        self.ftab=[]
        self.rsmakeObj=[]
        self.rsmakeName=[]
        for obj in objlist: 
          #The tabwidget is a strange fellow.  It has a stacked widget inside it
          if "QTabWidget" in str(obj):
            #funny cause below would seem to get me back to QTabWidget but it doesnt
            #it takes me to the real stacked widget
            aswell=obj.currentWidget().parent()
            aswell.blockSignals(True)
            #Because QT does not like to make the widgets inside a tab widget the correct
            # size... i have to do it for them
            a1,a2,a3,a4=str(obj.geometry()).split("(")[1].split(")")[0].split(",")
            b1,b2,b3,b4=str(aswell.geometry()).split("(")[1].split(")")[0].split(",")
            aswell.setGeometry(QRect(int(b1),int(b2),int(a3),int(a4)))
            self.ftab.append(aswell)
            aswell.blockSignals(False)
          if "QStackedWidget" in str(obj.parent()):
            obj.blockSignals(True)
            #Because QT does not like to make the widgets inside a tab widget the correct
            # size... i have to do it for them
            a1,a2,a3,a4=str(obj.geometry()).split("(")[1].split(")")[0].split(",")
            b1,b2,b3,b4=str(obj.parent().geometry()).split("(")[1].split(")")[0].split(",")
            obj.setGeometry(QRect(int(a1),int(a2),int(b3),int(b4)))
            obj.blockSignals(False)
          self.wss.append([obj,obj.parent().objectName()])
          if not str(obj.parent().objectName()) in self.rsmakeName:
            #if i havent already done so add the object to the make list with a few pieces of info too
            self.rsmakeName.append(str(obj.parent().objectName()))
            self.rsmakeObj.append([self.howdeep(obj.parent()),obj.parent(),str(obj.parent().objectName())])
        self.rsmakeObj=sorted(self.rsmakeObj)

    def checkNew(self):
        if not self.ma:
          self.ma=True
          self.subscribeAll()
  
    def adjustAll(self):
        #check to see if i already subscribed the widgets don't want too twice
        #TODO build a way of resubscribing individual widgets that get moved 
        #     programatically
        self.checkNew()
        for arsw in self.rsw:
          arsw.resizeWidgets()
        #some funky tab widget stuff to keep the tab from clearing itself after resize
        for aobj in self.ftab:
           try:
             if aobj.currentIndex()==0:
               aobj.setCurrentIndex(1)
               aobj.setCurrentIndex(0)
             else:
               ci=aobj.currentIndex()
               aobj.setCurrentIndex(0)
               aobj.setCurrentIndex(ci)
           except:
             #if you cant then oh well
             pass

    def refresh(self):
        self.adjustAll()

    def howdeep(self,obj):
        #returns how deep a widget is for sorting
        a=1
        b=0
        name=obj.objectName()
        while a==1:
          try:
            obj=obj.parent()
            b+=1
          except Exception, e:
            return b

    def subscribeAll(self):
        ad=0
        #subscribe all the widgets in a container to a Resizer Class
        for obj in self.rsmakeObj:
          a=Resizer(obj[1])
          for cobj in self.wss:
            if cobj[1]==obj[2]:
              a.widgetSubscribe(cobj[0])
          ad+=1
          self.rsw.append(a)


class Resizer(object):
    def __init__(self,MainWidget):
        self.main=MainWidget
        #build starting geometry settings for the window
        self.ma,self.mb,self.mc,self.md=str(self.main.geometry()).split("(")[1].split(")")[0].split(",")
        self.allw=[]

    def widgetSubscribe(self,widget):
        #TODO handle fonts resize associated with the widgets
        a,b,c,d=str(widget.geometry()).split("(")[1].split(")")[0].split(",")
        self.allw.append([widget,a,b,c,d])

    def resizeWidgets(self,dolog=False):
        ma,mb,mc,md=str(self.main.geometry()).split("(")[1].split(")")[0].split(",")
        for widget in self.allw:
          #calculate and move / resize things
          son=(1.0*int(mc)/int(self.mc))*100
          pon=(1.0*int(md)/int(self.md))*100
          la=(son*.01)*int(widget[1])
          lb=(pon*.01)*int(widget[2])
          lc=(son*.01)*int(widget[3])
          ld=(pon*.01)*int(widget[4])
          if dolog:
            #log stuff to access.log if you want too gives detailed reasons as to why something was resized a certain way
            logit("widget: " + widget[0].objectName() + " instance:" + str(widget[0]) + " parent:" + widget[0].parent().objectName())
            logit("  i am moving "+widget[0].objectName()+" to " + str(la) + "," +str(lb))
            logit("    from its current position at" + widget[1] + "," + widget[2])
            logit("  i am resizing "+widget[0].objectName()+" to " + str(lc) + "," +str(ld))
            logit("    from its current size of " + widget[3] + "," + widget[4])
            logit("      because "+widget[0].parent().objectName() + " is now "+str(widget[0].parent().geometry()))
          widget[0].setGeometry(QRect(la,lb,lc,ld))
