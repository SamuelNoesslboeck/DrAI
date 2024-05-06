import cv2
import matplotlib.pyplot as plt

img = cv2.imread( "./infinity.jpg" )
img = cv2.cvtColor( img, cv2.COLOR_BGR2HSV )

fig = plt.figure()

ax1 = fig.add_subplot( 3, 1, 1 )
ax1.imshow( img[ :, :, 0 ] )

ax1 = fig.add_subplot( 3, 1, 2 )
ax1.imshow( img[ :, :, 1 ] )

ax1 = fig.add_subplot( 3, 1, 3 )
ax1.imshow( img[ :, :, 2 ] )

plt.show()