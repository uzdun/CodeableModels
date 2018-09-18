# import os
# import shutil
# from subprocess import call
from codeableModels import CException
from codeableModels.internal.commons import isCEnum, isCClassifier, setKeywordArgs
# from enum import Enum 
# from codeableModels import CNamedElement
from modelRenderer import RenderingContext, ModelRenderer

class ClassifierRenderingContext(RenderingContext):
    def __init__(self):
        super().__init__()
        self.visitedAssociations = set()
        self.renderAssociations = True
        self.renderInheritance = True
        self.renderAttributes = True
        self.excludedAssociations = []

class ClassModelRenderer(ModelRenderer):
    def renderClassifierSpecification(self, context, cl):
        context.addLine("class " + self.renderName(cl) + " as " + self.getNodeID(context, cl) + self.renderAttributes(context, cl))

    def renderAttributes(self, context, cl):
        if context.renderAttributes == False:
            return ""
        if len(cl.attributes) == 0: 
            return "" 
        attributeString = "{\n"
        for attribute in cl.attributes:
            attributeString += self.renderAttribute(attribute)
        attributeString += "}\n"
        return attributeString
    
    def renderAttribute(self, attribute):
        type = attribute.type
        t = None
        if isCEnum(type) or isCClassifier(type):
            t = type.name
        elif type == str:
            t = "String"
        elif type == int:
            t = "Integer"
        elif type == float:
            t = "Float"
        elif type == bool:
            t = "Boolean"
        if t == None:
            raise CException(f"unknown type of attribute: '{attribute!s}")
        return attribute.name + ": " + t + "\n"

    def renderAssociations(self, context, cl, classList):
        if context.renderAssociations == False:
            return
        for association in cl.associations:
            if association in context.excludedAssociations:
                continue
            if not association.source == cl:
                # only render associations outgoing from this class
                continue
            if not association in context.visitedAssociations:
                context.visitedAssociations.add(association)
                if association.target in classList:
                    self.renderAssociation(context, association)

    def renderAssociation(self, context, association):
        arrow = " --> "
        if association.aggregation:
            arrow = " o-- "
        elif association.composition:
            arrow = " *-- "

        label = ""
        if association.name != None and len(association.name) != 0:
            label = ": \"" + association.name + "\" "
        headLabel = ""
        if (not (association.aggregation or association.composition)):
            headLabel = " \" " + association.sourceMultiplicity + " \" "
        tailLabel =  " \" " + association.multiplicity + " \" "

        context.addLine(self.getNodeID(context, association.source) + headLabel +
                arrow + tailLabel + self.getNodeID(context, association.target) + label)

    def renderInheritanceRelations(self, context, classList):
        if context.renderInheritance == False:
            return
        for cl in classList:
            for subClass in cl.subclasses:
                if subClass in classList:
                    context.addLine(self.getNodeID(context, cl) + " <|--- " + self.getNodeID(context, subClass));

    def renderClasses(self, context, classList):
        for cl in classList:
            if not isCClassifier(cl):
                raise CException(f"'{cl!s}' handed to class renderer is not a classifier'")
            self.renderClassifierSpecification(context, cl)
        self.renderInheritanceRelations(context, classList)
        for cl in classList:
            self.renderAssociations(context, cl, classList)

    def renderClassModel(self, classList, **kwargs):
        context = ClassifierRenderingContext()
        setKeywordArgs(context, 
            ["renderAssociations", "renderInheritance", "renderAttributes", "excludedAssociations"], **kwargs)
        self.renderStartGraph(context)
        self.renderClasses(context, classList)
        self.renderEndGraph(context)
        return context.result

    def renderClassModelToFile(self, fileNameBase, classList, **kwargs):
        source = self.renderClassModel(classList, **kwargs)
        self.renderToFiles(fileNameBase, source)
    

