import cv2
import numpy as np
import os
import datetime

cap = cv2.VideoCapture("rtsp://admin:123456@192.168.0.15")
#cap = cv2.VideoCapture("tcp://192.168.0.15:8000/")

output_dir="C:\\Users\\Paul\\Videos\\Security_Camera_Recordings"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
file_name=datetime.datetime.now().strftime("%Y-%b-%d %I-%M-%S%p")
print(file_name)
output_path = os.path.join(output_dir, file_name+".avi")

resolution = (640, 480)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, 25.0, resolution)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

while (cap.isOpened()):
    ret, frame = cap.read()
    
    
    if ret == True:
        frame = cv2.resize(frame, resolution)
        
        cv2.imshow('frame',frame)
        
        out.write(frame)
    
        #grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('grayscale', grayscale)
        
        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #cv2.imshow('hsv', hsv)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()