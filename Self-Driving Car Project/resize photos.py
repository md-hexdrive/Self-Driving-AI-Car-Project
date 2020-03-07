"""
This program resizes all the pictures in a given directory.
I need it because some of my AI training pictures were too big to upload to Google Drive for
training - it would have taken too long to upload them all otherwise.

I don't need the pictures to be 640*480 in size, I previously took an AI course that trained an AI to play
games with only a 64*64 image as input. Therefore, the AI should be fine with only 85*64 images as input.
"""
import cv2
import sys
import os
import os.path
import fnmatch


def resize_all(in_path='/home/pi/Desktop/recordings/Pictures2',
               out_path ='/home/pi/Desktop/recordings/Resized_Photos', width=85, height=64):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
        
    if not os.path.exists(in_path):
        print('ERROR, Path: %s does not exist' % in_path)
    else:
        file_list = os.listdir(in_path)
        pattern="*.jpg"
        photo_paths=[]
        photo_names=[]
        for filename in file_list:
            if fnmatch.fnmatch(filename, pattern):
                photo_paths.append(os.path.join(in_path,filename))
                photo_names.append(filename)
        
        for photo_name in photo_names:
            img = cv2.imread(os.path.join(in_path, photo_name))
            img = cv2.resize(img, (width, height))
            cv2.imwrite(os.path.join(out_path, photo_name), img)
            print('Resizing image %s' % photo_name)

resize_all()