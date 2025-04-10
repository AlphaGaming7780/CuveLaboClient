import time
from typing import List

# TESTING
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Common.CuveLaboAPI import MotorCommand
from Common.CuveLaboClient import CuveLaboClient

class Tortank(CuveLaboClient) : 

    def __init__(self, serverIP : str = "10.20.30.140", serverPort : str = "5000"):
        super().__init__(serverIP, serverPort)
        pass

    def SetMotor1Speed(self, speed : float) -> bool:

        if ( speed < 0 ) : speed = 0
        if ( speed > 1 ) : speed = 1

        return self._api.SetMotorSpeed(0, speed)

    def SetMotor2Speed(self, speed : float) -> bool:

        if ( speed < 0 ) : speed = 0
        if ( speed > 1 ) : speed = 1

        return self._api.SetMotorSpeed(1, speed)

    def SetMotor3Speed(self, speed : float) -> bool :

        if ( speed < 0 ) : speed = 0
        if ( speed > 1 ) : speed = 1

        return self._api.SetMotorSpeed(2, speed)

    def SetMotorsSpeed(self, motorsCommand : List[MotorCommand]) -> bool:
        return self._api.SetMotorsSpeed(motorsCommand)

    def GetMotor1Speed(self) -> float:
        return self._api.GetMotorSpeed(0)
    
    def GetMotor2Speed(self) -> float:
        return self._api.GetMotorSpeed(1)
    
    def GetMotorsSpeed(self) -> List[float]:
        return self._api.GetMotorsSpeed()

    def GetWaterLevel1(self) -> float:
        return self._api.GetWaterLevel(0)
    
    def GetWaterLevel2(self) -> float:
        return self._api.GetWaterLevel(1)
    
    def GetWaterLevel3(self) -> float:
        return self._api.GetWaterLevel(2)
    
    def GetWaterLevels(self) -> List[float]:
        return self._api.GetWaterLevels()


# TESTING
if __name__ == "__main__":

    tortank : Tortank = Tortank()

