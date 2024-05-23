import cv2
import numpy as np

# choose codec according to format needed
fourcc = cv2.VideoWriter_fourcc(*'DIVX') 
video = cv2.VideoWriter('video.avi', fourcc, 10., (512, 720))


for j in range(0,100):
    img = np.ones( ( 512, 720, 3 ), dtype = np.uint8 ) * 255
    img = cv2.line( img, ( j * 10, 720 - j * 20 ), ( j * 3, 100 ), ( 0, 0, 0 ), 5  )
    img = cv2.resize(img,(512, 720))
    video.write(img)

video.release()