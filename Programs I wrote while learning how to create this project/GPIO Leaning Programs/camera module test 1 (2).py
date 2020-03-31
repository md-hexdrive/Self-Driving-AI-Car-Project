from picamera import PiCamera
from time import sleep

camera = PiCamera()
#camera.resolution = "HD"
#camera.framerate = 60
camera.start_preview(fullscreen = False, window = (10, 10, 1024, 768))
#camera.start_recording('/home/pi/video.h264')

sleep(20)
#sleep(100)
#camera.stop_recording()
#camera.capture("/home/pi/Desktop/image.jpg")

camera.stop_preview()