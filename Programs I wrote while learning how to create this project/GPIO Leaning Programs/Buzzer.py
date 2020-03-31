from gpiozero import PWMOutputDevice
from time import sleep

buzzer = PWMOutputDevice(15, True, 0, 1318)

buzzer.value = .5

while True:
    buzzer.value = .5
    sleep(.5)
    buzzer.value = 0
    sleep(.5)