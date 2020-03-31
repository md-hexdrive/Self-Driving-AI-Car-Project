import cv2
import numpy as np

cap = cv2.VideoCapture(0)
i = 0

while True:
    ret, frame = cap.read()
    
    cv2.imshow('frame', frame)
    
    key = cv2.waitKey(1) 
    if key == ord(' '):
        cv2.imwrite("/home/pi/Desktop/Capture_" + str(i) + ".png", frame)
        i += 1
    
    if key == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()