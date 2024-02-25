import matplotlib.pyplot as plt
import numpy as np
import json
import cv2

SETTINGS = json.load( open( "./config.json", "r" ) )

def markerDetection( img, h = ( 10, 100 ), s = ( 10, 20 ) ):
    blackWhiteImg = np.where( ( ( img[ :, :, 0 ] >= h[ 0 ] ) & ( img[ :, :, 0 ] <= h[ 1 ] ) 
                              & ( img[ :, :, 1 ] >= s[ 0 ] ) & ( img[ :, :, 1 ] <= s[ 1 ] ) ), 255, 0 )
    
    return blackWhiteImg.astype( np.uint8 )
    

img = cv2.imread( "./plattform.png" )
img = cv2.cvtColor( img, cv2.COLOR_BGR2HSV ) 

fig = plt.figure()

ax1 = fig.add_subplot( 2, 2, 1 )
ax1.imshow( img[ :, :, 0 ] )

ax1 = fig.add_subplot( 2, 2, 2 )
ax1.imshow( img[ :, :, 1 ] )

ax1 = fig.add_subplot( 2, 2, 3 )
ax1.imshow( img[ :, :, 2 ] )
plt.show()

paperImg = markerDetection( img, ( SETTINGS[ "pen" ][ "h-min" ], SETTINGS[ "pen" ][ "h-max" ] ), ( SETTINGS[ "pen" ][ "s-min" ], SETTINGS[ "pen" ][ "s-max" ] ) )

plt.imshow( paperImg )
plt.show()