from codeable_models.cexception import CException
from codeable_models.internal.commons import checkIsCClass, isCClass, isCLink, setKeywordArgs, checkIsCStereotype, isCStereotype, checkNamedElementIsNotDeleted

class CStereotypesHolder:
    def __init__(self, element):
        self._stereotypes = []
        self.element = element

    @property
    def stereotypes(self):
        return list(self._stereotypes)

    # methods to be overridden in subclass
    def _removeFromStereotype(self):
        for s in self._stereotypes:
            s._extended.remove(self.element)
    def _appendOnStereotype(self, stereotype):
        stereotype._extended.append(self.element)
    def _checkStereotypeCanBeAdded(self, stereotype):
        if stereotype in self._stereotypes:
            raise CException(f"'{stereotype.name!s}' is already a stereotype of '{self.element.name!s}'")
    def _initExtendedElement(self, stereotype):
        pass

    # template method
    def _setStereotypes(self, elements):
        if elements == None:
            elements = []
        self._removeFromStereotype()
        self._stereotypes = []
        if isCStereotype(elements):
            elements = [elements]
        elif not isinstance(elements, list):
            raise CException(f"a list or a stereotype is required as input")
        for s in elements:
            checkIsCStereotype(s)
            if s != None:
                checkNamedElementIsNotDeleted(s)
            self._checkStereotypeCanBeAdded(s)
            self._stereotypes.append(s)
            self._appendOnStereotype(s)
            self._initExtendedElement(s)
                
    @stereotypes.setter
    def stereotypes(self, elements):
        self._setStereotypes(elements)

class CStereotypeInstancesHolder(CStereotypesHolder):
    def __init__(self, element):
        super().__init__(element)
    
    def _setAllDefaultTaggedValuesOfStereotype(self, stereotype):
        for a in stereotype.attributes:
            if a.default != None:
                self.element.setTaggedValue(a._name, a.default, stereotype)
        
    def _getStereotypeInstancePathSuperclasses(self, stereotype):
        stereotypePath = [stereotype]
        for superclass in stereotype.superclasses:
            for superclassStereotype in self._getStereotypeInstancePathSuperclasses(superclass):
                if not superclassStereotype in stereotypePath:
                    stereotypePath.append(superclassStereotype)
        return stereotypePath                    
    
    def getStereotypeInstancePath(self):
        stereotypePath = []
        for stereotypeOfThisElement in self.stereotypes:
            for stereotype in self._getStereotypeInstancePathSuperclasses(stereotypeOfThisElement):
                if not stereotype in stereotypePath:
                    stereotypePath.append(stereotype)
        return stereotypePath

    def _removeFromStereotype(self):
        for s in self._stereotypes:
            s._extendedInstances.remove(self.element)

    def _appendOnStereotype(self, stereotype):
        stereotype._extendedInstances.append(self.element)

    def _getElementNameString(self):
        if isCClass(self.element):
            return f"'{self.element.name!s}'"
        elif isCLink(self.element):
            return f"link from '{self.element.source!s}' to '{self.element.target!s}'"
        raise CException(f"unexpected element type: {self.element!r}")

    def _checkStereotypeCanBeAdded(self, stereotype):
        if stereotype in self._stereotypes:
            raise CException(f"'{stereotype.name!s}' is already a stereotype instance on {self._getElementNameString()!s}")
        if not stereotype.isElementExtendedByStereotype(self.element):
            raise CException(f"stereotype '{stereotype!s}' cannot be added to {self._getElementNameString()!s}: no extension by this stereotype found")

    def _initExtendedElement(self, stereotype):
        self._setAllDefaultTaggedValuesOfStereotype(stereotype)
        for sc in stereotype.allSuperclasses:
            self._setAllDefaultTaggedValuesOfStereotype(sc)