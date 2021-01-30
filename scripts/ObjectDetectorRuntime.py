from ObjectDetector import ObjectDetector
from picamera.array import PiRGBArray
from picamera import PiCamera
from XML import XML
import socket
import time

########## FUNÇÕES DA CAMERA ##########

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


########## LEITURA DE CONFIGURAÇÕES ##########

runtimeConfiguration = XML("/home/pi/Desktop/scripts/runtime.xml")
detectionXMLName = "/home/pi/Desktop/object-detection/" + runtimeConfiguration.getText("configurationXML")
ip = runtimeConfiguration.getText("ip")
port = runtimeConfiguration.getValue("port")


########## INICIALIZAÇÕES ##########

camera, rawCapture = startCamera(detectionXMLName)
objectDetector = ObjectDetector(detectionXMLName)
UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
isDetected = False
counter = 0


########## PRINT DE STATUS ##########

print("Detection configuration file: " + detectionXMLName)
print("UDP Target: " + ip + ":" + str(port))


########## LOOP DE EXECUÇÃO ##########

while True:
    image = takePicture()
    isDetected = objectDetector.evaluate(image)
    byte_message = bytes("isDetected:" + str(isDetected), "utf-8")
    UDPSocket.sendto(byte_message, (ip, port))
    time.sleep(0.1)
    counter += 1
    if counter >= 10:
        counter = 0
        print("[STATUS] isDetected: " + str(isDetected))