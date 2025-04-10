from typing import Callable
from Common.CuveLaboAPI import CuveLaboAPI

class CuveLaboClient(object):

    _api : CuveLaboAPI

    _Ready : bool = False

    _updateFunc = None

    def __init__(self, serverIP : str, serverPort : str = "5000"):
        
        self._api = CuveLaboAPI(serverIP, serverPort)
        self._Ready = self._api.GetBaseData()
        pass

    def NumberOfCuve(self) -> int:
        return self._api._NbCuve
    
    def NumberOfMotor(self) -> int:
        return self._api._NbMotor

    def IsReady(self) -> bool :
        return self._Ready
    
    def UpdateFunc(self) :
        def decorator(func):

            if(self._updateFunc == None ): 
                self._updateFunc = func
            else :
                print("Update function is already set.")
            
            return func
        return decorator
    
    def Run(self, name : str = None) : 

        if( not self._api.RegisterClient(name)): return

        try:
            self._updateFunc()

        except:
            print("ERROR")

        while( not self._api.UnregisterClient() ):
            pass

        pass