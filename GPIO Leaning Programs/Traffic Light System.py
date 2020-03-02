from gpiozero import Button, TrafficLights, Buzzer
from time import sleep

lButton = Button(3)
rButton = Button(2)

tr1 = TrafficLights(7, 8, 25)
tr2 = TrafficLights(21, 20, 16)

left_light_sequence = False

tr1.green.on()
tr1.amber.off()
tr1.red.off()

tr2.green.off()
tr2.amber.off()
tr2.red.on()

def lightSequence1():
    tr2.green.off()
    tr2.amber.on()
    sleep(3)
    tr2.amber.off()
    tr2.red.on()
    sleep(3)
    
    tr1.red.off()
    tr1.green.on()
    left_light_sequence = True
    delay(20)
    tr1.green.off()
    tr1.amber.on()
    sleep(3)
    tr1.amber.off()
    tr1.red.on()
    sleep(3)

def lightSequence2():
    tr1.green.off()
    tr1.amber.on()
    sleep(3)
    tr1.amber.off()
    tr1.red.on()
    
    sleep(3)
    tr2.red.off()
    tr2.green.on()
    left_light_sequence = False
    delay(20)
    tr2.green.off()
    tr2.amber.on()
    sleep(3)
    tr2.amber.off()
    tr2.red.on()
    sleep(3)
    
def delay(seconds):
    count = seconds * 50
    iter = 0
    while True:
        iter +=1
        if iter > count:
            break
        if lButton.is_pressed and not left_light_sequence:
            lightSequence1()
            break
        elif rButton.is_pressed and left_light_sequence:
            lightSequence2()
            break
        sleep(.02)
    


while True:
    tr1.red.off()
    tr1.green.on()
    left_light_sequence = True
    delay(20)
    tr1.green.off()
    tr1.amber.on()
    sleep(3)
    tr1.amber.off()
    tr1.red.on()
    
    sleep(3)
    tr2.red.off()
    tr2.green.on()
    left_light_sequence = False
    delay(20)
    tr2.green.off()
    tr2.amber.on()
    sleep(3)
    tr2.amber.off()
    tr2.red.on()
    sleep(3)
    
    
