from clip_interrogator import Config, Interrogator
from PIL import Image
import time

file = open( "./timeTests/time.txt", "w+" )

for imgSize in [ ( 256, 256 ), ( 512, 256 ), ( 768, 512 ) ]:
    for model in [ "ViT-B-16/openai", "ViT-B-32/openai", "ViT-L-14/openai" ]:
        for device in [ "cpu", "cuda" ]:
            img = Image.open( "./test.png" ).convert('RGB')
            img = img.resize( imgSize )

            config = Config(clip_model_name = model )
            config.apply_low_vram_defaults()
            config.device = device
            INTEROGATOR = Interrogator( config )

            gesStart = time.time()
            start = time.time()
            INTEROGATOR.interrogate_fast( img )
            end = time.time()
            print( imgSize, device, model, end - start )
            file.write( "   ".join(  [ str( imgSize ), device, model, str( end - start ) ] ) + "\n" )
file.close()