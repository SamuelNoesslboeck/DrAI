from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import torch
import time
import tqdm


def getStableTime():
    print( "|-------------------------------------|" )
    print( "|  Testing Time for Stable Diffusion  |" )
    print( "|-------------------------------------|" )
    print( " " )

    print( ">>> Loading the Model to gpu" )
    STABLE_MODEL = StableDiffusionImg2ImgPipeline.from_pretrained( "stabilityai/stable-diffusion-2", torch_dtype = torch.float16, variant="fp16" )
    STABLE_MODEL.enable_model_cpu_offload()
    STABLE_MODEL.to( "cuda" )
    print( ">>> Model successfully loaded to gpu" )

    print( "Times will be saved in the following document:" )
    print( "./timeTests/times/stable.txt" )
    print( " " )


    file = open( "./timeTests/times/stable.txt", "w+" ) 
    file.write( "image Size | num Steps | time " )

    for imgSize in tqdm.tqdm( [ ( 256, 256 ), ( 512, 256 ), ( 768, 512 ) ] ):
        img = Image.open( "./images/testImages/test1.png" ).convert('RGB')
        img = img.resize( imgSize )
        
        for steps in tqdm.tqdm( [ 20, 30, 40, 50 ] ):

            start = time.time()        
            for _ in range( 2 ):
                _ = STABLE_MODEL(prompt = "A black and white ink drawing of a futuristic city, emphasizing geometric shapes and clean lines. In the foreground, the tower-top has the face on it representing some spiritual meaning for that future society. The towers are connected by bridges with light beams shining on them representing optimism about communication technology in this new era. The background is filled with a gradient" , negative_prompt = "filled areas, ugly, other colors than black lines", image=img, strength=0.9, guidance_scale=7, num_inference_steps = steps ).images
            
            end = time.time()

            file.write( " | ".join( [ str( imgSize ), str( steps ), str( ( end - start ) / 2 ) ] ) + "\n" )

            print( imgSize, steps, str( ( end - start ) / 2 ) )

    file.close()