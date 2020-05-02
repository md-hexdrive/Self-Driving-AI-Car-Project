from gpiozero import DistanceSensor
from driving import *
from time import sleep

threshold = 1

left = DistanceSensor(echo = 26, trigger = 2, max_distance = 4, threshold_distance = threshold)
center = DistanceSensor(echo = 19, trigger = 3, max_distance = 4, threshold_distance = threshold)
right = DistanceSensor(echo = 6, trigger = 4, max_distance = 4, threshold_distance = threshold)

def turnDirection():
    if center.distance > threshold and left.distance > threshold and right.distance > threshold:
        turnStraight()
        driveForward()
        
        
    elif left.distance < threshold and right.distance < threshold and not center.distance < threshold:
        turnStraight()
        driveForward()
    
    elif not left.distance < threshold and right.distance < threshold and center.distance < threshold and center.distance > .4:
        turnLeft()
        driveForward()

    elif left.distance < threshold and not right.distance < threshold and center.distance < threshold and center.distance > .4:
        turnRight()
        driveForward()
    
    
    elif left.distance < 1:
        turnRight()
    elif right.distance < 1:
        turnLeft()
    else:
        fullBrake()

center.when_in_range = turnDirection
center.when_out_of_range = turnDirection

right.when_in_range = turnDirection
right.when_out_of_range = turnDirection

left.when_in_range = turnDirection
left.when_out_of_range = turnDirection