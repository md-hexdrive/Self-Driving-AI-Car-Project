import driving
import drive_with_ai

import cv2
import os

def test_frame(frame):
    pass

def test_video(video_path):
    drive_with_ai.drive_ai_drive(video_source=video_path, monitor_distance=False)
    


if __name__ == '__main__':
    recording_dir = '/home/pi/Desktop/recordings/testing'
    #specific_dir = '200226_162200'
    #video_date = '200226_162200'
    video_date = '2002_27_222155'
    video_name = 'video_' + video_date + '.avi'
    video_path = os.path.join(recording_dir, video_date, video_name)
    test_video(video_path)