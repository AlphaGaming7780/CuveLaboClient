import json
import threading
from typing import Any, List, TypedDict
import requests
import sseclient

class MotorCommand(TypedDict):
    MotorIndex: int
    MotorSpeed: float

class CuveLaboAPI(object):

    class SSEListenerThread(threading.Thread):
        def __init__(self, url):
            super().__init__()
            self.url = url
            self._running = threading.Event()
            self._running.set()
            self.session = requests.Session()
            self.data = None

        def stop(self):
            self._running.clear()
            self.session.close()

        def run(self):
            try:
                while(True):
                # with self.session.get(self.url, stream=True) as response:
                    # client = sseclient.SSEClient(response)
                    client = sseclient.SSEClient(self.url)
                    for event in client:
                        if not self._running.is_set():
                            print("[SSE] Arrêt du thread demandé.")
                            return
                        try:
                            self.data = json.loads(event.data)  # <- ici le fix
                            print("[SSE] Donnée reçue :", self.data)
                        except json.JSONDecodeError as e:
                            print("[SSE] Erreur de parsing JSON :", e)
            except Exception as e:
                print("[SSE] Erreur :", e)
                # print(response.headers)


    REGISTER_CLIENT = "RegisterClient"
    UNREGISTER_CLIENT = "UnregisterClient"

    SIGNAL_CLIENT_IS_STILL_ACTIVE = "ClientIsStillActive"

    CLIENT_DATA_UPDATE = "ClientsDataUpdate"

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

    def __init__(self, serverIP : str, serverPort : str = "5000"):
 
        self._serverIP = serverIP
        self._serverPort = serverPort
        pass

    def CreateClientDataUpdateStream(self) -> SSEListenerThread:
        return self.SSEListenerThread(self.FormatRequestLink(self.CLIENT_DATA_UPDATE))
    
    def KillClientDataUpdateStream(self, sse_thread : SSEListenerThread ):
        if(not sse_thread.is_alive()): return
        sse_thread.stop()
        # sse_thread.join()

    def FormatRequestLink(self, command : str) -> str:
        return f"http://{self._serverIP}:{self._serverPort}/{command}"
    
    def Post(self, command : str, json : Any = None) -> bool:
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
    
    def RegisterClient(self, name : str) -> bool :
        return self.Post(self.REGISTER_CLIENT, {"Name": name})

    def UnregisterClient(self) -> bool :
        return self.Post(self.UNREGISTER_CLIENT)

    def SignalClientIsStillActive(self):
        return self.Post(self.SIGNAL_CLIENT_IS_STILL_ACTIVE)

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
        
    

