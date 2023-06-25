
from gpiozero import DigitalOutputDevice
from gpiozero import PWMOutputDevice
from time import sleep

# TODO: Give these pins the correct number
PWMA_FB = 22
FORWARD_PIN = 17
REVERSE_PIN = 27

PWMB_LR = 13
LEFT_PIN = 6
RIGHT_PIN = 5

drive = PWMOutputDevice(PWMA_FB, True, 0, 1000)
turn = PWMOutputDevice(PWMB_LR, True, 0, 1000)

forward = DigitalOutputDevice(FORWARD_PIN)
backward = DigitalOutputDevice(REVERSE_PIN)
left = DigitalOutputDevice(LEFT_PIN)
right = DigitalOutputDevice(RIGHT_PIN)


def fullBrake():
    forward.value = True
    backward.value = True
    
    drive.value = 0
def stopDriving(centerWheels = False):
    forward.value = False
    backward.value = False
    
    drive.value = 0
    
    if(centerWheels):
        straightenWheels()

def driveForward(straightWheels = False):
    forward.value = True
    backward.value = False
    
    drive.value = 1
    
    if straightWheels:
        straightenWheels()

def driveBackward():
    forward.value = False
    backward.value = True
    
    drive.value = 1

def straightenWheels():
    left.value = False
    right.value = False
    
    turn.value = 0
    return

def turnLeft():
    left.value = True
    right.value = False
    
    turn.value = 1

def turnRight():
    left.value = False
    right.value = True
    
    turn.value = 1

def driveForTime(seconds = 10):
    driveForward(straightWheels = True)
    sleep(seconds)
    stopDriving()

def isDrivingForwards():
    return forward.value
def isBackingUp():
    return backward.value
def isTurnedStraight():
    if not left.value and not right.value:
        return True
    else:
        return False

def isTurnedLeft():
    return left.value
def isTurnedRight():
    return right.value
if __name__ == '__main__':
    driveForward()
    #turnRight()
    sleep(5)
    stopDriving()