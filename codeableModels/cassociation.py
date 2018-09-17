from codeableModels.internal.commons import setKeywordArgs, isCClassifier, isCMetaclass, isCStereotype
from codeableModels.cexception import CException
from codeableModels.cnamedelement import CNamedElement
from codeableModels.internal.stereotype_holders import CStereotypesHolder
import re

class CAssociation(CNamedElement):
    STAR_MULTIPLICITY = -1

    def __init__(self, source, target, descriptor = None, **kwargs):
        self.source = source
        self.target = target
        self.roleName = None
        self.sourceRoleName = None
        self._sourceMultiplicityString = "1"
        self._sourceLowerMultiplicity = 1
        self._sourceUpperMultiplicity = 1
        self._multiplicityString = "*"
        self._lowerMultiplicity = 0
        self._upperMultiplicity = self.STAR_MULTIPLICITY
        self._aggregation = False
        self._composition = False
        self._stereotypesHolder = CStereotypesHolder(self)
        name = kwargs.pop("name", None)
        self.ends = None
        super().__init__(name, **kwargs)
        if descriptor != None:
            self._evalDescriptor(descriptor)
    
    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = []
        legalKeywordArgs.extend(["multiplicity", "roleName", "sourceMultiplicity", 
            "sourceRoleName", "aggregation", "composition", "stereotypes"])
        super()._initKeywordArgs(legalKeywordArgs, **kwargs)

    def __str__(self):
        return super(CAssociation, self).__str__()
    def __repr__(self):
        name = ""
        if self.name != None:
            name = self.name
        return f"CAssociation name = {name!s}, source = {self.source!s} -> target = {self.target!s}"
    
    def _getOppositeClass(self, cl):
        if cl == self.source:
            return self.target
        else:
            return self.source

    def _matches(self, classifier, roleName, associationClassifier, associationRoleName):
        if classifier == None and roleName == None:
            return False
        matches = True
        if roleName != None:
            if roleName != associationRoleName:
                matches = False
        if matches and classifier != None:
            if not classifier.conformsToType(associationClassifier):
                matches = False
        if matches:
            return True
        return False

    def _matchesTarget(self, classifier, roleName):
        return self._matches(classifier, roleName, self.target, self.roleName)

    def _matchesSource(self, classifier, roleName):
        return self._matches(classifier, roleName, self.source, self.sourceRoleName)

    @property
    def aggregation(self):
        return self._aggregation
    @aggregation.setter
    def aggregation(self, aggregation):
        if aggregation:
            self._composition = False
        self._aggregation = aggregation

    def _setMultiplicity(self, multiplicity, isTargetMultiplicity):
        if not isinstance(multiplicity, str):
            raise CException("multiplicity must be provided as a string")
        lower = -2
        upper = -2
        try:
            dotsPos = multiplicity.find("..")
            if dotsPos != -1:
                lowerMatch = multiplicity[:dotsPos]
                upperMatch = multiplicity[dotsPos+2:]
                lower = int(lowerMatch)
                if lower < 0:
                    raise CException(f"negative multiplicity in '{multiplicity!s}'")
                if upperMatch.strip() == "*":
                    upper = self.STAR_MULTIPLICITY
                else:
                    upper = int(upperMatch)
                    if lower < 0 or upper < 0:
                        raise CException(f"negative multiplicity in '{multiplicity!s}'")
            elif multiplicity.strip() == "*":
                lower = 0
                upper = self.STAR_MULTIPLICITY
            else:
                lower = int(multiplicity)
                if lower < 0:
                    raise CException(f"negative multiplicity in '{multiplicity!s}'")
                upper = lower
        except Exception as e:
            if isinstance(e, CException):
                raise e
            raise CException(f"malformed multiplicity: '{multiplicity!s}'")

        if isTargetMultiplicity:
            self._upperMultiplicity = upper
            self._lowerMultiplicity = lower
        else:
            self._sourceUpperMultiplicity = upper
            self._sourceLowerMultiplicity = lower

    @property
    def multiplicity(self):
        return self._multiplicityString
    @multiplicity.setter
    def multiplicity(self, multiplicity):
        self._multiplicityString = multiplicity
        self._setMultiplicity(multiplicity, True)

    @property
    def sourceMultiplicity(self):
        return self._sourceMultiplicityString
    @sourceMultiplicity.setter
    def sourceMultiplicity(self, multiplicity):
        self._sourceMultiplicityString = multiplicity
        self._setMultiplicity(multiplicity, False)
        
    @property
    def composition(self):
        return self._composition
    @composition.setter
    def composition(self, composition):
        if composition:
            self._aggregation = False
        self._composition = composition

    @property
    def stereotypes(self):
        return self._stereotypesHolder.stereotypes
    
    @stereotypes.setter
    def stereotypes(self, elements):
        self._stereotypesHolder.stereotypes = elements

    def delete(self):
        if self._isDeleted == True:
            return
        if isCMetaclass(self.source):
            allInstances = self.source.allClasses
        elif isCStereotype(self.source):
            allInstances = self.source.allExtendedInstances
        else:
            allInstances = self.source.allObjects
        for instance in allInstances:
            for link in instance.linkObjects:
                link.delete()
        self.source._associations.remove(self)
        if self.source != self.target:
            self.target._associations.remove(self)
        for s in self._stereotypesHolder._stereotypes:
            s._extended.remove(self)
        self._stereotypesHolder._stereotypes = []
        super().delete()
  
    def _checkMultiplicity(self, object, actualLength, actualOppositeLength, checkTargetMultiplicity):
        if checkTargetMultiplicity:
            upper = self._upperMultiplicity
            lower = self._lowerMultiplicity
            otherSideLower = self._sourceLowerMultiplicity
            multiplicityString = self._multiplicityString
        else:
            upper = self._sourceUpperMultiplicity
            lower = self._sourceLowerMultiplicity
            otherSideLower = self._lowerMultiplicity
            multiplicityString = self._sourceMultiplicityString

        if (upper != CAssociation.STAR_MULTIPLICITY and actualLength > upper) or actualLength < lower:
            # if there is actually no link as actualOppositeLength is zero, this is ok, if the otherLower including zero:
            if not (actualOppositeLength == 0 and otherSideLower == 0):
                raise CException(f"links of object '{object}' have wrong multiplicity '{actualLength!s}': should be '{multiplicityString!s}'")
        
    def _evalDescriptor(self, descriptor):
        # handle name only if a ':' is found in the descriptor
        index = descriptor.find(":")
        if index != -1:
            name = descriptor[0:index]
            descriptor = descriptor[index+1:]
            self.name = name.strip()

        # handle type of relation
        aggregation = False
        composition = False
        index = descriptor.find("->")
        length = 2
        if index == -1:
            index = descriptor.find("<>-")
            if index != -1:
                length = 3
                aggregation = True
            else:
                index = descriptor.find("<*>-")
                length = 4
                composition = True
                if index == -1:
                    raise CException("association descriptor malformed: '" + descriptor + "'")

        # handle role names and multiplicities
        sourceStr = descriptor[0:index]
        targetStr = descriptor[index+length:]
        regexpWithRoleName = '\s*\[([^\]]+)\]\s*(\S*)\s*'
        regexpOnlyMultiplicity = '\s*(\S*)\s*'

        m = re.search(regexpWithRoleName, sourceStr)
        if m != None:
            self.sourceRoleName = m.group(1)
            if m.group(2) != '':
                self.sourceMultiplicity = m.group(2)
        else:
            m = re.search(regexpOnlyMultiplicity, sourceStr)
            self.sourceMultiplicity = m.group(1)

        m = re.search(regexpWithRoleName, targetStr)
        if m != None:
            self.roleName = m.group(1)
            if m.group(2) != '':
                self.multiplicity = m.group(2)
        else:
            m = re.search(regexpOnlyMultiplicity, targetStr)
            self.multiplicity = m.group(1)
        
        if aggregation:
            self.aggregation = True
        elif composition:
            self.composition = True
