from ctransformers import AutoModelForCausalLM
import time


def getMistralTime():
    print( "|-----------------------------------------|" )
    print( "|  Testing Time for the Mistral 7B Model  |" )
    print( "|-----------------------------------------|" )
    print( " " )
    print( "Times will be saved in the following document:" )
    print( "./timeTests/times/mistral.txt" )
    print( " " )

    file = open( "./timeTests/times/mistral.txt", "w+" )

    prompt = """You are a very creative artist. 
    Thing of something extraordinary.
    thing of something what you can add to this image to make it magic and special
    think in a way that inspires people and which makes them happy
    do not describe the style of the new image mention that no areas should be filled and style is black and white linestyle
    be very creative for example to a house you could add a garden or to a car a trailer you can even draw a truck out of a car
    the description should be something which makes sense
    The image description is
    a black and white drawing of a city, minimalist ink drawing of a city, tall buildings, monoliths, modern city scape, emphasis on tall buildings, townscape, city scape, highrise buildings, tall minimalist skyscrapers, tall buildings on the sides, tall buildings in background, brutalist city, tectonic cityscape, photo of futuristic cityscape
    New image description:
    """

    for i in range( 1, 40 ):
        print( "|-----------------------------------------|")
        print( f">>> Loading Model with {i} gpu layers" )

        #Load the mistral 7b model
        llm = AutoModelForCausalLM.from_pretrained(
                    model_path_or_repo_id="TheBloke/Mistral-7B-Instruct-v0.1-GGUF", 
                    model_file="mistral-7b-instruct-v0.1.Q2_K.gguf", 
                    model_type="mistral",
                    temperature=0.7,
                    top_p=1,
                    top_k=50,
                    repetition_penalty=1.2,
                    context_length=8096,
                    max_new_tokens=2048,
                    gpu_layers=i
                    )
        print( ">>> Model loaded" )
        
        print( ">>> Generating prompt..." )
        start = time.time()

        #Generate text
        llm( prompt, max_new_tokens = 77 )

        end = time.time()
        print( ">>>> Prompt generated" )
        print( ">>> Time taken for 77 tokens" )
        print( end - start )

        file.write( f"GPU Layers: {i}       Time:" + str( end - start ).replace( ".", "," ) + "\n" )

    file.close()