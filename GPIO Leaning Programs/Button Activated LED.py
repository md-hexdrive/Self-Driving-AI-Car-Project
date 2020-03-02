from gpiozero import Button, TrafficLights, Buzzer

button = Button(3)
tr1 = TrafficLights(25, 8, 7)
tr2 = TrafficLights(16, 20, 21)
buzzer = Buzzer(15)

while True:
    tr2.on()
    buzzer.off()
    button.wait_for_press()
    
    tr2.off()
    #buzzer.on(245)
    button.wait_for_release()
    
    
    