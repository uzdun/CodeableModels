from codeableModels.cexception import CException

class CTaggedValues:
    def __init__(self):
        self._taggedValues = {}

    def setTaggedValue(self, taggedValueName, value, legalStereotypes, stereotype = None):
        if stereotype == None:
            for s in legalStereotypes:
                if s.getAttribute(taggedValueName) != None:
                    self._setValueUsingSpecifiedStereotype(taggedValueName, value, s)
                    return
            raise CException(f"tagged value '{taggedValueName!s}' unknown")
        else:
            if not stereotype in legalStereotypes:
                raise CException(f"stereotype '{stereotype!s}' is not a stereotype of element")
            return self._setValueUsingSpecifiedStereotype(taggedValueName, value, stereotype)

    def _setValueUsingSpecifiedStereotype(self, name, value, stereotype):
        attribute = stereotype.getAttribute(name)
        if attribute == None:
            raise CException(f"tagged value '{name!s}' unknown for stereotype '{stereotype!s}'")
        attribute.checkAttributeTypeIsNotDeleted()
        attribute.checkAttributeValueType(name, value)
        try:
            self._taggedValues[stereotype].update({name: value})
        except KeyError:
            self._taggedValues[stereotype] = {name: value}

    def getTaggedValue(self, taggedValueName, legalStereotypes, stereotype = None):
        if stereotype == None:
            for s in legalStereotypes:
                if s.getAttribute(taggedValueName) != None:
                    return self._getValueUsingSpecifiedStereotype(taggedValueName, s)
            raise CException(f"tagged value '{taggedValueName!s}' unknown")
        else: 
            if not stereotype in legalStereotypes:
                raise CException(f"stereotype '{stereotype!s}' is not a stereotype of element")
            return self._getValueUsingSpecifiedStereotype(taggedValueName, stereotype)

    def _getValueUsingSpecifiedStereotype(self, name, stereotype):
        attribute = stereotype.getAttribute(name)
        if attribute == None:
            raise CException(f"tagged value '{name!s}' unknown for stereotype '{stereotype!s}'")
        attribute.checkAttributeTypeIsNotDeleted()
        try:
            taggedValuesClassifier = self._taggedValues[stereotype]
        except KeyError:
            return None
        try:
            return taggedValuesClassifier[name]
        except KeyError:
            return None

    def removeTaggedValue(self, attributeName, stereotype):
        try:
            self._taggedValues[stereotype].pop(attributeName, None)
        except KeyError:
            return
