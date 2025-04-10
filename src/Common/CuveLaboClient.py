from typing import Callable
from Common.CuveLaboAPI import CuveLaboAPI

class CuveLaboClient(object):

    _api : CuveLaboAPI

    _updateFunc = None

    def __init__(self, serverIP : str, serverPort : str = "5000"):
        
        self._api = CuveLaboAPI(serverIP, serverPort)

        pass

    def NumberOfCuve(self) -> int:
        return self._api._NbCuve
    
    def NumberOfMotor(self) -> int:
        return self._api._NbMotor

    def IsReady(self) -> bool :
        return self._api._Ready
    
    def UpdateFunc(self) :
        def decorator(func):

            if(self._updateFunc == None ): 
                self._updateFunc = func
            else :
                print("Update function is already set.")
            
            return func
        return decorator
