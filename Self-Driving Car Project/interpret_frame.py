"""
This program takes an input frame and the currently active driving command and gives the user
visual feedback on the live camera stream of what the car is doing at a given moment.
"""
import driving

import cv2
import logging

def whats_going_on(frame):
    height, width, _ = frame.shape
    overlay_height = height // 10
    if driving.isStopped():
        overlay = cv2.rectangle(frame, (0, height-overlay_height), (width, height), (0, 0, 128), -1)
    
    elif driving.isTurnedLeft():
        overlay = cv2.rectangle(frame, (0, height-overlay_height), (width//2, height), (0, 128, 0), -1)
    
    elif driving.isTurnedStraight() and driving.isDrivingForwards():
        overlay = cv2.rectangle(frame, (0, height-overlay_height), (width, height), (0, 128, 0), -1)
    
    elif driving.isBackingUp():
        overlay = cv2.rectangle(frame, (0, height-overlay_height), (width, height), (0, 128, 128), -1)
    
    elif driving.isTurnedRight():
        overlay = cv2.rectangle(frame, (width//2, height-overlay_height), (width, height), (0, 128, 0), -1)
        
    return overlay