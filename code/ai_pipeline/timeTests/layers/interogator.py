from clip_interrogator import Config, Interrogator
from PIL import Image
import torch
import time
import tqdm


def timeInterrogator( testImgPath : str = "./images/testImages/test1.png" ):
    print( "|-------------------------|" )
    print( "|  Testing Time for CLIP  |" )
    print( "|-------------------------|" )
    print( " " )
    print( "Times will be saved in the following document:" )
    print( "./timeTests/times/interrogator.txt" )
    print( " " )

    file = open( "./timeTests/times/interrogator.txt", "w+" )

    file.write( "Time measuring the clip interrogator" )
    file.write( "image Size     |   Model type  |   device" )
    #Iterate over possible image sizes
    for imgSize in tqdm.tqdm( [ ( 256, 256 ), ( 512, 256 ), ( 768, 512 ) ] ):

        #Iterate over different Clip Models
        for model in tqdm.tqdm( [ "ViT-B-16/openai", "ViT-B-32/openai", "ViT-L-14/openai" ] ):

            #If cpu and gpu is available test both else only test the cpu
            for device in tqdm.tqdm( [ "cpu", "cuda" ] if torch.cuda.is_available() else [ "cpu" ] ):
                
                #Read the image
                img = Image.open( testImgPath ).convert('RGB')
                img = img.resize( imgSize )

                #Configurate the clip model and load it
                config = Config(clip_model_name = model )
                config.apply_low_vram_defaults()
                config.device = device

                interrogator = Interrogator( config )

                #Measure the time it takes to interpret an image
                #Here the interrrogate fast method is used 
                start = time.time()
                interrogator.interrogate_fast( img )
                end = time.time()

                file.write( " | ".join(  [ str( imgSize ), device, model, str( end - start ) ] ) + "\n" )
                
    file.close()