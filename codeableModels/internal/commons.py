from codeableModels.cexception import CException

def setKeywordArgs(object, allowedValues, **kwargs):
    for key in kwargs:
        if key in allowedValues:
            setattr(object, key, kwargs[key])
        else:
            raise CException(f"unknown keyword argument '{key!s}', should be one of: {allowedValues!s}")

def getAttributeType(attr):
    if isinstance(attr, str):
        return str
    elif isinstance(attr, bool):
        return bool
    elif isinstance(attr, int):
        return int
    elif isinstance(attr, float):
        return float
    elif isinstance(attr, list):
        return list
    elif isCObject(attr):
        checkNamedElementIsNotDeleted(attr)
        return attr.classifier
    elif isCClass(attr):
        checkNamedElementIsNotDeleted(attr)
        return attr.metaclass
    return None
    
def isKnownAttributeType(type):
    if isCNamedElement(type):
        return False
    return (type == str or type == bool or type == int or type == float or type == list)

def isCEnum(elt):
    from codeableModels.cenum import CEnum
    if isinstance(elt, CEnum):
        return True
    return False

def isCClassifier(elt):
    from codeableModels.cclassifier import CClassifier
    if isinstance(elt, CClassifier):
        return True
    return False

def isCNamedElement(elt):
    from codeableModels.cnamedelement import CNamedElement
    if isinstance(elt, CNamedElement):
        return True
    return False

def isCAttribute(elt):
    from codeableModels.cattribute import CAttribute
    if isinstance(elt, CAttribute):
        return True
    return False

def isCObject(elt):
    from codeableModels.cobject import CObject
    if isinstance(elt, CObject):
        return True
    return False

def isCClass(elt):
    from codeableModels.cclass import CClass
    if isinstance(elt, CClass):
        return True
    return False

def isCMetaclass(elt):
    from codeableModels.cmetaclass import CMetaclass
    if isinstance(elt, CMetaclass):
        return True
    return False

def isCStereotype(elt):
    from codeableModels.cstereotype import CStereotype
    if isinstance(elt, CStereotype):
        return True
    return False

def isCBundle(elt):
    from codeableModels.cbundle import CBundle
    if isinstance(elt, CBundle):
        return True
    return False

def isCBundlable(elt):
    from codeableModels.cbundlable import CBundlable
    if isinstance(elt, CBundlable):
        return True
    return False

def isCAssociation(elt):
    from codeableModels.cassociation import CAssociation
    if isinstance(elt, CAssociation):
        return True
    return False

def isCLink(elt):
    from codeableModels.clink import CLink
    if isinstance(elt, CLink):
        return True
    return False

def checkIsCMetaclass(elt):
    if not isCMetaclass(elt):
        raise CException(f"'{elt!s}' is not a metaclass")

def checkIsCClassifier(elt):
    if not isCClassifier(elt):
        raise CException(f"'{elt!s}' is not a classifier")

def checkIsCClass(elt):
    if not isCClass(elt):
        raise CException(f"'{elt!s}' is not a class")

def checkIsCStereotype(elt):
    if not isCStereotype(elt):
        raise CException(f"'{elt!s}' is not a stereotype")

def checkIsCObject(elt):
    if not isCObject(elt):
        raise CException(f"'{elt!s}' is not an object")

def checkIsCBundle(elt):
    if not isCBundle(elt):
        raise CException(f"'{elt!s}' is not a bundle") 

def checkIsCAssociation(elt):
    if not isCAssociation(elt):
        raise CException(f"'{elt!s}' is not a association") 

def checkNamedElementIsNotDeleted(namedElement):
    if namedElement._isDeleted == True:
        raise CException(f"cannot access named element that has been deleted") 

# get the common (top level) classifier in a list of objects
def getCommonClassifier(objects):
    commonClassifier = None
    for o in objects:
        if o == None or not isCObject(o):
            raise CException(f"not an object: '{o!s}'")
        if commonClassifier == None:
            commonClassifier = o.classifier
        else:
            if commonClassifier == o.classifier:
                continue
            if commonClassifier in o.classifier.allSuperclasses:
                continue
            if commonClassifier in o.classifier.allSubclasses:
                commonClassifier = o.classifier
                continue
            raise CException(f"object '{o!s}' has an incompatible classifier")
    return commonClassifier

def checkIsCommonClassifier(classifier, objects):
    for o in objects:
        if not o.instanceOf(classifier):
            raise CException(f"object '{o!s}' not compatible with classifier '{classifier!s}'")

def _removeSuperclassesAndDuplicates(classes):
    result = []
    while len(classes) > 0:
        currentClass = classes.pop(0)
        append = True
        for cl in classes:
            if cl == currentClass or cl in currentClass.allSubclasses:
                append = False
                break
        if append:
            for cl in result:
                if cl == currentClass or cl in currentClass.allSubclasses:
                    append = False
                    break
        if append:
            result.append(currentClass)
    return result

def getCommonMetaclasses(classes):
    commonMetaclasses = None
    for c in classes:
        if c == None or not isCClass(c):
            raise CException(f"not a class: '{c!s}'")
        if commonMetaclasses == None:
            commonMetaclasses = [c.metaclass] + c.classObject.classPath
        else:
            updatedCommonMetaclasses = []
            metaclasses = [c.metaclass] + c.classObject.classPath
            for cmc in commonMetaclasses:
                for mc in metaclasses:
                    if cmc == mc:
                        updatedCommonMetaclasses.append(cmc)
            if len(updatedCommonMetaclasses) == 0:
                break
            commonMetaclasses = updatedCommonMetaclasses
    if commonMetaclasses == None:
        return [None]
    if len(commonMetaclasses) == 0:
        raise CException(f"class '{c!s}' has an incompatible classifier")
    # if some superclasses and their subclasses are in the list, take only the subclasses 
    # and remove duplicates form the list
    commonMetaclasses = _removeSuperclassesAndDuplicates(commonMetaclasses)
    return commonMetaclasses

def getLinkObjects(objList):
    result = []
    for o in objList:
        obj = o
        if not isCObject(o):
            if isCClass(o):
                obj = o.classObject
            else:
                raise CException(f"'{o!s}' is not an object")
        result.extend(obj.linkObjects)
    return result