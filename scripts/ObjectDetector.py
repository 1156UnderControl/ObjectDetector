from XML import XML
import cv2
import numpy as np

class ObjectDetector():
    def __init__(self, configurationXML=None):
        if configurationXML != None:
            config = XML(configurationXML)
            self.__lowerThreshold = (config.getValue("/hue/minimum"), config.getValue("/saturation/minimum"), config.getValue("/value/minimum"))
            self.__upperThreshold = (config.getValue("/hue/maximum"), config.getValue("/saturation/maximum"), config.getValue("/value/maximum"))
            self.__resolution = (config.getValue("resolution/width"), config.getValue("resolution/height"))
            self.__minimumX = config.getValue("scanarea/xcoordinates/minimum")
            self.__maximumX = config.getValue("scanarea/xcoordinates/maximum")
            self.__minimumY = config.getValue("scanarea/ycoordinates/minimum")
            self.__maximumY = config.getValue("scanarea/ycoordinates/maximum")
            deltaX = self.__maximumX - self.__minimumX
            deltaY = self.__maximumY - self.__minimumY
            self.__totalArea = deltaX * deltaY
            fullness = config.getValue("scanarea/fullness") 
            self.__minimumDetectedArea = self.__totalArea * fullness / 100
        dilationKernelSize = 3
        self.__kernel = np.ones((dilationKernelSize, dilationKernelSize), dtype = "uint8")
        
    def setLowerThreshold(self, hue, saturation, value):
        self.__lowerThreshold = (hue, saturation, value)
        
    def setUpperThreshold(self, hue, saturation, value):
        self.__upperThreshold = (hue, saturation, value)
        
    def setResolution(self, width, height):
        self.__resolution = (width, height)
        
    def setCropArea(self, minimumX, maximumX, minimumY, maximumY, fullness):
        self.__minimumX = minimumX
        self.__maximumX = maximumX
        self.__minimumY = minimumY
        self.__maximumY = maximumY
        deltaX = self.__maximumX - self.__minimumX
        deltaY = self.__maximumY - self.__minimumY
        self.__totalArea = deltaX * deltaY
        self.__minimumDetectedArea = self.__totalArea * fullness / 100
        
    def evaluate(self, image):
        totalDetectedArea = self.__calculateDetectedArea(image)
        if totalDetectedArea > self.__minimumDetectedArea:
            return True
        else:
            return False
        
    def calculateFullness(self, image):
        totalDetectedArea = self.__calculateDetectedArea(image)
        return ( 100 * totalDetectedArea / self.__totalArea )
        
    def __calculateDetectedArea(self, image):
        croppedImage = self.__getCroppedImage(image)
        detectionImage = self.__detectColor(croppedImage)
        filteredImage = self.__filterNoise(detectionImage)
        return self.__getDetectedArea(filteredImage)
        
    def __getCroppedImage(self, originalImage):
        resized = cv2.resize(originalImage, self.__resolution, interpolation = cv2.INTER_AREA)
        return resized[self.__minimumY:self.__maximumY, self.__minimumX:self.__maximumX]
    
    def __detectColor(self, image):
        HSVImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return cv2.inRange(HSVImage, self.__lowerThreshold, self.__upperThreshold)
    
    def __filterNoise(self, noisyImage):
        eroded = cv2.erode(noisyImage, self.__kernel, iterations = 1)
        return cv2.dilate(eroded, self.__kernel, iterations = 5)
    
    def __getDetectedArea(self, detectionImage):
        contours, hierarchy = cv2.findContours(detectionImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        totalDetectedArea = 0
        for contour in contours:
            moment = cv2.moments(contour)
            momentArea = moment['m00']
            totalDetectedArea += momentArea
        return totalDetectedArea