import driving
import logging
import cv2
import os
import os.path
import time
from threading import Thread


"""
This program allows recording of driving data (the steering position of the car at every video frame)

Recorded data will be used to train the neural network later on.
"""

actions = ["lft", "rht", "mid", "fwd", "bck", "stp",]

class RecordDriving():
    # use the starting time in milliseconds by default to identify different recordings
    def __init__(self, source = 0, save_dir = '/home/pi/Desktop/recordings/', recordingN = int(time.time())):
        self.source = source
        self.cap = cv2.VideoCapture(self.source)
        self.recording_number = recordingN
        self.recording_directory = save_dir + str(self.recording_number) + '/'
        
        if not os.path.exists(self.recording_directory):
            os.makedirs(self.recording_directory)
        self.frameN = 0

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('%svideo_%s.avi' % (self.recording_directory, self.recording_number),
                                   self.fourcc, 30.0, (640,480))
        


    def start_recording(self):
        self.record()
    
    def record(self):
        while (self.cap.isOpened()):
            
            key = cv2.waitKey(2) & 0xFF
                        
            self.capture_frame(key)
        
            if key == ord('q'):
                break
            
            elif ord('s') == key:
                print('reverse')
                driving.turnStraight()
                driving.driveBackward()
                
            elif ord('w') == key:
                print('str')
                driving.turnStraight()
                driving.driveForward()
                
            elif ord('a') == key: #in self.recent_keys:
                print('lft')
                driving.turnLeft()
                driving.driveForward()
                
            elif ord('d') == key: #in self.recent_keys:
                print('rht')
                driving.turnRight()
                driving.driveForward()
            
            elif ord('r') == key:
                print('restarting')
                self.stop_recording()
                run_recording_thread()
            
            elif ord(' ') == key:
                print('end of track')
                driving.stopDriving()
                driving.turnStraight()
                
            else:
                print("stopped")
                driving.stopDriving()
                driving.turnStraight()
            
        self.stop_recording()
        
    def stop_recording(self):
        self.out.release()
        self.cap.release()
        cv2.destroyAllWindows()
    
    def capture_frame(self, key):
        self.frameN += 1
        ret, frame = self.cap.read()
        cv2.imshow('frame', frame)
        self.out.write(frame)
        
        if key == ord(' '):
            cv2.imwrite('%simage_%03i_%s_%i.jpg' % (self.recording_directory, self.frameN,
                                        self.recording_number,
                                     3), frame) # the 3 is used to tell the car where to stop

        elif driving.isDrivingForwards():
            cv2.imwrite('%simage_%03i_%s_%i.jpg' % (self.recording_directory, self.frameN,
                                                    self.recording_number,
                                                 self.curSteeringPos()), frame)

    
    def curSteeringPos(self):
        pos = driving.getSteeringPos()
        return pos
    """
        if driving.isTurnedStraight():
            return "mid"
        elif driving.isTurnedLeft():
            return "lft"
        elif driving.isTurnedRight():
            return "rht"
        else:
            logging.debug("Incorrect Steering Position")
            return "err"
    """
def flight_recorder():
    recorder = RecordDriving(0)
    recorder.start_recording()
    recorder.stop_recording()
    del recorder

def run_recording_thread():
    t1 = Thread(target=flight_recorder)
    t1.run()
commands = []
command_number = 0


run_recording_thread()



        
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

