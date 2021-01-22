import xml.etree.ElementTree as ET

class XML:
    def __init__(self, filename):
        tree = ET.parse(filename)
        self.__root = tree.getroot()
        
    def getValue(self, fieldName):
        for field in self.__root.findall("./" + fieldName):
            return int(field.text)
        
    def getText(self, fieldName):
        for field in self.__root.findall("./" + fieldName):
            return str(field.text)