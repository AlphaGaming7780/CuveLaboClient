from Common.CuveLaboClient import CuveLaboClient

class Carapuce(CuveLaboClient) : 

    def __init__(self, serverIP : str = "10.20.30.141", serverPort : str = "5000"):
        super().__init__(serverIP, serverPort)
        pass

    def SetMotorSpeed(self, speed : float):

        if ( speed < 0 ) : speed = 0
        if ( speed > 1 ) : speed = 1

        self._api.SetMotorSpeed(0, speed)

    def GetMotorSpeed(self) -> float:
        return self._api.GetMotorSpeed(0)

    def GetWaterLevel(self) -> float:
        return self._api.GetWaterLevel(0)