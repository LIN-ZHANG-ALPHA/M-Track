#  MTrack.py
#  This file is part of the mTrack program
#  Created by Sheldon Reeves on 6/24/15.
#  Email: sheldonreeves316@gmail.com
#  Language: Python 3.4
#  OpenCV Version: 3.0.0

import cv2
import numpy as np

#   Class MTrack:
#       Purpose: mTrack Tracking Functionality
#       Created by Sheldon Reeves on 6/24/15.
#       Language: Python 3.4
#
#       Dictionary of Variables:
#           - body_collision_detect: boolean for enabling collision detection on mouse bodies
#           - body_color_image: Body color selector image
#           - body_color_lower_hue: Body color mask lower hue value
#           - body_color_lower_sat: Body color mask lower sat value
#           - body_color_lower_val: Body color mask lower val value
#           - body_color_upper_hue: Body color mask upper hue value
#           - body_color_upper_sat: Body color mask upper sat value
#           - body_color_upper_sat: Body color mask upper sat value
#           - body_dilation: Body color mask dilation value
#           - body_minBoxSize: Body tracking minimum box(object) size
#           - box_scale: Mouse body box scaling factor
#           - capture: Opencv Video Capture Object
#           - crop_list: Storage buffer for cropped mouse bounding box images
#           - deNoise_val: Value for amount of de-noising
#           - first_frame: Image of the first frame loaded from video
#           - img_height: Height of frame
#           - img_width: Width of frame
#           - left_foot_collision_detect: boolean for enabling collision detection on left feet
#           - left_foot_color_image: Left Foot color selector image
#           - left_foot_color_lower_hue: Left Foot color mask lower hue value
#           - left_foot_color_lower_sat: Left Foot color mask lower sat value
#           - left_foot_color_lower_val: Left Foot color mask lower val value
#           - left_foot_color_upper_hue: Left Foot color mask upper hue value
#           - left_foot_color_upper_sat: Left Foot color mask upper sat value
#           - left_foot_color_upper_sat: Left Foot color mask upper sat value
#           - left_foot_dilation: Left Foot color mask dilation value
#           - left_foot_minBoxSize: Left Foot tracking minimum box(object) size
#           - mouse_count: Number of mice to be tracked
#           - noiseReduction_on: boolean for activating noise reduction
#           - right_foot_collision_detect: boolean for enabling collision detection on right feet
#           - right_foot_color_image: Right Foot color selector image
#           - right_foot_color_lower_hue: Right Foot color mask lower hue value
#           - right_foot_color_lower_sat: Right Foot color mask lower sat value
#           - right_foot_color_lower_val: Right Foot color mask lower val value
#           - right_foot_color_upper_hue: Right Foot color mask upper hue value
#           - right_foot_color_upper_sat: Right Foot color mask upper sat value
#           - right_foot_color_upper_sat: Right Foot color mask upper sat value
#           - right_foot_dilation: Right Foot color mask dilation value
#           - right_foot_minBoxSize: Right Foot tracking minimum box(object) size
#           - term_crit: CamShift termination criteria
#           - wall1: Storage buffer for first dividing wall vertices
#           - wall2: Storage buffer for second dividing wall vertices

class MTrack:

    # Inline Private Member Method: __init__
    # Method that reads the opens video file and reads first frame
    # Precondition: No video file opened
    # Postcondition: Video file open and first frame read
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def __init__(self, filename):
        # Initial Frame capture
        self.capture = cv2.VideoCapture(filename)
        # background subtraction
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        fgbg = cv2.BackgroundSubtractorMOG()()


        f, self.first_frame = self.capture.read()

        #self.first_frame = fgbg.apply(self.first_frame)

        self.img_height, self.img_width, channels = self.first_frame.shape

        self.__initialize_variables()

    # Inline Member Method: __initialize_variables
    # Method to initialize all variables for the class
    # Precondition: Variables undefined
    # Postcondition: Variables created and initialized
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def __initialize_variables(self):
        self.crop_list = []
        self.wall1 = []
        self.wall2 = []
        self.box_scale = 1.1
        self.body_color_lower_hue = 0
        self.body_color_lower_sat = 0
        self.body_color_lower_val = 0
        self.body_color_upper_hue = 180
        self.body_color_upper_sat = 255
        self.body_color_upper_val = 255
        self.body_collision_detect = 0
        self.body_dilation = 1
        self.body_minBoxSize = 1
        self.left_foot_color_lower_hue = 0
        self.left_foot_color_lower_sat = 0
        self.left_foot_color_lower_val = 0
        self.left_foot_color_upper_hue = 180
        self.left_foot_color_upper_sat = 255
        self.left_foot_color_upper_val = 255
        self.left_foot_collision_detect = 0
        self.left_foot_dilation = 1
        self.left_foot_minBoxSize = 0
        self.right_foot_color_lower_hue = 0
        self.right_foot_color_lower_sat = 0
        self.right_foot_color_lower_val = 0
        self.right_foot_color_upper_hue = 180
        self.right_foot_color_upper_sat = 255
        self.right_foot_color_upper_val = 255
        self.right_foot_collision_detect = 0
        self.right_foot_dilation = 1
        self.right_foot_minBoxSize = 0
        self.noiseReduction_on = False
        self.deNoise_val = 1
        self.mouse_count = 0
        self.body_color_image = []
        self.left_foot_color_image = []
        self.right_foot_color_image = []

        # Meanshift Termination Criteria
        self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 1)

    # Inline Member Method: calculate_wall_pixels
    # Method to calculate the pixels for each wall line
    # Precondition: Wall Pixels Unknown
    # Postcondition: Wall Pixels Known
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def calculate_wall_pixels(self, vertices, mouse_count):
        # Bresenham Algorithm on Wall Lines
        if mouse_count > 1:
            self.wall1 = self.line_bres(vertices[0], vertices[1])
        if mouse_count > 2:
            self.wall2 = self.line_bres(vertices[2], vertices[3])

    # Inline Member Method: generate_selector_images
    # Method to generate color selector images
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def generate_selector_images(self):

        # Selector Color Images
        body_color_image_lower = np.zeros((50, 150, 3), np.uint8)
        body_color_image_upper = np.zeros((50, 150, 3), np.uint8)
        left_foot_color_image_lower = np.zeros((50, 150, 3), np.uint8)
        left_foot_color_image_upper = np.zeros((50, 150, 3), np.uint8)
        right_foot_color_image_lower = np.zeros((50, 150, 3), np.uint8)
        right_foot_color_image_upper = np.zeros((50, 150, 3), np.uint8)

        # Generate images based on color selector values
        body_color_image_lower[:, :] = (
            self.body_color_lower_hue, self.body_color_lower_sat, self.body_color_lower_val)
        body_color_image_upper[:, :] = (
            self.body_color_upper_hue, self.body_color_upper_sat, self.body_color_upper_val)
        left_foot_color_image_lower[:, :] = (
            self.left_foot_color_lower_hue, self.left_foot_color_lower_sat, self.left_foot_color_lower_val)
        left_foot_color_image_upper[:, :] = (
            self.left_foot_color_upper_hue, self.left_foot_color_upper_sat, self.left_foot_color_upper_val)
        right_foot_color_image_lower[:, :] = (
            self.right_foot_color_lower_hue, self.right_foot_color_lower_sat, self.right_foot_color_lower_val)
        right_foot_color_image_upper[:, :] = (
            self.right_foot_color_upper_hue, self.right_foot_color_upper_sat, self.right_foot_color_upper_val)

        # Combine Images
        self.body_color_image = np.concatenate((body_color_image_lower, body_color_image_upper), axis=1)
        self.left_foot_color_image = np.concatenate((left_foot_color_image_lower, left_foot_color_image_upper), axis=1)
        self.right_foot_color_image = np.concatenate((right_foot_color_image_lower, right_foot_color_image_upper),
                                                     axis=1)
    # Inline Member Method: process_image_color
    # Method to perform color based object detection on a single image
    # Precondition: Object(s) undetected
    # Postcondition: Object(s) detected
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def process_image_color(self, img, color_lower_hue, color_lower_sat, color_lower_val, color_upper_hue,
                            color_upper_sat,
                            color_upper_val, collision_detect, dilation, minboxsize, box_scale):

        box_list = []  # Box storage
        center_points = []  # Center Points

        # Noise Reduction
        #if self.noiseReduction_on is True:
            #img = cv2.fastNlMeansDenoisingColored(img, h=self.deNoise_val)

        # Generate Color Mask
        color_binary = self.map_binary_color(img, color_lower_hue, color_lower_sat, color_lower_val,
                                             color_upper_hue,
                                             color_upper_sat, color_upper_val, dilation)

        image, contours, hierarchy = cv2.findContours(color_binary, cv2.RETR_EXTERNAL,
                                                              cv2.CHAIN_APPROX_SIMPLE)  # Find Contours

        # Generate box list from contours
        for idx, contour in enumerate(contours):
            moment = cv2.moments(contour)
            if moment["m00"] > minboxsize:
                bound_rect = cv2.boundingRect(contour)
                pt1 = (int(bound_rect[0] / box_scale), int(bound_rect[1] / box_scale))
                pt2 = (int(bound_rect[0] * box_scale) + int(bound_rect[2] * box_scale),
                       int(bound_rect[1] * box_scale) + int(bound_rect[3] * box_scale))
                box_list.append((pt1, pt2))

        # Box collision detection
        if box_list and collision_detect == True:
            box_list = self.box_collision_detect(box_list)

        for i in box_list:
            # Center point calculations
            x = int((i[1][0] + i[0][0]) / 2)
            y = int((i[1][1] + i[0][1]) / 2)
            center_points.append((x, y))

        return box_list, center_points

    # Inline Member Method: process_image_roi
    # Method to perform roi based object detection on a single image
    # Precondition: Object undetected
    # Postcondition: Object detected
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def process_image_roi(self, img, roi_hist, track_window, color_lower_hue, color_lower_sat, color_lower_val,
                          color_upper_hue,
                          color_upper_sat,
                          color_upper_val, dilation):

        center_points = []  # Center Points

        # Noise Reduction
        if self.noiseReduction_on is True:
            img = cv2.fastNlMeansDenoisingColored(img, h=self.deNoise_val)

        # Generate Color Mask
        color_binary = self.map_binary_color(img, color_lower_hue, color_lower_sat, color_lower_val,
                                             color_upper_hue,
                                             color_upper_sat, color_upper_val, dilation)

        masked_img = cv2.bitwise_and(img, img, mask=color_binary)

        # Back Projection
        BP = cv2.calcBackProject([masked_img], [0], roi_hist, [0, 180], 1)


        # apply meanshift to get the new location
        object, track_window = cv2.CamShift(BP, track_window, self.term_crit)

        x = int(object[0][0])
        y = int(object[0][1])
        center_points.append((x, y))

        return center_points, track_window

    # Inline Static Member Method: map_binary_color
    # Method to generate a binary color mask from threshold color values
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    @staticmethod
    def map_binary_color(img, color_lower_hue, color_lower_sat, color_lower_val, color_upper_hue,
                         color_upper_sat,
                         color_upper_val, dilation):
        color_lower = np.array([color_lower_hue, color_lower_sat, color_lower_val], np.uint8)
        color_upper = np.array([color_upper_hue, color_upper_sat, color_upper_val], np.uint8)
        color_binary = cv2.inRange(img, color_lower, color_upper)
        dilation = np.ones((dilation, dilation), "uint8")
        color_binary = cv2.dilate(color_binary, dilation)
        return color_binary

    # Inline Member Method: calcRoiHist
    # Method to generate hue channel histogram of ROI
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def calcRoiHist(self, img, roi, color_lower_hue, color_lower_sat, color_lower_val, color_upper_hue,
                    color_upper_sat,
                    color_upper_val, collision_detect, dilation):

        # Noise Reduction
        if self.noiseReduction_on is True:
            img = cv2.fastNlMeansDenoisingColored(img, h=self.deNoise_val)

        roi_img = img[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]
        track_window = (roi[0][0], roi[0][1], roi[1][0] - roi[0][0], roi[1][1] - roi[0][1])

        color_binary = self.map_binary_color(roi_img, color_lower_hue, color_lower_sat, color_lower_val,
                                             color_upper_hue,
                                             color_upper_sat, color_upper_val, dilation)

        roi_hist = cv2.calcHist([roi_img], [0], color_binary, [180], [0, 180])

        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        return roi_hist, track_window

    # Inline Member Method: box_collision_detect
    # Method to perform collision detection and merging on list of boxes
    # Precondition: Collisions Not Detected
    # Postcondition: Collided Boxes Merged
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def box_collision_detect(self, box_list):
        # Boxes must be in the format:
        # ((topleftx),(toplefty)), ((bottomrightx),(bottomrighty)))
        for i in box_list:

            # Collision detect every box:
            for j in box_list:
                if i is j:
                    continue  # Skip self

                # Assume collision
                collision = True

                if i[1][0] * 1.015 < j[0][0] * 0.985:
                    collision = False
                if i[0][0] * .985 > j[1][0] * 1.015:
                    collision = False

                if i[1][1] * 1.015 < j[0][1] * 0.985:
                    collision = False
                if i[0][1] * 0.985 > j[1][1] * 1.015:
                    collision = False
                if collision:
                    # merge boxes
                    top_left_x = min(i[0][0], j[0][0])
                    top_left_y = min(i[0][1], j[0][1])
                    bottom_right_x = max(i[1][0], j[1][0])
                    bottom_right_y = max(i[1][1], j[1][1])

                    new = ((top_left_x, top_left_y), (bottom_right_x, bottom_right_y))

                    box_list.remove(i)
                    box_list.remove(j)
                    box_list.append(new)

                    # Start over with the new list:
                    return self.box_collision_detect(box_list)

        return box_list

    # Inline Member Method: detect_mice
    # Method to perform mouse body detection on a single image
    # Precondition: Mice not detected
    # Postcondition: Mice detected
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def detect_mice(self, img, mouse_count):
        self.mouse_count = mouse_count
        mouse_box_list, mouse_center_points = self.process_image_color(img,
                                                                                           self.body_color_lower_hue,
                                                                                           self.body_color_lower_sat,
                                                                                           self.body_color_lower_val,
                                                                                           self.body_color_upper_hue,
                                                                                           self.body_color_upper_sat,
                                                                                           self.body_color_upper_val,
                                                                                           self.body_collision_detect,
                                                                                           self.body_dilation,
                                                                                           self.body_minBoxSize,
                                                                                           self.box_scale)

        return mouse_box_list, mouse_center_points

    # Inline Member Method: detect_left_feet
    # Method to perform mouse left foot detection on a single image
    # Precondition: Left feet not detected
    # Postcondition: Left feet detected
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def detect_left_feet(self, img, mouse_count, mouse_box_list):
        left_foot_box_list = [[0 for x in range(100)] for x in range(100)]
        left_foot_center_points = [[0 for x in range(100)] for x in range(100)]

        crop_list = self.crop_images(img, mouse_box_list)

        for i in range(0, len(crop_list)):
            left_foot_box_list[i], left_foot_center_points[i] = self.process_image_color(
                crop_list[i],
                self.left_foot_color_lower_hue,
                self.left_foot_color_lower_sat,
                self.left_foot_color_lower_val,
                self.left_foot_color_upper_hue,
                self.left_foot_color_upper_sat,
                self.left_foot_color_upper_val,
                self.left_foot_collision_detect,
                self.left_foot_dilation,
                self.left_foot_minBoxSize,
                1)

        return left_foot_box_list, left_foot_center_points, crop_list

    # Inline Member Method: detect_right_feet
    # Method to perform mouse right foot detection on a single image
    # Precondition: Right feet not detected
    # Postcondition: Right feet detected
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def detect_right_feet(self, img, mouse_count, mouse_box_list):
        right_foot_box_list = [[0 for x in range(100)] for x in range(100)]
        right_foot_center_points = [[0 for x in range(100)] for x in range(100)]

        crop_list = self.crop_images(img, mouse_box_list)

        for i in range(0, len(crop_list)):
            right_foot_box_list[i], right_foot_center_points[i] = self.process_image_color(
                crop_list[i],
                self.right_foot_color_lower_hue,
                self.right_foot_color_lower_sat,
                self.right_foot_color_lower_val,
                self.right_foot_color_upper_hue,
                self.right_foot_color_upper_sat,
                self.right_foot_color_upper_val,
                self.right_foot_collision_detect,
                self.right_foot_dilation,
                self.right_foot_minBoxSize,
                1)

        return right_foot_box_list, right_foot_center_points, crop_list

    # Inline Static Member Method: line_bres
    # Method to execute generic bresenham algorithm
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    @staticmethod
    def line_bres(pt1, pt2):
        x = pt1[0]
        y = pt1[1]
        x2 = pt2[0]
        y2 = pt2[1]
        width = x2 - x
        height = y2 - y
        points = []
        swap = 0
        # If height is increasing faster than width, swap x and y
        if abs(height) > abs(width):
            holder = x
            x = y
            y = holder

            holder = x2
            x2 = y2
            y2 = holder

            swap = 1

        # If line is going in negative x direction, swap endpoints
        if x > x2:
            holder = x
            x = x2
            x2 = holder

            holder = y
            y = y2
            y2 = holder

        # Calculate Constants
        dx = x2 - x
        dy = abs(y2 - y)
        twody = dy * 2
        twodx = dx * 2

        # Set decision variable
        p = twody - dx

        # Determine y increment direction
        if y < y2:
            increment_y = 1
        else:
            increment_y = -1

        for x in range(x, x2):
            if abs(height) > abs(width):
                points.append((y, x))
            else:
                points.append((x, y))

            if p < 0:
                p += twody
            else:
                y += increment_y
                p += twody - twodx

        return swap, points

    # Inline Member Method: sort_mouse_list
    # Method to sort mouse list from top left to bottom right
    # Precondition: Mouse list not sorted
    # Postcondition:Mouse List Sorted
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    def sort_mouse_list(self, box_list, center_points, line_points, left_foot_roi_hist_buffer,
                        left_foot_roi_window_buffer,right_foot_roi_hist_buffer,right_foot_roi_window_buffer):
        # Storage Tuples
        top_left = ()
        top_right = ()
        bottom_left = ()
        bottom_right = ()
        top_single = ()
        bottom_single = ()
        left_single = ()
        right_single = ()
        top_left_box = ()
        top_right_box = ()
        bottom_left_box = ()
        bottom_right_box = ()
        top_single_box = ()
        bottom_single_box = ()
        left_single_box = ()
        right_single_box = ()
        left_foot_top_left_roi_hist = ()
        left_foot_top_right_roi_hist = ()
        left_foot_bottom_left_roi_hist = ()
        left_foot_bottom_right_roi_hist = ()
        right_foot_top_left_roi_hist = ()
        right_foot_top_right_roi_hist = ()
        right_foot_bottom_left_roi_hist = ()
        right_foot_bottom_right_roi_hist = ()
        left_foot_top_left_roi_window = ()
        left_foot_top_right_roi_window = ()
        left_foot_bottom_left_roi_window = ()
        left_foot_bottom_right_roi_window = ()
        right_foot_top_left_roi_window = ()
        right_foot_top_right_roi_window = ()
        right_foot_bottom_left_roi_window = ()
        right_foot_bottom_right_roi_window = ()
        left_foot_top_single_roi_hist = ()
        left_foot_bottom_single_roi_hist = ()
        left_foot_left_single_roi_hist = ()
        left_foot_right_single_roi_hist = ()
        right_foot_top_single_roi_hist = ()
        right_foot_bottom_single_roi_hist = ()
        right_foot_left_single_roi_hist = ()
        right_foot_right_single_roi_hist = ()
        left_foot_top_single_roi_window = ()
        left_foot_bottom_single_roi_window = ()
        left_foot_left_single_roi_window = ()
        left_foot_right_single_roi_window = ()
        right_foot_top_single_roi_window = ()
        right_foot_bottom_single_roi_window = ()
        right_foot_left_single_roi_window = ()
        right_foot_right_single_roi_window = ()

        # For each center point...
        for i in range(0, len(center_points)):
            if self.mouse_count > 1:
                # Initialize Booleans
                left = False
                right = False
                top = False
                bottom = False

                if self.wall1[0] == 0:  # If the wall is Horizontal
                    for j in self.wall1[1]:  # For each point on the line
                        if j[1] > center_points[i][1] and j[0] == center_points[i][0]:
                            top = True
                        else:
                            bottom = True
                elif self.wall1[0] == 1:  # If the wall is vertical
                    for j in self.wall1[1]:  # For each point on the line
                        if j[0] > center_points[i][0] and j[1] == center_points[i][1]:
                            left = True
                        else:
                            right = True

            if self.mouse_count > 2:  # If there are 4 mice
                if self.wall2[0] == 0:  # If wall 2 is horizontal
                    for j in self.wall2[1]:  # For each point on the line
                        if j[1] > center_points[i][1] and j[0] == center_points[i][0]:
                            top = True
                        else:
                            bottom = True
                if self.wall2[0] == 1:  # If wall 2 is vertical
                    for j in self.wall2[1]:  # For each point on the line
                        if j[0] > center_points[i][0] and j[1] == center_points[i][1]:
                            left = True
                        else:
                            right = True
                if top is True:
                    if left is True:
                        top_left = center_points[i]
                        top_left_box = box_list[i]
                        left_foot_top_left_roi_hist = left_foot_roi_hist_buffer[i]
                        right_foot_top_left_roi_hist = right_foot_roi_hist_buffer[i]
                        left_foot_top_left_roi_window = left_foot_roi_window_buffer[i]
                        right_foot_top_left_roi_window = right_foot_roi_window_buffer[i]
                    elif right is True:
                        top_right = center_points[i]
                        top_right_box = box_list[i]
                        left_foot_top_right_roi_hist = left_foot_roi_hist_buffer[i]
                        right_foot_top_right_roi_hist = right_foot_roi_hist_buffer[i]
                        left_foot_top_right_roi_window = left_foot_roi_window_buffer[i]
                        right_foot_top_right_roi_window = right_foot_roi_window_buffer[i]
                elif bottom is True:
                    if left is True:
                        bottom_left = center_points[i]
                        bottom_left_box = box_list[i]
                        left_foot_bottom_left_roi_hist = left_foot_roi_hist_buffer[i]
                        right_foot_bottom_left_roi_hist = right_foot_roi_hist_buffer[i]
                        left_foot_bottom_left_roi_window = left_foot_roi_window_buffer[i]
                        right_foot_bottom_left_roi_window = right_foot_roi_window_buffer[i]
                    elif right is True:
                        bottom_right = center_points[i]
                        bottom_right_box = box_list[i]
                        left_foot_bottom_right_roi_hist = left_foot_roi_hist_buffer[i]
                        right_foot_bottom_right_roi_hist = right_foot_roi_hist_buffer[i]
                        left_foot_bottom_right_roi_window = left_foot_roi_window_buffer[i]
                        right_foot_bottom_right_roi_window = right_foot_roi_window_buffer[i]

            else:  # If there are 2 mice
                if top is True:
                    top_single = center_points[i]
                    top_single_box = box_list[i]
                    left_foot_top_single_roi_hist = left_foot_roi_hist_buffer[i]
                    right_foot_top_single_roi_hist = right_foot_roi_hist_buffer[i]
                    left_foot_top_single_roi_window = left_foot_roi_window_buffer[i]
                    right_foot_top_single_roi_window = right_foot_roi_window_buffer[i]
                elif bottom is True:
                    bottom_single = center_points[i]
                    bottom_single_box = box_list[i]
                    left_foot_bottom_single_roi_hist = left_foot_roi_hist_buffer[i]
                    right_foot_bottom_single_roi_hist = right_foot_roi_hist_buffer[i]
                    left_foot_bottom_single_roi_window = left_foot_roi_window_buffer[i]
                    right_foot_bottom_single_roi_window = right_foot_roi_window_buffer[i]
                if left is True:
                    left_single = center_points[i]
                    left_single_box = box_list[i]
                    left_foot_left_single_roi_hist = left_foot_roi_hist_buffer[i]
                    right_foot_left_single_roi_hist = right_foot_roi_hist_buffer[i]
                    left_foot_left_single_roi_window = left_foot_roi_window_buffer[i]
                    right_foot_left_single_roi_window = right_foot_roi_window_buffer[i]
                elif right is True:
                    right_single = center_points[i]
                    right_single_box = box_list[i]
                    left_foot_right_single_roi_hist = left_foot_roi_hist_buffer[i]
                    right_foot_right_single_roi_hist = right_foot_roi_hist_buffer[i]
                    left_foot_right_single_roi_window = left_foot_roi_window_buffer[i]
                    right_foot_right_single_roi_window = right_foot_roi_window_buffer[i]

        if self.mouse_count > 2:  # If there are 4 mice
            center_points = (top_left, top_right, bottom_left, bottom_right)
            box_list = (top_left_box, top_right_box, bottom_left_box, bottom_right_box)
            left_foot_roi_hist_buffer = [left_foot_top_left_roi_hist,left_foot_top_right_roi_hist,
                                         left_foot_bottom_left_roi_hist,left_foot_bottom_right_roi_hist]
            right_foot_roi_hist_buffer = [right_foot_top_left_roi_hist,right_foot_top_right_roi_hist,
                                         right_foot_bottom_left_roi_hist,right_foot_bottom_right_roi_hist]
            left_foot_roi_window_buffer = [left_foot_top_left_roi_window,left_foot_top_right_roi_window,
                                         left_foot_bottom_left_roi_window,left_foot_bottom_right_roi_window]
            right_foot_roi_window_buffer = [right_foot_top_left_roi_window,right_foot_top_right_roi_window,
                                         right_foot_bottom_left_roi_window,right_foot_bottom_right_roi_window]
        else:  # If there are 2 mice
            if self.wall1[0] == 0:
                center_points = (top_single, bottom_single)
                box_list = (top_single_box, bottom_single_box)
                left_foot_roi_hist_buffer = [left_foot_top_single_roi_hist,left_foot_bottom_single_roi_hist]
                right_foot_roi_hist_buffer = [right_foot_top_single_roi_hist,right_foot_bottom_single_roi_hist]
                left_foot_roi_window_buffer = [left_foot_top_single_roi_window,left_foot_bottom_single_roi_window]
                right_foot_roi_window_buffer = [right_foot_top_single_roi_window,right_foot_bottom_single_roi_window]
            if self.wall1[0] == 1:
                center_points = (left_single, right_single)
                box_list = (left_single_box, right_single_box)
                left_foot_roi_hist_buffer = [left_foot_left_single_roi_hist,left_foot_right_single_roi_hist]
                right_foot_roi_hist_buffer = [right_foot_left_single_roi_hist,right_foot_right_single_roi_hist]
                left_foot_roi_window_buffer = [left_foot_left_single_roi_window,left_foot_right_single_roi_window]
                right_foot_roi_window_buffer = [right_foot_left_single_roi_window,right_foot_right_single_roi_window]

        return box_list, center_points, line_points, left_foot_roi_hist_buffer, left_foot_roi_window_buffer, right_foot_roi_hist_buffer, right_foot_roi_window_buffer

    # Inline Static Member Method: draw_boxes
    # Method to draw boxes on an image
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    @staticmethod
    def draw_boxes(box_list, color, img):
        for i in box_list:
            if len(i) != 0:
                cv2.rectangle(img, i[0], i[1], color, 2)

    # Inline Static Member Method: draw_center_points
    # Method to draw points on an image
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    @staticmethod
    def draw_center_points(point_list, color, img):
        for i in point_list:
            if len(i) != 0:
                cv2.circle(img, i, 1, color, 3)

    # Inline Static Member Method: crop_images
    # Method to crop boxed regions from an image
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    @staticmethod
    def crop_images(img, box_list):
        crop_list = []
        for i in box_list:
            if len(i) != 0:
                crop_list.append(img[i[0][1]:i[1][1], i[0][0]:i[1][0]])
        return crop_list

    # Inline Static Member Method: insert_images
    # Method to insert cropped regions back into image
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    @staticmethod
    def insert_images(box_list, crop_list, orig_img):
        if len(box_list) != 0:  # No mice detected
            for i in range(len(box_list) - 1, -1, -1):
                if len(box_list[i]) != 0:  # Expected mouse not found
                    orig_img[box_list[i][0][1]:box_list[i][1][1], box_list[i][0][0]:box_list[i][1][0]] = crop_list[i]

    # Inline Static Member Method: globalize_center_points
    # Method to convert relative center point coords into global coords
    # Created by Sheldon Reeves on 6/24/15.
    # Language: Python 3.4
    @staticmethod
    def globalize_center_points(box_list, center_points):
        if len(box_list) != 0:  # No mice detected
            for i in range(0, len(box_list)):
                for j in range(0, len(center_points[i])):
                    if center_points[i][j] != 0:
                        center_points[i][j] = list(center_points[i][j])
                        if center_points[i][j][0] != 0:
                            center_points[i][j][0] += box_list[i][0][0]
                        if center_points[i][j][1] != 0:
                            center_points[i][j][1] += box_list[i][0][1]
                        center_points[i][j] = tuple(center_points[i][j])
        return center_points



