import sys
import os
import os.path
import driving
import record_driving
import pygame
from pygame.locals import *

import cv2

def setup_controller():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Manual Control of AI Car')
    screen.fill((255,255,255))
    pygame.mouse.set_visible(0)
    pygame.key.set_repeat(0,0)
    pygame.display.update()

def setup_recording():
    recorder = record_driving.RecordDriving(0)
    

if __name__ == '__main__':
    setup_controller()
    recorder = setup_recording()
    