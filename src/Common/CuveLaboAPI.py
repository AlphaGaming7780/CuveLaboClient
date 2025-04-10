from typing import Any, List, TypedDict
import requests

class MotorCommand(TypedDict):
    MotorIndex: int
    MotorSpeed: float

class CuveLaboAPI(object):

    GET_BASE_DATA = "GetBaseData"

    SET_MOTOR_SPEED = "SetMotorSpeed"
    SET_MOTORS_SPEED = "SetMotorsSpeed"
    GET_MOTOR_SPEED = "GetMotorSpeed"
    GET_MOTORS_SPEED = "GetMotorsSpeed"

    GET_WATER_LEVEL = "GetWaterLevel"
    GET_WATER_LEVELS = "GetWaterLevels"

    _serverIP : str
    _serverPort : str

    _NbCuve : int = -1
    _NbMotor : int = -1

    _Ready : bool = False

    def __init__(self, serverIP : str, serverPort : str = "5000"):

        self._serverIP = serverIP
        self._serverPort = serverPort

        self._Ready = self.GetBaseData()
        pass

    def FormatRequestLink(self, command : str) -> str:
        return f"http://{self._serverIP}:{self._serverPort}/{command}"
    
    def Post(self, command : str, json : Any) -> bool:
        response = requests.post(
            self.FormatRequestLink(command),
            json = json
        )
        
        if( not response.ok ) : 
            print(f"Request Post {command}, didn't return an OK code, error : {response.reason}")
            return False
        return True

    
    def Get(self, command: str, params: Any = None) -> Any:
        response = requests.get(
            self.FormatRequestLink(command),
            params=params
        )

        if not response.ok:
            print(f"Request Get {command}, didn't return an OK code, error : {response.reason}")
            return None

        return response.json()
    
    def GetBaseData(self) -> bool:
        data = self.Get(self.GET_BASE_DATA)

        if(data == None): return False
    
        self._NbCuve = data["numberOfCuve"]
        self._NbMotor = data["numberOfMotor"]

        return True


    def SetMotorSpeed(self, motorIdx : int, motorSpeed : float) -> bool :
        if(motorIdx < 0 or motorIdx >= self._NbMotor): return False
        return self.Post(self.SET_MOTOR_SPEED, { "MotorIndex": motorIdx, "MotorSpeed": motorSpeed })

    def SetMotorsSpeed(self, motorsCommand : List[MotorCommand] ) -> bool : 
        return self.Post(self.SET_MOTORS_SPEED, motorsCommand)

    def GetMotorSpeed(self, motorIdx : int) -> float: 
        if(motorIdx < 0 or motorIdx >= self._NbMotor): return -1
        return self.Get(self.GET_MOTOR_SPEED, {"MotorIndex": motorIdx})
    
    def GetMotorsSpeed(self) -> List[float]: 
        return self.Get(self.GET_MOTORS_SPEED)
    
    def GetWaterLevel(self, cuveIndex : int) -> float:
        if(cuveIndex < 0 or cuveIndex >= self._NbCuve): return -1
        return self.Get(self.GET_WATER_LEVEL, {"CuveIndex": cuveIndex})

    def GetWaterLevels(self) -> List[float]:
        return self.Get(self.GET_WATER_LEVELS)
        
    

