#import numpy as np
import cv2
from time import sleep
cap = cv2.VideoCapture('C:\\Users\\Paul\\Videos\\ANDROID PHONE DEC 2014 098.3gp')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

for i in range(0, 19):
    print(cap.get(i))
while(cap.isOpened()):
    ret, frame = cap.read()
    #sleep(.025)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
