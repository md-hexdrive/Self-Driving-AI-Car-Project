"""
Here we are, finally!
Driving the car using only a neural network.

Some of this code was adapted from the DeepPiCar tutorial, specifically, end_to_end_lane_follower.py

"""
import driving
import train_model
import distance_monitoring

import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
import cv2

import os
import os.path
import logging
import sys
import time

logging.basicConfig(level=logging.ERROR)

model_path = '/home/pi/Desktop/models/nvidia_model_final.h5'
driving_commands = ['drive forward, turn left', 'drive forward, turn straight',
                    'drive forward, turn right', 'stop driving']
# ;-) -> "Run Flash, Run" ~= "Drive AI, Drive"; I'm a bit of a fan of "The Flash"
def drive_ai_drive(model_path=model_path):
    halt = False
    
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('/home/pi/Desktop/recordings/test_drive_%i.avi' % int(time.time()),
                          fourcc, 20.0, (640, 480))
    
    if not os.path.exists(model_path):
        logging.error(model_path, "does not exist, exiting")
        sys.exit()
    model = tf.keras.models.load_model(model_path)
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
            frame = train_model.img_preprocess(frame)
            x = np.asarray([frame])
            driving_command = np.argmax(model.predict(x)[0])
            
            
            if driving_command == 3:
                print("end of track")
                driving.stopDriving()
            
            else:
                #driving.driveForward()

                if distance_monitoring.ultrasonic_sensor.distance < .45:
                    driving.stopDriving()
                    print("object too close, stopping")
                else:
                    driving.setSteeringPos(driving_command)
                    driving.driveForward()
                    #print(driving_command)
                    print(driving_commands[driving_command])
                
        
        else:
            driving.stopDriving()
            print("stopped")
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    sys.exit()
   
drive_ai_drive()