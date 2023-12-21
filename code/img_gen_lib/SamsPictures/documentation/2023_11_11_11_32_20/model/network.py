from utils.layers import *

inp = Interogator( "inter1", "./test.png" )

simp0 = SimpleString( "simp0", "./model/layers/string0.txt" )
simp1 = SimpleString( "simp1", "./model/layers/string1.txt" )
merg = Merger( "merg1", [ simp0, simp1 ] )
llm = LLM( "llm1", prompt = merg, prevElement = inp, prevElementKey = "<INPUT>" )
rand = RandomLineDrawer( "rand0", llm, "./test.png", "./stableoutput/test.png" )
diff = StableDiffusion( "diff1", "./model/layers/stable.json", rand )
over = Overlapper( "over0", diff, "./test.png", "./stableoutput/test.png", mergedOutputFolder = "./output/" )
model = Model( over )