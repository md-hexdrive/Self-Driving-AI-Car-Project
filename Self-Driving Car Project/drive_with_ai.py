"""
Here we are, finally!
Driving the car using only a neural network.

Some of this code was adapted from the DeepPiCar tutorial, specifically, end_to_end_lane_follower.py

"""
import driving
import distance_monitoring

from tensorflow.keras.models import load_model
#import tensorflow.keras as keras
import numpy as np
import cv2

import os
import os.path
import logging
import sys
import time

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
model_name = 'Final-Driving-Model'
model_path = os.path.join(model_dir, model_name, model_name + '_final.h5')

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

# ;-) -> "Run Flash, Run" ~= "Drive AI, Drive"; I'm a bit of a fan of "The Flash"
def drive_ai_drive(model_path=model_path):
    halt = False
    
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 240)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('/home/pi/Desktop/recordings/test_drive_%i.avi' % int(time.time()),
                          fourcc, 10.0, (320, 240))
    
    if not os.path.exists(model_path):
        logging.error(model_path, "does not exist, exiting")
        sys.exit()
    model = load_model(model_path) # load tensorflow model
    print(model.summary())
    
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        out.write(frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '): # allow space key to stop the car
            halt = not halt
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

                if distance_monitoring.ultrasonic_sensor.distance < .45:
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
    driving.fullBrake()
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    sys.exit()
   
drive_ai_drive()