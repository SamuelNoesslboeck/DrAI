import numpy as np
import serial
import json
import cv2

def setupSerial():
    ser = serial.Serial()

    ser.baudrate = 115_200
    ser.port = "COM0"

    ser.open()

    return ser


def waitForStart():
    input( "Start:" )


ser = setupSerial()

info = json.loads( open( "./data.json", "r" ) )

while True:
    waitForStart()

    serial.write( f"{info['startKeyword']}".encode( "ascii" ) )

    if info[ "compromise" ]:
        imageBufferLength = serial.read( info[ "maxImageBufferLength" ] )

        imageBuffer = serial.read( imageBufferLength )

        arr = np.frombuffer( imageBuffer, np.uint8 )
        arr = np.reshape( arr, ( 1, -1 ) )

        img = cv2.imdecode( arr, cv2.IMREAD_COLOR )

    else:
        imgSize = serial.read( info[ "maxImageBufferLength" ] )

        imgSize = imgSize.replace( " ", "" )
        imgSize = imgSize.split( "x" )
        
        i = 0

        mergedImage = np.zeros( ( imgSize[ 0 ], imgSize[ 1 ], imgSize[ 2 ] ) )
        while i < imgSize[ 0 ]:
            numBytes = int( imgSize[ 1 ] ) * 3

            imgBytesArr = serial.read( numBytes )
            arr = np.frombuffer( imgBytesArr, np.uint8 )

            try:
                img = np.reshape( arr, ( 1, imgSize[ 1 ], 3 ) )

                mergedImage[ i, :, : ] = img

                serial.write( " " * ( info[ "maxImageBufferLength" ] - 4 ) + "True" )
            except:
                serial.write( " " * ( info[ "maxImageBufferLength" ] - 5 ) + "False" )
            
        img = mergedImage