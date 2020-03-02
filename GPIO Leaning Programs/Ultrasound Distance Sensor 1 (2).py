from gpiozero import DistanceSensor
from time import sleep
ultrasonic = DistanceSensor(echo = 26, trigger = 2, max_distance = 4)

# left sensor: echo = 26, trigger = 2,
# center sensor: echo =  19, trigger = 3,
# right sensor: echo = 6, trigger = 4,
# 2,3,4, + 6, 19, 26
while True:
    print(str(ultrasonic.distance * 100) + "cm")
    sleep(0.1)
    