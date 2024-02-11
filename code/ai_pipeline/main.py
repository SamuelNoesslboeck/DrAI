from utils.chains import *

if __name__ == "__main__":
    c = Chain( document = True, verbose = True )

    print( "Start" )
    while True:
        c.run()
        inp = input()
        