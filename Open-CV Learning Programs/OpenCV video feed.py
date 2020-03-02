import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    cv2.imshow('frame',frame)
    
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('grayscale', grayscale)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('hsv', hsv)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()