from codeable_models.internal.commons import setKeywordArgs, checkNamedElementIsNotDeleted, isCBundle, isCMetaclass, isCClass, isCStereotype, isCBundlable
from codeable_models.cexception import CException
from codeable_models.cnamedelement import CNamedElement

class CBundlable(CNamedElement):
    def __init__(self, name, **kwargs):
        self._bundles = []
        super().__init__(name, **kwargs)

    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = [] 
        legalKeywordArgs.append("bundles")
        super()._initKeywordArgs(legalKeywordArgs, **kwargs)

    @property
    def bundles(self):
        return list(self._bundles)

    @bundles.setter
    def bundles(self, bundles):
        if bundles == None:
            bundles = []
        for b in self._bundles:
            b.remove(self)
        self._bundles = []
        if isCBundle(bundles):
            bundles = [bundles]
        elif not isinstance(bundles, list):
            raise CException(f"bundles requires a list of bundles or a bundle as input")    
        for b in bundles:
            if not isCBundle(b):
                raise CException(f"bundles requires a list of bundles or a bundle as input")
            checkNamedElementIsNotDeleted(b)
            if b in self._bundles:
                raise CException(f"'{b.name!s}' is already a bundle of '{self.name!s}'")              
            self._bundles.append(b)
            b._elements.append(self)

    def delete(self):
        if self._isDeleted == True:
            return
        bundlesToDelete = list(self._bundles)
        for b in bundlesToDelete:
            b.remove(self)
        self._bundles = []
        super().delete()

    def getConnectedElements(self, **kwargs):
        context = ConnectedElementsContext()

        allowedKeywordArgs = ["addBundles", "processBundles", "stopElementsInclusive", "stopElementsExclusive"]
        if isCMetaclass(self) or isCBundle(self) or isCStereotype(self):
            allowedKeywordArgs = ["addStereotypes", "processStereotypes"] + allowedKeywordArgs
        setKeywordArgs(context, allowedKeywordArgs, **kwargs)

        if self in context.stopElementsExclusive:
            return []
        context.elements.append(self)
        self._computeConnected(context)
        if context.addBundles == False:
            context.elements = [elt for elt in context.elements if not isCBundle(elt)]
        if context.addStereotypes == False:
            context.elements = [elt for elt in context.elements if not isCStereotype(elt)]
        return context.elements

    def _appendConnected(self, context, connected):
        for c in connected:
            if not c in context.elements:
                context.elements.append(c)
                if not c in context._allStopElements:
                    c._computeConnected(context)

    def _computeConnected(self, context):
        connected = []
        for bundle in self._bundles:
            if not bundle in context.stopElementsExclusive:
                connected.append(bundle)
        self._appendConnected(context, connected)

class ConnectedElementsContext(object):
    def __init__(self):
        self.elements = []
        self.addBundles = False
        self.addStereotypes = False
        self.processBundles = False
        self.processStereotypes = False
        self._stopElementsInclusive = []
        self._stopElementsExclusive = []
        self._allStopElements = []

    @property
    def stopElementsInclusive(self):
        return list(self._stopElementsInclusive)

    @stopElementsInclusive.setter
    def stopElementsInclusive(self, stopElementsInclusive):
        if isCBundlable(stopElementsInclusive):
            stopElementsInclusive = [stopElementsInclusive]
        if not isinstance(stopElementsInclusive, list):
            raise CException(f"expected one element or a list of stop elements, but got: '{stopElementsInclusive!s}'")
        for e in stopElementsInclusive:
            if not isCBundlable(e):
                raise CException(f"expected one element or a list of stop elements, but got: '{stopElementsInclusive!s}' with element of wrong type: '{e!s}'")
        self._stopElementsInclusive = stopElementsInclusive
        self._allStopElements = self._stopElementsInclusive + self._stopElementsExclusive

    @property
    def stopElementsExclusive(self):
        return list(self._stopElementsExclusive)

    @stopElementsExclusive.setter
    def stopElementsExclusive(self, stopElementsExclusive):
        if isCBundlable(stopElementsExclusive):
            stopElementsExclusive = [stopElementsExclusive]
        if not isinstance(stopElementsExclusive, list):
            raise CException(f"expected a list of stop elements, but got: '{stopElementsExclusive!s}'")
        for e in stopElementsExclusive:
            if not isCBundlable(e):
                raise CException(f"expected a list of stop elements, but got: '{stopElementsExclusive!s}' with element of wrong type: '{e!s}'")
        self._stopElementsExclusive = stopElementsExclusive
        self._allStopElements = self._stopElementsInclusive + self._stopElementsExclusive