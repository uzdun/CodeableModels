from codeable_models.cclassifier import CClassifier
from codeable_models.cexception import CException
from codeable_models.internal.commons import checkIsCClass, setKeywordArgs, checkIsCStereotype, isCStereotype, checkNamedElementIsNotDeleted
from codeable_models.internal.stereotype_holders import CStereotypesHolder

class CMetaclass(CClassifier):
    def __init__(self, name=None, **kwargs):
        self._classes = []
        self._stereotypesHolder = CStereotypesHolder(self)
        super().__init__(name, **kwargs)

    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = [] 
        legalKeywordArgs.append("stereotypes")
        super()._initKeywordArgs(legalKeywordArgs, **kwargs)

    @property
    def classes(self):
        return list(self._classes)

    @property
    def allClasses(self):
        allClasses = list(self._classes)
        for scl in self.allSubclasses:
            for cl in scl._classes:
                allClasses.append(cl)
        return allClasses

    def getClasses(self, name):
        return list(cl for cl in self.classes if cl.name == name)
    def getClass(self, name):
        l = self.getClasses(name)
        return None if len(l) == 0 else l[0]

    def getStereotypes(self, name):
        return list(cl for cl in self.stereotypes if cl.name == name)
    def getStereotype(self, name):
        l = self.getStereotypes(name)
        return None if len(l) == 0 else l[0]
    
    def _addClass(self, cl):
        checkIsCClass(cl)
        if cl in self._classes:
            raise CException(f"class '{cl!s}' is already a class of the metaclass '{self!s}'")
        self._classes.append(cl)
    
    def _removeClass(self, cl):
        if not cl in self._classes:
            raise CException(f"can't remove class instance '{cl!s}' from metaclass '{self!s}': not a class instance")
        self._classes.remove(cl)

    def delete(self):
        if self._isDeleted == True:
            return
        classesToDelete = list(self._classes)
        for cl in classesToDelete:
            cl.delete()
        self._classes = []
        for s in self._stereotypesHolder._stereotypes:
            s._extended.remove(self)
        self._stereotypesHolder._stereotypes = []
        super().delete()
        
    @property
    def stereotypes(self):
        return self._stereotypesHolder.stereotypes
    
    @stereotypes.setter
    def stereotypes(self, elements):
        self._stereotypesHolder.stereotypes = elements

    def _updateDefaultValuesOfClassifier(self, attribute = None):
        for i in self.allClasses:
            attrItems = self._attributes.items()
            if attribute != None:
                attrItems = {attribute._name: attribute}.items()
            for attrName, attr in attrItems:
                if attr.default != None:
                    if i.getValue(attrName, self) == None:
                        i.setValue(attrName, attr.default, self)

    def _removeAttributeValuesOfClassifier(self, attributesToKeep):
        for i in self.allClasses:
            for attrName in self.attributeNames:
                if not attrName in attributesToKeep:
                    i.deleteValue(attrName, self)

    def association(self, target, descriptor = None, **kwargs):
        if not isinstance(target, CMetaclass):
            raise CException(f"metaclass '{self!s}' is not compatible with association target '{target!s}'")
        return super(CMetaclass, self).association(target, descriptor, **kwargs)

    def _computeConnected(self, context):
        super()._computeConnected(context)
        connected = []
        for s in self.stereotypes:
            if not s in context.stopElementsExclusive:
                connected.append(s)
        self._appendConnected(context, connected)