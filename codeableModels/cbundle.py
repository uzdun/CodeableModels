from codeableModels.cobject import CObject
from codeableModels.cclassifier import CClassifier
from codeableModels.cexception import CException
from codeableModels.cmetaclass import CMetaclass
from codeableModels.cbundlable import CBundlable
from codeableModels.cstereotype import CStereotype
from codeableModels.cclass import CClass
from codeableModels.cenum import CEnum
from codeableModels.internal.commons import isCNamedElement, setKeywordArgs, checkNamedElementIsNotDeleted

class CBundle(CBundlable):
    def __init__(self, name=None, **kwargs):
        self._elements = []
        super().__init__(name, **kwargs)

    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = [] 
        legalKeywordArgs.append("elements")
        super()._initKeywordArgs(legalKeywordArgs, **kwargs)

    def add(self, elt):
        if elt != None:
            if elt in self._elements:
                raise CException(f"element '{elt!s}' cannot be added to bundle: element is already in bundle")
            if isinstance(elt, CBundlable):
                self._elements.append(elt)
                elt._bundles.append(self)
                return
        raise CException(f"can't add '{elt!s}': not an element")

    def remove(self, element):
        if (element == None or 
            (not isinstance(element, CBundlable)) or 
            (not self in element.bundles)):
            raise CException(f"'{element!s}' is not an element of the bundle")
        self._elements.remove(element)
        element._bundles.remove(self)

    def delete(self):
        if self._isDeleted == True:
            return
        elementsToDelete = list(self._elements)
        for e in elementsToDelete:
            e._bundles.remove(self)
        self._elements = []
        super().delete()

    @property
    def elements(self):
        return list(self._elements)

    @elements.setter
    def elements(self, elements):
        if elements == None:
            elements = []
        for e in self._elements:
            e._bundle = None
        self._elements = []
        if isCNamedElement(elements):
            elements = [elements]
        elif not isinstance(elements, list):
            raise CException(f"elements requires a list or a named element as input")
        for e in elements:
            if e != None:
                checkNamedElementIsNotDeleted(e)
            else:
                raise CException(f"'None' cannot be an element of bundle")
            isCNamedElement(e)
            if not e in self._elements:
                # if it is already in the bundle, do not add it twice
                self._elements.append(e)
                e._bundles.append(self)

    def getElements(self, **kwargs):
        type = None
        name = None
        # use this as name can also be provided as None
        nameSpecified = False
        for key in kwargs:
            if key == "type":
                type = kwargs["type"]
            elif key == "name":
                name = kwargs["name"]
                nameSpecified = True
            else:
                raise CException(f"unknown argument to getElements: '{key!s}'")
        elements = []
        for elt in self._elements:
            append = True
            if nameSpecified and elt.name != name:
                append = False
            if type != None and not isinstance(elt, type):
                append = False
            if append:
                elements.append(elt)
        return elements

    def getElement(self, **kwargs):
        l = self.getElements(**kwargs)
        return None if len(l) == 0 else l[0]

    def _computeConnected(self, context):
        super()._computeConnected(context)
        if context.processBundles == False:
            return
        connected = []
        for element in self._elements:
            if not element in context.stopElementsExclusive:
                connected.append(element)
        self._appendConnected(context, connected)

class CPackage(CBundle):
    pass

class CLayer(CBundle):
    def __init__(self, name=None, **kwargs):
        self._subLayer = None
        self._superLayer = None
        super().__init__(name, **kwargs)

    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = [] 
        legalKeywordArgs.append("subLayer")
        legalKeywordArgs.append("superLayer")
        super()._initKeywordArgs(legalKeywordArgs, **kwargs)

    @property
    def subLayer(self):
        return self._subLayer

    @subLayer.setter
    def subLayer(self, layer):
        if layer != None and not isinstance(layer, CLayer):
            raise CException(f"not a layer: {layer!s}")
        if self._subLayer != None:
            self._subLayer._superLayer = None
        self._subLayer = layer
        if layer != None:
            if layer._superLayer != None:
                layer._superLayer._subLayer = None
            layer._superLayer = self

    @property
    def superLayer(self):
        return self._superLayer

    @superLayer.setter
    def superLayer(self, layer):
        if layer != None and not isinstance(layer, CLayer):
            raise CException(f"not a layer: {layer!s}")
        if self._superLayer != None:
            self._superLayer._subLayer = None
        self._superLayer = layer
        if layer != None:
            if layer._subLayer != None:
                layer._subLayer._superLayer = None
            layer._subLayer = self


