#  DisplayLabel.py
#  This file is part of the mTrack program
#  Created by Sheldon Reeves on 6/24/15.
#  Email: sheldonreeves316@gmail.com
#  Language: Python 3.4
#  OpenCV Version: 3.0.0

import cv2
import numpy as np
from PyQt4 import QtGui
from PyQt4.QtGui import QWidget, QLabel

#   Class Display_Label
#       Purpose: Redefine QLabel class for main display and cage drawing
#       Created by Sheldon Reeves on 6/24/15.
#       Language: Python 3.4
#
#       Dictionary of Variables:
#           - QtInstance: Reference to the main MTrack_Qt instance
#           - byte_width: Calculated Image byte width
#           - cage_complete: boolean for cage completed
#           - cage_vertex_count: counter for cage vertices
#           - cage_vertices: Storage buffer for cage vertices
#           - cage_wall_vertex_count: counter for cage dividing wall vertices
#           - cage_wall_vertices: Storage buffer for cage wall vertices
#           - cage_walls_complete: boolean for cage dividing wall completion
#           - crop: boolean to crop image or not
#           - current_img: the most recently displayed image
#           - first_click: boolean for first click
#           - first_frame: First frame image
#           - frame: copy of first frame to be processed
#           - img_height: Height of frame
#           - img_width: Width of frame
#           - left_click: boolean for left click
#           - mTrack: Reference to MTrack class instance
#           - mouse_count: Number of mice to be tracked
#           - zoom: zoom value

class DisplayLabel(QLabel):

    # Inline Private Member Method: __init__
    # Method to initialize variables
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def __init__(self,first_frame,mouseTracker,zoom,QtInstance):
        super(DisplayLabel, self).__init__()
        self.first_frame = first_frame
        self.mTrack = mouseTracker
        self.zoom = zoom
        self.QtInstance = QtInstance
        self.cage_complete = True
        self.cage_walls_complete = True
        self.left_click = False
        self.first_click = False
        self.img_height, self.img_width, self.channels = self.first_frame.shape

    # Inline Member Method: drawSetup
    # Method to setup variables for drawing
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def drawSetup(self, mouse_count):
        self.mouse_count = int(mouse_count)
        self.frame = self.first_frame.copy()
        self.cage_vertex_count = 0
        self.cage_wall_vertex_count = 0
        self.cage_complete = False
        self.cage_walls_complete = False
        self.first_click = True
        self.crop = True # Intermediate Step
        self.cage_vertices = []  # Cage vertex storage
        self.cage_wall_vertices = []
        self.current_img = []
        self.display_image(self.frame,self.crop,self.zoom)
        self.img_height, self.img_width, self.channels = self.frame.shape

    # Overridden Inline Member Method: mousePressEvent
    # Method that defines actions for mouse presses
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def mousePressEvent(self, eventQMouseEvent):
        # Disable Zoom
        self.QtInstance.Zoom_ScrollBar.setEnabled(False)
        self.QtInstance.Zoom_ScrollBar.setDisabled(True)

        # Capture Vertex 1
        if self.cage_complete is False:
            if self.first_click is True:
                self.cage_vertices.append((int(eventQMouseEvent.x()/self.zoom), int(eventQMouseEvent.y()/self.zoom)))
                self.first_click = False
            self.left_click = True

        elif self.cage_walls_complete is False:
            self.cage_wall_vertices.append((int(eventQMouseEvent.x()/self.zoom), int(eventQMouseEvent.y()/self.zoom)))
            self.left_click = True

        QWidget.mousePressEvent(self,eventQMouseEvent)

    # Overridden Inline Member Method: mouseMoveEvent
    # Method that defines actions for mouse movement
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def mouseMoveEvent(self, eventQMouseEvent):
        if self.left_click is True:
            if self.cage_complete is False:
                copy = self.frame.copy()
                cv2.line(copy, self.cage_vertices[self.cage_vertex_count],
                         (int(eventQMouseEvent.x()/self.zoom),
                          int(eventQMouseEvent.y()/self.zoom)), (211, 0, 148), 2, 8)
                self.display_image(copy,self.crop,self.zoom)

            elif self.cage_walls_complete is False:
                copy = self.current_img.copy()
                cv2.line(copy, self.cage_wall_vertices[self.cage_wall_vertex_count],
                         (int(eventQMouseEvent.x()/self.zoom),
                          int(eventQMouseEvent.y()/self.zoom)), (211, 0, 148), 2, 8)
                img = cv2.cvtColor(copy, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (0,0), fx = self.zoom, fy = self.zoom)
                self.byte_width = img.shape[1]*3
                qimg = QtGui.QImage(img.data,img.shape[1], img.shape[0],self.byte_width, QtGui.QImage.Format_RGB888)
                p1 = QtGui.QPixmap.fromImage(qimg)
                self.setPixmap(p1)

        QWidget.mouseMoveEvent(self,eventQMouseEvent)

    # Overridden Inline Member Method: mouseReleaseEvent
    # Method that defines actions for mouse releases
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def mouseReleaseEvent(self, eventQMouseEvent):
        if self.left_click is True:
            #Cage Walls
            if self.cage_complete is False:
                self.cage_vertices.append((int(eventQMouseEvent.x()/self.zoom), int(eventQMouseEvent.y()/self.zoom)))
                self.left_click = False
                cv2.line(self.frame, self.cage_vertices[self.cage_vertex_count],
                         (int(eventQMouseEvent.x()/self.zoom),
                          int(eventQMouseEvent.y()/self.zoom)), (0, 0, 0), 2, 8)
                self.cage_vertex_count += 1
                if self.cage_vertex_count == 3:
                    self.cage_complete = True
                    cv2.line(self.frame, self.cage_vertices[self.cage_vertex_count], self.cage_vertices[0], (0, 0, 0), 2,8)

                    # Compensate for zoom
                    for i in self.cage_vertices:
                        i = list(i)
                        i[0] = int(i[0]*self.zoom)
                        i[1] = int(i[1]*self.zoom)
                        i = tuple(i)

                    # Enable Zoom
                    self.QtInstance.Zoom_ScrollBar.setEnabled(True)
                    self.QtInstance.Zoom_ScrollBar.setDisabled(False)

                    # Update current image
                    self.QtInstance.parent_img = self.crop_image(self.first_frame)

                    if self.mouse_count == 1:
                        self.cage_walls_complete = True

                        # Enable Viewing Mode Switcher
                        self.QtInstance.View_Mode_comboBox.setEnabled(True)
                        self.QtInstance.View_Mode_comboBox.setDisabled(False)

                        # Enable Buttons
                        self.QtInstance.Detect_Mice_pushButton.setEnabled(True)
                        self.QtInstance.Detect_LF_pushButton.setEnabled(True)
                        self.QtInstance.Detect_RF_pushButton.setEnabled(True)
                        self.QtInstance.Draw_LF_Roi_pushButton.setEnabled(True)
                        self.QtInstance.Draw_RF_Roi_pushButton.setEnabled(True)
                        self.QtInstance.Detect_Mice_pushButton.setDisabled(False)
                        self.QtInstance.Detect_LF_pushButton.setDisabled(False)
                        self.QtInstance.Detect_RF_pushButton.setDisabled(False)
                        self.QtInstance.Draw_LF_Roi_pushButton.setDisabled(False)
                        self.QtInstance.Draw_RF_Roi_pushButton.setDisabled(False)

                    else:
                        self.QtInstance.dialog.infoDialog("Now draw a line for each dividing wall")

                    self.display_image(self.first_frame,self.crop,self.zoom)

                if self.cage_vertex_count == 3:
                    self.crop = False

            # Cage dividers
            elif self.cage_walls_complete is False:
                self.cage_wall_vertices.append((int(eventQMouseEvent.x()/self.zoom),
                                                int(eventQMouseEvent.y()/self.zoom)))
                self.left_click = False
                cv2.line(self.current_img, self.cage_wall_vertices[self.cage_wall_vertex_count],
                         (int(eventQMouseEvent.x()/self.zoom),
                          int(eventQMouseEvent.y()/self.zoom)), (211, 0, 148), 2, 8)
                self.cage_wall_vertex_count += 2
                if self.cage_wall_vertex_count >= self.mouse_count:
                    self.cage_walls_complete = True

                    self.mTrack.calculate_wall_pixels(self.cage_wall_vertices,self.mouse_count)

                    # Compensate for zoom
                    for i in self.cage_wall_vertices:
                        i = list(i)
                        i[0] = int(i[0]*self.zoom)
                        i[1] = int(i[1]*self.zoom)
                        i = tuple(i)

                    # Enable Viewing Mode Switcher
                    self.QtInstance.View_Mode_comboBox.setEnabled(True)
                    self.QtInstance.View_Mode_comboBox.setDisabled(False)

                    # Enable Zoom
                    self.QtInstance.Zoom_ScrollBar.setEnabled(True)
                    self.QtInstance.Zoom_ScrollBar.setDisabled(False)

                    # Enable Buttons
                    self.QtInstance.Detect_Mice_pushButton.setEnabled(True)
                    self.QtInstance.Detect_LF_pushButton.setEnabled(True)
                    self.QtInstance.Detect_RF_pushButton.setEnabled(True)
                    self.QtInstance.Draw_LF_Roi_pushButton.setEnabled(True)
                    self.QtInstance.Draw_RF_Roi_pushButton.setEnabled(True)
                    self.QtInstance.Detect_Mice_pushButton.setDisabled(False)
                    self.QtInstance.Detect_LF_pushButton.setDisabled(False)
                    self.QtInstance.Detect_RF_pushButton.setDisabled(False)
                    self.QtInstance.Draw_LF_Roi_pushButton.setDisabled(False)
                    self.QtInstance.Draw_RF_Roi_pushButton.setDisabled(False)

                    # Save vertices to Qtinstance
                    self.QtInstance.cage_vertices = self.cage_vertices
                    self.QtInstance.cage_wall_vertices = self.cage_wall_vertices

                    self.display_image(self.first_frame,True,self.zoom)


        QWidget.mouseReleaseEvent(self,eventQMouseEvent)

    # Inline Member Method: display_image
    # Method that displays image on Qlabel
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def display_image(self,img,crop,zoom):
        if self.cage_complete is True and crop is True:
            img = self.crop_image(img)
            self.current_img = img # Define current image
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            img = cv2.resize(img, None, fx = self.zoom*1, fy = self.zoom*1,interpolation=cv2.INTER_CUBIC)
            qimg = QtGui.QImage(img.data , img.shape[1], img.shape[0], img.shape[1]*3, QtGui.QImage.Format_RGB888)
            p1 = QtGui.QPixmap.fromImage(qimg)
        else:
            self.current_img = img
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #img = cv2.resize(img, (0,0), fx = self.zoom, fy = self.zoom)
            img = cv2.resize(img, None, fx = self.zoom*1, fy = self.zoom*1,interpolation=cv2.INTER_CUBIC)
            qimg = QtGui.QImage(img.data,img.shape[1], img.shape[0],img.shape[1]*3, QtGui.QImage.Format_RGB888)
            p1 = QtGui.QPixmap.fromImage(qimg)
        self.setPixmap(p1)

    # Inline Member Method: crop_image
    # Method that crops and rotates image based on the cage
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def crop_image(self,img):
            bounding_rect = cv2.minAreaRect(np.array(list(self.cage_vertices)))
            cage_midx = bounding_rect[0][0]
            cage_midy = bounding_rect[0][1]
            cage_angle = bounding_rect[2]
            cage_width = int(bounding_rect[1][0])
            cage_height = int(bounding_rect[1][1])
            if bounding_rect[2] < -45.:
                cage_angle += 90.0
                temp = cage_width
                cage_width = cage_height
                cage_height = temp
            rot_M = cv2.getRotationMatrix2D((cage_midx, cage_midy), cage_angle, 1.0)
            rotated = cv2.warpAffine(img, rot_M, (self.img_width, self.img_height))
            img = cv2.getRectSubPix(rotated, (int(cage_width), int(cage_height)),(cage_midx, cage_midy))
            return img

    # resclae image
    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)