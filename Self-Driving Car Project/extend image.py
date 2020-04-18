import cv2
import numpy as np

import os

frame = cv2.imread("/home/pi/Desktop/test_image.jpg")
height, width, _ = frame.shape
print(frame.shape)
cv2.imshow("frame", frame)
mod = np.zeros((height+height//10, width, _), np.int32)
    
mod[:height,:width]=frame
print(mod.shape)
#mod = cv2.rectangle(mod, (0, height), (width, height+height//10), (0, 128, 0), -1)
cv2.imshow("modified", mod)
key = cv2.waitKey(0) & 0xFF

cv2.destroyAllWindows()