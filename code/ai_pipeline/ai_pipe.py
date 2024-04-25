from utils.chains import *

if __name__ == "__main__":
    ##########################
    # This script is there to test the ai-chain
    # The chain can be modified while this scipt keeps running
    ##########################
    #Setup the chain
    c = Chain( document = True, verbose = True )

    print( "Start" )
    while True:
        c.run()
        #Wait for user to start the chain again
        inp = input()