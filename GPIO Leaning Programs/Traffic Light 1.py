from gpiozero import LED
from time import sleep

red = LED(7)
amber = LED(8)
green = LED(25)

green.on()
amber.off()
red.off()

while True:
    sleep(10)
    green.off()
    amber.on()
    sleep(3)
    amber.off()
    red.on()
    sleep(10)
    
    red.off()
    green.on()