import driving
import drive_with_ai

import cv2
import os

def test_frame(frame):
    pass

def test_video(video_path):
    drive_with_ai.drive_ai_drive(video_source=video_path)
    


if __name__ == '__main__':
    recording_dir = '/home/pi/Desktop/recordings'
    video_name = 'test_drive_1582764943.avi'
    video_path = os.path.join(recording_dir, video_name)
    test_video(video_path)