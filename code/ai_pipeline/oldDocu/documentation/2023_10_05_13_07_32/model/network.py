from utils.layers import *

inp = Interogator( "inter1", "./test.png" )

simp0 = SimpleString( "simp0", "./model/layers/string0.txt" )
simp1 = SimpleString( "simp0", "./model/layers/string1.txt" )
merg = Merger( "merg1", [ simp0, simp1 ] )
llm = LLM( "llm1", prompt = merg, prevElement= inp, prevElementKey = "input" )
#diff = StableDiffusion( "diff1", "./model/layers/stable.json", llm )
over = Overlapper( "over0", merg, "./test.png", "./output/test.png" )
model = Model( over )