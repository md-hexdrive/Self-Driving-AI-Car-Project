import pygame

from time import sleep
from pygame.locals import *

from driving import *


def pygameSetup():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Manual Control of AI Car')
    screen.fill((255,255,255))
    pygame.mouse.set_visible(0)
    pygame.key.set_repeat(0,0)
    pygame.display.update()

def showtext(txt):
    fontObj = pygame.font.Font('freesansbold.ttf', 64)
    textSurface = fontObj.render(txt, True, (102, 0, 102), (255, 255, 255))
    textRectObj = textSurface.get_rect()
    textRectObj.center = (320, 200)
    screen.fill((255,255,255))
    screen.blit(textSurface, textRectObj)
    pygame.display.update()

def showDistance(dist):
    showtext(str(dist) + " cm")
#showDistance(110)