from typing import List
from Common.CuveLaboAPI import MotorCommand
from Common.CuveLaboClient import CuveLaboClient

class Tortank(CuveLaboClient) : 

    def __init__(self, serverIP : str = "10.20.30.142", serverPort : str = "5000"):
        super().__init__(serverIP, serverPort)
        pass

    def SetMotor1Speed(self, speed : float) -> bool:

        if ( speed < 0 or speed > 1 ) : 
            print("SetMotor2Speed : speed must be a float between 0 and 1.")
            return False

        return self._api.SetMotorSpeed(0, speed)

    def SetMotor2Speed(self, speed : float) -> bool:

        if ( speed < 0 or speed > 1 ) : 
            print("SetMotor2Speed : speed must be a float between 0 and 1.")
            return False

        return self._api.SetMotorSpeed(1, speed)

    def SetMotorsSpeed(self, motorsCommand : List[MotorCommand]) -> bool:

        if(len(motorsCommand) != 2):
            print("SetMotorsSpeed : motorsCommand must be a list of 2 float.")
            return False

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


# Testing stuff, need to be verified and improved or maybe removed.
# But I think it's a good idea to have a built in PID controller.
# Carapuce doesn't have one.

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

class PIDController2Tanks:
    def __init__(self, Kp1, Ki1, Kd1, Kp2, Ki2, Kd2, dt, Qmin=0.0, Qmax=1.0):
        # Constantes PID pour la cuve 1
        self.Kp1 = Kp1
        self.Ki1 = Ki1
        self.Kd1 = Kd1

        # Constantes PID pour la cuve 2
        self.Kp2 = Kp2
        self.Ki2 = Ki2
        self.Kd2 = Kd2

        # Pas de temps
        self.dt = dt

        # Saturation
        self.Qmin = Qmin
        self.Qmax = Qmax

        # États internes pour la cuve 1
        self.integral_h1 = 0.0
        self.previous_error_h1 = 0.0

        # États internes pour la cuve 2
        self.integral_h2 = 0.0
        self.previous_error_h2 = 0.0

    def update(self, h1_k, h2_k, h1_setpoint, h2_setpoint):
        """
        Met à jour les débits Q1 et Q2 pour maintenir les hauteurs des cuves 1 et 2 à leur consigne.

        :param h1_k: Hauteur actuelle de la cuve 1
        :param h2_k: Hauteur actuelle de la cuve 2
        :param h1_setpoint: Hauteur désirée pour la cuve 1
        :param h2_setpoint: Hauteur désirée pour la cuve 2
        :return: Q1 (pour moteur 1), Q2 (pour moteur 2)
        """

        # PID pour la cuve 1
        error_h1 = h1_setpoint - h1_k
        self.integral_h1 += error_h1 * self.dt
        derivative_h1 = (error_h1 - self.previous_error_h1) / self.dt

        Q1 = self.Kp1 * error_h1 + self.Ki1 * self.integral_h1 + self.Kd1 * derivative_h1
        Q1 = max(min(Q1, self.Qmax), self.Qmin)
        self.previous_error_h1 = error_h1

        # PID pour la cuve 2
        error_h2 = h2_setpoint - h2_k
        self.integral_h2 += error_h2 * self.dt
        derivative_h2 = (error_h2 - self.previous_error_h2) / self.dt

        Q2 = self.Kp2 * error_h2 + self.Ki2 * self.integral_h2 + self.Kd2 * derivative_h2
        Q2 = max(min(Q2, self.Qmax), self.Qmin)
        self.previous_error_h2 = error_h2

        return Q1, Q2  # Q1 → moteur cuve 1, Q2 → moteur cuve 2
    
class PIDController2TanksAntiWindup:
    def __init__(self, Kp1, Ki1, Kd1, Kp2, Ki2, Kd2, dt, Qmin=0.0, Qmax=1.0):
        # Constantes PID pour cuve 1
        self.Kp1 = Kp1
        self.Ki1 = Ki1
        self.Kd1 = Kd1

        # Constantes PID pour cuve 2
        self.Kp2 = Kp2
        self.Ki2 = Ki2
        self.Kd2 = Kd2

        # Pas de temps
        self.dt = dt

        # Bornes de saturation
        self.Qmin = Qmin
        self.Qmax = Qmax

        # États internes pour la cuve 1
        self.integral_h1 = 0.0
        self.previous_error_h1 = 0.0

        # États internes pour la cuve 2
        self.integral_h2 = 0.0
        self.previous_error_h2 = 0.0

    def update(self, h1_k, h2_k, h1_setpoint, h2_setpoint):
        """
        Met à jour les débits Q1 et Q2 pour les cuves 1 et 2 avec anti-windup.

        :param h1_k: Hauteur actuelle cuve 1
        :param h2_k: Hauteur actuelle cuve 2
        :param h1_setpoint: Consigne cuve 1
        :param h2_setpoint: Consigne cuve 2
        :return: Q1 (moteur cuve 1), Q2 (moteur cuve 2)
        """

        # === PID cuve 1 ===
        error_h1 = h1_setpoint - h1_k
        self.integral_h1 += error_h1 * self.dt
        derivative_h1 = (error_h1 - self.previous_error_h1) / self.dt

        # Calcul du signal de commande non saturé
        Q1_unsat = self.Kp1 * error_h1 + self.Ki1 * self.integral_h1 + self.Kd1 * derivative_h1

        # Saturation de la commande
        Q1 = max(self.Qmin, min(self.Qmax, Q1_unsat))

        # Anti-windup : ajustement de l'intégrale si saturation
        if Q1 != Q1_unsat and self.Ki1 != 0:
            self.integral_h1 += (Q1 - Q1_unsat) / self.Ki1

        # Mémorisation de l’erreur pour le calcul du dérivé au prochain appel
        self.previous_error_h1 = error_h1

        # === PID cuve 2 ===
        error_h2 = h2_setpoint - h2_k
        self.integral_h2 += error_h2 * self.dt
        derivative_h2 = (error_h2 - self.previous_error_h2) / self.dt

        Q2_unsat = self.Kp2 * error_h2 + self.Ki2 * self.integral_h2 + self.Kd2 * derivative_h2
        Q2 = max(self.Qmin, min(self.Qmax, Q2_unsat))

        if Q2 != Q2_unsat and self.Ki2 != 0:
            self.integral_h2 += (Q2 - Q2_unsat) / self.Ki2

        self.previous_error_h2 = error_h2

        return Q1, Q2  # Q1 = pour moteur cuve 1 ; Q2 = pour moteur cuve 2

