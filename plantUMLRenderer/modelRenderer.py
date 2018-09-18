import os
import shutil
from subprocess import call
from codeableModels.internal.commons import setKeywordArgs, isCObject
from enum import Enum 
from codeableModels import CNamedElement

class RenderingContext(object):
    def __init__(self):
        super().__init__()
        self.result = ""
        self.indent = 0
        self.indentCacheString = ""
        self.unnamedObjects = {}
        self.unnamedID = 0

    def getUnnamedCElementID(self, element):
        if isCObject(element) and element._classObjectClass != None:
            # use the class object's class rather than the class object to identify them uniquely
            element = element._classObjectClass
        if element in self.unnamedObjects:
            return self.unnamedObjects[element]
        else:
            self.unnamedID += 1
            name = f"__{self.unnamedID!s}"
            self.unnamedObjects[element] = name
            return name

    def addLine(self, string):
        self.result += self.indentCacheString + string + "\n"
    def addWithIndent(self, string):
        self.result += self.indentCacheString + string
    def add(self, string):
        self.result += string

    def increaseIndent(self):
        self.indent += 2
        self.indentCacheString = " "*self.indent
    def decreaseIndent(self):
        self.indent -= 2
        self.indentCacheString = " "*self.indent

class ModelStyle(Enum):
    PLAIN = 0
    HANDWRITTEN = 1
    ORIGINAL = 2

class ModelRenderer(object):
    def __init__(self, **kwargs):
        # defaults for config parameters
        self.directory = "./gen"
        self.plantUmlJarPath = "../libs/plantuml.jar"
        self.renderPNG = True
        self.renderSVG = True

        self.nameBreakLength = 18
        self.namePadding = ""
        self.style = ModelStyle.PLAIN

        self.ID = 0

        super().__init__()
        self._initKeywordArgs(**kwargs)

    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = ["directory", "plantUmlJarPath", "genSVG", "genPNG"]
        setKeywordArgs(self, legalKeywordArgs, **kwargs)

    def renderStartGraph(self, context):
        context.addLine("@startuml")
        if self.style == ModelStyle.HANDWRITTEN or self.style == ModelStyle.PLAIN:
            context.addLine("skinparam monochrome true")
            context.addLine("skinparam ClassBackgroundColor White")
            context.addLine("hide empty members")
            context.addLine("hide circle")
            if self.style == ModelStyle.HANDWRITTEN:
                #context.addLine("skinparam defaultFontName MV Boli")
                context.addLine("skinparam defaultFontName Segoe Print")
                context.addLine("skinparam defaultFontSize 14")
                context.addLine("skinparam handwritten true")
                context.addLine("skinparam shadowing false")
            if self.style == ModelStyle.PLAIN:
                context.addLine("skinparam defaultFontName Arial")
                context.addLine("skinparam defaultFontSize 11")
                context.addLine("skinparam classfontstyle bold")

    def renderEndGraph(self, context):
        context.addLine("@enduml")

    def padAndBreakName(self, name, namePadding = None):
        if namePadding == None:
            namePadding = self.namePadding

        if len(name) <= self.nameBreakLength:
            return namePadding + name + namePadding

        result = ""
        count = 0
        currentFirstIndex = 0
        for i, v in enumerate(name):
            if v == ' ' and count >= self.nameBreakLength:
                if name[i-1] == ':':
                    # we don't want to end the line with a ':', break on next occasion
                    continue
                count = 0
                result = result + namePadding + name[currentFirstIndex:i] + namePadding + "\\n"
                currentFirstIndex = i + 1
            count += 1
        result = result + namePadding + name[currentFirstIndex:len(name)] + namePadding
        return result

    def breakName(self, name):
        return self.padAndBreakName(name, "")


    def getNodeID(self, context, element):
        if isinstance(element, CNamedElement):
            name = element.name
            if name == None:
                name = context.getUnnamedCElementID(element)
        else:
            # else this must be a string
            name = element
        name = name.replace(' ', '_')
        name = name.replace('#', '_')
        name = name.replace('-', '_')
        return name

    def renderName(self, element):
        return '"' + self.padAndBreakName(element.name) + '"'

    def renderToFiles(self, fileNameBase, source):
        fileNameBaseWithDir = f"{self.directory!s}/{fileNameBase!s}"
        fileNameTxt = fileNameBaseWithDir + ".txt"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        file = open(fileNameTxt,"w") 
        file.write(source)
        file.close()
        if self.renderPNG:
            call(f"java -jar {self.plantUmlJarPath!s} {fileNameTxt!s}")
        if self.renderSVG:
            call(f"java -jar {self.plantUmlJarPath!s} {fileNameTxt!s} -tsvg")
