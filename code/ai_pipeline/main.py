from utils.chains import *
import utils.les as les
from flask import Flask
import utils.raspberryClient as raspberryClient
import piwebserver.pdars as pdars
import requests

AI_CHAIN = Chain( document = True, verbose = True )
CLIENT = raspberryClient.RPClient()

app = Flask( __name__ )

@app.route( "/points" )
def getImage():
    global AI_CHAIN

    img1 = CLIENT.getImage()

    #Move Servos
    requests.request( method = "post", url = "http://127.0.0.1:5000/moveServos" )

    img2 = CLIENT.getImage()

    mergedImg = pdars.process( img1, img2 )
    cv2.imwrite( "./test.png", mergedImg )
    
    AI_CHAIN.run()
    
    points = les.GetPointsFromImage( "./test.png", "./output/output.png", penSize = 5 )

    return { "points": points }

if __name__ == "__main__":
    app.run()