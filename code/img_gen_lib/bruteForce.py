from multiprocessing import Pool
#import matplotlib.pyplot as plt
#from pipeline import *
import numpy as np
import cv2

def detectLines( image : np.ndarray ) -> np.ndarray:
    return cv2.Canny( image, 10, 80 )


def Recursiv( contours, currentCont ):
    if len( contours ) == 0:
        return { "dist": 0, "idx": [] }
    minReturn = np.inf

    for cont in contours:
        _contours = contours.copy()
        _contours.remove( cont )
        ret = Recursiv( _contours, cont )

        dist = ret[ "dist" ] + np.sum( ( currentCont[ "endPoint"] - cont[ "startPoint" ] ) ** 2 ) ** 0.5
        
        if dist < minReturn:
            indexes = [ currentCont[ "contourIdx" ] ] + ret[ "idx" ]
            minReturn = dist
    
    return { "dist": minReturn, "idx": indexes }

if __name__ == "__main__":
    import time

    start = time.time()
    lines = cv2.imread( "./images/chrisi/merged/overloaded.png", cv2.IMREAD_GRAYSCALE )
    lines = cv2.resize( lines, ( 768, 512 ) )
    lines = 255 - lines

    cont,_ = cv2.findContours( lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE )

    lines = np.ones( ( 512, 768, 3 ), dtype = np.uint8 ) * 255

    #21 länge, 14,8 breite
    gesPixDistance = 0
    p2 = ( 0, 0 )
    contourPoints = []
    for i in range( len( cont ) ):
        area = cv2.contourArea( cont[ i ] )
        if area > 20:
            startPoint = cont[ i ][ 0, 0, : ]
            endPoint = cont[ i ][ -1, 0, : ]
            contourPoints.append( { "contourIdx": i, "startPoint": startPoint, "endPoint": endPoint } )

    gesIndexes = []
    startContour =  { "contourIdx": -1, "startPoint": np.array( [ 0, 0 ] ), "endPoint": np.array( [ 0, 0 ] ) }
    for i in range( 0, ( len( contourPoints ) // 8 + 1 ) * 8, 8 ):
        ret = Recursiv( contourPoints[ i : min( ( i + 8 ), len( contourPoints ) ) ], startContour )
        gesIndexes += ret[ "idx" ]
        startPoint = cont[ i ][ 0, 0, : ]
        endPoint = cont[ i ][ -1, 0, : ]
        contourPoints.append( { "contourIdx": i, "startPoint": startPoint, "endPoint": endPoint } )
        startContour = { "contourIdx": i, "startPoint": startPoint, "endPoint": endPoint }
    
    print( len( gesIndexes ) )

    gesPixDistance = 0
    for i in gesIndexes:
        for l in range( 1, cont[ i ].shape[ 0 ], 1 ):
            p1 = ( int( cont[ i ][ l - 1, 0, 0 ] ), int( cont[ i ][ l - 1, 0, 1 ] ) )

            if l == 1:
                gesPixDistance += ( ( ( p1[ 0 ] - p2[ 0 ] ) / 768 * 21 ) ** 2 + ( ( p1[ 1 ] - p2[ 1 ] ) / 512 * 14.8 ) ** 2 ) ** 0.5
            
            p2 = ( int( cont[ i ][ l, 0, 0 ] ), int( cont[ i ][ l, 0, 1 ] ) )
            lines = cv2.line( lines, p1, p2, ( 0, 0, 0 ), 1 )
            gesPixDistance += ( ( ( p1[ 0 ] - p2[ 0 ] ) / 768 * 21 ) ** 2 + ( ( p1[ 1 ] - p2[ 1 ] ) / 512 * 14.8 ) ** 2 ) ** 0.5
            #lines = cv2.circle( lines, ( cont[ i ][ 0, 0, 0 ], cont[ i ][ 0, 0, 1 ] ), 5, ( 255, 0, 0 ), -1 )

            cv2.imshow( "", lines )
            cv2.waitKey( 1 )

    end = time.time()
    print( ( end - start ) )
    print( "Pixeldistance:", gesPixDistance )
    cv2.imwrite( "./images/test/test1.png", lines )
    #orgImg = cv2.imread( "./images/test/line.png", cv2.IMREAD_GRAYSCALE )
    #orgImg = cv2.resize( orgImg, ( 768, 512 ) )
    #ov = overlapImg( orgImg, lines )
    #cv2.imwrite( "./images/test/test.png", ov )