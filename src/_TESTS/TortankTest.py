if __name__ == "__main__":
    
    import time
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from Tortank.Tortank import Tortank

    tortank : Tortank = Tortank()

    @tortank.UpdateFunc()
    def func():
        
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


    tortank.Run()  