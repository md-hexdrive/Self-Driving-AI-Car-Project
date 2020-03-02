from driving import *
#from pygame_status_window import *

from time import sleep
from gpiozero import DistanceSensor


warn_threshold = 65
stop_threshold = 45

ultrasonic = DistanceSensor(echo = 19, trigger = 3, max_distance = 4)

#pygameSetup()

def getDistance():
    distance = ultrasonic.distance * 100
    print(distance)
    return distance

stopDriving()
sleep(3)


while True:
    if getDistance() < 100:
        fullBrake()
        
    else:
        driveForward()

fullBrake()
    
    
