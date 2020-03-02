
from gpiozero import DigitalOutputDevice
from gpiozero import PWMOutputDevice
from time import sleep

# TODO: Give these pins the correct number
PWMA_FB = 21
FORWARD_PIN = 20
REVERSE_PIN = 16

PWMB_LR = 14
LEFT_PIN = 15
RIGHT_PIN = 18

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

def turnStraight():
    straightenWheels()
    
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
    return bool(forward.value and (not backward.value))
def isBackingUp():
    return bool((not forward.value) and backward.value)
def isStopped():
    return bool((forward.value and backward.value) or (not forward.value and not backward.value))

def isTurnedStraight():
    return bool(not left.value and not right.value)

def isTurnedLeft():
    return bool(left.value and not right.value)
def isTurnedRight():
    return bool(not left.value and right.value)
if __name__ == '__main__':
    driveForward()
    
    print("Going Forward: " + str(isDrivingForwards()))
    print("Going Backwards: " + str(isBackingUp()))
    print("Stopped: " + str(isStopped()))
    print('\n\n')
    turnLeft()
    print("Turned Straight: " + str(isTurnedStraight()))
    print("Turned Left: " + str(isTurnedLeft()))
    print("Turned Right: " + str(isTurnedRight()))
    print('\n\n')
    #sleep(5)
    turnStraight()
    print("Turned Straight: " + str(isTurnedStraight()))
    print("Turned Left: " + str(isTurnedLeft()))
    print("Turned Right: " + str(isTurnedRight()))
    print('\n\n')
    stopDriving()
    print("Going Forward: " + str(isDrivingForwards()))
    print("Going Backwards: " + str(isBackingUp()))
    print("Stopped: " + str(isStopped()))
