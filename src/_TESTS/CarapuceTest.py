if __name__ == "__main__":
    
    import time
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from Carapuce.Carapuce import Carapuce

    carapuce : Carapuce = Carapuce()

    @carapuce.UpdateFunc()
    def func():
        if( not carapuce.IsReady() ): 
            print("Carapuce isn't ready")

        print(f"Water Level : {carapuce.GetWaterLevel()}")
        carapuce.SetMotorSpeed(1)
        print(f"Motor Speed : {carapuce.GetMotorSpeed()}")
        time.sleep(5)
        print(f"Water Level : {carapuce.GetWaterLevel()}")
        carapuce.SetMotorSpeed(0)
        print(f"Motor Speed : {carapuce.GetMotorSpeed()}")

        time.sleep(10)

        print(f"Water Level : {carapuce._api.GetWaterLevels()}")
        carapuce._api.SetMotorsSpeed( [ {"MotorIndex": 0, "MotorSpeed": 1} ] )
        print(f"Motor Speed : {carapuce._api.GetMotorsSpeed()}")
        time.sleep(5)
        print(f"Water Level : {carapuce._api.GetWaterLevels()}")
        carapuce._api.SetMotorsSpeed( [ {"MotorIndex": 0, "MotorSpeed": 0} ] )
        print(f"Motor Speed : {carapuce._api.GetMotorsSpeed()}")

    carapuce._updateFunc()