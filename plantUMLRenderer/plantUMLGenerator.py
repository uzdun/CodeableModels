from plantUMLRenderer.classModelRenderer import ClassModelRenderer
from plantUMLRenderer.objectModelRenderer import ObjectModelRenderer
import os
import shutil

class PlantUMLGenerator(object):
    def __init__(self, deleteGenDir = True):
        self._directory = "../_generated"
        self._plantUmlJarPath = "../../libs/plantuml.jar"
        if deleteGenDir:
            if os.path.exists(self.directory):
                shutil.rmtree(self.directory)
            os.makedirs(self.directory)
        self.classModelRenderer = ClassModelRenderer(plantUmlJarPath = self._plantUmlJarPath, directory = self._directory)
        self.objectModelRenderer = ObjectModelRenderer(plantUmlJarPath = self._plantUmlJarPath, directory = self._directory)

    def getFileName(self, elementName):
        name = elementName.replace(' ', '_')
        return name

    def generateClassModel(self, bundle, **kwargs): 
        self.classModelRenderer.renderClassModelToFile(self.getFileName(bundle.name), bundle.elements, **kwargs)

    def generateObjectModel(self, bundle, **kwargs): 
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

    @property
    def plantUmlJarPath(self):
        return self._plantUmlJarPath
    @plantUmlJarPath.setter
    def plantUmlJarPath(self, plantUmlJarPath):
        self._plantUmlJarPath = plantUmlJarPath
        self.classModelRenderer.plantUmlJarPath = plantUmlJarPath
        self.objectModelRenderer.plantUmlJarPath = plantUmlJarPath

    @property
    def directory(self):
        return self._directory
    @directory.setter
    def directory(self, directory):
        self._directory = directory
        self.classModelRenderer.directory = directory
        self.objectModelRenderer.directory = directory