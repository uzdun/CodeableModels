from plantUMLRenderer.classModelRenderer import ClassModelRenderer
from plantUMLRenderer.objectModelRenderer import ObjectModelRenderer
import os
import shutil

class PlantUMLGenerator(object):
    def __init__(self, deleteGenDir = True):
        self.directory = "../_generated"
        self.plantUmlJarPath = "../../libs/plantuml.jar"
        if deleteGenDir:
            if os.path.exists(self.directory):
                shutil.rmtree(self.directory)
            os.makedirs(self.directory)
        self.classModelRenderer = ClassModelRenderer(plantUmlJarPath = self.plantUmlJarPath, directory = self.directory)
        self.objectModelRenderer = ObjectModelRenderer(plantUmlJarPath = self.plantUmlJarPath, directory = self.directory)

    def getFileName(self, elementName):
        name = elementName.replace(' ', '_')
        return name

    def generateClassModel(self, bundle, **kwargs): 
        self.classModelRenderer.directory = self.directory
        self.classModelRenderer.renderClassModelToFile(self.getFileName(bundle.name), bundle.elements, **kwargs)

    def generateObjectModel(self, bundle, **kwargs):
        self.objectModelRenderer.directory = self.directory
        self.objectModelRenderer.renderObjectModelToFile(self.getFileName(bundle.name), bundle.elements, **kwargs)

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

