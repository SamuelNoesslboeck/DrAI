import numpy as np
import serial
import cv2

class RPClient():
    def __init__( self, port = "COM1" ):
        self.ser = serial.Serial( port, 9600 )
        
    def getImage( self ):
        self.ser.write( "send_img\n".encode() )

        length = self.ser.read( 1024 )
        length = length.decode()

        imgBytes = self.ser.read( length )

        decodedImgBytes = imgBytes.decode()
        numpyArray = np.fromstring( decodedImgBytes, np.uint8 )
        
        numpyArray = numpyArray.reshape( 1, -1 )

        img = cv2.imdecode( numpyArray, cv2.IMREAD_COLOR )

        configData = self.ser.readline()
        return img, configData