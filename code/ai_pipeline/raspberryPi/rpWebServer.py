from flask import Flask, jsonify
import base64
import json
import cv2
from picamera2 import Picamera2

app = Flask(__name__)
app.config['SERVER_NAME'] = 'raspberrypi:40324'

SETTINGS = json.load(open("./config.json", "r"))

CAMERA = Picamera2()
config = CAMERA.create_preview_configuration({"size": ( 480 * 3, 640 * 3 ) })

CAMERA.options["quality"] = 100

CAMERA.controls.Brightness  = ( SETTINGS[ "camera" ][ "brightness" ] - 50 ) / 100
CAMERA.controls.Sharpness  = ( SETTINGS[ "camera" ][ "sharpness" ] - 50 ) / 100


@app.route("/image")
def image():
    try:
        SETTINGS = json.load(open("./config.json", "r"))

        CAMERA.capture('./IMAGE.jpg')

        img = cv2.imread("./IMAGE.jpg" )
        img = cv2.rotate( img, cv2.ROTATE_90_CLOCKWISE )
        cv2.imwrite( "./IMAGE.jpg", img )

        with open("./IMAGE.jpg", "rb") as img_file:
            img_string = base64.b64encode(img_file.read())
        
        return jsonify({"img": img_string.decode('utf-8'), "error": "None"} )

    except Exception as e:
        return jsonify({"img": img_string.decode('utf-8'), "error": "Error with the raspberry pi camera" } )
    

@app.route("/config")
def config():
    SETTINGS = json.load(open("./config.json", "r"))
    return jsonify(SETTINGS)

if __name__ == "__main__":
    app.run( host="0.0.0.0", port = "40324" )