
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

def fullBrake(centerWheels = False):
    forward.value = True
    backward.value = True
    
    drive.value = 0
    
    if(centerWheels):
        straightenWheels()


def stopDriving(centerWheels = True):
    forward.value = False
    backward.value = False
    
    drive.value = 0
    
    if(centerWheels):
        straightenWheels()

def driveForward(straightWheels = False):
    forward.value = True
    backward.value = False
    
    drive.value = .5
    
    if straightWheels:
        straightenWheels()

def driveBackward():
    forward.value = False
    backward.value = True
    
    drive.value = .8

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

def setSteeringPos(pos):
    
    if pos == 0:
        turnLeft()
    elif pos == 1:
        turnStraight()
    elif pos == 2:
        turnRight()
    else:
        print("ERROR - incorrect steering position %f" % pos)

def getSteeringPos():
    pos = turn.value
    if isTurnedLeft():
        pos *= -1
    return pos + 1

def setDrivingSpeed(speed):
    if abs(speed) > 1:
        print('Error, incorrect value for driving speed')
        return
    if speed > 0: # go forwards
        forward.value = True
        backward.value = False
    elif speed < 0: # go backwards
        forward.value = False
        backward.value = True
    elif speed == 0: # stopped
        forward.value = False
        backward.value = False
    drive.value = abs(speed)

def getDrivingSpeed():
    speed = drive.value
    if isBackingUp():
        speed *= -1
    return speed + 1
if __name__ == '__main__':
    setSteeringPos(-.8)
    print(getSteeringPos())