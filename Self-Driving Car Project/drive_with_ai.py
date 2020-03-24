"""
Here we are, finally!
Driving the car using only a neural network.

Some of this code was adapted from the DeepPiCar tutorial, specifically, end_to_end_lane_follower.py

"""
import driving
import distance_monitoring
import interpret_frame
import record_driving
from tensorflow.keras.models import load_model
import numpy as np
import cv2

import os
import os.path
import logging
import sys
import time


halt = False

logging.basicConfig(level=logging.ERROR)
model_dir = '/home/pi/Desktop/models/'
# test driving straight and stopping without turning
#model_path = '/home/pi/Desktop/models/Smaller-Model/smaller_model_final.h5'

# first model built to drive on blue tape
#model_path = '/home/pi/Desktop/models/Blue-Tape/blue_tape_model_final.h5'

# testing nvidia model on track made with blue tape
#model_path = '/home/pi/Desktop/models/Nividia_Model_on_Blue_Circle_Track/Nividia_Model_on_Blue_Circle_Track_final.h5'

# nvidia model driving on upgraded track and better training data
#model_name = 'Nividia_Model_on_Lets_Do_This_Blue_Circle_Track'
#model_name = 'Lets_Do_This_Blue_Circle_Track_Properly_With_NVDIA_Model'

# the final model, drives successfully around the blue loop
#model_name = 'Final-Driving-Model'

# test final model on full track without being trained to automatically stop
#model_name = 'Final-Driving-Model-Without-Stop-Conditions'

# test final model on full track without being trained to automatically stop
#model_name = 'Good-Model'

#model_name = 'Lets Just Do This'
#model_name = 'Drive-Around-Table-Model'
model_name = 'Table-Day-Model'
model_path = os.path.join(model_dir, model_name, model_name + '_check.h5')

driving_commands = ['drive forward, turn left', 'drive forward, turn straight',
                    'drive forward, turn right', 'stop driving']

"""
img_preprocess() preprocesses the images for use in the neural network
- keep it in this file, otherwise everything in train_model and its imports would need to be loaded,
  which really slows things down on startup of program.
""" 
def img_preprocess(image):
    height, _, _ = image.shape
    #image = image[int(height/2):,:,:]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.GaussianBlur(image, (3,3), 0)
    image = cv2.resize(image, (85, 64))
    image = image / 255
    return image

class AIDrivingRecorder(record_driving.RecordDriving):
    def __init__(self, video_source = 0):
        super(AIDrivingRecorder,self).__init__(source=video_source, width=320, height=240,
                                               fps=20,
                                               is_training = False, record_interpretation = True)
    
    def keyboard_interaction(self, key):
        global halt
        if key == ord('q'):
            driving.fullBrake()
            self.stop_recording()
            sys.exit()
        elif key == ord(' '): # allow space key to stop the car
            halt = not halt


# ;-) -> "Run Flash, Run" ~= "Drive AI, Drive"; I'm a bit of a fan of "The Flash"
def drive_ai_drive(model_path=model_path, video_source=0, monitor_distance=True):
    
    recorder = AIDrivingRecorder(video_source)
    
    if not os.path.exists(model_path):
        logging.error(model_path, "does not exist, exiting")
        sys.exit()
    model = load_model(model_path) # load tensorflow model
    print(model.summary())
    
    while True:
        frame = recorder.capture_frame()
        
        if not halt:
            frame = img_preprocess(frame)
            x = np.asarray([frame])
            driving_command = np.argmax(model.predict(x)[0])
            
            print(driving_command)
            if driving_command == 3:
                print("end of track")
                driving.fullBrake()
            
            else:
                #driving.driveForward()
                
                if monitor_distance and distance_monitoring.ultrasonic_sensor.distance < .45:
                    driving.fullBrake()
                    driving.straightenWheels()
                    print("object too close, stopping")
                else:
                    driving.setSteeringPos(driving_command)
                    driving.driveForward()
                    #print(driving_command)
                    print(driving_commands[driving_command])
                
        
        else:
            driving.fullBrake()
            driving.straightenWheels()

            print("stopped")
    
if __name__=='__main__':
    drive_ai_drive()