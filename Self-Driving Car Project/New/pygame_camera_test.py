import pygame
from pygame.locals import *
import cv2
import os
import os.path
import time
import datetime
from driving import *

# returns the current time, used to uniquely identify recordings
def now():
    return datetime.datetime.now().strftime("%Y_%B_%d_%X") #found this in the DeepPiCar training code

pygame.init()

# setting the width and height of the window
WIDTH, HEIGHT = 480, 320
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RC Car")

# background color 
color = (0, 0, 0)

# 0 is the built in webcam
camera_width = 480
camera_height = 320
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

save_dir = '/home/user/Desktop/recordings/'
is_training=True

intFrameNumber = 0
recording_id = ""
batch_id = ""
recording_type = ""
recording_directory = ""
fourcc = None
video_out = None

# restart recording
def restart():
    global intFrameNumber, recording_id, batch_id, is_training, recording_type, recording_directory
    global camera_width, camera_height, fourcc, video_out
    intFrameNumber = 0
    recording_id = now()
    batch_id = now()
    if is_training:
        recording_type = os.path.join("training", 'batch_id_%s' % batch_id)
    else:
        recording_type = "testing"
    recording_directory = os.path.join(save_dir, "v2", recording_type, str(recording_id), '')
    if not os.path.exists(recording_directory):
        os.makedirs(recording_directory)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_out = cv2.VideoWriter('%svideo_%s.avi' % (recording_directory, recording_id),
                               fourcc, 6, (camera_width, camera_height))
    
# returns the current steering position
def curSteeringPos():
    pos = getSteeringPos()
    return pos

def draw_window():
    global intFrameNumber
    # background color 
    WINDOW.fill((color))
    
    # display object onto the surface (screen)
    success, camera_image = camera.read()
    if success:
          camera_surf = pygame.image.frombuffer(camera_image.tobytes(), camera_image.shape[1::-1], "RGB")
          image = cv2.cvtColor(camera_image, cv2.COLOR_BGR2RGB)
          if isDrivingForwards():
              intFrameNumber += 1
              frame = image # cv2.resize(image, (85,64))
              cv2.imwrite('%simage_%03i_%s_%i.jpg' % (recording_directory, intFrameNumber,
                                                    recording_id,
                                                 curSteeringPos()), frame)
          WINDOW.blit(camera_surf, (0, 0))
          video_out.write(image)
    
    # update the display
    pygame.display.update()

FPS = 30
def mainWindow():
    # keeping the window open
    restart()
    run = True 
    clock = pygame.time.Clock()
    while run: 
        # capping it at the set frame rate 
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stopDriving()
                run = False
            
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
                
                if event.key == K_r:
                    print("r key")
                    print()
                    print()
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    print("restarting")
                    video_out.release()
                    restart()
                    
                if event.key == K_ESCAPE:
                    print("esc key")
                    stopDriving()
                    run = False
                    #record_driving.running = False
#                     pygame.quit()
#                     sys.exit()
                    
            
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
                
                if event.key == K_ESCAPE:
                    print("esc key released")
                    stopDriving()
                    run = False
                    #record_driving.running = False
#                     pygame.quit()
#                     sys.exit()

        draw_window()


    # closing the window 
    pygame.quit()
    camera.release()
    video_out.release()


# main #
mainWindow()