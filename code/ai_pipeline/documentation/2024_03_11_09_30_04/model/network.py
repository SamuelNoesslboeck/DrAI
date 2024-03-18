from utils.layers import *
import json


settings = json.load( open( "./model/config.json", "r") ) 

input_image = settings[ "original-image-path" ]


inp = Interrogator( "inter1", input_image )
rand = RandomLineDrawer( "rand0", inp, input_image, settings[ "original-image-path" ], pen_size = 4 )

simp0 = SimpleString( "simp0", settings[ "string0" ] )
simp1 = SimpleString( "simp1", settings[ "string1" ] )

merg = Merger( "merg1", [ simp0, simp1 ] )

llm = LLM( "llm1", prompt = merg, prevElement = inp, prevElementKey = "<INPUT>" )

diff = StableDiffusion( "diff1", settings[ "stable-config-path" ], llm, rand )

over = Overlapper( "over0", 
                    diff, 
                    input_image, 
                    settings[ "original-image-path" ], 
                    mergedOutputFolder = settings[ "merge-output-folder" ], 
                    outputImageName = settings[ "output-image-name" ] )

model = Model( over )