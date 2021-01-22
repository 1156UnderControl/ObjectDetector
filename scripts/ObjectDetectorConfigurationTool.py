from ConfigurationBuilderUI import ConfigurationBuilderUI
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

def takePicture():
    rawCapture.truncate(0)
    camera.capture(rawCapture, format="bgr")
    return rawCapture.array

###### MAIN ######

camera, rawCapture = startCamera()
configurationBuilderUI = ConfigurationBuilderUI()
configurationBuilderUI.setTakePictureMethod(takePicture)
while True:
    userInput = input("\n> ")
    configurationBuilderUI.processUserInput(userInput)
    if configurationBuilderUI.shouldExit():
        break