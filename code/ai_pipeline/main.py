from utils.chains import *
import utils.les as les
from flask import Flask
import utils.raspberryClient as raspberryClient
import raspberryPi.pdars as pdars
import requests

AI_CHAIN = Chain( document = True, verbose = True )
CLIENT = raspberryClient.RPClient()

app = Flask( __name__ )

@app.route( "/points" )
def getImage():
    global AI_CHAIN

    img1, configData = CLIENT.getImage()

    #Move Servos
    requests.request( method = "post", url = "http://127.0.0.1:5000/moveServos" )

    img2, configData = CLIENT.getImage()

    pdars.SETTINGS = configData

    data = pdars.process( img1, img2 )

    mergedImg = data[ "img" ]
    cv2.imwrite( "./test.png", mergedImg )
    
    AI_CHAIN.run()
    
    points = les.GetPointsFromImage( "./test.png", "./output/output.png", penSize = configData[ "penSize" ] )

    points = les.pointsToRealWorld( points, data[ "offsets" ] )

    return { "points": points }

if __name__ == "__main__":
    app.run()