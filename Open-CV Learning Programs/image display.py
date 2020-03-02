import cv2
import numpy as np

img = cv2.imread('C:\\Users\\Paul\\Pictures\\Ubuntu Photos\\0822dfa58e210551db70ea6335392055f89cf37266108bbcd1a37a588313d037.jpg', 0)
cv2.imshow('image', img)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
elif k == ord('s'):
    cv2.imwrite('F:\\COMP 444 Embedded - Robotic Programming\\graysceenery.png', img)
    cv2.destroyAllWindows()
    
