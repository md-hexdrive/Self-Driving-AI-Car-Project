import cv2
import numpy as np


radius = 100
img = np.zeros((512,512, 3), np.uint8)

#cv2.rectangle(img, (0,0), (512,512), (255,255,255), -1)
cv2.circle(img, (256,256), radius, (0,0,255), 75, lineType = cv2.LINE_AA)

pts = np.array([[256,256], [500,256]], np.int32)
pts = pts.reshape((-1,1,2))
cv2.polylines(img, [pts],True,(255,255,255))


cv2.imshow('logo',img)
