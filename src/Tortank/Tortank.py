from typing import List
from Common.CuveLaboAPI import MotorCommand
from Common.CuveLaboClient import CuveLaboClient

class Tortank(CuveLaboClient) : 

    def __init__(self, serverIP : str = "10.20.30.142", serverPort : str = "5000"):
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


class PIDController3Tanks:
    def __init__(self, Kp, Ki, Kd, setpoints=(0.5, 0.5, 0.5), dt=0.1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint1, self.setpoint2, self.setpoint3 = setpoints

        self.dt = dt

        # Intégrales et erreurs précédentes
        self.integral1 = 0
        self.prev_error1 = 0

        self.integral3 = 0
        self.prev_error3 = 0

        self.integral2 = 0
        self.prev_error2 = 0

    def set_setpoints(self, sp1, sp2, sp3):
        self.setpoint1 = sp1
        self.setpoint2 = sp2
        self.setpoint3 = sp3

    def update(self, levels: List[float]) -> List[float]:
        level1, level2, level3 = levels

        # PID pour cuve 1
        error1 = self.setpoint1 - level1
        self.integral1 += error1 * self.dt
        derivative1 = (error1 - self.prev_error1) / self.dt
        output1 = self.Kp * error1 + self.Ki * self.integral1 + self.Kd * derivative1
        self.prev_error1 = error1

        # PID pour cuve 3
        error3 = self.setpoint3 - level3
        self.integral3 += error3 * self.dt
        derivative3 = (error3 - self.prev_error3) / self.dt
        output3 = self.Kp * error3 + self.Ki * self.integral3 + self.Kd * derivative3
        self.prev_error3 = error3

        # PID pour cuve 2 (influence les deux moteurs)
        error2 = self.setpoint2 - level2
        self.integral2 += error2 * self.dt
        derivative2 = (error2 - self.prev_error2) / self.dt
        correction2 = self.Kp * error2 + self.Ki * self.integral2 + self.Kd * derivative2
        self.prev_error2 = error2

        # Appliquer la régulation de cuve 2 à moitié sur chaque moteur
        motor1 = output1 + correction2 * 0.5
        motor2 = output3 + correction2 * 0.5

        # Clamp entre 0 et 1
        motor1_clamped = min(max(motor1, 0), 1)
        motor2_clamped = min(max(motor2, 0), 1)

        # Anti-windup basique
        if motor1 != motor1_clamped:
            self.integral1 -= error1 * self.dt
        if motor2 != motor2_clamped:
            self.integral3 -= error3 * self.dt
        if correction2 != (motor1_clamped - output1) * 2:
            self.integral2 -= error2 * self.dt

        # Debug
        print(f"[PID] Errors: e1={error1:.3f}, e2={error2:.3f}, e3={error3:.3f}")
        print(f"[PID] Motor outputs before clamp: m1={motor1:.3f}, m2={motor2:.3f}")
        print(f"[PID] Motor outputs after clamp:  m1={motor1_clamped:.3f}, m2={motor2_clamped:.3f}")

        return motor1_clamped, motor2_clamped


    # def update(self, levels : List[float]) -> List[float]:
    #     level1, level2, level3 = levels

    #     # PID pour cuve 1
    #     error1 = self.setpoint1 - level1
    #     self.integral1 += error1 * self.dt
    #     derivative1 = (error1 - self.prev_error1) / self.dt
    #     output1 = self.Kp * error1 + self.Ki * self.integral1 + self.Kd * derivative1
    #     self.prev_error1 = error1

    #     # PID pour cuve 3
    #     error3 = self.setpoint3 - level3
    #     self.integral3 += error3 * self.dt
    #     derivative3 = (error3 - self.prev_error3) / self.dt
    #     output3 = self.Kp * error3 + self.Ki * self.integral3 + self.Kd * derivative3
    #     self.prev_error3 = error3

    #     # PID pour cuve 2 (influence les deux moteurs)
    #     error2 = self.setpoint2 - level2
    #     self.integral2 += error2 * self.dt
    #     derivative2 = (error2 - self.prev_error2) / self.dt
    #     correction2 = self.Kp * error2 + self.Ki * self.integral2 + self.Kd * derivative2
    #     self.prev_error2 = error2

    #     # Appliquer la régulation de cuve 2 à moitié sur chaque moteur
    #     motor1 = output1 + correction2 * 0.5
    #     motor2 = output3 + correction2 * 0.5

    #     # Clamp entre 0 et 1
    #     motor1 = min(max(motor1, 0), 1)
    #     motor2 = min(max(motor2, 0), 1)

    #     return motor1, motor2



