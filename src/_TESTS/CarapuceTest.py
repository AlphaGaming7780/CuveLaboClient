if __name__ == "__main__":
    
    import time
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from Carapuce.Carapuce import Carapuce

    carapuce : Carapuce = Carapuce()

    @carapuce.UpdateFunc()
    def func():
        waterLevel = carapuce.GetWaterLevel()

        if(waterLevel < 0.18):
            carapuce.SetMotorSpeed(1)
        else:
            carapuce.SetMotorSpeed(0.82 - ( waterLevel - 0.18) * 15 / 0.82)


    carapuce.Run("Carapuce Test")  