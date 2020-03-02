import numpy as np
import cv2

cap = cv2.VideoCapture('C:\\Users\\Paul\\Videos\\ANDROID PHONE DEC 2014 098.3gp')

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('C:\\Users\\Paul\\Videos\\The Elements of the Periodic Table Song correctly flipped with no audio.avi', fourcc, 20.0, (640, 480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret== True:
        frame = cv2.flip(frame,1)
        frame = cv2.flip(frame,0)
        
        out.write(frame)
        
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
out.release()

cv2.destroyAllWindows()
        
