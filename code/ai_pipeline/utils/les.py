import numpy as np
import tqdm
import cv2

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

def Recursiv( contours, currentCont ):
    if len( contours ) == 0:
        return { "dist": 0, "idx": [] }
    
    minReturn = np.inf
    min_contours = []
    min_cont = []

    for cont in contours:
        _contours = contours.copy()
        _contours.remove( cont )
        dist = np.sum( ( currentCont[ "endPoint"] - cont[ "startPoint" ] ) ** 2 ) ** 0.5
        
        if dist < minReturn:
            
            minReturn = dist
            min_contours = _contours
            min_cont = cont

    ret = Recursiv( min_contours, min_cont )
    indexes = [ min_cont[ "contourIdx" ] ]
    indexes += ret[ "idx" ]
    
    return { "dist": minReturn, "idx": indexes }

def Draw( lines, contours, penSize = 3 ):
    p2 = [ 0, 0 ]
    contourPoints = []

    output_lines = []

    for i in range( len( contours ) ):
        area = cv2.contourArea( contours[ i ] )
        startPoint = contours[ i ][ 0, 0, : ]
        endPoint = contours[ i ][ -1, 0, : ]
        contourPoints.append( { "contourIdx": i, "startPoint": startPoint, "endPoint": endPoint } )

    if len( contourPoints ) == 0:
        return lines, [], output_lines
    
    ret = Recursiv( contourPoints, { "idx": -1, "startPoint": np.array( [ 0, 0 ] ), "endPoint": np.array( [ 0, 0 ] ) } )
    
    for i in tqdm.tqdm( ret[ "idx" ] ):
        #Contour drawing
        for l in range( 1, contours[ i ].shape[ 0 ], 1 ):
            p1 = [ int( contours[ i ][ l - 1, 0, 0 ] ), int( contours[ i ][ l - 1, 0, 1 ] ) ]
            p2 = [ int( contours[ i ][ l, 0, 0 ] ), int( contours[ i ][ l, 0, 1 ] ) ]
            
            lines = cv2.line( lines, p1, p2, ( 0, 0, 0 ), penSize )

            output_lines.append( { "p1": p1, "p2": p2 } )

    return lines, len( ret[ "idx" ] ), output_lines


def GetPointsFromImage( orgImgName = "./images/chrisi/original/test4.png", genImgName = "./images/chrisi/merged/overloaded.png", penSize = 2 ):
    '''
    Parameters
    '''
    #Plan the path

    lines_to_draw = []

    org = LoadAndResize( orgImgName )
    gen = LoadAndResize( genImgName )
    
    gesContours = []
    prevNumber = 0
    prevNumberCounter = 0
    while True:
        diff = difference( org, gen )

        lines = diff
        lines = np.array( lines ).astype( np.uint8 )
        cont,_ = cv2.findContours( lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE )
        for i in range( len( cont ) ):
            gesContours.append( cont[ i ] ) 

        lines = org

        lines = np.reshape( lines, ( 512, 768, 1 ) )
        lines = np.concatenate( [ lines, lines, lines ], axis = -1 )

        lines, c, output_lines = Draw( lines, cont, penSize = penSize )

        lines_to_draw = lines_to_draw + output_lines

        if c == prevNumber:
            prevNumberCounter += 1
        else:
            prevNumber = c

        if c == 0:
            break

        if prevNumberCounter > 5:
            break

        org = lines
        org = np.mean( org, axis = -1, keepdims = True )

    return lines_to_draw

def rotMat( angle ):
    mat = np.array( [
        [ np.math.cos( angle ), -np.math.sin( angle ) ],
        [ np.math.sin( angle ), np.math.cos( angle ) ] 
    ] )
    return mat

def pointToRealWorld( p, offsets, paperWidth, paperHeight ):
    p[ 0 ] = p[ 0 ] / 768 * paperHeight
    p[ 1 ] = p[ 1 ] / 512 * paperWidth

    rotatedPosition1 = rotMat( offsets[ "paperRotation" ] ) * p + np.array( [ offsets[ "offset-X" ], offsets[ "offset-Y" ] ] )
    rotatedPosition1[ 0 ], rotatedPosition1[ 1 ] = rotatedPosition1[ 1 ], rotatedPosition1[ 0 ]
    return rotatedPosition1


def linesToRealWorld( points, offsets, config ):
    """
    Converts the pixel values of the points to real world coordinates
    points: list[ dict[ "p1": [ x, y ], "p2": [x, y ] ] ]
    offsets: { "paperRotation": paperRotation, "offset-X": offsetX, "offset-Y": offsetY }
    """

    toDrawOutputs = { "lines": [] }

    for point in points:
        p1 = point[ "p1" ]; p2 = point[ "p2" ]

        p1 = pointToRealWorld( p1, offsets, config[ "paperWidth" ], config[ "paperHeight" ] )
        p2 = pointToRealWorld( p2, offsets, config[ "paperWidth" ], config[ "paperHeight" ] )

        toDrawOutputs[ "lines" ].append( { "p1": p1, "p2": p2 } )
    return toDrawOutputs

if __name__ == "__main__":
    lines = GetPointsFromImage()