from codeable_models.internal.commons import *
from codeable_models.cexception import CException
from codeable_models.cenum import CEnum

class CAttribute(object):
    def __init__(self, **kwargs):
        self._name = None
        self._classifier = None
        self._type = None
        self._default = None
        setKeywordArgs(self, ["type", "default"], **kwargs)
    
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return f"CAttribute type = {self._type!s}, default = {self._default!s}"

    def checkAttributeTypeIsNotDeleted(self):
        if isCNamedElement(self._type):
            checkNamedElementIsNotDeleted(self._type)

    @property
    def name(self):
        return self._name

    @property
    def classifier(self):
        return self._classifier

    @property
    def type(self):
        self.checkAttributeTypeIsNotDeleted()
        return self._type

    def __wrongDefaultException(self, default, type):
        raise CException(f"default value '{default!s}' incompatible with attribute's type '{type!s}'")

    @type.setter
    def type(self, type):
        if isCNamedElement(type):
            checkNamedElementIsNotDeleted(type)
        if self._default != None:
            if isCEnum(type):
                if not self._default in type.values:
                    self.__wrongDefaultException(self._default, type)
            elif isCClassifier(type):
                if (not self._default == type) and (not type in type.allSuperclasses):
                    self.__wrongDefaultException(self._default, type)
            else:
                if not isinstance(self._default, type):
                    self.__wrongDefaultException(self._default, type)
        self._type = type

    @property
    def default(self):
        self.checkAttributeTypeIsNotDeleted()
        return self._default
    
    @default.setter
    def default(self, default):
        if default == None:
            self._default = None
            return

        self.checkAttributeTypeIsNotDeleted()
        if self._type != None:
            if isCEnum(self._type):
                if not default in self._type.values:
                    self.__wrongDefaultException(default, self._type)
            elif isCClass(self._type):
                if not default in self._type.objects:
                    self.__wrongDefaultException(default, self._type)
            elif isCMetaclass(self._type):
                if not default in self._type.classes:
                    self.__wrongDefaultException(default, self._type)
            elif not isinstance(default, self._type):
                self.__wrongDefaultException(default, self._type)
        else:
            attrType = getAttributeType(default)
            if attrType == None:
                raise CException(f"unknown attribute type: '{default!r}'")
            self.type = attrType
        self._default = default
        if self._classifier != None:
            self._classifier._updateDefaultValuesOfClassifier(self)

    def checkAttributeValueType(self, name, value):
        attrType = getAttributeType(value)
        if attrType == None:
            raise CException(f"value for attribute '{name!s}' is not a known attribute type")
        if isCClassifier(attrType):
            if attrType != self._type and (not self._type in attrType.allSuperclasses):
                raise CException(f"type of '{value!s}' is not matching type of attribute '{name!s}'")
            return
        if attrType != self._type:
            if (self.type == float and attrType == int):
                return
            if not (isCEnum(self._type) and attrType == str):
                raise CException(f"value type for attribute '{name!s}' does not match attribute type")
        if isCEnum(self._type) and attrType == str and (not self._type.isLegalValue(value)):
            raise CException(f"value '{value!s}' is not element of enumeration")
