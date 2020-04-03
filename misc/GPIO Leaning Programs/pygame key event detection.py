import pygame
from time import sleep
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption('Manual Control of AI Car')
pygame.mouse.set_visible(0)
pygame.key.set_repeat(0,0)

while True:
    #print("doing a function")
    for event in pygame.event.get():
        if (event.type == KEYUP) or (event.type == KEYDOWN):
            if event.key == K_SPACE:
                print(event.key)
                sleep(0.1)