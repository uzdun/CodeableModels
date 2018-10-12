from codeableModels.internal.commons import setKeywordArgs, isCObject, isCClass, getCommonMetaclass, getCommonClassifier, checkIsCAssociation, checkIsCObject
from codeableModels.cexception import CException
from codeableModels.internal.taggedvalues import CTaggedValues
from codeableModels.internal.stereotype_holders import CStereotypeInstancesHolder

class CLink(object):
    def __init__(self, association, sourceObject, targetObject, **kwargs):
        self._isDeleted = False
        self._source = sourceObject
        self._target = targetObject
        self.association = association
        self._stereotypeInstancesHolder = CStereotypeInstancesHolder(self)
        self._taggedValues = CTaggedValues()
        super().__init__()
        self._initKeywordArgs(**kwargs)

    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = [] 
        legalKeywordArgs.append("stereotypeInstances")
        setKeywordArgs(self, legalKeywordArgs, **kwargs)

    def _getOppositeObject(self, object):
        if object == self._source:
            return self._target
        else:
            return self._source

    @property
    def roleName(self):
        return self.association.roleName

    @property
    def sourceRoleName(self):
        return self.association.sourceRoleName

    @property
    def source(self):
        if self._source._classObjectClass != None:
            return self._source._classObjectClass
        return self._source

    @property
    def target(self):
        if self._target._classObjectClass != None:
            return self._target._classObjectClass
        return self._target

    def delete(self):
        if self._isDeleted == True:
            return
        self._isDeleted = True
        for si in self.stereotypeInstances:
            si._extendedInstances.remove(self)
        self._stereotypeInstancesHolder._stereotypes = []
        if self._source != self._target:
            self._target._linkObjects.remove(self)
        self._source._linkObjects.remove(self)

    @property
    def stereotypeInstances(self):
        return self._stereotypeInstancesHolder.stereotypes
    
    @stereotypeInstances.setter
    def stereotypeInstances(self, elements):
        self._stereotypeInstancesHolder.stereotypes = elements

    def getTaggedValue(self, name, stereotype = None):
       return self._taggedValues.getTaggedValue(name, self._stereotypeInstancesHolder.getStereotypeInstancePath(), stereotype)

    def setTaggedValue(self, name, value, stereotype = None):
        self._taggedValues.setTaggedValue(name, value, self._stereotypeInstancesHolder.getStereotypeInstancePath(), stereotype)

    def _removeTaggedValue(self, attributeName, stereotype):
        self._taggedValues.removeTaggedValue(attributeName, stereotype)

    @property
    def taggedValues(self):
        return self._taggedValues.getTaggedValuesDict(self._stereotypeInstancesHolder.getStereotypeInstancePath())

    @taggedValues.setter
    def taggedValues(self, valuesDict):
        self._taggedValues.setTaggedValuesDict(valuesDict, self._stereotypeInstancesHolder.getStereotypeInstancePath())


def _getTargetObjectsFromDefinition(targets, isClassLinks):
    if targets == None:
        targets = []
    elif not isinstance(targets, list):
        targets = [targets]
    newTargets = []
    for t in targets:
        if isCClass(t):
            if not isClassLinks:
                raise CException(f"link target '{t!s}' is a class, but source is an object")
            newTargets.append(t._classObject)
        elif isCObject(t):
            if isClassLinks and t._classObjectClass == None:
                raise CException(f"link target '{t!s}' is an object, but source is an class")
            if not isClassLinks and t._classObjectClass != None:
                raise CException(f"link target '{t!s}' is an class, but source is an object")
            newTargets.append(t)
        else:
            raise CException(f"link target '{t!s}' is neither an object nor a class")
    return newTargets

def _checkLinkDefinitionAndReplaceClasses(linkDefinitions):
    if not isinstance(linkDefinitions, dict):
        raise CException("link definitions should be of the form {<link source 1>: <link target(s) 1>, ..., <link source n>: <link target(s) n>}")

    newDefs = {}
    for source in linkDefinitions:
        sourceObj = source
        if source == None or source == []:
            raise CException("link should not contain an empty source")
        if isCClass(source):
            sourceObj = source._classObject
        elif not isCObject(source):
            raise CException(f"link source '{source!s}' is neither an object nor a class")
        targets = _getTargetObjectsFromDefinition(linkDefinitions[source], sourceObj._classObjectClass != None)
        newDefs[sourceObj] = targets

    return newDefs

def _determineMatchingAssociationAndSetContextInfo(context, source, targets):
    if source._classObjectClass != None:
        context.targetClassifier = getCommonMetaclass([co._classObjectClass for co in targets])
        context.sourceClassifier = source._classObjectClass.metaclass
    else:
        context.targetClassifier = getCommonClassifier(targets)
        context.sourceClassifier = source.classifier    

    if context.association != None and context.targetClassifier == None:
        if context.sourceClassifier.conformsToType(context.association.source):
            context.targetClassifier = context.association.target
            context.sourceClassifier = context.association.source
        elif context.sourceClassifier.conformsToType(context.association.target):
            context.targetClassifier = context.association.source
            context.sourceClassifier = context.association.target

    associations = context.sourceClassifier.allAssociations
    if context.association != None:
        associations = [context.association]
    matchesAssociationOrder = []
    matchesReverseAssociationOrder = []
    for association in associations:
        if (association._matchesTarget(context.targetClassifier, context.roleName) and 
            association._matchesSource(context.sourceClassifier, None)):
            matchesAssociationOrder.append(association)
        elif (association._matchesSource(context.targetClassifier, context.roleName) and
            association._matchesTarget(context.sourceClassifier, None)):
            matchesReverseAssociationOrder.append(association)
    matches = len(matchesAssociationOrder) + len(matchesReverseAssociationOrder)
    if matches == 1:
        if len(matchesAssociationOrder) == 1:
            context.association = matchesAssociationOrder[0]
            context.matchesInOrder[source] = True
        else:
            context.association = matchesReverseAssociationOrder[0]
            context.matchesInOrder[source] = False
    elif matches == 0:
        raise CException(f"matching association not found for source '{source!s}' and targets '{[str(item) for item in targets]!s}'")
    else:
        raise CException(f"link specification ambiguous, multiple matching associations found for source '{source!s}' and targets '{[str(item) for item in targets]!s}'")


def _linkObjects(context, source, targets):      
    newLinks = []
    sourceObj = source
    if isCClass(source):
        sourceObj = source._classObject
    for t in targets:
        target = t
        if isCClass(t):
            target = t._classObject

        sourceForLink = sourceObj
        targetForLink = target
        if not context.matchesInOrder[sourceObj]:
            sourceForLink = target
            targetForLink = sourceObj
        for existingLink in sourceObj._linkObjects:
            if (existingLink._source == sourceForLink and existingLink._target == targetForLink 
                and existingLink.association == context.association):
                for link in newLinks:
                    link.delete()
                raise CException(f"trying to link the same link twice '{source!s} -> {target!s}'' twice for the same association")
        link = CLink(context.association, sourceForLink, targetForLink)

        newLinks.append(link)
        sourceObj._linkObjects.append(link)
        # for links from this object to itself, store only one link object
        if sourceObj != target:
            target._linkObjects.append(link)
        if context.stereotypeInstances != None:
            link.stereotypeInstances = context.stereotypeInstances
    return newLinks

def _removeLinksForAssociations(context, source, targets):
    if not source in context.objectLinksHaveBeenRemoved:
        context.objectLinksHaveBeenRemoved.append(source)
        for link in source._getLinksForAssociation(context.association):
            link.delete()
    for target in targets:
        if not target in context.objectLinksHaveBeenRemoved:
            context.objectLinksHaveBeenRemoved.append(target)
            for link in target._getLinksForAssociation(context.association):
                link.delete()


def setLinks(linkDefinitions, addLinks = False, **kwargs):
    context = LinkKeywordsContext(**kwargs)
    linkDefinitions = _checkLinkDefinitionAndReplaceClasses(linkDefinitions)

    newLinks = []
    for source in linkDefinitions:
        targets = linkDefinitions[source]
        _determineMatchingAssociationAndSetContextInfo(context, source, targets)
        if not addLinks:
            _removeLinksForAssociations(context, source, targets)
        try:
            newLinks.extend(_linkObjects(context, source, targets))
        except CException as e:
            for link in newLinks:
                link.delete()
            raise e
    try:
        for source in linkDefinitions:
            targets = linkDefinitions[source]
            sourceLen = len(source._getLinksForAssociation(context.association))
            if len(targets) == 0:
                context.association._checkMultiplicity(source, sourceLen, 0, context.matchesInOrder[source])
            else:
                for target in targets:
                    targetLen = len(target._getLinksForAssociation(context.association))
                    context.association._checkMultiplicity(source, sourceLen, targetLen, context.matchesInOrder[source])
                    context.association._checkMultiplicity(target, targetLen, sourceLen, not context.matchesInOrder[source])
    except CException as e:
        for link in newLinks:
            link.delete()
        raise e
    return newLinks

def addLinks(linkDefinitions, **kwargs):
    return setLinks(linkDefinitions, True, **kwargs)

def deleteLinks(linkDefinitions, **kwargs):
    # stereotypeInstances is not supported for delete links
    if "stereotypeInstances" in kwargs:
        raise CException(f"unknown keywords argument")

    context = LinkKeywordsContext(**kwargs)
    linkDefinitions = _checkLinkDefinitionAndReplaceClasses(linkDefinitions)

    for source in linkDefinitions:
        targets = linkDefinitions[source]
        #_determineMatchingAssociationAndSetContextInfo(context, source, targets)

        for target in targets:
            matchingLink = None
            for link in source._linkObjects:
                if context.association != None and link.association != context.association:
                    continue
                # if ((context.matchesInOrder[source] and source == link._source and target == link._target) or 
                #     (not context.matchesInOrder[source] and target == link._source and source == link._target)):
                matchesInOrder = True
                matches = False
                if (source == link._source and target == link._target):
                    matches = True
                    if context.roleName != None and not link.association.roleName == context.roleName:
                        matches = False
                if (target == link._source and source == link._target):
                    matches = True
                    matchesInOrder = False
                    if context.roleName != None and not link.association.sourceRoleName == context.roleName:
                        matches = False
                if matches:
                    if matchingLink == None:      
                        matchingLink = link
                    else:
                        raise CException(f"link definition in delete links ambiguous for link '{source!s}->{target!s}': found multiple matches")
            if matchingLink == None:
                roleNameString = ""
                if context.roleName != None:
                    roleNameString = f" for given role name '{context.roleName!s}'"
                associationString = ""
                if context.association != None:
                    associationString = f" for given association"
                    if roleNameString != "":
                        associationString = " and" + associationString
                raise CException(f"no link found for '{source!s} -> {target!s}' in delete links" + roleNameString + associationString)
            else:
                sourceLen = len(source._getLinksForAssociation(matchingLink.association)) - 1
                targetLen = len(target._getLinksForAssociation(matchingLink.association)) - 1
                matchingLink.association._checkMultiplicity(source, sourceLen, targetLen, matchesInOrder)
                matchingLink.association._checkMultiplicity(target, targetLen, sourceLen, not matchesInOrder)  
                matchingLink.delete()


class LinkKeywordsContext(object):
    def __init__(self, **kwargs):
        self.roleName = kwargs.pop("roleName", None)
        self.association = kwargs.pop("association", None)
        self.stereotypeInstances = kwargs.pop("stereotypeInstances", None)
        if len(kwargs) != 0:
            raise CException(f"unknown keywords argument")
        if self.association != None:
            checkIsCAssociation(self.association)
        self.sourceClassifier = None
        self.targetClassifier = None
        self.matchesInOrder = {}
        self.objectLinksHaveBeenRemoved = []
