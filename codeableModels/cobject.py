from codeableModels.cbundlable import CBundlable
from codeableModels.cmetaclass import CMetaclass
from codeableModels.cexception import CException
from codeableModels.clink import CLink, LinkKeywordsContext, addLinks, deleteLinks
from codeableModels.internal.commons import (checkIsCClass, isCClass, setKeywordArgs, isCMetaclass, 
    checkNamedElementIsNotDeleted, getCommonClassifier, checkIsCommonClassifier, checkIsCAssociation,
    checkIsCClassifier, getCommonMetaclass)

class CObject(CBundlable):
    def __init__(self, cl, name=None, **kwargs):
        self._classObjectClass = None
        if '_classObjectClass' in kwargs:
            classObjectClass = kwargs.pop('_classObjectClass', None)
            self._classObjectClass = classObjectClass
        else:
            # don't check if this is a class object, as classifier is then a metaclass 
           checkIsCClass(cl)
        if cl != None:
            checkNamedElementIsNotDeleted(cl)
        super().__init__(name, **kwargs)
        self._classifier = cl
        if self._classObjectClass == None:
            # don't add instance if this is a class object 
            self._classifier._addObject(self)
        self._initAttributeValues()
        self._linkObjects = []

    def _initAttributeValues(self):
        self._attributeValues = {}
        # init default values of attributes
        for cl in self.classPath:
            for attrName, attr in cl._attributes.items():
                if attr.default != None:
                    self.setValue(attrName, attr.default, cl)

    @property
    def classifier(self):
        return self._classifier

    @classifier.setter
    def classifier(self, cl):
        checkIsCClass(cl)
        if (self._classifier != None):
             self._classifier._removeObject(self)
        if cl != None:
            checkNamedElementIsNotDeleted(cl)
        self._classifier = cl
        self._classifier._addObject(self)

    def _getClassPath(self, classifier = None):
        if classifier == None:
            classifier = self.classifier
        classPath = [classifier]
        for sc in classifier.superclasses:
            for cl in self._getClassPath(sc):
                if not cl in classPath:
                    classPath.append(cl)
        return classPath

    @property
    def classPath(self):
        return self._getClassPath()

    def delete(self):
        if self._isDeleted == True:
            return
        if not isinstance(self.classifier, CMetaclass):
            # for class objects, the class cleanup removes the instance
            self._classifier._removeObject(self)
        self._classifier = None
        super().delete()

    def instanceOf(self, cl):
        if self.classifier == None:
            return False
        if cl == None:
            raise CException(f"'None' is not a valid argument")
        if isinstance(self.classifier, CMetaclass):
            # this is a class object
            if not isCMetaclass(cl):
                raise CException(f"'{cl!s}' is not a metaclass")
        else:
            if not isCClass(cl):
                raise CException(f"'{cl!s}' is not a class")

        if self.classifier == cl:
            return True
        if cl in self.classifier.allSuperclasses:
            return True
        return False
        
    def _checkIsAttributeOfOwnClassifier(self, attributeName, classifier):
        attribute = classifier.getAttribute(attributeName)
        if attribute == None:
            raise CException(f"attribute '{attributeName!s}' unknown for '{classifier!s}'")
        if not classifier in self.classPath:
            raise CException(f"'{classifier!s}' is not a classifier of '{self!s}'")
        return attribute

    def getValue(self, attributeName, classifier = None):
        if self._isDeleted:
            raise CException(f"can't get value '{attributeName!s}' on deleted object")
        if classifier == None:
            # search on class path
            for cl in self.classPath:
                if cl.getAttribute(attributeName) != None:
                    return self.getValue(attributeName, cl)
            raise CException(f"attribute '{attributeName!s}' unknown for object '{self!s}'")
        else:
            # search only on specified classifier
            attribute = self._checkIsAttributeOfOwnClassifier(attributeName, classifier)
            attribute.checkAttributeTypeIsNotDeleted()
            try:
                attributeValuesClassifier = self._attributeValues[classifier]
            except KeyError:
                return None
            try:
                return attributeValuesClassifier[attributeName]
            except KeyError:
                return None

    def setValue(self, attributeName, value, classifier = None):
        if self._isDeleted:
            raise CException(f"can't set value '{attributeName!s}' on deleted object")
        if classifier == None:
            # search on class path
            for cl in self.classPath:
                if cl.getAttribute(attributeName) != None:
                    return self.setValue(attributeName, value, cl)
            raise CException(f"attribute '{attributeName!s}' unknown for object '{self!s}'")
        else:
            # search only on specified classifier
            attribute = self._checkIsAttributeOfOwnClassifier(attributeName, classifier)
            attribute.checkAttributeTypeIsNotDeleted()
            attribute.checkAttributeValueType(attributeName, value)
            try:
                self._attributeValues[classifier].update({attributeName: value})
            except KeyError:
                self._attributeValues[classifier] = {attributeName: value}

    def _removeValue(self, attributeName, classifier):
        try:
            self._attributeValues[classifier].pop(attributeName, None)
        except KeyError:
            return

    @property
    def linkObjects(self):
        return list(self._linkObjects)

    @property
    def links(self):
        result = []
        for link in self._linkObjects:
            if self._classObjectClass != None:
                result.append(link._getOppositeObject(self)._classObjectClass)
            else:   
                result.append(link._getOppositeObject(self))
        return result

    def _getLinksForAssociation(self, association):
        associationLinks = []
        for link in list(self._linkObjects):
            if link.association == association:
                associationLinks.extend([link])
        return associationLinks
        
    def _removeLinksForAssociations(self, association, matchesinAssociationsDirection, targets):
        for link in self._getLinksForAssociation(association):
            link.delete()
        for t in targets:
            for link in t._getLinksForAssociation(association):
                link.delete()

    def getLinks(self, **kwargs):
        context = LinkKeywordsContext(**kwargs)

        linkedObjs = []
        for l in self._linkObjects:
            append = True
            if context.association != None:
                if l.association != context.association:
                    append = False
            if context.roleName != None:
                if ((self == l._source and not l.association.roleName == context.roleName) or
                    (self == l._target and not l.association.sourceRoleName == context.roleName)):
                    append = False
            if append:
                if self == l._source:
                    if self._classObjectClass != None:
                        linkedObjs.append(l._target._classObjectClass)
                    else:   
                        linkedObjs.append(l._target)
                else:
                    if self._classObjectClass != None:
                        linkedObjs.append(l._source._classObjectClass)
                    else: 
                        linkedObjs.append(l._source)
        return linkedObjs

    def addLinks(self, links, **kwargs):
        return addLinks({self: links}, **kwargs)

    def deleteLinks(self, links, **kwargs):
        return deleteLinks({self: links}, **kwargs)

    def _computeConnected(self, context):
        super()._computeConnected(context)
        connected = []
        for link in self._linkObjects:
            opposite = link._getOppositeObject(self)
            if not opposite in context.stopElementsExclusive:
                connected.append(opposite)
        self._appendConnected(context, connected)

