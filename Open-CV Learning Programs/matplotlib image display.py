import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('C:\\Users\\Paul\\Pictures\\Ubuntu Photos\\0187e645c2c1c53753cd7b247ccf9eba9de5129971ee97e255ccb9231b7507c8.jpg',0)
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])
plt.show()
