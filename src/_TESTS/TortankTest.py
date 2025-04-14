if __name__ == "__main__":
    
    import time
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from Tortank.Tortank import Tortank, PIDController3Tanks

    tortank : Tortank = Tortank()

    controller = PIDController3Tanks(
        Kp=1.0,
        Ki=0.1,
        Kd=0.01,
        dt=1,
    )

    # @tortank.UpdateFunc()
    def funcTest():
        
        if( not tortank.IsReady() ): 
            print("Carapuce isn't ready")

        time.sleep(10)

        print(f"Water levels : {tortank.GetWaterLevels()}")
        tortank.SetMotorsSpeed( [ {"MotorIndex": 0, "MotorSpeed": 1}, {"MotorIndex": 1, "MotorSpeed": 1}, {"MotorIndex": 2, "MotorSpeed": 1} ] )
        print(f"Motors speed : {tortank.GetMotorsSpeed()}")

        time.sleep(5)

        print(f"Water levels : {tortank.GetWaterLevels()}")
        tortank.SetMotorsSpeed( [ {"MotorIndex": 0, "MotorSpeed": 0}, {"MotorIndex": 1, "MotorSpeed": 0}, {"MotorIndex": 2, "MotorSpeed": 0} ] )
        print(f"Motors speed : {tortank.GetMotorsSpeed()}")

        time.sleep(10)

        print(f"Water levels : {tortank.GetWaterLevel1()}")
        tortank.SetMotor1Speed(1)
        print(f"Motors speed : {tortank.GetMotor1Speed()}")

        time.sleep(5)

        print(f"Water levels : {tortank.GetWaterLevel1()}")
        tortank.SetMotor1Speed(0)
        print(f"Motors speed : {tortank.GetMotor1Speed()}")

    @tortank.UpdateFunc()
    def funcPID():
        # À chaque itération de simulation ou mesure :
        h1, h2, h3 = tortank.GetWaterLevels()
        print(f"Water levels : {h1}, {h2}, {h3}")
        Q1_speed, Q2_speed = controller.update([h1, h2, h3])
        print(f"Motor speeds : {Q1_speed}, {Q2_speed}")
        tortank.SetMotorsSpeed([{"MotorIndex": 0, "MotorSpeed": Q1_speed}, {"MotorIndex": 1, "MotorSpeed": Q2_speed}])
        time.sleep(1)

    tortank.Run("Tortank Test")  
