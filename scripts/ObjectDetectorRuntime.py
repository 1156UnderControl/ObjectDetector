from networktables import NetworkTables
from ObjectDetector import ObjectDetector
from picamera.array import PiRGBArray
from picamera import PiCamera
from XML import XML
import threading
import time
import logging

        
def startCamera(detectionXMLName):
    camera = PiCamera()
    cameraConfig = XML(detectionXMLName)
    resolution = (cameraConfig.getValue("resolution/width"), cameraConfig.getValue("resolution/height"))
    camera.resolution = resolution
    rawCapture = PiRGBArray(camera, size=resolution)
    # Allow the camera to warmup
    time.sleep(0.1)
    return camera, rawCapture

def takePicture():
    rawCapture.truncate(0)
    camera.capture(rawCapture, format="bgr")
    return rawCapture.array

logging.basicConfig(level=logging.DEBUG)
runtimeConfiguration = XML("/home/pi/Desktop/scripts/runtime.xml")
detectionXMLName = "/home/pi/Desktop/object-detection/" + runtimeConfiguration.getText("configurationXML")
print("Detection configuration file: " + detectionXMLName)
camera, rawCapture = startCamera(detectionXMLName)
objectDetector = ObjectDetector(detectionXMLName)
ip = runtimeConfiguration.getText("ip")
print("Target networktables ip: " + ip)
NetworkTables.initialize(server=ip)

print("Connected!")
cameraVision = NetworkTables.getTable("CameraVision")
isDisabled = False
isDetected = False
counter = 0
cameraVision.putBoolean("isDisabled", isDisabled)
cameraVision.putBoolean("isDetected", isDetected)

while True:
    isDisabled = cameraVision.getBoolean("isDisabled", False)
    if not isDisabled:
        image = takePicture()
        isDetected = objectDetector.evaluate(image)
        cameraVision.putBoolean("isDetected", isDetected)
    time.sleep(0.1)
    counter += 1
    if counter >= 10:
        counter = 0
        print("[STATUS] isDisabled: " + str(isDisabled) + "\t\tisDetected: " + str(isDetected))