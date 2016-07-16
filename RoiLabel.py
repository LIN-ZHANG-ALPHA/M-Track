#  MTrack.py
#  This file is part of the M-Track program
#  For support and questions, please email Annalisa Scimemi (scimemia@gmail.com)
#  Language: Python 2.7
#  OpenCV Version: 3.0
#  PyQt Version: 4.8


import cv2
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget, QLabel
from DisplayLabel import DisplayLabel
import numpy as np
#   Class RoiLabel:
#       Purpose: Redefine QLabel class for main display and roi drawing
#       Dictionary of Variables:
#           - QtInstance: Reference to the main MTrack_Qt instance
#           - crop_list: Buffer containing cropped mouse bounding boxes
#           - current_img: the most recently displayed image
#           - foot: which foot
#           - left_click: boolean for left click
#           - mTrack: Reference to MTrack class instance
#           - mouse_count: Number of mice to be tracked
#           - roi_buffer: Storage buffer for roi vertices
#           - roi_hist_buffer: Storage buffer for roi histograms
#           - roi_window_buffer: Storage buffer for roi tracking windows
#           - zoom: zoom value

class RoiLabel(QLabel):


    # Method to initialize variables
    def __init__(self, mouse_count, crop_list, mouseTracker, zoom, QtInstance, foot):
        super(RoiLabel, self).__init__()
        self.mouse_count = int(mouse_count)
        self.crop_list = crop_list
        self.mTrack = mouseTracker
        self.zoom = zoom
        self.QtInstance = QtInstance
        self.foot = foot
        self.setup()


    # Method to setup variables for drawing
    def setup(self):
        self.left_click = False
        self.roi_count = 0
        self.list_complete = False
        self.roi_buffer = [[] for x in range(10)]
        self.roi_hist_buffer = []
        self.roi_window_buffer = []
        self.display_image(self.crop_list[self.roi_count], self.zoom)


    # Method that defines actions for mouse presses

    def mousePressEvent(self, eventQMouseEvent):
        if self.list_complete is False:
            # Disable Zoom
            # self.QtInstance.Zoom_ScrollBar.setEnabled(False)
            # self.QtInstance.Zoom_ScrollBar.setDisabled(True)

            self.roi_buffer[self.roi_count].append(
                (int(eventQMouseEvent.x() / self.zoom), int(eventQMouseEvent.y() / self.zoom)))
            self.left_click = True
        QWidget.mousePressEvent(self, eventQMouseEvent)

    # Overridden Inline Member Method: mouseMoveEvent
    # Method that defines actions for mouse movement
    def mouseMoveEvent(self, eventQMouseEvent):
        if self.list_complete is False:
            # print "eventQMouseEvent:", eventQMouseEvent

            if self.left_click is True:

                copy = self.crop_list[self.roi_count].copy()

                if self.foot == 'left':
                    cv2.rectangle(copy, self.roi_buffer[self.roi_count][0],
                              (int(eventQMouseEvent.x() / self.zoom), int(eventQMouseEvent.y() / self.zoom)),
                              ( 95 ,61 ,255), 2)
                elif self.foot == 'right':
                    cv2.rectangle(copy, self.roi_buffer[self.roi_count][0],
                              (int(eventQMouseEvent.x() / self.zoom), int(eventQMouseEvent.y() / self.zoom)),
                              (125,  63, 255), 2)

                # cv2.rectangle(copy, self.roi_buffer[self.roi_count][0],
                #               (int(eventQMouseEvent.x() / self.zoom), int(eventQMouseEvent.y() / self.zoom)),
                #               (255, 255, 255), 2)

                # shoe average HSV for roi dynamically
                start = self.roi_buffer[self.roi_count][0]
                New = int(eventQMouseEvent.x() / self.zoom), int(eventQMouseEvent.y() / self.zoom)


                [x1,y1] = start
                [x2,y2] = New
                roiImage = copy[x1:x2+2,y1:y2+2]
                hsvImage = cv2.cvtColor(roiImage, cv2.COLOR_BGR2HSV)
                #print "HSV", hsvImage
                hue, sat, val = hsvImage[:,:,0], hsvImage[:,:,1], hsvImage[:,:,2]
                H = int(np.mean(hue))
                S = int(np.mean(sat))
                V = int(np.mean(val))
                ave_hsv = [H,S,V]

                cv2.putText(copy, "AveHSV:{}".format(ave_hsv), (10,20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100,255,255), 1)


                # cv2.putText(copy, "AveHSV:{}".format(ave_hsv), (int(eventQMouseEvent.x() / self.zoom), int(eventQMouseEvent.y() / self.zoom)),
                # cv2.FONT_HERSHEY_SIMPLEX, 0.7, (127,0,255), 1)

                self.display_image(copy, self.zoom)


            QWidget.mouseMoveEvent(self, eventQMouseEvent)


    # Method that defines actions for mouse releases

    def mouseReleaseEvent(self, eventQMouseEvent):
        if self.list_complete is False:
            copy = self.crop_list[self.roi_count].copy()

            if self.left_click is True:
                self.roi_buffer[self.roi_count].append(
                    (int(eventQMouseEvent.x() / self.zoom), int(eventQMouseEvent.y() / self.zoom)))

                cv2.rectangle(self.crop_list[self.roi_count], self.roi_buffer[self.roi_count][0],
                              (int(eventQMouseEvent.x() / self.zoom), int(eventQMouseEvent.y() / self.zoom)),
                              (255, 255, 255), 2)

                #print "HH",self.roi_buffer[self.roi_count]
                # Compensate for zoom
                for i in self.roi_buffer[self.roi_count]:
                    i = list(i)
                    i[0] = int(i[0] * self.zoom)
                    i[1] = int(i[1] * self.zoom)
                    i = tuple(i)

                # Enable Zoom
                self.QtInstance.Zoom_ScrollBar.setEnabled(True)
                self.QtInstance.Zoom_ScrollBar.setDisabled(False)

                # Calculate histograms
                if self.foot == 'left':
                    roi_hist, track_window = self.mTrack.calcRoiHist(self.crop_list[self.roi_count],
                                                                           self.roi_buffer[self.roi_count],
                                                                           self.mTrack.left_foot_color_lower_hue,
                                                                           self.mTrack.left_foot_color_lower_sat,
                                                                           self.mTrack.left_foot_color_lower_val,
                                                                           self.mTrack.left_foot_color_upper_hue,
                                                                           self.mTrack.left_foot_color_upper_sat,
                                                                           self.mTrack.left_foot_color_upper_val,
                                                                           self.mTrack.left_foot_collision_detect,
                                                                           self.mTrack.left_foot_dilation)

                else:
                    roi_hist, track_window = self.mTrack.calcRoiHist(self.crop_list[self.roi_count],
                                                                           self.roi_buffer[self.roi_count],
                                                                           self.mTrack.right_foot_color_lower_hue,
                                                                           self.mTrack.right_foot_color_lower_sat,
                                                                           self.mTrack.right_foot_color_lower_val,
                                                                           self.mTrack.right_foot_color_upper_hue,
                                                                           self.mTrack.right_foot_color_upper_sat,
                                                                           self.mTrack.right_foot_color_upper_val,
                                                                           self.mTrack.right_foot_collision_detect,
                                                                           self.mTrack.right_foot_dilation)

                self.roi_hist_buffer.append(roi_hist)
                self.roi_window_buffer.append(track_window)

                self.left_click = False
                self.roi_count = self.roi_count + 1

                if self.roi_count < len(self.crop_list):
                    #cv2.putText(self.crop_list[self.roi_count], "HSV:",(10,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (127,0,255), 2)
                    self.display_image(self.crop_list[self.roi_count], self.zoom)

                if self.roi_count == len(self.crop_list):
                    self.list_complete = True

                    # Enable Viewing Mode Switcher
                    self.QtInstance.View_Mode_comboBox.setEnabled(True)
                    self.QtInstance.View_Mode_comboBox.setDisabled(False)


                    # roiLabel will cease to exist so data must be saved to QtInstance
                    if self.foot == 'left':
                        self.QtInstance.left_foot_roi_hist_buffer = self.roi_hist_buffer
                        self.QtInstance.left_foot_roi_window_buffer = self.roi_window_buffer
                        #print "left",self.roi_window_buffer

                        # cv2.putText(img, "RF_HSV: {}".format(hsvImage[1][1]), (10, 20),
                        # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                    else:
                        self.QtInstance.right_foot_roi_hist_buffer = self.roi_hist_buffer
                        self.QtInstance.right_foot_roi_window_buffer = self.roi_window_buffer
                        #print "right",self.roi_window_buffer

                    # displayLabel object must be initialized and restored to its previous condition in QtInstance
                    self.QtInstance.displayLabel = DisplayLabel(self.mTrack.first_frame, self.mTrack,
                                                                self.zoom, self.QtInstance)


                    self.QtInstance.displayLabel.setGeometry(QtCore.QRect(0, 0, 831, 821))
                    self.QtInstance.displayLabel.setText("")
                    self.QtInstance.displayLabel.setAlignment(
                        QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
                    self.QtInstance.displayLabel.setObjectName("displayLabel")
                    self.QtInstance.displayLabel.setMouseTracking(True)
                    self.QtInstance.displayLabel.cage_vertices = self.QtInstance.cage_vertices
                    self.QtInstance.displayLabel.cage_wall_vertices = self.QtInstance.cage_wall_vertices

                    # roiLabel instance is destroyed in c++ space
                    self.QtInstance.Display_scrollArea.setWidget(self.QtInstance.displayLabel)
                    self.QtInstance.displayImage(self.QtInstance.parent_img, False)

                    # Enable Buttons
                    self.QtInstance.DrawCage_pushButton.setEnabled(True)
                    self.QtInstance.Detect_Mice_pushButton.setEnabled(True)
                    self.QtInstance.Detect_LF_pushButton.setEnabled(True)
                    self.QtInstance.Detect_RF_pushButton.setEnabled(True)
                    self.QtInstance.Draw_LF_Roi_pushButton.setEnabled(True)
                    self.QtInstance.Draw_RF_Roi_pushButton.setEnabled(True)
                    self.QtInstance.DrawCage_pushButton.setDisabled(False)
                    self.QtInstance.Detect_Mice_pushButton.setDisabled(False)
                    self.QtInstance.Detect_LF_pushButton.setDisabled(False)
                    self.QtInstance.Detect_RF_pushButton.setDisabled(False)
                    self.QtInstance.Draw_LF_Roi_pushButton.setDisabled(False)
                    self.QtInstance.Draw_RF_Roi_pushButton.setDisabled(False)

                    if self.foot == 'left':
                        if len(self.QtInstance.right_foot_roi_hist_buffer) != 0:
                            self.QtInstance.Execute_pushButton.setEnabled(True)
                            self.QtInstance.Execute_pushButton.setDisabled(False)
                    else:
                        if len(self.QtInstance.left_foot_roi_hist_buffer) != 0:
                            self.QtInstance.Execute_pushButton.setEnabled(True)
                            self.QtInstance.Execute_pushButton.setDisabled(False)
        #return self.roi_window_buffer


    # Method that displays image on Qlabel
    def display_image(self, img, zoom):
        self.current_img = img
        img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (0, 0), fx=self.zoom, fy=self.zoom)
        #img = cv2.resize(img, None, fx = self.zoom*0.6, fy = self.zoom*0.6,interpolation=cv2.INTER_CUBIC)
        qimg = QtGui.QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QtGui.QImage.Format_RGB888)
        p1 = QtGui.QPixmap.fromImage(qimg)
        #print "P1", p1.size()


        self.setPixmap(p1)
