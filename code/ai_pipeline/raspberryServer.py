# See 
# https://opensource.com/article/20/5/usb-port-raspberry-pi-pythonpu

from picamera import PiCamera
import serial
import time
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
        imgBytes = imgBytes.encode()

        bufferLength = ( 1024 - len( imgBytes ) ) * " " + str( len( imgBytes ) )
        bufferLength = bufferLength.encode()

        ser.write( bufferLength )
        ser.write( imgBytes.encode() )

