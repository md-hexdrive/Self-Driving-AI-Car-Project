import os
import sys
from threading import Thread
import pygame
from time import sleep
from pygame.locals import *

from driving import *
#import record_driving

import pygame.camera
import pygame.image

# def setup():
#     pygame.init()
#     
#     pygame.camera.init()
#     cameras = pygame.camera.list_cameras()
#     print("Using camera %s ..." % cameras[0])
#     webcam = pygame.camera.Camera(cameras[0])
#     webcam.start()
#     
#     # grab first frame
#     img = webcam.get_image()
#     
#     WIDTH = img.get_width()
#     HEIGHT = img.get_height()
#     
#     screen = pygame.display.set_mode((WIDTH,HEIGHT))
#     pygame.display.set_caption('pyGame Camera View')
#     
# #     screen = pygame.display.set_mode((640,480))
# #     pygame.display.set_caption('Manual Control of AI Car')
# #     screen.fill((255,255,255))
#     pygame.mouse.set_visible(0)
#     pygame.key.set_repeat(0,0)
#     pygame.display.update()



def manual_control():
    stopDriving(True)
    
    pygame.init()
    pygame.camera.init()
    cameras = pygame.camera.list_cameras()
    print("Using camera %s ..." % cameras[0])
    webcam = pygame.camera.Camera(cameras[0])
    webcam.start()
    
    # grab first frame
    img = webcam.get_image()
    
    WIDTH = img.get_width()
    HEIGHT = img.get_height()
    
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('pyGame Camera View')
    
#     screen = pygame.display.set_mode((640,480))
#     pygame.display.set_caption('Manual Control of AI Car')
#     screen.fill((255,255,255))
    pygame.mouse.set_visible(0)
    pygame.key.set_repeat(0,0)
    pygame.display.update()

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
                    
            elif (event.type == pygame.QUIT):
                sys.exit()
        
        # draw frame
        screen.blit(img, (0,0))
        pygame.display.flip()
        # grab next frame
        img = webcam.get_image()

def run():
#     setup()
    manual_control()
if __name__=='__main__':
    #recorder = record_driving.RecordDriving(0)
    #recordingThread = Thread(target = recorder.start_recording)
    controlThread = Thread(target = run)

    #recordingThread.run()
    controlThread.run()
