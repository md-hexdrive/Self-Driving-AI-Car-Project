import sys
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
pygame.key.set_repeat()
pygame.display.update()

#record_driving.run_recording_thread()
try:
    stopDriving(True)

    while True:
    
        #print("doing a function")
        for event in pygame.event.get():
            if (event.type == KEYDOWN):
                if event.key == K_LEFT:
                    print("left key")
                    
                if event.key == K_RIGHT:
                    print("right key")
                
                if event.key == K_UP:
                    print("up key")
                
                if event.key == K_DOWN:
                    print("down key")
                
                if event.key == K_SPACE:
                    print("space key")
                    
            
            elif (event.type == KEYUP):
                if event.key == K_LEFT:
                    print("left key released")
                    
                if event.key == K_RIGHT:
                    print("right key released")
                
                if event.key == K_UP:
                    print("up key released")
                
                if event.key == K_DOWN:
                    print("down key released")
                
                if event.key == K_SPACE:
                    print("space key released")
                    
        
            """        
            if ((event.type == KEYDOWN) or (event.type == KEYUP)):
                if ((event.type == KEYDOWN) or (event.type == KEYUP)) and event.key == K_SPACE:
                    print("space key")
                    stopDriving()
                    return
                
                elif (event.type == KEYDOWN) and event.key == K_UP:
                        print("up arrow")
                        driveForward()
                elif (event.type == KEYUP) and event.key == K_UP:
                        stopDriving()
                        print("up arrow release")
                        
                elif (event.type == KEYDOWN) and event.key == K_DOWN:
                        print("down arrow")
                        driveBackward()
                elif (event.type == KEYUP) and event.key == K_DOWN:
                        stopDriving()
                        print("down arrow release")
                        
                elif (event.type == KEYDOWN) and event.key == K_LEFT:
                        print("left arrow")
                        turnLeft()
                elif (event.type == KEYUP) and event.key == K_LEFT:
                        straightenWheels()
                        print("left arrow release")
                        
                elif (event.type == KEYDOWN) and event.key == K_RIGHT:
                        print("right arrow")
                        turnRight()
                elif (event.type == KEYUP) and event.key == K_RIGHT:
                        straightenWheels()
                        print("right arrow release")
                
                """
                

finally:
    stopDriving(True)

stopDriving(True)
pygame.quit()
sys.exit()