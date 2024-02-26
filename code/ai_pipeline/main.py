from utils.chains import *
import utils.les as les
from flask import Flask
import utils.rpWebClient as rpWebClient
import raspberryPi.pdars as pdars

AI_CHAIN = Chain( document = True, verbose = True )
CLIENT = rpWebClient.RPClient()

IP = "127.0.0.1"

app = Flask( __name__ )

@app.route( "/points" )
def getImage():
    global AI_CHAIN, IP

    img1, configData = CLIENT.getImage()

    #Move Servos
    input( "Move Servos and press enter:" )
    #requests.request( method = "post", url = f"http://{IP}:5000/moveServos" )

    img2, configData = CLIENT.getImage()

    import json
    configData = json.load( open( "./raspberryPi/config.json", "r" ) )
    pdars.SETTINGS = configData

    data = pdars.process( img1, img2 )

    mergedImg = data[ "img" ]

    cv2.imwrite( "./test.png", mergedImg )

    AI_CHAIN.run()
    
    points = les.GetPointsFromImage( "./test.png", "./output/output.png", penSize = configData[ "penSize" ] )

    points = les.linesToRealWorld( points, data[ "offsets" ], configData )

    return { "points": points }


if __name__ == "__main__":
    print( "\n" * 3 )
    print( "--------------------------------------------" )
    print( "||                                        ||" )
    print( "||      ----    ----      --     -----    ||" )
    print( "||      |    |  |   |     /  \\     |      ||" )
    print( "||      |    |  |---     /----\\    |      ||" )
    print( "||      -----   |   \\   /      \\ -----    ||" )
    print( "||                                        ||" )
    print( "--------------------------------------------" )
    print( "        Humans interacting with AI      " )
    print( "\n" * 3 )
    print( ">>> Enter the ip of the raspberry pi controller" )
    print( ">>> Example: 127.0.0.1" )
    IP = input( )

    app.run( host = "0.0.0.0", port = 5000 )