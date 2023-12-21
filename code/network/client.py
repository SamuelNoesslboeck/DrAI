import serial
import json
import cv2
import numpy as np

def setupSerial():
    ser = serial.Serial()
    ser.baudrate = 115_200
    ser.port = "COM1"

    ser.open()

    return ser

def setupCamera():
    cap = cv2.VideoCapture( 0 )

    ret, frame = cap.read()

    return cap


ser = setupSerial()
cap = setupCamera()

info = json.loads( open( "./data.json", "r" ) )

while True:
    if ser.is_open:
        bytes = ser.read( info[ "maxImageBufferLength" ] )
        msg = bytes.decode( "ascii" )

        if msg == "img":
            ret, frame = cap.read()

            if ret:
                if info[ "compromiseImg" ]: 
                    conv, buff = cv2.imencode( info[ "compromisingType" ], frame )

                    if conv:
                        buffLength = " " * info[ "maxImageBufferLength" ] - len( buff )
                        ser.write( buffLength.encode( "ascii" ) )
                        ser.write( buff.tobytes() )
                    
                    else:
                        print( "Error converting camera image into a buffer" )

                else:
                    conv = True

                    imgSize = " " * info[ "maxImageBufferLength" ] + frame.shape[ 0 ] + "x" + frame.shape[ 1 ]
                    
                    serial.write( imgSize )

                    i = 0
                    while i < frame.shape[ 0 ]:
                        buff = np.array( frame[ i, :, : ] ).reshape( -1, )
                        bytesArray = buff.tobytes()

                        serial.write( bytesArray )

                        check = serial.read( info[ "maxImageBufferLength" ] )

                        if check.decode( "ascii" )[ -4 : ] == "True":
                            i += 1

            else:
                print( "Error capturing camera image" )
    

