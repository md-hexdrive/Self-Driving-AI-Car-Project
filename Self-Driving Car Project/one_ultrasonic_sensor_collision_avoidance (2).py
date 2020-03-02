from driving import *
from pygame_status_window import *

from time import sleep
from gpiozero import DistanceSensor


warn_threshold = 65
stop_threshold = 45

ultrasonic = DistanceSensor(echo = 19, trigger = 26)

#pygameSetup()

def getDistance():
    return int(ultrasonic.distance * 100)

while True:
    distance = getDistance()
    print(distance)
    #showDistance(distance)
    
    if(distance < stop_threshold):
        #stopDriving()
        #sleep(2)
        
        turnLeft()
        driveBackward()
    
    elif(distance < warn_threshold):
        turnRight()
        driveForward()
    else:
        straightenWheels()
        driveForward()
    
  
    
    