from picamera import PiCamera
import serial
import time
import json
import cv2

ser = serial.Serial( "/dev/ttyACM0", 9600 )
cam = PiCamera()

while True:
    msg = ser.readline()
    msg = msg.decode( "utf-8" )

    print( ">>> Recived Msg over Serial" )
    print( ">>> Msg: " )
    print( msg )

    if msg == "send_img":
        cam.start_preview()
        time.sleep( 0.1 )
        cam.capture( "/home/pi/Desktop/image.png" )

        img = cv2.imread( "/home/pi/Desktop/image.png" )
        img = cv2.imencode( ".png", img )[ 1 ]
        imgBytes = img.toString()

        bufferLength = ( 1024 - len( imgBytes ) ) * " " + str( len( imgBytes ) )
        bufferLength = bufferLength.encode( "ascii" )

        ser.write( bufferLength )
        ser.write( imgBytes.encode( "ascii" ) )

        try:
            jsonData = json.load( open( "./config.json", "r" ) )
        except:
            jsonData = { "Error": "no config.json file on the raspberry pi. Check if the setup was correctly completetd" }

        data = json.dumps( jsonData )
        ser.write( data.encode( "ascii" ) )
        ser.flush()

        

