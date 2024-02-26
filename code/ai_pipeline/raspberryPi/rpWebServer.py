from flask import Flask, jsonify
import base64
import json
from picamera import PiCamera

app = Flask(__name__)
app.config['SERVER_NAME'] = 'raspberrypi:5000'

CAMERA = PiCamera()

@app.route("/image")
def image():
    SETTINGS = json.load(open("./config.json", "r"))

    CAMERA.resolution = (480 * 3, 640 * 3)
    CAMERA.rotation = 90

    CAMERA.brightness = SETTINGS["camera"]["brightness"]
    CAMERA.sharpness = SETTINGS["camera"]["sharpness"]
    CAMERA.contrast = SETTINGS["camera"]["contrast"]

    CAMERA.start_preview()
    CAMERA.capture('./IMAGE.jpg')

    with open("./IMAGE.jpg", "rb") as img_file:
        img_string = base64.b64encode(img_file.read())

    return jsonify({"img": img_string.decode('utf-8')})

@app.route("/config")
def config():
    SETTINGS = json.load(open("./config.json", "r"))
    return jsonify(SETTINGS)

if __name__ == "__main__":
    app.run() #host="192.168.8.111", port=5000