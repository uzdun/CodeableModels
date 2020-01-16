# import os
# import shutil
# from subprocess import call
from codeable_models import CException
from codeable_models.internal.commons import is_cenum, is_cclassifier, set_keyword_args, is_cclass, is_cobject
# from enum import Enum 
# from codeable_models import CNamedElement
from plant_uml_renderer.modelRenderer import RenderingContext, ModelRenderer

class ObjectRenderingContext(RenderingContext):
    def __init__(self):
        super().__init__()
        self.visitedLinks = set()
        self.renderAttributeValues = True
        self.renderEmptyAttributes = False
        self.renderAssociationNamesWhenNoLabelIsGiven = False
        self.excludedLinks = []

class ObjectModelRenderer(ModelRenderer):
    def renderObjectNameWithClassifier(self, object):
        objName = object.name
        if objName == None:
            objName = ""
        if is_cclass(object):
            object = object.class_object

        sterotypeString = ""
        if object.class_object_class_ != None:
            sterotypeString = self.renderStereotypes(object.class_object_class_, object.class_object_class_.stereotype_instances)

        clName = object.classifier.name
        if clName == None:
            clName = ""
        objClassString = self.padAndBreakName(" : " + clName)
        if objName != "":
            objString = self.padAndBreakName(objName)
            if len(objString + objClassString) > self.nameBreakLength:
                objClassString = "\\n" + objClassString
            objClassString = objString + objClassString
        return '"' + sterotypeString + objClassString + '"'

    def renderObjectSpecification(self, context, obj):
        context.addLine("class " + self.renderObjectNameWithClassifier(obj) + " as " + self.getNodeID(context, obj) + self.renderAttributeValues(context, obj))

    def renderLink(self, context, link):
        association = link.association 

        arrow = " --> "
        if association.aggregation:
            arrow = " o-- "
        elif association.composition:
            arrow = " *-- "

        sterotypeString = self.renderStereotypes(link, link.stereotype_instances)

        label = ""
        if sterotypeString != "":
            label = sterotypeString
        if link.label != None and len(link.label) != 0:
            if len(label) > 0:
                label = label + " "
            label = label + link.label
        elif context.renderAssociationNamesWhenNoLabelIsGiven and association.name != None and len(association.name) != 0:
            if len(label) > 0:
                label = label + " "
            label = label + association.name
        label = ": \"" + self.breakName(label) + "\" "

        context.addLine(self.getNodeID(context, link.source) + arrow + self.getNodeID(context, link.target) + label)

    def renderLinks(self, context, obj, objList):
        for classifier in obj.classifier.class_path:
            for association in classifier.associations:
                links = [l for l in obj.link_objects if l.association == association]
                for link in links:
                    if link in context.excludedLinks:
                        continue
                    source = link.source
                    if is_cclass(source):
                        source = source.class_object
                    target = link.target
                    if is_cclass(target):
                        target = target.class_object
                    if source != obj:
                        # only render links outgoing from this object
                        continue
                    if not link in context.visitedLinks:
                        context.visitedLinks.add(link)
                        if target in objList:
                            self.renderLink(context, link)

    def renderObjects(self, context, objects):
        objList = []
        for obj in objects:
            if is_cclass(obj):
                # use class objects and not classes in this renderer
                objList.extend([obj.class_object_])
            elif is_cobject(obj):
                objList.extend([obj])
            else:
                raise CException(f"'{obj!s}' handed to object renderer is no an object or class'")
        for obj in objList:
            self.renderObjectSpecification(context, obj)
        for obj in objList:
            self.renderLinks(context, obj, objList)

    def renderObjectModel(self, objectList, **kwargs):
        context = ObjectRenderingContext()
        set_keyword_args(context,
                         ["renderAttributeValues", "renderEmptyAttributes", "renderAssociationNamesWhenNoLabelIsGiven", "excludedLinks"], **kwargs)
        self.renderStartGraph(context)
        self.renderObjects(context, objectList)
        self.renderEndGraph(context)
        return context.result

    def renderObjectModelToFile(self, fileNameBase, classList, **kwargs):
        source = self.renderObjectModel(classList, **kwargs)
        self.renderToFiles(fileNameBase, source)
    


