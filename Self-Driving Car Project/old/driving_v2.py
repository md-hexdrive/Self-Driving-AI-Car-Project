
from gpiozero import DigitalOutputDevice
from gpiozero import PWMOutputDevice
from time import sleep

# TODO : Give these pins the correct number
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

def fullBrake(centerWheels = False):
    forward.value = True
    backward.value = True
    
    drive.value = 0
    
    if(centerWheels):
        straightenWheels()
    
    sleep(0.1)
    
    stopDriving()


def stopDriving(centerWheels = False):
    forward.value = False
    backward.value = False
    
    drive.value = 0
    
    if(centerWheels):
        straightenWheels()

def driveForward(straightWheels = False):
    if not isDrivingForwards():
        forward.value = True
        backward.value = False
        
        drive.value = .5
    
    if straightWheels:
        straightenWheels()

def driveBackward():
    if not isBackingUp():
        forward.value = False
        backward.value = True
        
        drive.value = .8

def straightenWheels():
    if not isTurnedStraight():
        left.value = True
        right.value = True
        
        turn.value = 0
        
        sleep(0.05)
        
        left.value = False
        right.value = False
        
        return

def turnStraight():
    straightenWheels()
    
def turnLeft():
    if not isTurnedLeft():
        left.value = True
        right.value = False
        
        turn.value = 1

def turnRight():
    if not isTurnedRight():
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
    setSteeringPos(1)
    print(getSteeringPos())
