"""
 
File: skidsteer_two_pwm_test.py
 
This code will test Raspberry Pi GPIO PWM on four GPIO
pins. The code test ran with L298N H-Bridge driver module connected.
 
Website:    www.bluetin.io
Date:       27/11/2017
"""
 
__author__ = "Mark Heywood"
__version__ = "0.1.0"
__license__ = "MIT"
 
from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from time import sleep
 
#///////////////// Define Motor Driver GPIO Pins /////////////////
# Motor A, Left Side GPIO CONSTANTS
PWM_DRIVE_LEFT = 21     # ENA - H-Bridge enable pin
FORWARD_LEFT_PIN = 26   # IN1 - Forward Drive
REVERSE_LEFT_PIN = 19   # IN2 - Reverse Drive
# Motor B, Right Side GPIO CONSTANTS
PWM_DRIVE_RIGHT = 5     # ENB - H-Bridge enable pin
FORWARD_RIGHT_PIN = 13  # IN1 - Forward Drive
REVERSE_RIGHT_PIN = 6   # IN2 - Reverse Drive
 
# Initialise objects for H-Bridge GPIO PWM pins
# Set initial duty cycle to 0 and frequency to 1000
driveLeft = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 1000)
driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0, 1000)
 
# Initialise objects for H-Bridge digital GPIO pins
forwardLeft = DigitalOutputDevice(FORWARD_LEFT_PIN)
reverseLeft = DigitalOutputDevice(REVERSE_LEFT_PIN)
forwardRight = DigitalOutputDevice(FORWARD_RIGHT_PIN)
reverseRight = DigitalOutputDevice(REVERSE_RIGHT_PIN)
 
def allStop():
    forwardLeft.value = False
    reverseLeft.value = False
    forwardRight.value = False
    reverseRight.value = False
    driveLeft.value = 0
    driveRight.value = 0
 
def forwardDrive():
    forwardLeft.value = True
    reverseLeft.value = False
    forwardRight.value = True
    reverseRight.value = False
    driveLeft.value = 1.0
    driveRight.value = 1.0
 
def reverseDrive():
    forwardLeft.value = False
    reverseLeft.value = True
    forwardRight.value = False
    reverseRight.value = True
    driveLeft.value = 1.0
    driveRight.value = 1.0
 
def spinLeft():
    forwardLeft.value = False
    reverseLeft.value = True
    forwardRight.value = True
    reverseRight.value = False
    driveLeft.value = 1.0
    driveRight.value = 1.0
 
def SpinRight():
    forwardLeft.value = True
    reverseLeft.value = False
    forwardRight.value = False
    reverseRight.value = True
    driveLeft.value = 1.0
    driveRight.value = 1.0
 
def forwardTurnLeft():
    forwardLeft.value = True
    reverseLeft.value = False
    forwardRight.value = True
    reverseRight.value = False
    driveLeft.value = 0.2
    driveRight.value = 0.8
 
def forwardTurnRight():
    forwardLeft.value = True
    reverseLeft.value = False
    forwardRight.value = True
    reverseRight.value = False
    driveLeft.value = 0.8
    driveRight.value = 0.2
 
def reverseTurnLeft():
    forwardLeft.value = False
    reverseLeft.value = True
    forwardRight.value = False
    reverseRight.value = True
    driveLeft.value = 0.2
    driveRight.value = 0.8
 
def reverseTurnRight():
    forwardLeft.value = False
    reverseLeft.value = True
    forwardRight.value = False
    reverseRight.value = True
    driveLeft.value = 0.8
    driveRight.value = 0.2
 
def main():
    allStop()
    forwardDrive()
    sleep(5)
    reverseDrive()
    sleep(5)
    spinLeft()
    sleep(5)
    SpinRight()
    sleep(5)
    forwardTurnLeft()
    sleep(5)
    forwardTurnRight()
    sleep(5)
    reverseTurnLeft()
    sleep(5)
    reverseTurnRight()
    sleep(5)
    allStop()
 
 
if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()