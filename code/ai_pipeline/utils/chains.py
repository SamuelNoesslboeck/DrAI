from datetime import datetime
from utils.layers import *
import shutil
import time
import os

class Chain():
    def __init__( self, document : bool = True, verbose : bool = True, configFile : str = "./model/config.json", network : str = "./model/network.py" ):
        global LLM_MODEL, STABLE_MODEL, INTEROGATOR

        self.__network = network

        configData = json.load( open( configFile, "r" ) )

        self.document = document
        self.verbose = verbose

        if self.document:
            self.__documentationPath = configData[ "docu-path" ]

            if not os.path.exists( self.__documentationPath ):
                os.mkdir( self.__documentationPath )

    def run( self ) -> None:
        print( ">>>[CHAIN]: Reading Chain" )

        now = datetime.now()
        id = str( now.strftime("%Y_%m_%d_%H_%M_%S") )

        if self.document:
            if not os.path.exists( self.__documentationPath ):
                os.mkdir( self.__documentationPath )

            os.mkdir( self.__documentationPath + id )
            os.mkdir( self.__documentationPath + id + "/history/" )

            shutil.copytree( "./model/", f"{self.__documentationPath}{id}/model/" )

        codeFile = open( self.__network, "r" )
        code = "".join( codeFile.readlines() )

        exec( code )
        l = locals()

        for var in l.values():
            if isinstance( var, Model ):
                print( ">>>[CHAIN]: Started Chain..." )
                start = time.time()
                var.forward( self.__documentationPath + id + "/history/", self.verbose, self.document )
                end = time.time()
                print( ">>>[CHAIN]: Chain finished" )
                print( f">>>[CHAIN]: Time elapsed since start {end - start}s" )