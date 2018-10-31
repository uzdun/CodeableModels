from codeableModels.cbundlable import CBundlable
from codeableModels.cenum import CEnum
from codeableModels.cattribute import CAttribute
from codeableModels.cassociation import CAssociation
from codeableModels.cexception import CException
from codeableModels.internal.commons import *

class CClassifier(CBundlable):
    def __init__(self, name=None, **kwargs):
        self._superclasses = []
        self._subclasses = []
        self._attributes = {}
        self._associations = []
        super().__init__(name, **kwargs)

    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = [] 
        legalKeywordArgs.append("attributes")
        legalKeywordArgs.append("superclasses")
        super()._initKeywordArgs(legalKeywordArgs, **kwargs)

    @property
    def attributes(self):
        return list(self._attributes.values())

    def _setAttribute(self, name, value):
        if name in self._attributes.keys():
            raise CException(f"duplicate attribute name: '{name!s}'")
        attr = None
        if isCAttribute(value):
            attr = value
        elif isKnownAttributeType(value) or isinstance(value, CEnum) or isCClassifier(value):
            # if value is a CClass, we interpret it as the type for a CObject attribute, not the default 
            # value of a CMetaclass type attribute: if you need to set a metaclass type default value, use 
            # CAttribute's default instead
            attr = CAttribute(type = value)
        else:
            attr = CAttribute(default = value)
        attr._name = name
        attr._classifier = self
        self._attributes.update({name: attr})

    @attributes.setter
    def attributes(self, attributeDescriptions):
        if attributeDescriptions == None:
            attributeDescriptions = {}
        self._removeAttributeValuesOfClassifier(attributeDescriptions.keys())
        self._attributes = {}
        if not isinstance(attributeDescriptions, dict):
            raise CException(f"malformed attribute description: '{attributeDescriptions!s}'")
        for attributeName in attributeDescriptions:
            self._setAttribute(attributeName, attributeDescriptions[attributeName])
        self._updateDefaultValuesOfClassifier()

    def _removeAttributeValuesOfClassifier(self, attributesToKeep):
        raise CException("should be overridden by subclasses to update defaults on instances")
    def _updateDefaultValuesOfClassifier(self, attribute = None):
        raise CException("should be overridden by subclasses to update defaults on instances")

    def _checkSameTypeAsSelf(self, cl):
        return isinstance(cl, self.__class__)

    @property
    def subclasses(self):
        return list(self._subclasses)

    @property
    def superclasses(self):
        return list(self._superclasses)
    
    @superclasses.setter
    def superclasses(self, elements):
        if elements == None:
            elements = []
        for sc in self._superclasses:
            sc._subclasses.remove(self)
        self._superclasses = []
        if isCClassifier(elements):
            elements = [elements]
        for scl in elements:
            if scl != None:
                checkNamedElementIsNotDeleted(scl)
            if not isinstance(scl, self.__class__):
                raise CException(f"cannot add superclass '{scl!s}' to '{self!s}': not of type {self.__class__!s}")
            if scl in self._superclasses:
                raise CException(f"'{scl.name!s}' is already a superclass of '{self.name!s}'")
            self._superclasses.append(scl)
            scl._subclasses.append(self)
        
    @property
    def allSuperclasses(self):
        return self._getAllSuperclasses()

    @property
    def allSubclasses(self):
        return self._getAllSubclasses()

    def conformsToType(self, classifier):
        typeClassifiers = classifier.allSubclasses
        typeClassifiers.add(classifier)
        if self in typeClassifiers:
            return True
        return False

    @property
    def attributeNames(self):
        return list(self._attributes.keys())
    
    def getAttribute(self, attributeName):
        if attributeName == None or not isinstance(attributeName, str):
            return None
        try:
            return self._attributes[attributeName]
        except KeyError:
            return None
    
    def _removeAllAssociations(self):
        associations = self.associations.copy()
        for association in associations:
            association.delete()

    def _removeSubclass(self, cl):
        if not cl in self._subclasses:
            raise CException(f"can't remove subclass '{cl!s}' from classifier '{self!s}': not a subclass")
        self._subclasses.remove(cl)

    def _removeSuperclass(self, cl):
        if not cl in self._superclasses:
            raise CException(f"can't remove superclass '{cl!s}' from classifier '{self!s}': not a superclass")
        self._superclasses.remove(cl)

    def delete(self):
        if self._isDeleted == True:
            return
        super().delete()
        # self.superclasses removes the self subclass from the superclasses
        self.superclasses = []
        for subclass in self._subclasses:
            subclass._removeSuperclass(self)
        self._subclasses = []
        self._removeAllAssociations()
        for a in self.attributes:
            a._name = None
            a._classifier = None
        self._attributes = {}

    def _getAllSuperclasses(self, iteratedClasses = None):
        if iteratedClasses == None:
            iteratedClasses = set()
        result = set()
        for sc in self.superclasses:
            if not sc in iteratedClasses:
                iteratedClasses.add(sc)
                result.add(sc)
                result.update(sc._getAllSuperclasses(iteratedClasses))
        return result

    def _getAllSubclasses(self, iteratedClasses = None):
        if iteratedClasses == None:
            iteratedClasses = set()
        result = set()
        for sc in self.subclasses:
            if not sc in iteratedClasses:
                iteratedClasses.add(sc)
                result.add(sc)
                result.update(sc._getAllSubclasses(iteratedClasses))
        return result

    def hasSubclass(self, cl):
        return (cl in self._getAllSubclasses())

    def hasSuperclass(self, cl):
        return (cl in self._getAllSuperclasses())

    @property
    def associations(self):
        return list(self._associations)

    @property
    def allAssociations(self):
        allAssociations = self.associations
        for sc in self.allSuperclasses:
            for a in sc.associations:
                if not a in allAssociations: 
                    allAssociations.extend([a])
        return allAssociations
    
    def association(self, target, descriptor = None, **kwargs):
        a = CAssociation(self, target, descriptor, **kwargs)
        self._associations.append(a)
        if self != target:
            target._associations.append(a)
        return a

    def _computeConnected(self, context):
        super()._computeConnected(context)
        connectedCandidates = []
        connected = []
        for association in self.associations:
            connectedCandidates.append(association._getOppositeClass(self))
        connectedCandidates = self.superclasses + self.subclasses + connectedCandidates
        for c in connectedCandidates:
            if not c in context.stopElementsExclusive:
                connected.append(c)
        self._appendConnected(context, connected)

    # get class path starting from this classifier, including this classifier
    def _getClassPath(self):
        classPath = [self]
        for sc in self.superclasses:
            for cl in sc._getClassPath():
                if not cl in classPath:
                    classPath.append(cl)
        return classPath

    @property
    def classPath(self):
        return self._getClassPath()