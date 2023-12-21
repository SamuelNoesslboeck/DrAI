from clip_interrogator import Config, Interrogator
from diffusers import StableDiffusionImg2ImgPipeline
import numpy as np
import typing
import torch
import PIL
import cv2
import os

def getRandomLine( imgSize : typing.Tuple, length : int = 40, step : int = 5, dDegree : int = 5 ) -> np.ndarray:
    #Initialize random points
    x = np.random.randint( 0, imgSize[ 1 ] )
    y = np.random.randint( 0, imgSize[ 0 ] )

    #convert degree to radiants
    dDegree = dDegree * 2 * np.math.pi / 360

    #choose a random direction in which the line should be drawn
    direction = np.random.rand( 1 ) * 2 * np.math.pi
    points = [ [ x, y ] ]

    #interate through the line and change the direction a bit
    for i in range( length ):
        direction = direction + np.random.normal( 0, 1 ) * dDegree
        x = int( x + step * np.math.cos( direction ) )
        y = int( y + step * np.math.sin( direction ) ) 
        points.append( [ x, y ] )

    points = np.array( points, dtype = np.int32 ).reshape( -1, 1, 2 )
    return points

def getText( image, clip, speed = True ) -> str:
    if speed:
        return clip.interrogate_fast( image )
    else:
        return clip.interrogate( image )

def setupPipeline():
    #Initialize stable diffusion
    if os.path.exists( "./data/diffuser/" ):
        modelPath = "./data/diffuser/" 
    else:
        modelPath = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(modelPath)

    if modelPath != "./data/diffuser/":
        os.mkdir( "./data/diffuser/" )
        pipe.save_pretrained( "./data/diffuser/" )

    #initialize clip transformer for text captioning
    ci = Interrogator( Config( clip_model_name="ViT-L-14/openai" ) )
    return pipe, ci

def overlapImg( orgImg, genImg ) -> np.ndarray:
    if orgImg.shape[ : 2 ] != genImg.shape[ : 2 ]:
        raise( f"Error when overlapping images\nShapes do not match\noriginal Image has shape {orgImg.shape[:2]} and generated Image has shape {genImg.shape[:2] }" )

    return np.where( ( orgImg < 200 ) | ( genImg < 200 ), 0, 255 )

def difference( orgImg, genImg ) -> np.ndarray:
    diff = np.where( ( genImg <= 220 ) & ( orgImg >= 220 ), 255, 0 )
    return diff

def simpleDrawing():
    import time

    start = time.time()
    lines = cv2.imread( "./images/chrisi/merged/overloaded.png", cv2.IMREAD_GRAYSCALE )
    lines = cv2.resize( lines, ( 768, 512 ) )
    lines = 255 - lines

    cont,_ = cv2.findContours( lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE )

    lines = np.ones( ( 512, 768, 3 ), dtype = np.uint8 ) * 255
    end = time.time()
    print( end - start )
    #21 länge, 14,8 breite
    
    gesPixDistance = 0
    p2 = ( 0, 0 )
    for i in range( len( cont ) ):
        area = cv2.contourArea( cont[ i ] )
        if area > 20:
            for l in range( 1, cont[ i ].shape[ 0 ], 1 ):
                p1 = ( int( cont[ i ][ l - 1, 0, 0 ] ), int( cont[ i ][ l - 1, 0, 1 ] ) )

                if l == 1:
                    gesPixDistance += ( ( ( p1[ 0 ] - p2[ 0 ] ) / 768 * 21 ) ** 2 + ( ( p1[ 1 ] - p2[ 1 ] ) / 512 * 14.8 ) ** 2 ) ** 0.5
                
                p2 = ( int( cont[ i ][ l, 0, 0 ] ), int( cont[ i ][ l, 0, 1 ] ) )
                lines = cv2.line( lines, p1, p2, ( 0, 0, 0 ), 1 )
                gesPixDistance += ( ( ( p1[ 0 ] - p2[ 0 ] ) / 768 * 21 ) ** 2 + ( ( p1[ 1 ] - p2[ 1 ] ) / 512 * 14.8 ) ** 2 ) ** 0.5
                #lines = cv2.circle( lines, ( cont[ i ][ 0, 0, 0 ], cont[ i ][ 0, 0, 1 ] ), 5, ( 255, 0, 0 ), -1 )

                cv2.imshow( "", lines )
                cv2.waitKey( 1 )

    print( "Pixeldistance:", gesPixDistance )
    cv2.imwrite( "./images/test/test1.png", lines )

if __name__ == "__main__":
    #Setup stable diffusion pipeline
    pipe, clip = setupPipeline()

    #load the image
    image = PIL.Image.open( "./images/test/original/test.png" ).convert( "RGB" )
    image = image.resize( ( 768, 512 ) )

    prompt = getText( image, clip, speed = True )
    prompt = "childish drawing style, black and white, minimalistic" + prompt 

    '''
    nouns = wordcloud.getNouns( prompt )   
   
    gesAppendingText = ""
    for n in nouns:
        gesAppendingText += wordcloud.findSimilar( n )[ 0 ][ 0 ] + ", "
    gesAppendingText += "childish drawing style, black and white, minimalistic"
    '''

    images = pipe( prompt = prompt, image = image, strength = 0.65, guidance_scale = 7.5, negative_prompt = "different, new lines, ugly" ).images
    images[0].save( "./images/generated/test.png" )

