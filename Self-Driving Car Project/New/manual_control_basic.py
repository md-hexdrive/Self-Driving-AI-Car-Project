import os
import sys
from threading import Thread
import pygame
from time import sleep
from pygame.locals import *

from driving import *
#import record_driving

pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption('Manual Control of AI Car')
screen.fill((255,255,255))
pygame.mouse.set_visible(0)
pygame.key.set_repeat(0,0)
pygame.display.update()



def manual_control():
    stopDriving(True)

    while True:
        os.system("xset r rate 30 30")
        for event in pygame.event.get():
            if (event.type == KEYDOWN):
                if event.key == K_LEFT:
                    print("left key")
                    turnLeft()
                    
                if event.key == K_RIGHT:
                    print("right key")
                    turnRight()
                    
                if event.key == K_UP:
                    print("up key")
                    driveForward()
                    
                if event.key == K_DOWN:
                    print("down key")
                    driveBackward()
                    
                if event.key == K_SPACE:
                    print("space key")
                    stopDriving()
                    #record_driving.running = False
                    pygame.quit()
                    sys.exit()
                    
            
            elif (event.type == KEYUP):
                if event.key == K_LEFT:
                    print("left key released")
                    turnStraight()
                    
                if event.key == K_RIGHT:
                    print("right key released")
                    turnStraight()
                    
                if event.key == K_UP:
                    print("up key released")
                    stopDriving()
                    
                if event.key == K_DOWN:
                    print("down key released")
                    stopDriving()
                
                if event.key == K_SPACE:
                    print("space key released")
                    stopDriving()
                    #record_driving.running = False
                    pygame.quit()
                    sys.exit()

#recorder = record_driving.RecordDriving(0)
#recordingThread = Thread(target = recorder.start_recording)
controlThread = Thread(target = manual_control)

#recordingThread.run()
controlThread.run()