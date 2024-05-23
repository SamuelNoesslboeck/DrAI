from flask import Flask, render_template, send_file
import matplotlib.pyplot as plt
import cv2
import numpy as np
from io import BytesIO
import pdars
import flask
import time
import json

"""
Checking for existing settings and create a copy of those settings
If no settings exist create new settings
"""
try:
    SETTINGS = json.load( open( "./config.json", "r" ) )
except:
    SETTINGS = {"plattformHeight": 290, "plattformWidth": 167, "marker-height": 24.8, "marker-width": 39.8, "paperHeight": 210, "paperWidth": 148, "camera": {"brightness": 50, "sharpness": 0, "contrast": 50}, "pen": {"h-min": 0, "h-max": 255, "s-min": 0, "s-max": 255, "v-min": 55, "v-max": 150}, "markers": {"h-min": 100, "h-max": 125, "s-min": 200, "s-max": 255}, "plattform": {"h-min": 55, "h-max": 110, "s-min": 20, "s-max": 115}}


SETTINGS = json.load( open( "./config.json", "r" ) )
json.dump( SETTINGS, open( "./config_copy.json", "w+" ))


"""
Ckeck if it is possible to capture images with the raspberry pi camera
"""


from picamera2 import Picamera2
CAMERA = Picamera2()
config = CAMERA.create_preview_configuration()
CAMERA.configure(config)


CAMERA.options["quality"] = 100

CAMERA.controls.Brightness  = ( SETTINGS[ "camera" ][ "brightness" ] - 50 ) / 100
CAMERA.controls.Sharpness  = ( SETTINGS[ "camera" ][ "sharpness" ] - 50 ) / 100

CAMERA.start_preview()
CAMERA.start()
time.sleep( 0.5 )
CAMERA.capture_file( "./IMAGE.jpg" )


img = cv2.imread("./IMAGE.jpg" )
img = cv2.rotate( img, cv2.ROTATE_90_CLOCKWISE )
img = cv2.rotate( img, cv2.ROTATE_90_CLOCKWISE )
img = cv2.rotate( img, cv2.ROTATE_90_CLOCKWISE )
cv2.imwrite( "./IMAGE.jpg", img )
print( "Image shape:", img.shape )

image_path = "./IMAGE.jpg"
IMAGE = cv2.imread(image_path)
IMAGE = cv2.copyMakeBorder( IMAGE, 200, 200, 200, 200, cv2.BORDER_CONSTANT )


#Initialize the flask app
app = Flask(__name__)


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


@app.route( "/savePenSize", methods = [ "POST" ] )
def savePenSize():
    configSettings = json.load( open( "./config.json", "r" ) )

    data = json.loads( flask.request.data )

    configSettings[ "penSize" ] = int( data[ "value" ] )

    json.dump( configSettings, open( "./config.json", "w+" ) )

    return "200"


###
#
# Send the images
#
###
@app.route( "/take_image", methods = [ "POST" ],  )
def take_image():
    global IMAGE, CAMERA

    data = json.loads( flask.request.data )

    SETTINGS[ "camera" ][ "brightness" ] = int( data[ "brightness" ] )
    SETTINGS[ "camera" ][ "sharpness" ] = int( data[ "sharpness" ] )
    SETTINGS[ "camera" ][ "contrast" ] = int( data[ "contrast" ] )
    json.dump( SETTINGS, open( "./config_copy.json", "w+" ))
    
    CAMERA.controls.Brightness  = ( float( data[ "brightness" ] ) - 50 ) / 100
    CAMERA.controls.Sharpness  = ( float( data[ "sharpness" ] ) - 50 ) / 100

    CAMERA.capture_file( "./IMAGE.jpg" )

    img = cv2.imread("./IMAGE.jpg" )
    img = cv2.rotate( img, cv2.ROTATE_90_CLOCKWISE )
    img = cv2.rotate( img, cv2.ROTATE_90_CLOCKWISE )
    img = cv2.rotate( img, cv2.ROTATE_90_CLOCKWISE )
    cv2.imwrite( "./IMAGE.jpg", img )

    print( "Image shape:", img.shape )

    IMAGE = cv2.imread( "./IMAGE.jpg" )
    IMAGE = cv2.copyMakeBorder( IMAGE, 200, 200, 200, 200, cv2.BORDER_CONSTANT )

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
def getImage( IMAGE, result, coords, hsvExtraktion = np.zeros( ( 512, 512 ) ) ):
    markerCorners = np.copy( IMAGE )

    for i in range( len( coords ) ):
        x = int( coords[ i ][ 1 ] ); y = int( coords[ i ][ 0 ] )
        markerCorners = cv2.circle( markerCorners, ( x, y ), 4, ( 255, 255, 255 ), -1 )
        markerCorners = cv2.circle( markerCorners, ( x, y ), 10, ( 0, 255, 0 ), 4 )

    hsvImage = cv2.cvtColor( IMAGE, cv2.COLOR_BGR2HSV )

    if hsvExtraktion.shape != ( 512, 512 ):
        mergedImg = np.zeros( ( IMAGE.shape[ 0 ], IMAGE.shape[ 1 ] * 5 ) )

        mergedImg[ :, : IMAGE.shape[ 1 ] ] = result
        mergedImg[ :, IMAGE.shape[ 1 ] : IMAGE.shape[ 1 ] * 2 ] = hsvExtraktion
        mergedImg[ :, IMAGE.shape[ 1 ] * 2 : IMAGE.shape[ 1 ] * 3 ] = hsvImage[ :, :, 0 ]
        mergedImg[ :, IMAGE.shape[ 1 ] * 3 : IMAGE.shape[ 1 ] * 4 ] = hsvImage[ :, :, 1 ] 

        mergedImg = np.expand_dims( mergedImg, axis = -1 )
        mergedImg = np.concatenate( [ mergedImg, mergedImg, mergedImg ], axis = -1 )

        mergedImg[ :, -IMAGE.shape[ 1 ] :, : ] = markerCorners

        mergedImg = cv2.resize( mergedImg, ( 1280, 840 ), interpolation = cv2.INTER_LINEAR )

    else:
        mergedImg = np.zeros( ( IMAGE.shape[ 0 ], IMAGE.shape[ 1 ] * 4 ) )

        mergedImg[ :, : IMAGE.shape[ 1 ] ] = result
        mergedImg[ :, IMAGE.shape[ 1 ] : IMAGE.shape[ 1 ] * 2 ] = hsvImage[ :, :, 0 ]
        mergedImg[ :, IMAGE.shape[ 1 ] * 2 : IMAGE.shape[ 1 ] * 3 ] = hsvImage[ :, :, 1 ] 

        mergedImg = np.expand_dims( mergedImg, axis = -1 )
        mergedImg = np.concatenate( [ mergedImg, mergedImg, mergedImg ], axis = -1 )

        mergedImg[ :, -IMAGE.shape[ 1 ] :, : ] = markerCorners

        mergedImg = cv2.resize( mergedImg, ( 1280, 840 ), interpolation = cv2.INTER_LINEAR )
    return mergedImg


@app.route('/original')
def original_image_view():
    _, buffer = cv2.imencode('.jpg', IMAGE)
    image_io = BytesIO(buffer)
    return send_file(image_io, mimetype='IMAGE/jpeg', as_attachment=False)

@app.route('/marker_image')
def marker_image_view():
    global IMAGE

    result = pdars.markerPlattformCoords( IMAGE, resultImg = True, loadCopy = True )

    try:
        a, b = pdars.markerPlattformCoords( IMAGE, loadCopy = True )
        plattformCords = pdars.getOutherPlattformPoints( IMAGE, a, b )
    
    except:
        plattformCords = np.zeros( ( 4, 2 ) )

    mergedImg = getImage( IMAGE, result, plattformCords )

    _, buffer = cv2.imencode('.jpg', mergedImg )
    hsv_image_io = BytesIO(buffer)
    return send_file(hsv_image_io, mimetype='IMAGE/jpeg', as_attachment=False)

@app.route("/paper_image" )
def paper_image_view():
    global IMAGE

    plattformCords = pdars.markerPlattformCoords( IMAGE, loadCopy = True )
    img1 = pdars.undisturbImg( IMAGE, plattformCords )

    cv2.imwrite( "./undisturbed.png", img1 )

    a, b = pdars.markerPlattformCoords( img1, loadCopy = True )
    plattformCords = pdars.getOutherPlattformPoints( img1, a, b )

    plattformImg = pdars.transform( img1, plattformCords, device = "plattform" )

    cv2.imwrite( "./plattform.png", plattformImg )

    result = pdars.getPaperCorners( plattformImg, resultImg = True, loadCopy = True )
    
    try:
        paperCoords = pdars.getPaperCorners( plattformImg, loadCopy = True )
    except:
        paperCoords = np.zeros( ( 4, 2 ) )
    
    try:
        offsets = pdars.getRealWorldPaperPoints( ( plattformCords, paperCoords ), plattformImg.shape[ 1 ], plattformImg.shape[ 0 ] )
        print( "Offsets" )
        print( offsets )
    except:
        pass

    mergedImg = getImage( plattformImg, result, paperCoords )

    _, buffer = cv2.imencode('.jpg', mergedImg )
    hsv_image_io = BytesIO(buffer)
    return send_file(hsv_image_io, mimetype='IMAGE/jpeg', as_attachment=False)

@app.route( "/pen_image" )
def pen_image_view():
    global IMAGE

    plattformCords = pdars.markerPlattformCoords( IMAGE )
    img1 = pdars.undisturbImg( IMAGE, plattformCords )

    coords = pdars.getCoords( img1 ) 

    #Transform the images to get the paper from bird view
    plattformImg = pdars.transform( img1, coords[ 0 ] )

    stableDiffImg1 = pdars.transform( plattformImg, coords[ 1 ], device = "paper" )

    result = pdars.penDetection( stableDiffImg1, loadCopy = True )

    #generate IMAGE for the webserver
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
    return send_file(hsv_image_io, mimetype='IMAGE/jpeg', as_attachment=False)

if __name__ == '__main__':
    app.run( host = "0.0.0.0", processes=1 )