from gpiozero import DistanceSensor
from time import sleep
from driving import *
from threading import Thread

running = True
left_clear = True
right_clear = True
center_clear = True

left = DistanceSensor(echo = 26, trigger = 2, max_distance = 4, threshold_distance = 1)
center = DistanceSensor(echo = 19, trigger = 3, max_distance = 4, threshold_distance = 1)
right = DistanceSensor(echo = 6, trigger = 4, max_distance = 4, threshold_distance = 1)


def check_sensors():
    global left_clear
    global right_clear
    global center_clear
    while running:
        leftDist = left.distance
        if left.distance < 1:
            left_clear = False
        else:
            left_clear = True
        
        if center.distance < 1:
            center_clear = False
        else:
            center_clear = True
        
        if right.distance < 1:
            right_clear = False
        else:
            right_clear = True

t1 = Thread(target=check_sensors)
t1.start()

while True:
    centDist = center.distance * 100
    leftDist = left.distance * 100
    rightDist = right.distance * 100
    
    if not center_clear:
        print("obstacle ahead")
        fullBrake()
        straightenWheels()
        
    elif not left_clear:
        print("obstacle to the left")
        turnRight()
        driveForward()
        
    elif not right_clear:
        print("obstacle to the right")
        turnLeft()
        driveForward()
        
    else:
        print("no obstacle")
        driveForward()
    
    sleep(0.05)

fullBrake()