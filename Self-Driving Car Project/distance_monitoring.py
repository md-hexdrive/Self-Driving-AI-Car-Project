from gpiozero import DistanceSensor

"""
This file handles the distance sensor while the ai car is driving.
"""
#in_range = False # in_range detects if an object is in range

ultrasonic_sensor = DistanceSensor(echo=19, trigger=3, threshold_distance=.45)
