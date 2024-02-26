from ctransformers import AutoModelForCausalLM
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import torch
import json
import os
import cv2


from clip_interrogator import Config, Interrogator
from langchain.llms import LlamaCpp
from diffusers import StableDiffusionImg2ImgPipeline

configFile = "./model/config.json"
configData = json.load( open( configFile, "r" ) )

try: 
    if torch.cuda.is_available():
        STABLE_MODEL = StableDiffusionImg2ImgPipeline.from_pretrained( configData[ "stable-path" ], torch_dtype = torch.float16 )
        STABLE_MODEL = STABLE_MODEL.to( "cuda" )
        print( ">>> [STABLE DIFFUSION]: Stable diffusion successfully loaded to GPU" )
    else:
        STABLE_MODEL = StableDiffusionImg2ImgPipeline.from_pretrained( configData[ "stable-path" ], device_type = "cpu", low_cpu_mem_usage = True )
        print( ">>> [STABLE DIFFUSION]: Stable diffusion successfully loaded to CPU" )

except:
    print( "<<< ERROR >>> [STABLE DIFFUSION]: Error when setting up Stable diffusion. Check if your gpu is available and if the path to weights is correct" )
    STABLE_MODEL = None

try:
    config = Config(clip_model_name="ViT-L-14/openai" )
    config.apply_low_vram_defaults()
    INTEROGATOR = Interrogator( config )
except:
    print( "<<< ERROR >>> [INTEROGATOR]: Error when setting up the interrogator" )
    INTEROGATOR = None


if configData[ "llm-model" ] == "llama2":
    print( "<<< INFO >>> [LLM]: Using LLama2-7b" )
    LLM_MODEL_ID = "LLama2"
    try:
        LLM_MODEL = LlamaCpp( model_path = configData[ "llm-path" ], verbose = False )
    except:
        print( "<<< ERROR >>> [LLM-LLAMA2]: No LLM weights found in the given directory" )
        LLM_MODEL = None

elif configData[ "llm-model" ] == "mistral":
    print( "<<< INFO >>> [LLM]: Using Mistral-7b" )
    LLM_MODEL_ID = "Mistral"
    try:
        if torch.cuda.is_available():
            LLM_MODEL = AutoModelForCausalLM.from_pretrained(
                model_path_or_repo_id="TheBloke/Mistral-7B-Instruct-v0.1-GGUF", 
                model_file="mistral-7b-instruct-v0.1.Q2_K.gguf", 
                model_type="mistral",
                temperature=0.7,
                top_p=1,
                top_k=50,
                repetition_penalty=1.2,
                context_length=8096,
                max_new_tokens=2048,
                gpu_layers=configData[ "llm-layers" ]
                )
            print( ">>> [LLM-MISTRAL]: LLM-MISTRAL successfully loaded to GPU" )

        else:
            LLM_MODEL = AutoModelForCausalLM.from_pretrained(
                model_path_or_repo_id="TheBloke/Mistral-7B-Instruct-v0.1-GGUF", 
                model_file="mistral-7b-instruct-v0.1.Q2_K.gguf", 
                model_type="mistral",
                temperature=0.7,
                top_p=1,
                top_k=50,
                repetition_penalty=1.2,
                context_length=8096,
                max_new_tokens=2048,
            )
            print( ">>> [LLM-MISTRAL]: LLM-MISTRAL successfully loaded to CPU" )
    except:
        print( "<<< ERROR >>> [LLM-MISTRAL]: No LLM weights found in the given directory" )
        LLM_MODEL = None


class ChainElement():
    def __init__( self ):
        pass

    def addToHistory( self, id, fileName, input : str = "", output : str = "", inputImage = None, outputImage = None ):
        with open( id + fileName + "_history.txt", "w+" ) as file:
            file.write( "Input:\n" )
            file.write( input )
            file.write( "\n\n\n\nOutput:\n" )
            file.write( output )
        
        if inputImage != None:
            print( id + fileName + "_history_input_image.jpg" )
            inputImage.save( id + fileName + "_history_input_image.jpg" )
        
        if outputImage != None:
            outputImage.save( id + fileName + "_history_output_image.jpg" )


    def checkEnding( self, path : str, ending : list[str] ):
        correctEnding = False

        for end in ending:
            if path.split( "." )[-1] == end:
                correctEnding = True

        if not correctEnding:
            raise Exception( f"Error with {path}\nThe filepath is not a {ending} file" )
        

class Interogator( ChainElement ):
    def __init__( self, name, imagePath : str, prevElement = None ):
        super().__init__()
        
        self.__imgPath = imagePath

        self.prevElement = prevElement
        self.name = name

    def forward( self, id : str, verbose : bool = True, document : bool = True ) -> str:
        global INTEROGATOR

        if self.prevElement != None:
            self.prevElement.forward( id, verbose )

        try:
            img = Image.open( self.__imgPath ).convert('RGB')
        except:
            raise Exception( f"Error with Interogator\nCouldnt find image with the path{self.__imgPath}" )

        print( ">>>[CHAIN][Interogator]: Generating prompt..." )
        prompt = INTEROGATOR.interrogate_fast( img )

        if document:
            self.addToHistory( id, self.name, output = prompt, inputImage = img )

        return prompt
    

class Merger( ChainElement ):
    def __init__( self, name, elements : list[ ChainElement ], mergingSymbole : str = " " ):
        super().__init__()

        self.__elements = elements
        self.__mergingSymbole = mergingSymbole

        self.name = name

    def forward( self, id : str, verbose : bool = True, document : bool = True ) -> str:
        print( ">>>[CHAIN][MERGER] Merging..." )
        outputs = [ e.forward( id, verbose, document ) for i, e in enumerate( self.__elements ) ]
        outputs = self.__mergingSymbole.join( outputs ) 

        if document:
            self.addToHistory( id, self.name, outputs )

        return outputs
    


class LLM( ChainElement ):
    def __init__( self, name, prompt : [ None, ChainElement ] = None, prevElement : [None, ChainElement] = None, prevElementKey : str = "{input}" ):
        super().__init__()

        self.__prevElement = prevElement
        self.__prevElementKey = prevElementKey

        self.__promptElement = prompt

        self.name = name

    def forward( self, id : str, verbose : bool = True, document : bool = True ):
        global LLM_MODEL
        print( ">>>[CHAIN][LLM] running..." )
        prompt = self.__promptElement.forward( id, verbose, document )
        print( f">>>[CHAIN][LLM] prompt = {prompt}")

        insertment = self.__prevElement.forward( id, verbose, document )
        print( f">>>[CHAIN][LLM]: Insertment {insertment} " )
        prompt = prompt.replace( self.__prevElementKey, insertment )

        if verbose:
            print( f">>>[CHAIN][LLM]: Generating prompt..." )

        if LLM_MODEL_ID == "LLama2":
            num_tokens = LLM_MODEL.get_num_tokens( prompt )

            if verbose:
                print( f">>>[CHAIN][LLM]: Current token length is {num_tokens}, new prompt length is {num_tokens + 77}" )

        if LLM_MODEL_ID == "LLama2":
            modelPrompt = LLM_MODEL( prompt, max_tokens = num_tokens + 77 )
        else:
            modelPrompt = LLM_MODEL( prompt, max_new_tokens = 77 )

        if verbose:
            print( f">>>[CHAIN][LLM]: Generated Prompt:\n{modelPrompt}" )
            print( f">>>[CHAIN][LLM]: Prompt generated" )

        if document:
            self.addToHistory( id, self.name, prompt, modelPrompt )

        return modelPrompt
    

class SimpleString( ChainElement ):
    def __init__( self, name, stringPath : str ):
        super().__init__()

        self.checkEnding( stringPath, [ "txt" ] )

        self.__stringPath = stringPath

        self.name = name

    def forward( self, id : str, verbose : bool = True, document : bool = True ) -> str:
        if verbose:
            print( f">>>[CHAIN][{self.__stringPath}]: Reading prompt..." )

        with open( self.__stringPath, "r" ) as file:
            p = "".join( file.readlines() )

        if document:
            self.addToHistory( id, self.name, "", p )

        return p
    

class StableDiffusion( ChainElement ):
    def __init__( self, name, parameterPath : str, prevElement : ChainElement, prevImageElement : ChainElement ):
        super().__init__()

        self.checkEnding( parameterPath, ["json"] )

        params = json.load( open( parameterPath, "r" ) )

        self.__imgPath = params[ "imagePath" ]
        self.__cache = params[ "cache" ]

        if not isinstance( self.__imgPath, str ):
            raise Exception( "Error\nStable Diffusion Image Path is not a string" )

        if not isinstance( self.__cache, str ):
            raise Exception( "Error\nStable Diffusion Cache Path is not a string" )

        self.__guidance = params[ "guidance_scale" ]
        self.__strength = params[ "strength" ]

        if not isinstance( self.__guidance, ( float, int ) ):
            raise Exception( "Error\nStable Diffusion Guidance is not a float or int" )
        if not isinstance( self.__strength, ( float, int ) ):
            raise Exception( "Error\nStable Diffusion Strength is not a float or int" )

        self.__prevElement = prevElement

        self.__prevImageElement = prevImageElement

        self.checkEnding( self.__imgPath, ["jpg","png","jpeg"] )
        self.checkEnding( self.__cache, ["jpg","png","jpeg"] )

        self.name = name

    def forward( self, id : str, verbose : bool = True, document : bool = True ):
        global STABLE_MODEL

        if verbose:
            print( ">>>[CHAIN][DIFFUSION]: Getting Prompt..." )

        self.__prevImageElement.forward( id, verbose, document )
        prompt = self.__prevElement.forward( id, verbose, document )

        if verbose:
            print( ">>>[CHAIN][DIFFUSION]: Getting Image..." )

        img = Image.open( self.__imgPath ).convert('RGB')
        img = img.resize((768, 512))

        if verbose:
            print( ">>>[CHAIN][DIFFUSION]: Generating Image..." )

        images = STABLE_MODEL(prompt=prompt, negative_prompt = "filled areas, ugly, other colors than black lines", image=img, strength=self.__strength, guidance_scale=self.__guidance).images

        if verbose:
            print( ">>>[CHAIN][DIFFUSION]: Image generated" )

        if document:
            self.addToHistory( id, self.name, prompt, "", img, images[ 0 ] )
    
        images[0].save( self.__cache )


class RandomLineDrawer( ChainElement ):
    def __init__( self, name, prevElement, input_image : str, output_image : str, num_random_lines : int = 40, line_length : int = 40 ):
        super().__init__()

        self.name = name
        self.__prevElement = prevElement
        self.__inputPath = input_image
        self.__outputPath = output_image

        self.__num_random_lines = num_random_lines
        self.__line_length = line_length


    def forward( self, id : str, verbose : bool = True, document : bool = True ):
        self.__prevElement.forward( id, verbose, document )

        img = cv2.imread( self.__inputPath )
        img = cv2.resize( img, ( 768, 512 ) )
        img = np.array( img ).reshape( 512, 768, 3 )
         
        image = np.copy( img )
        for i in range( self.__num_random_lines ):
            line = self.getRandomLine( image.shape, np.random.randint( 10, 40 ), dDegree = 30 )
            image = cv2.polylines( image, line, True, ( 0, 0, 0 ), 8, lineType = cv2.LINE_AA )
        
        inputImage = Image.open( self.__inputPath ).convert('RGB')

        cv2.imwrite( self.__outputPath, image )

        outputImage = Image.open( self.__outputPath ).convert('RGB')
        if document:
            self.addToHistory(  id, self.name, inputImage = inputImage, outputImage = outputImage )

        
        
        
    def getRandomLine( self, imgSize, length : int = 40, step : int = 5, dDegree : int = 5 ) -> np.ndarray:
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

class Overlapper( ChainElement ):
    def __init__( self, name, prevElement, image_1 : str, image_2 : str, mergedOutputFolder : str = "./mergedOutputImages/" ):
        super().__init__()

        self.name = name

        self.__prevElement = prevElement

        self.__mergedOutputFolder = mergedOutputFolder

        self.__image1 = image_1
        self.__image2 = image_2
 
    def forward( self, id : str, verbose : bool = True, document : bool = True ):
        self.__prevElement.forward( id, verbose, document )

        try:
            genImg = cv2.imread( self.__image2, cv2.IMREAD_GRAYSCALE )
            genImg = cv2.resize( genImg, ( 768, 512 ) ) 
            genImg = np.where( genImg > 200, 0, 256 )
        except:
            raise( f"<<< ERROR >>> [CHAIN][OVERLAPPER][{self.name}] Check if the path to the image 2 does exist" )

        try:
            orgImg = cv2.imread( self.__image1, cv2.IMREAD_GRAYSCALE )
            orgImg = cv2.resize( orgImg, ( 768, 512 ) )
            orgImg = np.where( orgImg > 200, 0, 256 )
        except:
            raise( f"<<< ERROR >>> [CHAIN][OVERLAPPER][{self.name}] Check if the path to the image 1 does exist" )

        newImg = genImg + orgImg
        newImg = np.where( newImg > 200, 0, 256 )
        orgImg = np.where( orgImg > 200, 0, 256 )

        idFolder = id.split( "/" )[ -3 ]

        fig = plt.figure()
        ax1 = fig.add_subplot( 2, 1, 1 )
        ax1.imshow( orgImg, cmap = "gray" )

        ax2 = fig.add_subplot( 2, 1, 2 )
        ax2.imshow( newImg, cmap = "gray" )

        if not os.path.exists( self.__mergedOutputFolder ):
            os.mkdir( self.__mergedOutputFolder )
         
        fig.savefig( self.__mergedOutputFolder + idFolder + ".jpg" )

        img = Image.open( self.__mergedOutputFolder + idFolder + ".jpg" ).convert('RGB')
        os.remove( self.__mergedOutputFolder + idFolder + ".jpg" )

        if document:
            self.addToHistory(  id, self.name, outputImage = img )

        cv2.imwrite( self.__mergedOutputFolder + "output.png", newImg )
        

class Model():
    def __init__( self, output : ChainElement ):
        self.output = output

    def forward( self, id : str = "", verbose : bool = True, document : bool = True ):
        self.output.forward( id, verbose, document )
