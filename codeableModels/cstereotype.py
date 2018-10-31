from codeableModels.cclassifier import CClassifier
from codeableModels.cexception import CException
from codeableModels.cmetaclass import CMetaclass
from codeableModels.cassociation import CAssociation
from codeableModels.internal.commons import *
from codeableModels.internal.values import _deleteValue, _setValue, _getValue, _getValues, _setValues, ValueKind


def _determineExtendedTypeOfList(elements):
    if len(elements) == 0:
        return None
    if isCMetaclass(elements[0]):
        return CMetaclass
    if isCAssociation(elements[0]):
        return CAssociation
    raise CException(f"unknown type of extend element: '{elements[0]!s}'")

class CStereotype(CClassifier):
    def __init__(self, name=None, **kwargs):
        self._extended = []
        self._extendedInstances = []
        self._defaultValues = {}
        super().__init__(name, **kwargs)

    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = [] 
        legalKeywordArgs.append("extended")
        legalKeywordArgs.append("defaultValues")
        super()._initKeywordArgs(legalKeywordArgs, **kwargs)

    @property
    def extended(self):
        return list(self._extended)
    
    @extended.setter
    def extended(self, elements):
        if elements == None:
            elements = []
        for e in self._extended:
            e._stereotypesHolder._stereotypes.remove(self)
        self._extended = []
        if isCMetaclass(elements):
            extendedType = CMetaclass
            elements = [elements]
        elif isCAssociation(elements):
            extendedType = CAssociation
            elements = [elements]
        elif not isinstance(elements, list):
            raise CException(f"extended requires a list or a metaclass as input")
        else:
            extendedType = _determineExtendedTypeOfList(elements)
    
        for e in elements:
            if extendedType == CMetaclass:
                checkIsCMetaclass(e)
            elif extendedType == CAssociation:
                checkIsCAssociation(e)
            else:
                raise CException(f"type of extend element incompatible: '{e!s}'")
            checkNamedElementIsNotDeleted(e)
            if e in self._extended:
                raise CException(f"'{e.name!s}' is already extended by stereotype '{self.name!s}'")
            self._extended.append(e)
            e._stereotypesHolder._stereotypes.append(self)
        
    @property
    def extendedInstances(self):
        return list(self._extendedInstances)

    @property
    def allExtendedInstances(self):
        allInstances = list(self._extendedInstances)
        for scl in self.allSubclasses:
            for cl in scl._extendedInstances:
                allInstances.append(cl)
        return allInstances

    def delete(self):
        if self._isDeleted == True:
            return
        for e in self._extended:
            e._stereotypesHolder._stereotypes.remove(self)
        self._extended = []
        super().delete()
        
    def _updateDefaultValuesOfClassifier(self, attribute = None):
        allClasses = [self] + list(self.allSubclasses)
        for sc in allClasses:
            for i in sc._extendedInstances:
                attrItems = self._attributes.items()
                if attribute != None:
                    attrItems = {attribute._name: attribute}.items()
                for attrName, attr in attrItems:
                    if attr.default != None:
                        if i.getTaggedValue(attrName, self) == None:
                            i.setTaggedValue(attrName, attr.default, self)

    def _removeAttributeValuesOfClassifier(self, attributesToKeep):
        for i in self._extendedInstances:
            for attrName in self.attributeNames:
                if not attrName in attributesToKeep:
                    i.deleteTaggedValue(attrName, self)

    def isMetaclassExtendedByThisStereotype(self, metaclass):
        if metaclass in self._extended:
            return True
        for mcSuperclass in metaclass._getAllSuperclasses():
            if mcSuperclass in self._extended:
                return True
        return False

    def isElementExtendedByStereotype(self, element):
        if isCClass(element):
            if self.isMetaclassExtendedByThisStereotype(element.metaclass):
                return True
            for superclass in self._getAllSuperclasses():
                if superclass.isMetaclassExtendedByThisStereotype(element.metaclass):
                    return True
            return False
        elif isCLink(element):
            if element.association in self.extended:
                return True
            for superclass in self._getAllSuperclasses():
                if element.association in superclass.extended:
                    return True
            return False
        raise CException("element is neither a metaclass nor an association")

    def association(self, target, descriptor = None, **kwargs):
        if not isinstance(target, CStereotype):
            raise CException(f"stereotype '{self!s}' is not compatible with association target '{target!s}'")
        return super(CStereotype, self).association(target, descriptor, **kwargs)

    def _computeConnected(self, context):
        super()._computeConnected(context)
        if context.processStereotypes == False:
            return
        connected = []
        for e in self.extended:
            if not e in context.stopElementsExclusive:
                connected.append(e)
        self._appendConnected(context, connected)

    def _getAllExtendedElements(self):
        result = []
        for cl in self.classPath:
            for extendedElement in cl.extended:
                if not extendedElement in result:
                    result.append(extendedElement)
        return result

    def _getDefaultValueClassPath(self):
        result = []
        for extendedElement in self._getAllExtendedElements():
            if not isCMetaclass(extendedElement):
                raise CException(f"default values can only be used on a stereotype that extends metaclasses")
            for mcl in extendedElement.classPath:
                if not mcl in result:
                    result.append(mcl)
        return result

    @property
    def defaultValues(self):
        if self._isDeleted:
            raise CException(f"can't get default values on deleted stereotype")
        classPath = self._getDefaultValueClassPath()
        return _getValues(classPath, self._defaultValues)

    @defaultValues.setter
    def defaultValues(self, newValues):
        if self._isDeleted:
            raise CException(f"can't set default values on deleted stereotype")
        classPath = self._getDefaultValueClassPath()
        if len(classPath) == 0:
            raise CException(f"default values can only be used on a stereotype that extends metaclasses")
        _setValues(self, newValues, ValueKind.DEFAULT_VALUE)

    def getDefaultValue(self, attributeName, classifier = None):
        if self._isDeleted:
            raise CException(f"can't get default value '{attributeName!s}' on deleted stereotype")
        classPath = self._getDefaultValueClassPath()
        if len(classPath) == 0:
            raise CException(f"default values can only be used on a stereotype that extends metaclasses")
        return _getValue(self, classPath, self._defaultValues, attributeName, ValueKind.DEFAULT_VALUE, classifier)
             
    def deleteDefaultValue(self, attributeName, classifier = None):
        if self._isDeleted:
            raise CException(f"can't delete default value '{attributeName!s}' on deleted stereotype")
        classPath = self._getDefaultValueClassPath()
        if len(classPath) == 0:
            raise CException(f"default values can only be used on a stereotype that extends metaclasses")
        return _deleteValue(self, classPath, self._defaultValues, attributeName, ValueKind.DEFAULT_VALUE, classifier)

    def setDefaultValue(self, attributeName, value, classifier = None):
        if self._isDeleted:
            raise CException(f"can't set default value '{attributeName!s}' on deleted stereotype")
        classPath = self._getDefaultValueClassPath()
        if len(classPath) == 0:
            raise CException(f"default values can only be used on a stereotype that extends metaclasses")
        _setValue(self, classPath, self._defaultValues, attributeName, value, ValueKind.DEFAULT_VALUE, classifier)
