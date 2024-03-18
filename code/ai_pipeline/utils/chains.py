from datetime import datetime
from utils.layers import *
import shutil
import time
import os

####
# Implementation of the AI-Chain 
####
class Chain():
    def __init__( self, document : bool = True, verbose : bool = True, configFile : str = "./model/config.json" ):
        """
        Chain( document : bool = True, verbose : bool = True, configFile : str = "./model/config.json", network : str = "./model/network.py" )
        """
        global LLM_MODEL, STABLE_MODEL, Interrogator

        configData = json.load( open( configFile, "r" ) )

        self.__network = configData[ "network-file" ]

        self.document = document
        self.verbose = verbose

        if self.document:
            self.__documentationPath = configData[ "docu-path" ]

            if not os.path.exists( self.__documentationPath ):
                os.mkdir( self.__documentationPath )

    def run( self ) -> None:
        # Running the chain
        print( ">>>[CHAIN]: Reading Chain" )

        #Get the current date and time for the documentation
        now = datetime.now()
        id = str( now.strftime("%Y_%m_%d_%H_%M_%S") )

        #If the execution should be documented create the folders
        if self.document:
            if not os.path.exists( self.__documentationPath ):
                os.mkdir( self.__documentationPath )

            os.mkdir( self.__documentationPath + id )
            os.mkdir( self.__documentationPath + id + "/history/" )

            shutil.copytree( "./model/", f"{self.__documentationPath}{id}/model/" )

        #open the chain description file
        codeFile = open( self.__network, "r" )
        code = "".join( codeFile.readlines() )

        #Go through every variable and check which one is from the model class
        #If there is a child of the model class start the chain

        exec( code )
        l = locals()

        started = False
        for var in l.values():
            if isinstance( var, Model ):
                started = True
                print( ">>>[CHAIN]: Started Chain..." )
                start = time.time()
                var.forward( self.__documentationPath + id + "/history/", self.verbose, self.document )
                end = time.time()
                print( ">>>[CHAIN]: Chain finished" )
                print( f">>>[CHAIN]: Time elapsed since start {end - start}s" )
        
        if not started:
            print( ">>>[CHAIN]: Error when starting the chain" )
            print( ">>>[CHAIN]: Model Class object has not been found")
            print( f">>>[CHAIN]: Check if the model class is implemented in the {self.__network} file")