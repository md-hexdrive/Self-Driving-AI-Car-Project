from gpiozero import DistanceSensor
from time import sleep
ultrasonic = DistanceSensor(echo = 19, trigger = 26)

while True:
    print(str(ultrasonic.distance * 100) + "cm")
    