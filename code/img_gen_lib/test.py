import matplotlib.pyplot as plt
import cv2
import os

directory = "samuel2"

orgImgPath = f"./images/{directory}/original/"
fileName = os.listdir( orgImgPath )[ 0 ]
img1 = cv2.imread( orgImgPath + fileName )

genImgPath = f"./images/{directory}/merged/"
fileName = os.listdir( genImgPath )[ 0 ]
img2 = cv2.imread( genImgPath + fileName )

fig = plt.figure()

ax1 = fig.add_subplot( 2, 1, 1 )
ax1.imshow( img1 )
ax1.set_title( "original" )

ax2 = fig.add_subplot( 2, 1, 2 )
ax2.imshow( img2 )
ax2.set_title( "merged" )

fig.tight_layout()
plt.show()