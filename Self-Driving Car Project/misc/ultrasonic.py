from driving import *
from time import sleep
from gpiozero import DistanceSensor

import random
ultrasound = DistanceSensor(echo = 19, trigger = 26,
                            threshold_distance = .45)

running = False



def avoidObstacles(threshold = 20):
    if running:
        print("avoid")
        if(ultrasound.distance < threshold):
            stopDriving()
            sleep(2)
            turnLeft()
            driveBackward()
            while(ultrasound.distance < ultrasound.threshold_distance):
                pass
            stopDriving()
            sleep(2)
            straightenWheels()
            return
            
        else:
            turnRight()
            driveForward()

#ultrasound.when_in_range = avoidObstacles
#ultrasound.when_out_of_range = driveForTime


"""
def getDistance():
    while True:
        dist = int(ultrasound.distance * 100)
        print(dist)
        if dist < 45:
            turnRight()
        else:
            straightenWheels()

getDistance()
"""
#driveForTime()
#running = True
#sleep(20)
#running = False


driveForward()
ultrasound.wait_for_in_range(8)
#sleep(1)
stopDriving()
