from networktables import NetworkTables
from ObjectDetector import ObjectDetector
from picamera.array import PiRGBArray
from picamera import PiCamera
from XML import XML
import threading
import time

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()
        
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

runtimeConfiguration = XML("/home/pi/Desktop/scripts/runtime.xml")
detectionXMLName = "/home/pi/Desktop/object-detection/" + runtimeConfiguration.getText("configurationXML")
print("Detection configuration file: " + detectionXMLName)
camera, rawCapture = startCamera(detectionXMLName)
objectDetector = ObjectDetector(detectionXMLName)
ip = runtimeConfiguration.getText("ip")
print("Target networktables ip: " + ip)
NetworkTables.initialize(server=ip)
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

# Insert your processing code here
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
        print("[STATUS] isDisabled: " + isDisabled + "\t\tisDetected: " + isDetected)