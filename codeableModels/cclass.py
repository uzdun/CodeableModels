from codeableModels.cclassifier import CClassifier
from codeableModels.internal.commons import checkIsCMetaclass, checkIsCObject, checkIsCStereotype, isCStereotype, checkNamedElementIsNotDeleted
from codeableModels.cexception import CException
from codeableModels.cobject import CObject
from codeableModels.internal.taggedvalues import CTaggedValues
from codeableModels.internal.stereotype_holders import CStereotypeInstancesHolder

class CClass(CClassifier):
    def __init__(self, metaclass, name=None, **kwargs):
        self._metaclass = None
        self.metaclass = metaclass
        self._objects = []
        self._classObject = CObject(self.metaclass, name, _classObjectClass = self)
        self._stereotypeInstancesHolder = CStereotypeInstancesHolder(self)
        self._taggedValues = CTaggedValues()
        super().__init__(name, **kwargs)
        
    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = [] 
        legalKeywordArgs.append("stereotypeInstances")
        super()._initKeywordArgs(legalKeywordArgs, **kwargs)

    @property
    def metaclass(self):
        return self._metaclass

    @property
    def classObject(self):
        return self._classObject

    @metaclass.setter
    def metaclass(self, mcl):
        checkIsCMetaclass(mcl)
        if (self._metaclass != None):
            self._metaclass._removeClass(self)
        if mcl != None:
            checkNamedElementIsNotDeleted(mcl)
        self._metaclass = mcl
        self._metaclass._addClass(self)

    @property
    def objects(self):
        return list(self._objects)

    @property
    def allObjects(self):
        allObjects = list(self._objects)
        for scl in self.allSubclasses:
            for cl in scl._objects:
                allObjects.append(cl)
        return allObjects

    def _addObject(self, obj):
        if obj in self._objects:
            raise CException(f"object '{obj!s}' is already an instance of the class '{self!s}'")
        checkIsCObject(obj)
        self._objects.append(obj)
    
    def _removeObject(self, obj):
        if not obj in self._objects:
            raise CException(f"can't remove object '{obj!s}'' from class '{self!s}': not an instance")
        self._objects.remove(obj)

    def delete(self):
        if self._isDeleted == True:
            return

        objectsToDelete = list(self._objects)
        for obj in objectsToDelete:
            obj.delete()
        self._objects = []

        for si in self.stereotypeInstances:
            si._extendedInstances.remove(self)
        self._stereotypeInstancesHolder._stereotypes = []

        self.metaclass._removeClass(self)
        self._metaclass = None

        super().delete()

        self._classObject.delete()
        

    @property
    def classPath(self):
        return self._classObject.classPath

    def instanceOf(self, cl):
        return self._classObject.instanceOf(cl)

    def _updateDefaultValuesOfClassifier(self, attribute = None):
        for i in self.allObjects:
            attrItems = self._attributes.items()
            if attribute != None:
                attrItems = {attribute._name: attribute}.items()
            for attrName, attr in attrItems:
                if attr.default != None:
                    if i.getValue(attrName, self) == None:
                        i.setValue(attrName, attr.default, self)

    def _removeAttributeValuesOfClassifier(self, attributesToKeep):
        for i in self.allObjects:
            for attrName in self.attributeNames:
                if not attrName in attributesToKeep:
                    i._removeValue(attrName, self)

    def getValue(self, attributeName, cl = None):
        return self._classObject.getValue(attributeName, cl)

    def setValue(self, attributeName, value, cl = None):
        return self._classObject.setValue(attributeName, value, cl)
        
    def _removeValue(self, attributeName, cl):
        return self._classObject._removeValue(attributeName, cl)
    
    def getObjects(self, name):
        return list(o for o in self.objects if o.name == name)
    def getObject(self, name):
        l = self.getObjects(name)
        return None if len(l) == 0 else l[0]

    @property
    def stereotypeInstances(self):
        return self._stereotypeInstancesHolder.stereotypes
    
    @stereotypeInstances.setter
    def stereotypeInstances(self, elements):
        self._stereotypeInstancesHolder.stereotypes = elements

    def getTaggedValue(self, name, stereotype = None):
       return self._taggedValues.getTaggedValue(name, self._stereotypeInstancesHolder.getStereotypeInstancePath(), stereotype)

    def setTaggedValue(self, name, value, stereotype = None):
        self._taggedValues.setTaggedValue(name, value, self._stereotypeInstancesHolder.getStereotypeInstancePath(), stereotype)

    def _removeTaggedValue(self, attributeName, stereotype):
        self._taggedValues.removeTaggedValue(attributeName, stereotype)

    def association(self, target, descriptor = None, **kwargs):
        if not isinstance(target, CClass):
            raise CException(f"class '{self!s}' is not compatible with association target '{target!s}'")
        return super(CClass, self).association(target, descriptor, **kwargs)

    @property
    def linkObjects(self):
        return self._classObject.linkObjects

    @property
    def links(self):
        return self._classObject.links

    def getLinks(self, **kwargs):
        return self._classObject.getLinks(**kwargs)

    def _getLinksForAssociation(self, association):
        return self._classObject._getLinksForAssociation(association)

    def addLinks(self, links, **kwargs):
        return self._classObject.addLinks(links, **kwargs)

    def deleteLinks(self, links, **kwargs):
        return self._classObject.deleteLinks(links, **kwargs)