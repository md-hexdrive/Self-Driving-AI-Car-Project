from gpiozero import Button
from time import sleep

button = Button(3)

while True:
    print(button.is_pressed)
    sleep(.25)