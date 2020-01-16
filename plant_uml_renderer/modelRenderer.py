import os
import shutil
from subprocess import call
from codeable_models.internal.commons import setKeywordArgs, isCObject, isCClass, isCEnum, isCClassifier
from enum import Enum 
from codeable_models import *

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

        self.nameBreakLength = 25
        self.namePadding = ""
        self.style = ModelStyle.PLAIN
        self.leftToRight = False

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
        if self.leftToRight == True:
            context.addLine("left to right direction")

    def renderEndGraph(self, context):
        context.addLine("@enduml")

    def renderStereotypesString(self, stereotypesString):
        return "«" + self.breakName(stereotypesString) +  "»\\n"

    def renderStereotypes(self, stereotypedElementInstance, stereotypes):
        if len(stereotypes) == 0:
            return ""

        result = "«"
        taggedValuesString = "\\n{"
        renderedTaggedValues = []

        firstStereotype = True
        for stereotype in stereotypes:
            if firstStereotype:
                firstStereotype = False
            else:
                result += ", "

            stereotypeClassPath = stereotype.classPath

            for stereotypeClass in stereotypeClassPath:
                for taggedValue in stereotypeClass.attributes:
                    if not [taggedValue.name, stereotypeClass] in renderedTaggedValues:
                        value = stereotypedElementInstance.getTaggedValue(taggedValue.name, stereotypeClass)
                        if value != None: 
                            if len(renderedTaggedValues) != 0:
                                taggedValuesString += ", "
                            taggedValuesString += self.renderAttributeValue(taggedValue, taggedValue.name, value)
                            renderedTaggedValues.append([taggedValue.name, stereotypeClass])

            result += stereotype.name

        result = self.breakName(result)

        if len(renderedTaggedValues) != 0:
            taggedValuesString += "}"
        else:
            taggedValuesString = ""
        result += "» " + taggedValuesString
        result += "\\n"
        return result 

    def renderAttributeValues(self, context, obj):
        if not context.renderAttributeValues:
            return ""
        attributeValueAdded = False
        attributeValueString = " {\n"
        renderedAttributes = set()
        for cl in obj.classifier.classPath:
            attributes = cl.attributes
            for attribute in attributes:
                name = attribute.name
                value = obj.getValue(name, cl)

                # don't render the same attribute twice, but only the one that is lowest in the class hierarchy
                if name in renderedAttributes:
                    continue
                else: 
                    renderedAttributes.add(name)

                if not context.renderEmptyAttributes:
                    if value == None:
                        continue
                attributeValueAdded = True
                attributeValueString += self.renderAttributeValue(attribute, name, value) + "\n"
        attributeValueString += "}\n"
        if attributeValueAdded == False:
            attributeValueString = ""
        return attributeValueString

    def renderAttributeValue(self, attribute, name, value):
        type = attribute.type
        if type == str:
            value = '"' + str(value) + '"'
        elif type == list and value != None:
            result = []
            for elt in value:
                if isinstance(elt, str):
                    result.append('"' + str(elt) + '"')
                else:
                    result.append(str(elt))
            value = "[" + ", ".join(result) + "]"
        _checkForIllegalValueCharacters(str(value))
        return self.breakName(name + ' = ' + str(value))

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
                if i+1 < len(name) and name[i+1] == '=':
                    # we don't want to break if the next line starts with '=' as this leads to some 
                    # undocumented font size increase in plant uml, break on next occasion
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
            
        # we add a "_" before the name to make sure the name is not a plantuml keyword
        name = name = f"_{name!s}"

        # put a placeholder in the name for special characters as plantuml does not
        # support many of them
        name = "".join([c if c.isalnum() else "_" + str(ord(c)) + "_" for c in name])
        return name

    def renderToFiles(self, fileNameBase, source):
        fileNameBaseWithDir = f"{self.directory!s}/{fileNameBase!s}"
        fileNameTxt = fileNameBaseWithDir + ".txt"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        file = open(fileNameTxt,"w") 
        file.write(source)
        file.close()
        if self.renderPNG:
            call(["java", "-jar", f"{self.plantUmlJarPath!s}", f"{fileNameTxt!s}"])
        if self.renderSVG:
            call(["java", "-jar", f"{self.plantUmlJarPath!s}", f"{fileNameTxt!s}", "-tsvg"])


def _checkForIllegalValueCharacters(value):
    if '(' in value or ')' in value:
        raise CException("do not use '(' or ')' in attribute values, as PlantUML interprets them as method parameters and would start a new compartment if they are part of an attribute value")
