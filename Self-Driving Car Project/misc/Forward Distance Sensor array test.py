from gpiozero import DistanceSensor
from time import sleep

left = DistanceSensor(echo = 26, trigger = 2, max_distance = 4)
center = DistanceSensor(echo = 19, trigger = 3, max_distance = 4)
right = DistanceSensor(echo = 6, trigger = 4, max_distance = 4)

while True:
    leftDist = str(int(left.distance * 100))
    centDist = str(int(center.distance * 100))
    rightDist = str(int(right.distance * 100))
    
    print(leftDist + " " + centDist + " " + rightDist)
    sleep(.1)