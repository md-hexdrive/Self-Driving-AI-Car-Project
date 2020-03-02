"""
Here we are, finally!
Driving the car using only a neural network.
"""
import driving
import train_model

import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
import cv2

import os
import os.path
import logging

logging.basicConfig(level=logging.ERROR)

model_path = '/home/pi/Desktop/models/nvidia_model.h5'

# ;-) -> "Run Flash, Run" -> "Drive AI, Drive", I'm a bit of a fan of "The Flash"
def drive_ai_drive(model_path=model_path):
    halt = False
    
    cap = cv2.VideoCapture(0)
    
    if not os.path.exists(model_path):
        logging.error(model_path, "does not exist, exiting")
        sys.exit()
    model = tf.keras.models.load_model(model_path)
    
    while True:
        frame, ret = cap.read()
        cv2.imshow('frame', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            halt = not halt
        if not halt:
            frame = train_model.img_preprocess(frame)
            x = np.asarray([frame])
            driving_command = abs(model.predict(x)[0])
            
            if driving_command == 3:
                print("end of track")
                driving.stopDriving()
            
            else:
                driving.setSteeringPos(driving_command)
                
                driving.driveForward()
        
        else:
            driving.stopDriving()
