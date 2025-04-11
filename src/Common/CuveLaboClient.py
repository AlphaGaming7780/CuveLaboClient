import socket
import threading
import time
from typing import Callable

import requests
from Common.CuveLaboAPI import CuveLaboAPI

class CuveLaboClient(object):

    class UpdateThread(threading.Thread):
        def __init__(self, update_func):
            super().__init__()
            self._updateFunc = update_func
            self._running = threading.Event()
            self._running.set()

        def stop(self):
            self._running.clear()

        def run(self):
            while self._running.is_set():
                try:
                    self._updateFunc()
                except Exception as e:
                    print(f"[UpdateThread] Une erreur est survenue : {e}")
                    self.stop()
                # time.sleep(1)  # Facultatif, selon la fréquence de mise à jour souhaitée


    _api : CuveLaboAPI
    _Ready : bool = False
    _updateFunc = None
    _Ip = ""

    _sseThread : CuveLaboAPI.SSEListenerThread
    _updateThread : UpdateThread

    def __init__(self, serverIP : str, serverPort : str = "5000"):
        
        self._api = CuveLaboAPI(serverIP, serverPort)
        self._Ready = self._api.GetBaseData()

        # response = requests.get('https://api.ipify.org?format=json')
        # self._Ip = response.json()['ip']
        self._Ip = self.get_local_ip()
        print(self._Ip)
        pass

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Connexion bidon juste pour récupérer l’IP locale assignée
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip


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
        
        if( not self.IsReady() ): 
            print("Isn't ready")
            return

        print("[Main] Lancement du thread SSE.")
        self._sseThread = self._api.CreateClientDataUpdateStream()
        self._sseThread.start()

        self._updateThread = self.UpdateThread(self._updateFunc)

        time.sleep(1)

        try:

            if( not self._api.RegisterClient(name)): return

            while( self._sseThread.data == None or self._sseThread.data["ActiveClient"] != self._Ip ):
                data = None
                if(self._sseThread.data != None): data = self._sseThreadself._sseThread.data["ActiveClient"]
                print(f"Waiting the authorization from the server to run. Current Client : {data}")
                if( not self._api.SignalClientIsStillActive()):
                    self.End()
                    return
                time.sleep(1)

            print("Starting.")
            self.ShouldEnd = False

            self._updateThread.start()

            while(self._sseThread.data["ActiveClient"] == self._Ip and not self.ShouldEnd) :
                if(not self._api.SignalClientIsStillActive()):
                    self.End()
                time.sleep(1)

            self.End()
            return

        except KeyboardInterrupt:
            self.End()
            return

    def Stop(self):
        self.ShouldEnd = True

    def End(self):
        self._api.UnregisterClient()
        if(self._updateThread.is_alive()):
            self._updateThread.stop()
            # self._updateThread.join(5)
        print("[Main] Interruption reçue, arrêt du thread...")
        self._api.KillClientDataUpdateStream(self._sseThread)