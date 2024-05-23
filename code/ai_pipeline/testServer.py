from flask import Flask, render_template, request, send_file, Response, jsonify
import datetime
import cv2
import base64
import numpy as np
import requests
import os
import json
import time

SERVER_IP = "127.0.0.1"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("testServer.html")

@app.route('/send', methods=['POST'])
def send_image():
    image_data = request.get_json()['image']
    image_bytes = base64.b64decode(image_data)
    with open('./images/test.jpg', 'wb') as f:
        f.write(image_bytes)

    with open("./images/test.jpg", "rb") as img_file:
        img_string = base64.b64encode(img_file.read())
    
    res = requests.post( f'http://{SERVER_IP}:40325/img2points', json={"img": img_string.decode('utf-8'), "error": "None"})

    data = res.json()

    ###Generate Video
    fourcc = cv2.VideoWriter_fourcc(*'DIVX') 
    video = cv2.VideoWriter('video.avi', fourcc, 10., (512, 768))

    originalImg = cv2.imread( "./images/test.jpg" )
    img = np.copy( originalImg )
    
    points = data[ "points" ][ "lines" ]
    for i in range( len( points ) ):
        x1 = int( points[ i ][ "p1" ][ 0 ] )
        y1 = int( points[ i ][ "p1" ][ 1 ] )

        x2 = int( points[ i ][ "p2" ][ 0 ] )
        y2 = int( points[ i ][ "p2" ][ 1 ] )
        
        img = cv2.line( img, ( x1, y1 ), ( x2, y2 ), ( 0, 0, 0 ), 2 )

        newImg = np.copy( img )
        video.write( newImg )

    cv2.imwrite( "./images/lastImg.jpg", newImg )

    path = "./examples/" + datetime.datetime.strftime( "%Y-%m-%d_%H-%M-%S" )
    os.mkdir( path )

    cv2.imwrite( path + "input.jpg", originalImg  )
    cv2.imwrite( path + "output.jpg", newImg  )

    video.release()

    return Response(status=200)

def gen():
    cap = cv2.VideoCapture('video.avi')
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + imgencode.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/last_frame')
def last_frame():
    last_frame = cv2.imread("./images/lastImg.jpg")
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', last_frame, encode_param)
    last_frame_b64 = base64.b64encode(imgencode)
    return 'data:image/jpeg;base64,' + last_frame_b64.decode('utf-8')





if __name__ == '__main__':
    app.run(debug=True)