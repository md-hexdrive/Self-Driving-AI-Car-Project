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

running = False
class RecordDriving():
    def __init__(self, source = 0, save_dir = '/home/pi/Desktop/recordings/%i/' % (int(time.time()))):
        self.source = source
        self.cap = cv2.VideoCapture(self.source)
        self.recording_directory = save_dir
        
        if not os.path.exists(self.recording_directory):
            os.makedirs(self.recording_directory)
        self.frameN = 0

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('%svideo_01.avi' % (self.recording_directory),
                                   self.fourcc, 20.0, (640,480))

    def start_recording(self):
        running = True
        self.record()
    
    def record(self):
        while running:
            
            self.capture_frame()
    
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
            
        self.stop_recording()
    def stop_recording(self):
        self.out.release()
        self.cap.release()
        cv2.destroyAllWindows()
    
    def capture_frame(self):
        self.frameN += 1
        angle = self.curSteeringPos()
        ret, frame = self.cap.read()
        
        overlay = frame
        
        height, width, _ = frame.shape
        
        if (angle == 0):
            overlay = cv2.rectangle(frame, (0, height - 50), (width // 2, height), (0, 0, 255), -1)
        
        if (angle == 2):
            overlay = cv2.rectangle(frame, (width // 2, height - 50), (width, height), (0, 255, 0), -1)
        
        if (angle == 1):
            overlay = cv2.rectangle(frame, (0, height - 50), (width, height), (0, 128, 255), -1)
            
        cv2.imshow('overlay', overlay)
        self.out.write(frame)
        
        cv2.imwrite('%simage_%03i_%i.jpg' % (self.recording_directory, self.frameN,
                                             angle), frame)

    
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

if __name__ == '__main__':
    run_recording_thread()