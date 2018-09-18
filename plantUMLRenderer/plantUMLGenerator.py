from classModelRenderer import ClassModelRenderer
from objectModelRenderer import ObjectModelRenderer
import os
import shutil

class PlantUMLGenerator(object):
    def __init__(self):
        self.directory = "../_generated"
        self.plantUmlJarPath = "../../libs/plantuml.jar"
        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)
        os.makedirs(self.directory)

    def getFileName(self, elementName):
        name = elementName.replace(' ', '_')
        return name

    def generateClassModel(self, bundle, **kwargs):
        renderer = ClassModelRenderer(plantUmlJarPath = self.plantUmlJarPath, directory = self.directory)
        renderer.renderClassModelToFile(self.getFileName(bundle.name), bundle.elements, **kwargs)

    def generateObjectModel(self, bundle, **kwargs):
        renderer = ObjectModelRenderer(plantUmlJarPath = self.plantUmlJarPath, directory = self.directory)
        renderer.renderObjectModelToFile(self.getFileName(bundle.name), bundle.elements, **kwargs)

    def generateClassModels(self, dirName, viewList):
        mainDir = self.directory
        self.directory = f"{mainDir!s}/{self.getFileName(dirName)!s}"
        for bundle, kwargs in zip(viewList[::2],viewList[1::2]):
            self.generateClassModel(bundle, **kwargs)
        self.directory = mainDir

    def generateObjectModels(self, dirName, viewList):
        mainDir = self.directory
        self.directory = f"{mainDir!s}/{self.getFileName(dirName)!s}"
        for bundle, kwargs in zip(viewList[::2],viewList[1::2]):
            self.generateObjectModel(bundle, **kwargs)
        self.directory = mainDir

