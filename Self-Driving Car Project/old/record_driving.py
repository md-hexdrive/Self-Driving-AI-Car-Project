import driving
import interpret_frame
import logging
import cv2
import os
import os.path
import time
import datetime
from threading import Thread

"""
This program allows recording of driving data (the steering position of the car at every video frame)

Recorded data will be used to train the neural network later on.
"""


# returns the current time, used to uniquely identify recordings
def now():
    return datetime.datetime.now().strftime("%y%m_%d_%H%M%S") #found this in the DeepPiCar training code

class RecordDriving():
    # setup recording:
    def __init__(self, source = 0, width = 640, height = 480, fps=20,
                 save_dir = '/home/user/Desktop/recordings/',
                 recording_id = now(), batch_id = now(), is_training=True, view_interpretation = False,
                 record_interpretation = False):
        self.source = source
        print(self.source)
        self.width = width
        self.height = height
        
        self.cap = cv2.VideoCapture(self.source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        self.is_training = is_training
        self.view_interpretation = view_interpretation
        self.record_interpretation = record_interpretation
        
        self.recording_id = recording_id
        self.batch_id = batch_id
        if is_training:
            recording_type = os.path.join("training", 'batch_id_%s' % self.batch_id)
        else:
            recording_type = "testing"
        self.recording_directory = os.path.join(save_dir, recording_type, str(self.recording_id), '')
        
        if not os.path.exists(self.recording_directory):
            os.makedirs(self.recording_directory)
        self.frameN = 0

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('%svideo_%s.avi' % (self.recording_directory, self.recording_id),
                                   self.fourcc, fps, (self.width, self.height))
        

    # starts the recording session
    def start_recording(self):
        os.system("xset r rate 13 13")
        self.record()
    
    # the recording loop
    def record(self):
        while (self.cap.isOpened()):
            os.system("xset r rate 13 13")
            self.capture_frame()
            
    # cleanup after running
    def stop_recording(self):
        self.out.release()
        self.cap.release()
        cv2.destroyAllWindows()
        os.system("xset r rate 500 30")
    
    # record and display the current video frame, include driving status info in the frame's name
    def capture_frame(self):

        self.frameN += 1
        ret, frame = self.cap.read()
        
        #image = frame.copy()
        #overlay = interpret_frame.whats_going_on(image)
        
        
        #if self.view_interpretation:
        #cv2.imshow('overlay', overlay)
        #else:
        cv2.imshow('frame', frame)
        
#         if self.record_interpretation:
#             self.out.write(overlay)
#         else:
#             self.out.write(frame)

        frame = cv2.resize(frame, (85,64))
        
        key = cv2.waitKey(1) & 0xFF
        self.keyboard_interaction(key)
        
#         if key == ord(' '):
#             cv2.imwrite('%simage_%03i_%s_%i.jpg' % (self.recording_directory, self.frameN,
#                                         self.recording_id,
#                                      3), frame) # the 3 is used to tell the car where to stop
# 
#         elif driving.isDrivingForwards():
#             cv2.imwrite('%simage_%03i_%s_%i.jpg' % (self.recording_directory, self.frameN,
#                                                     self.recording_id,
#                                                  self.curSteeringPos()), frame)
        return frame
    
    # handle user-keyboard interaction in the running window
    def keyboard_interaction(self, key):
        if key == ord('q'): # 'q' key quits the program
            self.stop_recording()
        
        elif ord('s') == key: # 's' reverses the car
            print('reverse')
            driving.turnStraight()
            driving.driveBackward()
            
        elif ord('w') == key: # 'w' drives the car straight ahead
            print('str')
            driving.turnStraight()
            driving.driveForward()
            
        elif ord('a') == key: # 'a' drives the car forwards and to the left
            print('lft')
            driving.turnLeft()
            driving.driveForward()
            
        elif ord('d') == key: # 'd' drives the car forwards and to the right
            print('rht')
            driving.turnRight()
            driving.driveForward()
        
        elif ord('r') == key: # 'r' restarts the recording process with a new batch of training data
            print('restarting')
            self.stop_recording()
            RecordDriving(0, recording_id = now(), batch_id=self.batch_id).start_recording()
        
        elif ord(' ') == key: # ' ' (the space key) stops the car and indicates that this location is a stop position
            print('end of track')
            driving.fullBrake()
            driving.turnStraight()
            
        else:    # otherwise (if any other key is pressed or if no key is pressed), stop the car
            print("stopped")
            driving.fullBrake()
            driving.turnStraight()

    # returns the current steering position
    def curSteeringPos(self):
        pos = driving.getSteeringPos()
        return pos
    
def flight_recorder():
    recorder = RecordDriving(0)
    recorder.start_recording()
    #recorder.stop_recording()
    #del recorder

# run recording process in a separate thread
def run_recording_thread():
    t1 = Thread(target=flight_recorder)
    t1.run()

if __name__=='__main__':
    run_recording_thread()
