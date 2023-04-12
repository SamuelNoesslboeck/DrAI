from clip_interrogator import Config, Interrogator
from diffusers import StableDiffusionImg2ImgPipeline
import utils.wordcloud as wordcloud
import numpy as np
import typing
import torch
import PIL
import cv2

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

def getText( image, clip ) -> str:
    return clip.interrogate( image )

def setupPipeline():
    #Initialize stable diffusion
    device = "cuda"
    model_id_or_path = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path)

    #initialize clip transformer for text captioning
    ci = Interrogator( Config( clip_model_name="ViT-L-14/openai" ) )
    return pipe, ci

def overlapImg( orgImg, genImg ) -> np.ndarray:
    if orgImg.shape[ : 2 ] != genImg.shape[ : 2 ]:
        raise( f"Error when overlapping images\nShapes do not match\noriginal Image has shape {orgImg.shape[:2]} and generated Image has shape {genImg.shape[:2] }" )

    return np.where( ( orgImg < 200 ) | ( genImg < 200 ), 0, 255 )


if __name__ == "__main__":
    #Setup stable diffusion pipeline
    pipe, clip = setupPipeline()

    #load the image
    image = PIL.Image.open( "./samuel2/original/test4.png" )
    image = image.resize( ( 512, 256 ) )

    #add random lines to the image for creativity
    for i in range( 20 ):
        line = getRandomLine( image.shape, int( np.random.normal( 30, 10 ) ), step = int( np.random.normal( 4, 2 ) ) )
        image = cv2.polylines( image, [ line ], False, ( 0,0,0 ), int( np.random.normal( 5, 2 ) ) )

    #get image prompt for generating new image
    prompt = getText( image )

    nouns = wordcloud.getNouns( line )   
   
    gesAppendingText = ""
    for n in nouns:
        gesAppendingText += wordcloud.findSimilar( n )[ 0 ][ 0 ] + ", "

    for infSteps in range( 20, 70, 10 ):
        for strength in [ 0.5, 0.6, 0.7, 0.8, 0.9 ]:
            for guidance in [ 5, 7, 9, 11, 13, 15, 17, 19 ]:
                images = pipe( prompt = gesAppendingText + prompt, num_inference_steps = infSteps, image = image, strength = strength, guidance_scale = guidance ).images
                images[0].save( f"./generated/gen_steps-{infSteps}_strength-{strength}_guidance-{guidance}.png" )

    