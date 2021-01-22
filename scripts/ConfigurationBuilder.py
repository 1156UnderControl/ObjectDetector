from ObjectDetector import ObjectDetector
from XML import XML
import cv2
import numpy as np
import xml.etree.ElementTree as ET

class ConfigurationBuilder():
    def __init__(self):
        self.__minHue = 0
        self.__maxHue = 255
        self.__minSaturation = 0
        self.__maxSaturation = 255
        self.__minValue = 0
        self.__maxValue = 255
        self.__resolutionWidth = 1280
        self.__resolutionHeight = 720
        self.__minX = 0
        self.__maxX = 1280
        self.__minY = 0
        self.__maxY = 720
        self.__fullness = 20
        
        self.__image = None
        self.__hasImage = False
        self.__thresholdedImage = None
        self.__startingX = 0
        self.__startingY = 0
        self.__x = 0
        self.__y = 0
        self.__lButton = False
        
    def loadXml(self, configurationXML):
        configuration = XML("/home/pi/Desktop/object-detection/" + configurationXML)
        self.__minHue = configuration.getValue("thresholds/hue/minimum")
        self.__maxHue = configuration.getValue("thresholds/hue/maximum")
        self.__minSaturation = configuration.getValue("thresholds/saturation/minimum")
        self.__maxSaturation = configuration.getValue("thresholds/saturation/maximum")
        self.__minValue = configuration.getValue("thresholds/value/minimum")
        self.__maxValue = configuration.getValue("thresholds/value/maximum")
        self.__resolutionWidth = configuration.getValue("resolution/width")
        self.__resolutionHeight = configuration.getValue("resolution/height")
        self.__minX = configuration.getValue("scanarea/xcoordinates/minimum")
        self.__maxX = configuration.getValue("scanarea/xcoordinates/maximum")
        self.__minY = configuration.getValue("scanarea/ycoordinates/minimum")
        self.__maxY = configuration.getValue("scanarea/ycoordinates/maximum")
        self.__fullness = configuration.getValue("scanarea/fullness")
        
    def __cropMouseCallback(self, event, x, y, flags, param):
        self.__x = x
        self.__y = y
        if event == cv2.EVENT_LBUTTONDOWN:
            self.__lButton = True
            self.__startingX = x
            self.__startingY = y
        if event == cv2.EVENT_LBUTTONUP:
            self.__lButton = False
            if x > self.__startingX:
                self.__minX = self.__startingX
                self.__maxX = x
            else:
                self.__minX = x
                self.__maxX = self.__startingX
            
            if y > self.__startingY:
                self.__minY = self.__startingY
                self.__maxY = y
            else:
                self.__minY = y
                self.__maxY = self.__startingY
            self.__closeImage = True
        
    def __colorMouseCallback(self, event, x, y, flags, param):
        self.__x = x
        self.__y = y
        if event == cv2.EVENT_LBUTTONDOWN:
            self.__lButton = True
            self.__startingX = x
            self.__startingY = y
        if event == cv2.EVENT_LBUTTONUP:
            self.__lButton = False
            if x > self.__startingX:
                minX = self.__startingX
                maxX = x
            else:
                minX = x
                maxX = self.__startingX
            
            if y > self.__startingY:
                minY = self.__startingY
                maxY = y
            else:
                minY = y
                maxY = self.__startingY
            selectedArea = cv2.cvtColor(self.__image[minY:maxY, minX:maxX], cv2.COLOR_BGR2HSV)
            hue, saturation, value = cv2.split(selectedArea)
            self.__minHue = int(hue.min())
            self.__maxHue = int(hue.max())
            self.__minSaturation = int(saturation.min())
            self.__maxaturation = int(saturation.max())
            self.__minValue = int(value.min())
            self.__maxValue = int(value.max())
            self.__closeImage = True
    
    def setImage(self, image):
        self.__hasImage = True
        self.__image = cv2.resize(image, (self.__resolutionWidth, self.__resolutionHeight), interpolation = cv2.INTER_AREA)
        
    def resize(self, width, height):
        self.__resolutionWidth = width
        self.__resolutionHeight = height
        self.setImage(self.__image)
        
    def crop(self):
        self.__closeImage = False
        cv2.imshow('Image', self.__image)
        cv2.setMouseCallback('Image', self.__cropMouseCallback)
        while not self.__closeImage:
            image = self.__image.copy()
            if self.__lButton:
                cv2.rectangle(image,(self.__startingX, self.__startingY),(self.__x, self.__y),(0,255,0),1)
            cv2.imshow('Image', image)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        
    def selectColor(self):
        self.__closeImage = False
        cv2.imshow('Image', self.__image)
        cv2.setMouseCallback('Image', self.__colorMouseCallback)
        while not self.__closeImage:
            image = self.__image.copy()
            if self.__lButton:
                cv2.rectangle(image,(self.__startingX, self.__startingY),(self.__x, self.__y),(0,255,0),1)
            cv2.imshow('Image', image)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        
    def setHue(self, minimum, maximum):
        self.__minHue = minimum
        self.__maxHue = maximum
        
    def setSaturation(self, minimum, maximum):
        self.__minSaturation = minimum
        self.__maxSaturation = maximum
        
    def setValue(self, minimum, maximum):
        self.__minValue = minimum
        self.__maxValue = maximum
        
    def setFullness(self, fullness):
        self.__fullness = fullness
        
    def showImage(self):
        if self.__hasImage:
            cv2.imshow('Image', self.__image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            self.__printMissingImageError()
        
    def showCroppedImage(self):
        if self.__hasImage:
            cv2.imshow('Cropped', self.__getCroppedImage())
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            self.__printMissingImageError()
        
    def showThresholdedImage(self):
        if self.__hasImage:
            cv2.imshow('Thresholded', self.__getThresholdedImage())
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            self.__printMissingImageError()
        
    def showFilteredImage(self):
        if self.__hasImage:
            self.__getThresholdedImage()
            cv2.imshow('Filtered', self.__getFilteredImage())
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            self.__printMissingImageError()
        
    def __printMissingImageError(self):
        print("[ERROR] To do this you must have taken a picture. Use the 'help' command")
        
    def evaluate(self):
        detector = self.__setupObjectDetector()
        print(detector.evaluate(self.__image))
        
    def calculateFullness(self):
        detector = self.__setupObjectDetector()
        print(detector.calculateFullness(self.__image))
        
    def __setupObjectDetector(self):
        detector = ObjectDetector()
        detector.setLowerThreshold(self.__minHue, self.__minSaturation, self.__minValue)
        detector.setUpperThreshold(self.__maxHue, self.__maxSaturation, self.__maxValue)
        detector.setResolution(self.__resolutionWidth, self.__resolutionHeight)
        detector.setCropArea(self.__minX, self.__maxX, self.__minY, self.__maxY, self.__fullness)
        return detector
        
    def printHue(self):
        if self.__minHue > 99:
            print("Minimum Hue: " + str(self.__minHue) + "\tMaximum Hue: " + str(self.__maxHue))
        else:
            print("Minimum Hue: " + str(self.__minHue) + "\t\tMaximum Hue: " + str(self.__maxHue))
        
    def printSaturation(self):
        print("Minimum Saturation: " + str(self.__minSaturation) + "\tMaximum Saturation: " + str(self.__maxSaturation))
        
    def printValue(self):
        print("Minimum Value: " + str(self.__minValue) + "\tMaximum Value: " + str(self.__maxValue))
        
    def printColor(self):
        self.printHue()
        self.printSaturation()
        self.printValue()
        
    def printResolution(self):
        print("Width: " + str(self.__resolutionWidth) + "\t\tHeight: " + str(self.__resolutionHeight))
        
    def printFullness(self):
        print("Fullness: " + str(self.__fullness))
        
    def __getCroppedImage(self):
        return self.__image[self.__minY:self.__maxY, self.__minX:self.__maxX]
        
    def __getThresholdedImage(self):
        lowerThreshold = (self.__minHue, self.__minSaturation, self.__minValue)
        upperThreshold = (self.__maxHue, self.__maxSaturation, self.__maxValue)
        HSVImage = cv2.cvtColor(self.__image, cv2.COLOR_BGR2HSV)
        self.__thresholdedImage = cv2.inRange(HSVImage, lowerThreshold, upperThreshold)
        return self.__thresholdedImage
    
    def __getFilteredImage(self):
        kernel = np.ones((3, 3), dtype = "uint8")
        eroded = cv2.erode(self.__thresholdedImage, kernel, iterations = 1)
        return cv2.dilate(eroded, kernel, iterations = 5)
        
    def saveXml(self, fileName):
        configuration = ET.Element('configuration')
        
        thresholds = ET.SubElement(configuration, 'thresholds')
        hue = ET.SubElement(thresholds, 'hue')
        minimumHue = ET.SubElement(hue, 'minimum')
        minimumHue.text = str(self.__minHue)
        maximumHue = ET.SubElement(hue, 'maximum')
        maximumHue.text = str(self.__maxHue)
        saturation = ET.SubElement(thresholds, 'saturation')
        minimumSaturation = ET.SubElement(saturation, 'minimum')
        minimumSaturation.text = str(self.__minSaturation)
        maximumSaturation = ET.SubElement(saturation, 'maximum')
        maximumSaturation.text = str(self.__maxSaturation)
        value = ET.SubElement(thresholds, 'value')
        minimumValue = ET.SubElement(value, 'minimum')
        minimumValue.text = str(self.__minValue)
        maximumValue = ET.SubElement(value, 'maximum')
        maximumValue.text = str(self.__maxValue)

        resolution = ET.SubElement(configuration, 'resolution')
        width = ET.SubElement(resolution, 'width')
        width.text = str(self.__resolutionWidth)
        height = ET.SubElement(resolution, 'height')
        height.text = str(self.__resolutionHeight)

        scanarea = ET.SubElement(configuration, 'scanarea')
        xcoordinates = ET.SubElement(scanarea, 'xcoordinates')
        minimumX = ET.SubElement(xcoordinates, 'minimum')
        minimumX.text = str(self.__minX)
        maximumX = ET.SubElement(xcoordinates, 'maximum')
        maximumX.text = str(self.__maxX)
        ycoordinates = ET.SubElement(scanarea, 'ycoordinates')
        minimumY = ET.SubElement(ycoordinates, 'minimum')
        minimumY.text = str(self.__minY)
        maximumY = ET.SubElement(ycoordinates, 'maximum')
        maximumY.text = str(self.__maxY)
        fullness = ET.SubElement(scanarea, 'fullness')
        fullness.text = str(self.__fullness)
        
        tree = ET.ElementTree(configuration)
        tree.write(open("/home/pi/Desktop/object-detection/" + fileName, 'w'), encoding='unicode')