from flask import Flask, render_template, send_file
import matplotlib.pyplot as plt
import cv2
import numpy as np
from io import BytesIO
import pdars
import flask
import time
import json


SETTINGS = json.load( open( "./config.json", "r" ) )


try:
    from picamera import PiCamera, Color
    camera = PiCamera()

    camera.brightness = SETTINGS[ "camera" ][ "brightness" ] 
    camera.sharpness = SETTINGS[ "camera" ][ "sharpness" ] 
    camera.contrast = SETTINGS[ "camera" ][ "contrast" ]

    camera.start_preview()
    time.sleep( 0.5 )
    camera.capture( "./image.jpg" )
except:
    print( "error no picamera library" )

app = Flask(__name__)

SETTINGS = json.load( open( "./config.json", "r" ) )
json.dump( SETTINGS, open( "./config_copy.json", "w+" ))


# Load and convert the image to HSV
image_path = './image.jpg'  # Replace with your image path
image = cv2.imread(image_path)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

@app.route('/')
def index():
    return render_template('index.html')

###
#
# Save values
#
###

@app.route( "/saveCameraValues", methods = [ "POST" ] )
def saveCameraValues():
    configSettings = json.load( open( "./config.json", "r" ) )

    data = json.loads( flask.request.data )

    configSettings[ "camera" ] = {
        "brightness": int( data[ "brightness" ] ),
        "sharpness": int( data[ "sharpness" ] ),
        "contrast": int( data[ "contrast" ] )
    }

    json.dump( configSettings, open( "./config.json", "w+" ) )

    return "200"

@app.route( "/savePaperValues", methods = [ "POST" ] )
def savePaperValues():
    configSettings = json.load( open( "./config.json", "r" ) )

    data = json.loads( flask.request.data )

    configSettings[ "plattform" ][ "h-min" ] = int( data[ "h-min" ] )
    configSettings[ "plattform" ][ "h-max" ] = int( data[ "h-max" ] )
    configSettings[ "plattform" ][ "s-min" ] = int( data[ "s-min" ] )
    configSettings[ "plattform" ][ "s-max" ] = int( data[ "s-max" ] )

    json.dump( configSettings, open( "./config.json", "w+" ) )

    return "200"

@app.route( "/saveMarkerValues", methods = [ "POST" ] )
def saveMarkerValues():
    configSettings = json.load( open( "./config.json", "r" ) )

    data = json.loads( flask.request.data )

    configSettings[ "markers" ][ "h-min" ] = int( data[ "h-min" ] )
    configSettings[ "markers" ][ "h-max" ] = int( data[ "h-max" ] )
    configSettings[ "markers" ][ "s-min" ] = int( data[ "s-min" ] )
    configSettings[ "markers" ][ "s-max" ] = int( data[ "s-max" ] )

    json.dump( configSettings, open( "./config.json", "w+" ) )

    return "200"

@app.route( "/savePenValues", methods = [ "POST" ] )
def savePenValues():
    configSettings = json.load( open( "./config.json", "r" ) )

    data = json.loads( flask.request.data )

    configSettings[ "pen" ][ "h-min" ] = int( data[ "h-min" ] )
    configSettings[ "pen" ][ "h-max" ] = int( data[ "h-max" ] )
    configSettings[ "pen" ][ "s-min" ] = int( data[ "s-min" ] )
    configSettings[ "pen" ][ "s-max" ] = int( data[ "s-max" ] )
    configSettings[ "pen" ][ "v-min" ] = int( data[ "v-min" ] )
    configSettings[ "pen" ][ "v-max" ] = int( data[ "v-max" ] )

    json.dump( configSettings, open( "./config.json", "w+" ) )

    return "200"


###
#
# Send the images
#
###
@app.route( "/take_image" )
def take_image():
    global image
    try:
        data = json.loads( flask.request.data )
        camera.brightness =  int( data[ "brightness" ] )
        camera.sharpness = int( data[ "sharpness" ] ) 
        camera.contrast = int( data[ "contrast" ] )

        camera.start_preview()
        time.sleep( 0.5 )
        camera.capture( "./image.jpg" )
    except:
        pass

    image = cv2.imread( "./image.jpg" )
    return "200"

@app.route('/markerHSV', methods = [ "POST" ] ) 
def markerHSV():
    data = json.loads( flask.request.data )

    SETTINGS[ "markers" ][ "h-min" ] = int( data[ "h-min" ] )
    SETTINGS[ "markers" ][ "h-max" ] = int( data[ "h-max" ] )
    SETTINGS[ "markers" ][ "s-min" ] = int( data[ "s-min" ] )
    SETTINGS[ "markers" ][ "s-max" ] = int( data[ "s-max" ] )

    json.dump( SETTINGS, open( "./config_copy.json", "w+" ))
    
    return "200"

@app.route('/paperHSV', methods = [ "POST" ] ) 
def paperHSV():
    data = json.loads( flask.request.data )

    SETTINGS[ "plattform" ][ "h-min" ] = int( data[ "h-min" ] )
    SETTINGS[ "plattform" ][ "h-max" ] = int( data[ "h-max" ] )
    SETTINGS[ "plattform" ][ "s-min" ] = int( data[ "s-min" ] )
    SETTINGS[ "plattform" ][ "s-max" ] = int( data[ "s-max" ] )

    json.dump( SETTINGS, open( "./config_copy.json", "w+" ))
    
    return "200"

@app.route('/penHSV', methods = [ "POST" ] ) 
def penHSV():
    data = json.loads( flask.request.data )

    SETTINGS[ "pen" ][ "h-min" ] = int( data[ "h-min" ] )
    SETTINGS[ "pen" ][ "h-max" ] = int( data[ "h-max" ] )
    SETTINGS[ "pen" ][ "s-min" ] = int( data[ "s-min" ] )
    SETTINGS[ "pen" ][ "s-max" ] = int( data[ "s-max" ] )
    SETTINGS[ "pen" ][ "v-min" ] = int( data[ "v-min" ] )
    SETTINGS[ "pen" ][ "v-max" ] = int( data[ "v-max" ] )

    json.dump( SETTINGS, open( "./config_copy.json", "w+" ))
    
    return "200"



@app.route( "/values" )
def values():
    return flask.jsonify( SETTINGS )

###
#
# Send the images
#
###
def getImage( image, result, coords ):
    markerCorners = np.copy( image )

    for i in range( len( coords ) ):
        x = int( coords[ i ][ 1 ] ); y = int( coords[ i ][ 0 ] )
        markerCorners = cv2.circle( markerCorners, ( x, y ), 4, ( 255, 255, 255 ), -1 )
        markerCorners = cv2.circle( markerCorners, ( x, y ), 10, ( 0, 255, 0 ), 4 )

    hsvImage = cv2.cvtColor( image, cv2.COLOR_BGR2HSV )

    mergedImg = np.zeros( ( image.shape[ 0 ], image.shape[ 1 ] * 4 ) )

    mergedImg[ :, : image.shape[ 1 ] ] = result
    mergedImg[ :, image.shape[ 1 ] : image.shape[ 1 ] * 2 ] = hsvImage[ :, :, 0 ]
    mergedImg[ :, image.shape[ 1 ] * 2 : image.shape[ 1 ] * 3 ] = hsvImage[ :, :, 1 ] 

    mergedImg = np.expand_dims( mergedImg, axis = -1 )
    mergedImg = np.concatenate( [ mergedImg, mergedImg, mergedImg ], axis = -1 )

    mergedImg[ :, -image.shape[ 1 ] :, : ] = markerCorners

    mergedImg = cv2.resize( mergedImg, ( 1280, 840 ), interpolation = cv2.INTER_LINEAR )
    return mergedImg


@app.route('/original')
def original_image_view():
    _, buffer = cv2.imencode('.jpg', image)
    image_io = BytesIO(buffer)
    return send_file(image_io, mimetype='image/jpeg', as_attachment=False)

@app.route('/marker_image')
def marker_image_view():
    global image
    result = pdars.markerPlattformCoords( image, resultImg = True, loadCopy = True )

    a, b = pdars.markerPlattformCoords( image, loadCopy = True )
    plattformCords = pdars.getOutherPlattformPoints( image, a, b )


    mergedImg = getImage( image, result, plattformCords )


    _, buffer = cv2.imencode('.jpg', mergedImg )
    hsv_image_io = BytesIO(buffer)
    return send_file(hsv_image_io, mimetype='image/jpeg', as_attachment=False)

@app.route("/paper_image" )
def paper_image_view():
    global image

    plattformCords = pdars.markerPlattformCoords( image, loadCopy = True )
    img1 = pdars.undisturbImg( image, plattformCords )

    a, b = pdars.markerPlattformCoords( img1, loadCopy = True )
    plattformCords = pdars.getOutherPlattformPoints( img1, a, b )

    plattformImg = pdars.transform( img1, plattformCords, device = "plattform" )

    paperCoords = pdars.getPaperCorners( plattformImg, loadCopy = True )

    result = pdars.getPaperCorners( plattformImg, resultImg = True, loadCopy = True )

    mergedImg = getImage( plattformImg, result, paperCoords )

    _, buffer = cv2.imencode('.jpg', mergedImg )
    hsv_image_io = BytesIO(buffer)
    return send_file(hsv_image_io, mimetype='image/jpeg', as_attachment=False)

@app.route( "/pen_image" )
def pen_image_view():
    global image

    plattformCords = pdars.markerPlattformCoords( image )
    img1 = pdars.undisturbImg( image, plattformCords )

    coords = pdars.getCoords( image ) 

    #Transform the images to get the paper from bird view
    plattformImg = pdars.transform( img1, coords[ 0 ] )

    stableDiffImg1 = pdars.transform( plattformImg, coords[ 1 ], device = "paper" )

    result = pdars.penDetection( stableDiffImg1, loadCopy = True )

    #generate image for the webserver
    mergedImg = np.zeros( ( result.shape[ 0 ], result.shape[ 1 ] * 4 ) )

    hsvImage = cv2.cvtColor( stableDiffImg1, cv2.COLOR_BGR2HSV )
    
    mergedImg[ :, : result.shape[ 1 ] ] = result
    mergedImg[ :, result.shape[ 1 ] : result.shape[ 1 ] * 2 ] = hsvImage[ :, :, 0 ]
    mergedImg[ :, result.shape[ 1 ] * 2 : result.shape[ 1 ] * 3 ] = hsvImage[ :, :, 1 ] 
    mergedImg[ :, result.shape[ 1 ] * 3 : ] = hsvImage[ :, :, 2 ] 

    mergedImg = np.expand_dims( mergedImg, axis = -1 )
    mergedImg = np.concatenate( [ mergedImg, mergedImg, mergedImg ], axis = -1 )

    mergedImg = cv2.resize( mergedImg, ( 1280, 840 ), interpolation = cv2.INTER_LINEAR )
    
    _, buffer = cv2.imencode('.jpg', mergedImg )
    hsv_image_io = BytesIO(buffer)
    return send_file(hsv_image_io, mimetype='image/jpeg', as_attachment=False)

if __name__ == '__main__':
    app.run( host = "0.0.0.0" )