from utils.chains import *
import utils.les as les
from flask import Flask
import raspberryClient

AI_CHAIN = Chain( document = True, verbose = True )
CLIENT = raspberryClient.RPClient()

app = Flask( __name__ )

@app.route( "/points" )
def getImage():
    global AI_CHAIN

    img = CLIENT.getImage()
    cv2.imwrite( "./originalImg.png", img )


    
    AI_CHAIN.run()
    
    points = les.GetPointsFromImage( "./test.png", "./output/output.png", penSize = 5 )

    return { "points": points }

if __name__ == "__main__":
    app.run()