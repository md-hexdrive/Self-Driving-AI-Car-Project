from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview(fullscreen = False, window = (10, 10, 1024, 768))
"""
for effect in camera.IMAGE_EFFECTS:
    camera.image_effect = effect
    camera.annotate_text = "Effect: %s" % effect
    sleep(5)
"""
sleep(35)
#camera.start_recording('/home/pi/video.h264')
#sleep(100)
#camera.stop_recording()
#camera.capture("/home/pi/Desktop/image.jpg")

camera.stop_preview()