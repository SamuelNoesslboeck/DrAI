from utils.chains import *
import json
import tqdm
import os

if __name__ == "__main__":
    c = Chain()

    print( "Start" )
    
    images = os.listdir( "./images/" )

    for img in tqdm.tqdm( images, desc = "images" ):
        for guidance in tqdm.tqdm( [ 1, 3, 5, 7, 9, 11, 13, 15 ], desc = "guidance" ):
            for strength in tqdm.tqdm( [ 0.1, 0.3, 0.5, 0.7, 0.9 ], desc = "strength" ):
                
                data = json.load( open( "./model/layers/stable.json", "r" ) )
                data[ "strength" ] = strength
                data[ "guidance_scale" ] = guidance

                if os.path.exists( "./test.png" ):
                    shutil.move( "./test.png", "./images/test.png" )

                shutil.move( "./images/" + img, "./" + img )
                os.rename( "./" + img, "./test.png" )

                json.dump( data, open( "./model/layers/stable.json", "w" ) )
                c.run()

                shutil.move( "./test.png", "./images/" + img )