from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview(fullscreen = False, window = (10, 10, 1024, 768))

#camera.exposure_mode = "night"
sleep(16)
camera.stop_preview()
