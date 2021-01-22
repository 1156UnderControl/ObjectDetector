from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

###### CONSTANTS ######
resolution = (1280, 720)
framerate = 32


def startCamera():
	camera = PiCamera()
	camera.resolution = resolution
	camera.framerate = framerate
	rawCapture = PiRGBArray(camera, size=resolution)
	# allow the camera to warmup
	time.sleep(0.1)
	return camera, rawCapture

###### MAIN ######

camera, rawCapture = startCamera()
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	cv2.imshow("Frame", frame.array)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
	if key == ord("q"):
		break