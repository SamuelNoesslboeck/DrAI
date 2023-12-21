import cv2
import numpy as np

img = np.ones( ( 512, 768, 3 ) ) * 255

cv2.imwrite( "./test.png", img )