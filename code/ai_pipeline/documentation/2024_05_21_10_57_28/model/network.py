from utils.layers import *
import json


settings = json.load( open( "./model/config.json", "r") ) 

input_image = settings[ "original-image-path" ]


inp = Interrogator( "inter1", input_image )
rand = RandomLineDrawer( "rand0", None, input_image, settings[ "random-line-cache" ], pen_size = 5, num_random_lines = 20 )

simp0 = SimpleString( "simp0", settings[ "string0" ] )
simp1 = SimpleString( "simp1", settings[ "string1" ] )

merg = Merger( "merg1", [ simp0, simp1 ] )

llm = LLM( "llm1", prompt = merg, prevElement = inp, prevElementKey = "<INPUT>" )

diff = StableDiffusion( "diff1", settings[ "stable-config-path" ], llm, rand )

over = Overlapper( "over0", 
                    diff, 
                    input_image, 
                    "./images/testCache.jpg", 
                    mergedOutputFolder = settings[ "merge-output-folder" ], 
                    outputImageName = settings[ "output-image-name" ] )

model = Model( over )