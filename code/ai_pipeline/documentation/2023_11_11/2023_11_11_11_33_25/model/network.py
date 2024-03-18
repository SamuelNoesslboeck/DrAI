from utils.layers import *

input_image = "./test.png"

inp = Interrogator( "inter1", input_image )

simp0 = SimpleString( "simp0", "./model/layers/string0.txt" )
simp1 = SimpleString( "simp1", "./model/layers/string1.txt" )
merg = Merger( "merg1", [ simp0, simp1 ] )
llm = LLM( "llm1", prompt = merg, prevElement = inp, prevElementKey = "<INPUT>" )
rand = RandomLineDrawer( "rand0", llm, input_image, "./stableoutput/test.png" )
diff = StableDiffusion( "diff1", "./model/layers/stable.json", rand )
over = Overlapper( "over0", diff, input_image, "./stableoutput/test.png", mergedOutputFolder = "./output/" )
model = Model( over )