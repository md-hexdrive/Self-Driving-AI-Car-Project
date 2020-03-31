from gpiozero import LED
from time import sleep
from signal import pause

led = LED(7)


led.blink(.5, .5)
pause()