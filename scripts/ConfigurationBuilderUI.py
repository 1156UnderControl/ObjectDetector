from ConfigurationBuilder import ConfigurationBuilder

class ConfigurationBuilderUI():
    def __init__(self):
        self.__takePicture = None
        self.__shouldExit = False
        self.__configurationBuilder = ConfigurationBuilder()
        print("\nDetection Configurator Started")
        
    def setTakePictureMethod(self, takePicture):
        self.__takePicture = takePicture

    def __startsWith(self, evaluatedText, expectedText):
        return ( evaluatedText[:len(expectedText)] == expectedText )

    def __endsWith(self, evaluatedText, expectedText):
        return ( evaluatedText[-len(expectedText):] == expectedText )

    def __showCommandErrorMessage(self, command):
        print("[ERROR] Command '" + command + "' not recognized. Type 'help' for help.")

    def __showExtensionErrorMessage(self):
        print("[ERROR] The configuration file must end with the '.xml' extension")
          
    def shouldExit(self):
        return self.__shouldExit
    
    def processUserInput(self, userInput):
        userInput = userInput.lower()
        if userInput == "exit":
            self.__shouldExit = True
        elif userInput == "snap":
            if self.__takePicture != None:
                self.__configurationBuilder.setImage(self.__takePicture())
        elif self.__startsWith(userInput, "show"):
            self.__processShowInput(userInput)
        elif self.__startsWith(userInput, "set"):
            self.__processSetInput(userInput)
        elif self.__startsWith(userInput, "load"):
            self.__processLoadInput(userInput)
        elif self.__startsWith(userInput, "save"):
            self.__processSaveInput(userInput)
        elif userInput == "crop":
            self.__configurationBuilder.crop()
        elif userInput == "evaluate":
            self.__configurationBuilder.evaluate()
        elif userInput == "select color":
            self.__configurationBuilder.selectColor()
        elif self.__startsWith(userInput, "print"):
            self.__processPrintInput(userInput)
        elif userInput == "calculate fullness":
            self.__configurationBuilder.calculateFullness()
        elif userInput == "help":
            self.__processHelpInput()
        else:
            self.__showCommandErrorMessage(userInput)
            
    def __processShowInput(self, userInput):
        if userInput == "show":
            print("\nUsage:")
            print("  show [image]")
            print("\nImages:")
            print("  original")
            print("  cropped")
            print("  thresholded")
            print("  filtered")
        elif userInput == "show original":
            self.__configurationBuilder.showImage()
        elif userInput == "show cropped":
            self.__configurationBuilder.showCroppedImage()
        elif userInput == "show thresholded":
            self.__configurationBuilder.showThresholdedImage()
        elif userInput == "show filtered":
            self.__configurationBuilder.showFilteredImage()
            
    def __processSetInput(self, userInput):
        if userInput == "set":
            print("\nUsage:")
            print("  set [variable] [values]")
            print("\nVariables:")
            print("  hue [minimum] [maximum]")
            print("  saturation [minimum] [maximum]")
            print("  value [minimum] [maximum]")
            print("  fullness [percentage]")
            print("  resolution [width] [height]")
        elif self.__startsWith(userInput, "set hue"):
            words = userInput.split()
            if len(words) == 4:
                self.__configurationBuilder.setHue(int(words[2]), int(words[3]))
            else:
                self.__showCommandErrorMessage(userInput)
        elif self.__startsWith(userInput, "set saturation"):
            words = userInput.split()
            if len(words) == 4:
                self.__configurationBuilder.setSaturation(int(words[2]), int(words[3]))
            else:
                self.__showCommandErrorMessage(userInput)
        elif self.__startsWith(userInput, "set value"):
            words = userInput.split()
            if len(words) == 4:
                self.__configurationBuilder.setValue(int(words[2]), int(words[3]))
            else:
                self.__showCommandErrorMessage(userInput)
        elif self.__startsWith(userInput, "set fullness"):
            words = userInput.split()
            if len(words) == 3:
                self.__configurationBuilder.setFullness(int(words[2]))
            else:
                self.__showCommandErrorMessage(userInput)
        elif self.__startsWith(userInput, "set resolution"):
            words = userInput.split()
            if len(words) == 4:
                width = int(words[2])
                height = int(words[3])
                self.__configurationBuilder.resize(width, height)
            else:
                self.__showCommandErrorMessage(userInput)
    
    def __processLoadInput(self, userInput):
        words = userInput.split()
        if not self.__endsWith(userInput, ".xml"):
            self.__showExtensionErrorMessage()
        elif len(words) == 2:
            self.__configurationBuilder.loadXml(words[1])
        else:
            self.__showCommandErrorMessage(userInput)
    
    def __processSaveInput(self, userInput):
        words = userInput.split()
        if not self.__endsWith(userInput, ".xml"):
            self.__showExtensionErrorMessage()
        elif len(words) == 2:
            self.__configurationBuilder.saveXml(words[1])
        else:
            self.__showCommandErrorMessage(userInput)
    
    def __processPrintInput(self, userInput):
        if userInput == "print":
            print("\nUsage:")
            print("  print [variable]")
            print("\nVariables:")
            print("  hue")
            print("  saturation")
            print("  value")
            print("  color")
            print("  resolution")
            print("  fullness")
        elif userInput == "print hue":
            self.__configurationBuilder.printHue()
        elif userInput == "print saturation":
            self.__configurationBuilder.printSaturation()
        elif userInput == "print value":
            self.__configurationBuilder.printValue()
        elif userInput == "print color":
            self.__configurationBuilder.printColor()
        elif userInput == "print resolution":
            self.__configurationBuilder.printResolution()
        elif userInput == "print fullness":
            self.__configurationBuilder.printFullness()
            
    def __processHelpInput(self):
        print("\nUsage:")
        print("  <command> [options]")
        print("\nCommands:")
        print("  snap\t\t\t\tTake a picture from the camera. Necessary for further commands")
        print("  show [image]\t\t\tOpen a window showing the desired image")
        print("  print [variable]\t\tShow the values of one of the parameters used for detection")
        print("  set [variable] [values]\tSet the values of one of the parameters used for detection")
        print("  crop\t\t\t\tSelect region of the picture where the presence of the object will be evaluated")
        print("  select color\t\t\tSelect a color on the picture to automatically define hue, saturation and value")
        print("  evaluate\t\t\tRun the detection algorithm for the selected values and image")
        print("  calculate fullness\t\tCalculates the percentage of the cropped region filled by the detected color")
        print("  load [file]\t\t\tSet all values from an existing configuration file")
        print("  save [file]\t\t\tSave all values to a configuration file")
        print("  exit\t\t\t\tLeave application")