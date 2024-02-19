import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import cv2

SETTINGS = json.load( open( "./config.json", "r" ) )

def img2Hsv( img ):
    img = cv2.cvtColor( img, cv2.COLOR_BGR2HSV )
    return img

def markerDetection( img, h = ( 10, 100 ), s = ( 10, 20 ) ):
    blackWhiteImg = np.where( ( ( img[ :, :, 0 ] >= h[ 0 ] ) & ( img[ :, :, 0 ] <= h[ 1 ] ) 
                              & ( img[ :, :, 1 ] >= s[ 0 ] ) & ( img[ :, :, 1 ] <= s[ 1 ] ) ), 255, 0 )
    
    return blackWhiteImg.astype( np.uint8 )
    
def detectCorners( img ):
    dst = cv2.cornerHarris( img, 15, 21, 0.15 )
    dst = cv2.dilate(dst,None)
    _, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
    dst = np.uint8(dst)

    indexes = np.where( dst == 255 )
    return indexes

def getL2DistToPoint( point, indexes ):
    point = np.array( point ).reshape( -1, 2 )

    yCords = indexes[ 0 ].reshape( -1, 1 )
    xCords = indexes[ 1 ].reshape( -1, 1 )

    cords = np.concatenate( [ yCords, xCords ], axis = -1 )

    distances = np.sum( ( cords - point ) ** 2, axis = -1 ) ** 0.5

    return distances

def getL2Distances( indexes, imgShape ): 
    topLeftDist = getL2DistToPoint( [ 0, 0 ], indexes )
    topRightDist = getL2DistToPoint( [ 0, imgShape[ 1 ] ], indexes )

    bottomLeftDist = getL2DistToPoint( [ imgShape[ 0 ], 0 ], indexes )
    bottomRightDist = getL2DistToPoint( [ imgShape[ 0 ], imgShape[ 1 ] ], indexes )

    return ( topLeftDist, topRightDist, bottomRightDist, bottomLeftDist )

def minL2Dist( distance ):
    return np.argmin( distance )

def transform( img, corners, device = "plattform" ):
    global SETTINGS
    ################################
    # Transform the image
    # coordinates to order: top-left, top-right, bottom-right, bottom-left

    if device == "plattform":
        maxWidth = SETTINGS[ "plattformWidth" ] * 3
        maxHeight = SETTINGS[ "plattformHeight" ] * 3
    else:
        maxWidth = SETTINGS[ "paperWidth" ] * 3
        maxHeight = SETTINGS[ "paperHeight" ] * 3

    destination_corners = [[0, 0], [maxWidth, 0], [maxWidth, maxHeight], [0, maxHeight]]

    corners = np.concatenate( [ np.expand_dims( corners[ :, 1 ], axis = -1 ), np.expand_dims( corners[ :, 0 ], axis = -1 ) ], axis = -1 )
    M = cv2.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))
    final = cv2.warpPerspective( img, M, (destination_corners[2][0], destination_corners[2][1]), flags=cv2.INTER_LINEAR)

    return final

def cornerDistances( indexes, imgWidth, imgHeight ):
    """
    return a list with the x, y coordinates of the points and a tuple consisting of the indexes of the 
    [ { "x": .., "y": .. }, {}.. ], ( top-left-corner, top-right-corner, bottom-left-corner, bottom-right-corner )
    """
    cornerDistances = []
    cornerPositions = []

    #Image Corners sorted by top-left, top-right, bottom-left, bottom-right
    imagePoints = np.array( [ [ 0, 0 ], [ imgWidth, 0 ], [ 0, imgHeight ], [ imgWidth, imgHeight ] ] )


    for i in range( len( indexes[ 0 ] ) ):
        y = indexes[ 0 ][ i ]; x = indexes[ 1 ][ i ]

        p = np.array( [ x, y ] )

        distances = np.sum( ( imagePoints - p ) ** 2, axis = -1 ) ** 0.5

        cornerDistances.append( distances )
        cornerPositions.append( { "x": x, "y": y } )

    cornerDistances = np.array( cornerDistances ).reshape( len( cornerDistances ), 4 )

    topLeftCorner = np.argmin( cornerDistances[ :, 0 ] )
    topRightCorner = np.argmin( cornerDistances[ :, 1 ] )
    bottomLeftCorner = np.argmin( cornerDistances[ :, 2 ] )
    bottomRightCorner = np.argmin( cornerDistances[ :, 3 ] )

    return cornerPositions, ( topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner )

def getDistanceToPoint( a, b ):
    """
    Get the l2 distances of two arrays where each array consists of ( -1, 2 ) and the coordinates are aranged in x, y
    """
    a = np.expand_dims( a, axis = 1 )
    b = np.expand_dims( b, axis = 0 )

    distances = np.sum( ( a - b ) ** 2, axis = -1 ) ** 0.5
    return distances
    
def retransformImg( img, points ):
    markerPoints, _ = points

    realWorldCoords = []
    
    for m_x in range( 2 ):
        for m_y in range( 2 ):

            for x in range( 2 ):
                for y in range( 2 ):
                    p_x = m_x * SETTINGS[ "plattformWidth" ] + ( ( -1 ) ** m_x ) * x * SETTINGS[ "marker-width" ]
                    p_y = m_y * SETTINGS[ "plattformHeight" ] + ( ( -1 ) ** m_y ) * y * SETTINGS[ "marker-height" ]

                    realWorldCoords.append( [ p_x, p_y ] )

    realWorldCoords = np.reshape( realWorldCoords, ( -1, 2 ) )

    objp = np.zeros((1, 16, 3), np.float32)
    objp[0,:,:2] = realWorldCoords

    imageCorners = np.array( [
        [ 0, 0 ],
        [ 0, img.shape[ 1 ] ],
        [ img.shape[ 0 ], 0 ],
        [ img.shape[ 0 ], img.shape[ 1 ] ]
    ])

    markerCenters = np.mean( markerPoints, axis = 1 )

    d = getDistanceToPoint( imageCorners, markerCenters )

    newMarkerPoints = np.zeros_like( markerPoints )
    arangedMarkerCenters = []

    for i in range( 4 ):
        newMarkerPoints[ i ][ :, : ] = markerPoints[ np.argmin( d[ i ] ) ][ :, : ]
        arangedMarkerCenters.append( markerCenters[ np.argmin( d[ i ] ) ] )

    markerPoints = newMarkerPoints

    paperCenter = np.expand_dims( np.mean( markerCenters, axis = 0 ), axis = 0 )

    arangedPoints = np.zeros( ( 16, 2 ), np.float32 )
    for mCIdx in range( 4 ):
        d = getDistanceToPoint( paperCenter, markerPoints[ mCIdx ] )

        p1 = markerPoints[ mCIdx ][ np.argmax( d, axis = -1 ) ]
        p4 = markerPoints[ mCIdx ][ np.argmin( d, axis = -1 ) ]

        #Detect p2
        if mCIdx == 0 or mCIdx == 1:
            sideMiddle = ( arangedMarkerCenters[ 0 ] + arangedMarkerCenters[ 1 ] ) / 2
            sideMiddle[ 0 ] -= 100
        else:
            sideMiddle = ( arangedMarkerCenters[ 2 ] + arangedMarkerCenters[ 3 ] ) / 2
            sideMiddle[ 0 ] += 100

        sideMiddle = np.expand_dims( sideMiddle, axis = 0 )

        d = getDistanceToPoint( sideMiddle, markerPoints[ mCIdx ] )
        p2 = markerPoints[ mCIdx ][ np.argmin( d, axis = -1 ) ]     

        #Detect p3
        if mCIdx == 0 or mCIdx == 2:
            sideMiddle = ( arangedMarkerCenters[ 0 ] + arangedMarkerCenters[ 2 ] ) / 2 
            sideMiddle[ 1 ] -= 100
        else:
            sideMiddle = ( arangedMarkerCenters[ 1 ] + arangedMarkerCenters[ 3 ] ) / 2 #
            sideMiddle[ 1 ] += 100

        sideMiddle = np.expand_dims( sideMiddle, axis = 0 )

        d = getDistanceToPoint( sideMiddle, markerPoints[ mCIdx ] )
        p3 = markerPoints[ mCIdx ][ np.argmin( d, axis = -1 ) ]   

        arangedPoints[  mCIdx * 4 : ( mCIdx + 1 ) * 4 ] = np.squeeze( np.array( [ p1, p2, p3, p4 ] ), axis = 1 )

    arangedPoints = np.reshape( arangedPoints, ( 1, -1, 2 ) )

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera( objp, arangedPoints, [ img.shape[ 1 ], img.shape[ 0 ] ], None, None)
    dst = cv2.undistort( img, mtx, dist, None, mtx )

    return dst

def markerPlattformCoords( img ):
    global SETTINGS
    img = img2Hsv( img )

    img = markerDetection( img, ( SETTINGS[ "markers" ][ "h-min" ], SETTINGS[ "markers" ][ "h-max" ] ), ( SETTINGS[ "markers" ][ "s-min" ], SETTINGS[ "markers" ][ "s-max" ] ) )
    plt.imshow( img )
    plt.show()

    #img = cv2.blur( img, ( 3, 3 ) )

    canny = cv2.Canny( img, 20, 255 )
 
    canny = cv2.blur( canny, ( 3, 3 ) )

    canny = np.where( canny > 40, 255, 0 )
    canny = canny.astype( np.uint8 )
    
    contours, _ = cv2.findContours(image=canny, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

    ######################
    # Draw the contours into a new image

    areas = []
    for i in range( len( contours ) ):
        c = contours[ i ]

        area = cv2.contourArea(c)

        if area > 500:
            areas.append( { "areas": area, "idx": i } )

    areas = sorted( areas, key = lambda x: x[ "areas" ], reverse=True )

    markerCenters = []
    markerPoints = []

    for i in range( len( areas ) ):
        rect = cv2.minAreaRect( contours[ areas[ i ][ "idx" ] ] )
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        

        length = np.sum( ( box[ 0 ] - box[ 1 ] ) ** 2 ) ** 0.5
        width = np.sum( ( box[ 1 ] - box[ 2 ] ) ** 2 ) ** 0.5

        scope = ( length + width ) * 2
        boxArea = length * width

        contourScope = cv2.arcLength( contours[ areas[ i ][ "idx" ] ], True )

        if len( areas ) != 4:
            if abs( 1 - boxArea / cv2.contourArea( contours[ areas[ i ][ "idx" ] ] ) ) < 0.5:
                if abs( 1 - scope / contourScope ) < 0.1:
                    approx = cv2.approxPolyDP( contours[ areas[ i ][ "idx" ] ], 0.05 * cv2.arcLength(contours[ areas[ i ][ "idx" ] ], True), True) 

                    centerApprox = np.reshape( approx, ( -1, 2 ) )
                    markerPoints.append( centerApprox )
                    
                    center = np.sum( centerApprox, axis = 0 ) / len( approx )
                    markerCenters.append( center )

        else:
            approx = cv2.approxPolyDP( contours[ areas[ i ][ "idx" ] ], 0.05 * cv2.arcLength(contours[ areas[ i ][ "idx" ] ], True), True) 

            centerApprox = np.reshape( approx, ( -1, 2 ) )
            markerPoints.append( centerApprox )
            
            center = np.sum( centerApprox, axis = 0 ) / len( approx )
            markerCenters.append( center )

    print( f"Found {len(markerPoints)} markers")

    markerCenters = np.reshape( markerCenters, ( -1, 2 ) )

    paperCenter = np.sum( markerCenters, axis = 0 ) / 4
    return ( markerPoints, paperCenter )

def getOutherPlattformPoints( img, markerPoints, paperCenter ):
    cornerPoints = []
    for j in range( len( markerPoints ) ): 
        distances = np.sum( ( paperCenter - markerPoints[ j ] ) ** 2, -1 ) ** 0.5

        point = markerPoints[ j ][ np.argmax( distances ) ]
        
        cornerPoints.append( point )

    cornerPoints = np.reshape( cornerPoints, ( -1, 2 ) )

    y = cornerPoints[ :, 1 ]; x = cornerPoints[ :, 0 ]
    cornerIndexes = [ y, x ]

    distances = getL2Distances( cornerIndexes, img.shape )

    #Get point index with the minimum l2 distance
    #pointidxs is a list of minimum distances aranged in the order like distances
    pointIdxs = [ minL2Dist( distances[ i ] ) for i in range( len( distances ) ) ]
    
    #get the coordinates of the points 
    cornerPoints = [ ( cornerIndexes[ 0 ][ pointIdxs[ i ] ], cornerIndexes[ 1 ][ pointIdxs[ i ] ] ) for i in range( len( distances ) ) ]
    cornerPoints = np.array( cornerPoints ).reshape( -1, 2 )

    return cornerPoints

def getPaperCorners( img ):
    global SETTINGS
    img = cv2.cvtColor( img, cv2.COLOR_BGR2HSV )
    #img = cv2.blur( img, ( 3, 3 ) )
    #img = cv2.blur( img, ( 3, 3 ) )

    paperImg = markerDetection( img, ( SETTINGS[ "plattform" ][ "h-min" ], SETTINGS[ "plattform" ][ "h-max" ] ), ( SETTINGS[ "plattform" ][ "s-min" ], SETTINGS[ "plattform" ][ "s-max" ] ) )

    #If you remove that dont forget to remove the -20 in the bottom in line 313

    paddedImg = np.zeros( ( paperImg.shape[ 0 ] + 40, paperImg.shape[ 1 ] + 40 ), dtype = np.uint8 )
    paddedImg[ 20:-20, 20:-20 ] = paperImg
    
    canny = cv2.Canny( paddedImg, 20, 255 )

    canny = cv2.blur( canny, ( 3, 3 ) )

    canny = np.where( canny > 40, 255, 0 )
    canny = canny.astype( np.uint8 )

    contours, _ = cv2.findContours(image=canny, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

    areas = []
    for i in range( len( contours ) ):
        c = contours[ i ]

        area = cv2.contourArea(c)

        areas.append( { "areas": area, "idx": i } )

    areas = sorted( areas, key = lambda x: x[ "areas" ], reverse=True )

    paperIdx = areas[ 0 ][ "idx" ]

    approx = cv2.approxPolyDP( contours[ paperIdx ], 0.05 * cv2.arcLength(contours[ paperIdx ], True), True) 

    coords = np.reshape( approx, ( -1, 2 ) ) - 20

    cornerIndexes = [ coords[ :, 1 ], coords[ :, 0 ] ]
    distances = getL2Distances( cornerIndexes, canny.shape )

    #Get point index with the minimum l2 distance
    #pointidxs is a list of minimum distances aranged in the order like distances
    pointIdxs = [ minL2Dist( distances[ i ] ) for i in range( len( distances ) ) ]
    
    #get the coordinates of the points 
    cornerPoints = [ ( cornerIndexes[ 0 ][ pointIdxs[ i ] ], cornerIndexes[ 1 ][ pointIdxs[ i ] ] ) for i in range( len( distances ) ) ]
    cornerPoints = np.array( cornerPoints ).reshape( -1, 2 )

    return cornerPoints

def getCoords( img ):
    #Detect the plattform in the retransformed img and get the outher points
    a, b = markerPlattformCoords( img )
    plattformCords = getOutherPlattformPoints( img, a, b )

    print( "PlattformImg" )
    for i in range( 4 ):
        img = cv2.circle( img, ( plattformCords[ i, 1 ], plattformCords[ i, 0 ] ), 1, ( 255, 0, 0 ), 1 )
        img = cv2.circle( img, ( plattformCords[ i, 1 ], plattformCords[ i, 0 ] ), 10, ( 255, 0, 0 ), 2 )

    plt.imshow( img )
    plt.show()

    plattformImg = transform( img, plattformCords, device = "plattform" )

    paperCoords = getPaperCorners( plattformImg )

    print( "Papercorners" )
    for i in range( 4 ):
        plattformImg = cv2.circle( plattformImg, ( paperCoords[ i, 1 ], paperCoords[ i, 0 ] ), 1, ( 255, 0, 0 ), 1 )
        plattformImg = cv2.circle( plattformImg, ( paperCoords[ i, 1 ], paperCoords[ i, 0 ] ), 10, ( 255, 0, 0 ), 2 )

    plt.imshow( plattformImg )
    plt.show()

    return ( plattformCords, paperCoords )

def drawPoints( img, points ):
    imgCopy = np.copy( img )

    for point in points:
        imgCopy = cv2.circle( imgCopy, ( int( point[ 1 ] ), int( point[ 0 ] ) ), 5, ( 255, 0, 0 ), -1 )

    cv2.imshow( "", imgCopy )
    cv2.waitKey( 0 )

def radtodeg( angle ):
    return angle / ( 2 * np.math.pi ) * 360

def getRealWorldPaperPoints( coords, imgWidth, imgHeight ):
    global SETTINGS
    bottom_right_paper_point = coords[ 1 ][ 2 ]
    bottom_left_paper_point = coords[ 1 ][ 3 ]

    paperRotation = np.arctan2( -( bottom_right_paper_point[ 0 ] - bottom_left_paper_point[ 0 ] ), bottom_right_paper_point[ 1 ] - bottom_left_paper_point[ 1 ] )

    offsetY = ( imgHeight - bottom_left_paper_point[ 0 ] ) / imgHeight * SETTINGS[ "plattformHeight" ]
    offsetX = (  bottom_left_paper_point[ 1 ] ) / imgWidth * SETTINGS[ "plattformWidth" ]

    return { "paperRotation": paperRotation, "offset-X": offsetX, "offset-Y": offsetY }

def getImage():
    #Take photo1
    img1 = cv2.imread( "./images/foo.jpg" )
    img1 = cv2.rotate( img1, cv2.ROTATE_90_COUNTERCLOCKWISE )
    img1 = cv2.rotate( img1, cv2.ROTATE_90_COUNTERCLOCKWISE )
    
    img1 = cv2.copyMakeBorder(img1, 0, 0, 200, 200, cv2.BORDER_CONSTANT )

    plattformCords = markerPlattformCoords( img1 )
    img1 = retransformImg( img1, plattformCords )

    coords = getCoords( img1 ) 

    plattformImg = transform( img1, coords[ 0 ] )

    offsets = getRealWorldPaperPoints( coords, plattformImg.shape[ 1 ], plattformImg.shape[ 0 ] )

    stableDiffImg1 = transform( plattformImg, coords[ 1 ], device = "paper" )

    plt.imshow( stableDiffImg1 )
    plt.show()
    
    #Move Servos
    requests.request( method = "post", url = "http://127.0.0.1:5000/moveServos" )

    #Take photo2
    img2 = cv2.imread( "./test_b50_s0_c50.png" )

    plattformImg = transform( img2, coords[ 0 ] )
    stableDiffImg2 = transform( plattformImg, coords[ 1 ], device = "paper" )

    stableDiffImg2 = cv2.resize( stableDiffImg2, ( stableDiffImg1.shape[ 1 ], stableDiffImg1.shape[ 0 ] ) ) 



if __name__ == "__main__":
    getImage()