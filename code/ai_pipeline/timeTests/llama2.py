from langchain.llms import LlamaCpp
import time

LLM_MODEL = LlamaCpp( model_path = "./weights/llm/llama-2-7b-chat.ggmlv3.q8_0.bin" )

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

start = time.time()
out = LLM_MODEL( prompt )
end = time.time()

numTokens = LLM_MODEL.get_num_tokens( out )
print( numTokens )
print( out )
print( end - start )