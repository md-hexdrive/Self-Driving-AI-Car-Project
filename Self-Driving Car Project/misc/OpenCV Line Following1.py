import cv2
import numpy as np
import picamera
import logging
import math
from time import sleep

def detect_edges(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('hsv', hsv)
    lower_black = np.array([60,40,40])
    upper_black = np.array([150,255,255])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    cv2.imshow('mask', mask)
    edges = cv2.Canny(mask, 200, 400)
    
    return edges

def region_of_interest(edges):
    height, width = edges.shape
    mask = np.zeros_like(edges)
    
    # only focus on bottom half of the screen
    polygon = np.array([[
        (0, height * 1 / 2),
        (width, height * 1 / 2),
        (width, height),
        (0, height),
        ]], np.int32)
    
    cv2.fillPoly(mask, polygon, 255)
    cropped_edges = cv2.bitwise_and(edges, mask)
    return cropped_edges

def detect_line_segments(cropped_edges):
    rho = 1
    angle = np.pi / 180
    min_threshold = 10
    line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, np.array([]),
                                    minLineLength = 8, maxLineGap = 4)
    return line_segments


def average_slope_intercept(frame, line_segments):
    
    lane_lines = []
    if line_segments is None:
        logging.info('No lane lines detected')
        return lane_lines
    
    height, width, _ = frame.shape
    left_fit = []
    right_fit = []
    
    boundary = 1/3
    left_region_boundary = width * (1 - boundary)
    right_region_boundary = width * boundary
    
    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                logging.info('skipping vertical line segment (slope = inf): %s' %line_segment)
                continue
            fit = np.polyfit((x1, x2),(y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))
    
    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))
    
    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))
    
    logging.debug('lane lines: %s' % lane_lines)
    
    return lane_lines


def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height
    y2 = int(y1 * 1 /2)
    
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]
    

def detect_lane(frame):
    
    edges = detect_edges(frame)
    cropped_edges = region_of_interest(edges)
    line_segments = detect_line_segments(cropped_edges)
    lane_lines = average_slope_intercept(frame, line_segments)
    
    return lane_lines

def display_lines(frame, lines, line_color = (0, 255, 0), line_width = 2):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image

def compute_steering_angle(frame, lane_lines):
    if len(lane_lines) == 0:
        logging.info("No lane lines detected, do nothing")
        return -90
    
    height, width, _ = frame.shape
    if len(lane_lines) == 1:
        logging.info("Only detected one lane line, just follow it. %s" % lane_lines[0])
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
    else:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        mid = int(width / 2)
        x_offset = (left_x2 + right_x2) / 2 - mid
    
    y_offset = int(height / 2)
    
    angle_to_mid_radian = math.atan(x_offset/y_offset)
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)
    steering_angle = angle_to_mid_deg + 90
    
    logging.debug('new steering angle %s' % steering_angle)
    return steering_angle

def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width = 5):
    heading_image = np.zeros_like(frame)
    height, width, _ = frame.shape
    
    # figure out the heading line from steering angle
    # heading line (x1,y1) is always center bottom of the screen
    # (x2, y2) requires a bit of trigonometry

    # Note: the steering angle of:
    # 0-89 degree: turn left
    # 90 degree: going straight
    # 91-180 degree: turn right
    
    steering_angle_radian = steering_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
    y2 = int(height / 2)
    
    cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)
    
    heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)
    
    return heading_image
    
logging.basicConfig(level=logging.INFO)
"""
frame = cv2.imread('/home/pi/DeepPiCar/driver/data/road1_240x320.png')
cv2.imshow('normal frame', frame)

lane_lines = detect_lane(frame)

lane_lines_image = display_lines(frame, lane_lines)
cv2.imshow('lane lines', lane_lines_image)

steering_angle = compute_steering_angle(frame, lane_lines)

heading_image = display_heading_line(lane_lines_image, steering_angle)
cv2.imshow('heading line', heading_image)

#sleep(20)
"""
#cap = cv2.VideoCapture('/home/pi/DeepPiCar/models/lane_navigation/data/images/video01.avi')
cap = cv2.VideoCapture(0)

cap.set(3, 320)
cap.set(4, 240)


while True:
    
    ret, frame = cap.read()
    cv2.imshow('normal', frame)
    
    lane_lines = detect_lane(frame)
    
    lane_lines_image = display_lines(frame, lane_lines)
    cv2.imshow('lane lines', lane_lines_image)
    
    steering_angle = compute_steering_angle(frame, lane_lines)

    heading_image = display_heading_line(lane_lines_image, steering_angle)
    cv2.imshow('heading line', heading_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()