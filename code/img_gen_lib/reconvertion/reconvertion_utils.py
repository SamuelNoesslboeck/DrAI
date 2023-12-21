import cv2
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import numpy as np
import time
import cv2


def detectCornersOfPlatform( img ):
    imgHeight, imgWidth = img.shape

    ###Use Canny for Edges
    canny = cv2.Canny( img, 10, 40 )
    canny = cv2.blur( canny, ( 3, 3 ) )

    ###################
    # Find Contours 
    # sort by size 
    # get only contours greater than 20
    # get the outside border of a contour and not the one inside onother

    contours, hierarchy = cv2.findContours(image=canny, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[ 0 ]


    ######################
    # Draw the contours into a new image
    image_copy = np.zeros( ( imgHeight, imgWidth ), dtype = np.uint8 )
    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(255, 255, 255), thickness=1)

    #############################
    # Detect contours with corner Harris
    # Draw the detected corners into a new image
    # Get the corner positions by simply searching for the color 255

    dst = cv2.cornerHarris( image_copy, 17, 29, 0.1)
    dst = cv2.dilate(dst,None)
    ret, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
    dst = np.uint8(dst)

    indexes = np.where( dst == 255 )

    return indexes


def cornerDistances( indexes, imgWidth, imgHeight ):
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


def transformPlatform( img ):
    imgWidth = img.shape[ 1 ]; imgHeight = img.shape[ 0 ]

    ###########################################################################################################################################
    ###Detect Platform and transform the image 
    ###########################################################################################################################################
    platform = np.zeros( ( imgHeight, imgWidth ), dtype = np.uint8 )
    platform = np.where( ( img[ :, :, 0 ] < 70 ) & ( ( img[ :, :, 1 ] > 50 ) & ( img[ :, :, 1 ] < 140 ) ) & ( img[ :, :, 2 ] > 220 ), 255, 0 )
    platform = platform.astype( np.uint8 )

    indexes = detectCornersOfPlatform( platform )

    #############################
    cornerPositions, ( topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner ) = cornerDistances( indexes, imgWidth, imgHeight )

    ################################
    # Transform the image
    # Rearrange coordinates to order: top-left, top-right, bottom-right, bottom-left

    corners = np.array( [ [ cornerPositions[ topLeftCorner ][ "x" ], cornerPositions[ topLeftCorner ][ "y" ] ],
                        [ cornerPositions[ topRightCorner ][ "x" ], cornerPositions[ topRightCorner ][ "y" ] ],
                        [ cornerPositions[ bottomRightCorner ][ "x" ], cornerPositions[ bottomRightCorner ][ "y" ] ],
                        [ cornerPositions[ bottomLeftCorner ][ "x" ], cornerPositions[ bottomLeftCorner ][ "y" ] ] ] )

    width1 = np.sum( ( corners[ 0 ] - corners[ 1 ] ) ** 2 ) ** 0.5
    width2 = np.sum( ( corners[ 3 ] - corners[ 2 ] ) ** 2 ) ** 0.5
    maxWidth = int( max( width1, width2 ) )

    height1 = np.sum( ( corners[ 0 ] - corners[ 3 ] ) ** 2 ) ** 0.5
    height2 = np.sum( ( corners[ 1 ] - corners[ 2 ] ) ** 2 ) ** 0.5
    maxHeight = int( max( height1, height2 ) )

    destination_corners = [[0, 0], [maxWidth, 0], [maxWidth, maxHeight], [0, maxHeight]]

    M = cv2.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))
    final = cv2.warpPerspective( img, M, (destination_corners[2][0], destination_corners[2][1]), flags=cv2.INTER_LINEAR)

    return final


def detectCornersOfPaper( img ):
    img = cv2.blur( img, ( 5, 5 ) )
    img = cv2.blur( img, ( 5, 5 ) )

    ###Use Canny for Edges
    canny = cv2.Canny( img, 20, 60 )
    canny = cv2.blur( canny, ( 2, 2 ) )

    canny = np.where( canny > 0, 255, 0 )
    canny = canny.astype( np.uint8 )

    ###################
    # Find Contours 
    # sort by size 
    # get only contours greater than 20
    # get the outside border of a contour and not the one inside onother

    contours, hierarchy = cv2.findContours(image=canny, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    hierarchy = hierarchy[ 0 ]

    ######################
    # Draw the contours into a new image

    lengths = []
    for i in range( len( contours ) ):
        c = contours[ i ]

        l = np.sum( np.sum( ( c[ 1:,0, : ] - c[ :-1,0, : ] ) ** 2, axis = -1 ) ** 0.5 )
        lengths.append( l )

    upperCont = np.argmax( lengths )
    copyImg = np.zeros_like( canny )
    cv2.drawContours(image=copyImg, contours=contours, contourIdx=upperCont, color=(255, 255, 255), thickness=1)


    #############################
    # Detect contours with corner Harris
    # Draw the detected corners into a new image
    # Get the corner positions by simply searching for the color 255

    dst = cv2.cornerHarris( copyImg, 17, 29, 0.1 )
    dst = cv2.dilate(dst,None)
    _, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
    dst = np.uint8(dst)
    
    indexes = np.where( dst == 255 )

    return indexes


def transformImg( img ):
    imgHeight, imgWidth, _ = img.shape

    newImg = np.where( ( ( img[ :, :, 2 ] < 240 ) & ( img[ :, :, 2 ] > 100 ) & ( img[ :, :, 0 ] > 50 ) ), 255, 0 )
    newImg = cv2.blur( newImg, ( 3, 3 ) )
    newImg = newImg.astype( np.uint8 )

    #################
    # Detect top-left and top-right corner

    indexes = detectCornersOfPaper( newImg[ : imgHeight // 2, : ] )
    cornerPositions, ( topLeftCorner, topRightCorner, _, _ ) = cornerDistances( indexes, img.shape[ 1 ], img.shape[ 0 ] )

    topLeftCornerCoords = [ cornerPositions[ topLeftCorner ][ "x" ], cornerPositions[ topLeftCorner ][ "y" ] ]
    topRightCornerCoords = [ cornerPositions[ topRightCorner ][ "x" ], cornerPositions[ topRightCorner ][ "y" ] ]

    ################
    # Detect bottom-left and bottom-right corner
    bottomImg = newImg[ imgHeight // 2 :, : ]
    bottomImg = cv2.flip( bottomImg, 0 )
    bottomImg = cv2.flip( bottomImg, 1 )

    indexes = detectCornersOfPaper( bottomImg )
    cornerPositions, ( topLeftCorner, topRightCorner, _, _ ) = cornerDistances( indexes, img.shape[ 1 ], img.shape[ 0 ] )

    bottomRightCornerCoords = [ imgWidth - cornerPositions[ topRightCorner ][ "x" ], imgHeight - cornerPositions[ topRightCorner ][ "y" ] ]
    bottomLeftCornerCoords = [ imgWidth - cornerPositions[ topLeftCorner ][ "x" ], imgHeight - cornerPositions[ topLeftCorner ][ "y" ] ]

    corners = np.array( [ topLeftCornerCoords,
                        topRightCornerCoords,
                        bottomLeftCornerCoords,
                        bottomRightCornerCoords ] )

    minY = min( corners[ 0, 1 ], corners[ 1, 1 ] )
    minX = min( corners[ 0, 0 ], corners[ 2, 1 ] )
    
    maxX = min( corners[ 1, 0 ], corners[ 3, 0 ] )
    maxY = min( corners[ 2, 1 ], corners[ 3, 1 ] )


    final = img[ minY : maxY, minX : maxX ]
    return final, ( minX, minY, maxX, maxY )



if __name__ == "__main__":

    pImg = cv2.imread( "./PapierTest/PaperTest.jpeg" )
    p = transformPlatform( pImg )

    iImg = cv2.imread( "./final.jpg" )
    i, points = transformImg( iImg )
