import driving
import logging
import cv2
import os
import time
"""
This program allows recording of the sequence of commands a user uses to control the car remotely.
In addition, the sequence of commands and the length of time they were used for can be retrieved afterwards.
The car can repeat the sequence of actions on its own.

Recorded data may also be used to help train the neural network later on.
"""

class RecordDriving():
    def __init__(this, source = 0, save_dir = '/home/pi/Desktop/recordings/%i/' % (int(time.time()))):
        this.source = source
        this.cap = cv2.VideoCapture(source)
        this.recording_directory = save_dir
        os.makedirs(recording_directory)
        this.frameN = 0

        this.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        this.out = cv2.VideoWriter('%svideo_01.avi' % (recording_directory), fourcc, 20.0, (640,480))


    def start_recording(this):
        this.cap = cv2.VideoCapture(source)
        this.recording_directory = save_dir
        os.makedirs(recording_directory)
        this.frameN = 0

        this.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        this.out = cv2.VideoWriter('%svideo_01.avi' % (recording_directory), fourcc, 20.0, (640,480))

    
    def record(this):
        while (cap.isOpened()):
            capture_frame()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        stop_recording()
    def stop_recording(this):
        out.release()
        cap.release()
        cv2.destroyAllWindows()
    
    def capture_frame(this):
            this.frameN += 1
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            out.write(frame)
            
            cv2.imwrite('%simage_%03i_%s.jpg' % (this.recording_directory, this.frameN, curSteeringPos()), frame)

    
    def curSteeringPos(this):
        if driving.isTurnedStraight():
            return "mid"
        elif driving.isTurnedLeft():
            return "lft"
        elif driving.isTurnedRight():
            return "rht"
        else:
            logging.debug("Incorrect Steering Position")
            return "err"

recorder = RecordDriving(0)

commands = []
command_number = 0

actions = ["fwd", "bck", "stp", "lft", "rht", "mid"]




        
def addCommand(direction = " ", time = 0):
    if direction.lower() in actions:
        commands.append((direction, time))
    else:
        logging.debug("Error, you attempted to record an Illegal action")

def getNthCommand():
    command = commands[command_number]
    command_number += 1
    return command

def returnCommandList():
    return commands

def playbackActions():
    pass

logging.basicConfig(level=logging.DEBUG)


addCommand("f", 100)
addCommand("S", 20)
addCommand('t', 1000)
print(returnCommandList())