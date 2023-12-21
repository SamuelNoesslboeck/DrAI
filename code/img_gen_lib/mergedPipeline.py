import drawingSoftware
import reconvertion_utils
import numpy as np
import json
import cv2

def rotPoint( alpha ):
    rot = np.array( [
        [ np.math.cos( alpha ), -np.math.sin( alpha ) ],
        [ np.math.sin( alpha ), np.math.cos( alpha ) ]
    ])
    return rot

def LoadAndResize( imgName ):
    org = cv2.imread( imgName, cv2.IMREAD_GRAYSCALE )
    org = cv2.resize( org, ( 768, 512 ) )
    org = np.array( org ).reshape( 512, 768, 1 )
    return org

def detectLines( image : np.ndarray ) -> np.ndarray:
    return cv2.Canny( image, 10, 80 )

def difference( orgImg, genImg ) -> np.ndarray:
    diff = np.where( ( genImg <= 220 ) & ( orgImg >= 220 ), 255, 0 )
    return diff





if __name__ == "__main__":
    '''
    PAPERWIDTH = 21.5
    PAPERHEIGHT = 14

    PLATTFORMWIDTH = 30
    PLATTFORMHEIGHT = 20

    originalImg = cv2.imread( "./PapierTest/PaperTest.jpeg" )

    plattformImg = reconvertion_utils.transformPlatform( originalImg )
    img, ( topLeftPoint, angle ) = reconvertion_utils.transformImg( plattformImg )

    topLeftRealPoint = np.array( [ topLeftPoint[ 0 ] * PLATTFORMWIDTH / plattformImg.shape[ 1 ],  topLeftPoint[ 1 ] * PLATTFORMHEIGHT / plattformImg.shape[ 0 ] ] )

    cv2.imwrite( "./orgImg.png" )
    '''

    #get a list of points to draw
    #the list contains json elements with p1: ( x, y ), p2: ( x, y )



    import os

    files = os.listdir( "./SamsPictures/Original/" )

    for file in files:
        lines = drawingSoftware.GetPointsFromImage( orgImgName = "./test.png", genImgName = "./SamsPictures/Original/" + file )

        data = { "contour": lines }

        n = file.replace( ".jpg", "" )
        n = n.replace( ".png", "" )
        json.dump( data, open( f"./{n}.json", "w+" ) )

    '''
    for l in lines:
        p1 = np.array( l[ "p1" ] ).reshape( -1, )
        p1[ 1 ] = -p1[ 1 ]

        p1 = rotPoint( angle ) * p1 
        p1[ 0 ] *= ( PAPERWIDTH / 768 )
        p1[ 1 ] *= ( PAPERHEIGHT / 512 )

        p1 += topLeftRealPoint
        
    '''
    
    