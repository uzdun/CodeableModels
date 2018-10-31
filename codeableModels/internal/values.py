from codeableModels.cexception import CException
from codeableModels.internal.commons import *

class ValueKind:
    ATTRIBUTE_VALUE = 1
    TAGGED_VALUE = 2
    DEFAULT_VALUE = 3
        
def _getAttributeUnknownException(valueKind, entity, attributeName):
    valueKindStr = ""
    if valueKind == ValueKind.TAGGED_VALUE:
        valueKindStr = "tagged value"
    elif valueKind == ValueKind.ATTRIBUTE_VALUE or valueKind == ValueKind.DEFAULT_VALUE:
        valueKindStr = "attribute"
    else:
        raise CException("unknown attribute kind")    

    if valueKind == ValueKind.DEFAULT_VALUE:
        return CException(f"{valueKindStr!s} '{attributeName!s}' unknown for metaclasses extended by stereotype '{entity!s}'")
    if isCLink(entity):
        return CException(f"{valueKindStr!s} '{attributeName!s}' unknown")
    return CException(f"{valueKindStr!s} '{attributeName!s}' unknown for '{entity!s}'")

def _getAndCheckAttributeClassifier(_self, classPath, attributeName, valueKind, classifier = None):
    if classifier == None:
        # search on a class path
        for cl in classPath:
            if cl.getAttribute(attributeName) != None:
                return _getAndCheckAttributeClassifier(_self, classPath, attributeName, valueKind, cl)
        raise _getAttributeUnknownException(valueKind, _self, attributeName)
    else:
        # check only on specified classifier
        attribute = classifier.getAttribute(attributeName)
        if attribute == None:
            raise _getAttributeUnknownException(valueKind, classifier, attributeName)
        attribute.checkAttributeTypeIsNotDeleted()
        return attribute

def _deleteValue(_self, classPath, valuesDict, attributeName, valueKind, classifier = None):
    if _self._isDeleted:
        raise CException(f"can't delete '{attributeName!s}' on deleted element")
    attribute = _getAndCheckAttributeClassifier(_self, classPath, attributeName, valueKind, classifier)
    try:
        valuesOfClassifier = valuesDict[attribute.classifier]
    except KeyError:
        return None
    try:
        value = valuesOfClassifier[attributeName]
        del valuesOfClassifier[attributeName]
        return value
    except KeyError:
        return None 

def _setValue(_self, classPath, valuesDict, attributeName, value, valueKind, classifier = None):
    if _self._isDeleted:
        raise CException(f"can't set '{attributeName!s}' on deleted element")
    attribute = _getAndCheckAttributeClassifier(_self, classPath, attributeName, valueKind, classifier)
    attribute.checkAttributeValueType(attributeName, value)
    try:
        valuesDict[attribute.classifier].update({attributeName: value})
    except KeyError:
        valuesDict[attribute.classifier] = {attributeName: value}

def _getValue(_self, classPath, valuesDict, attributeName, valueKind, classifier = None):
    if _self._isDeleted:
        raise CException(f"can't get '{attributeName!s}' on deleted element")
    attribute = _getAndCheckAttributeClassifier(_self, classPath, attributeName, valueKind, classifier)
    try:
        valuesOfClassifier = valuesDict[attribute.classifier]
    except KeyError:
        return None
    try:
        return valuesOfClassifier[attributeName]
    except KeyError:
        return None 

def _getValues(classPath, valuesDict):
    result = {}
    for cl in classPath:
        if cl in valuesDict:
            for attrName in valuesDict[cl]:
                if not attrName in result:
                    result[attrName] = valuesDict[cl][attrName]
    return result

def _setValues(_self, newValues, valuesKind):
        if newValues == None:
            newValues = {}
        if not isinstance(newValues, dict):
            valueKindStr = ""
            if valuesKind == ValueKind.TAGGED_VALUE:
                valueKindStr = "tagged values"
            elif valuesKind == ValueKind.ATTRIBUTE_VALUE:
                valueKindStr = "attribute values"
            elif valuesKind == ValueKind.DEFAULT_VALUE:
                valueKindStr = "default values"
            else:
                raise CException("unknown attribute kind")    
            raise CException(f"malformed {valueKindStr!s} description: '{newValues!s}'")
        for valueName in newValues:
            if valuesKind == ValueKind.ATTRIBUTE_VALUE:
                _self.setValue(valueName, newValues[valueName])
            elif valuesKind == ValueKind.TAGGED_VALUE:
                _self.setTaggedValue(valueName, newValues[valueName])
            elif valuesKind == ValueKind.DEFAULT_VALUE:
                _self.setDefaultValue(valueName, newValues[valueName])
            else:
                raise CException("unknown attribute kind")    


            
