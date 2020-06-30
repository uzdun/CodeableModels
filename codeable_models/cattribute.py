from codeable_models.internal.commons import *


class CAttribute(object):
    def __init__(self, **kwargs):
        """``CAttribute`` is internally used for storing attributes, and can be used by the user for
        detailed setting or introspection of attribute data.

        The ``attributes`` getter of :py:class:`.CClassifier` returns ``CAttribute`` objects.
        They can be used as an alternative method in
        the ``attributes`` setter of :py:class:`.CClassifier` to define attributes of a classifier.

        Args:
           **kwargs: ``CAttribute`` accepts: ``type``, ``default``.

                - The ``type`` kwarg accepts a type argument in the form acceptable to the ``type`` property.
                - The ``default`` kwarg accepts a default value in the form acceptable to the ``default`` property.

        """
        self.name_ = None
        self.classifier_ = None
        self.type_ = None
        self.default_ = None
        set_keyword_args(self, ["type", "default"], **kwargs)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"CAttribute type = {self.type_!s}, default = {self.default_!s}"

    def check_attribute_type_is_not_deleted(self):
        if is_cnamedelement(self.type_):
            check_named_element_is_not_deleted(self.type_)

    @property
    def name(self):
        """str: Property used to get the name of the attribute.

        Will be set automatically if the attribute is created on a classifier.
        """
        return self.name_

    @property
    def classifier(self):
        """:py:class:`.CClassifier`: Property used to get the classifier of the attribute.

        The attribute classifier is set automatically when the attribute is created on a classifier.
        """
        return self.classifier_

    @property
    def type(self):
        """supported_type: Property used to set or get the type of the attribute.

        If a default value is set before the type, an exception will be raised if the new type does
        not match the default value.

        Supported types of attributes are documented in the documentation of the ``attributes`` property
        of :py:class:`.CClassifier`.
        """
        self.check_attribute_type_is_not_deleted()
        return self.type_

    def _wrong_default_exception(self, default, attribute_type):
        raise CException(f"default value '{default!s}' incompatible with attribute's type '{attribute_type!s}'")

    @type.setter
    def type(self, new_type):
        if is_cnamedelement(new_type):
            check_named_element_is_not_deleted(new_type)
        if self.default_ is not None:
            if is_cenum(new_type):
                if self.default_ not in new_type.values:
                    self._wrong_default_exception(self.default_, new_type)
            elif is_cclassifier(new_type):
                if (not self.default_ == new_type) and (new_type not in new_type.all_superclasses):
                    self._wrong_default_exception(self.default_, new_type)
            else:
                if not isinstance(self.default_, new_type):
                    self._wrong_default_exception(self.default_, new_type)
        self.type_ = new_type

    @property
    def default(self):
        """default_value: Property used to set or get the default value of the attribute.

        If an attribute type is set before the default value, the default value must conform to the type.
        Else the type is guessed from the provided default value.
        """
        self.check_attribute_type_is_not_deleted()
        return self.default_

    @default.setter
    def default(self, default):
        if default is None:
            self.default_ = None
            return

        self.check_attribute_type_is_not_deleted()
        if self.type_ is not None:
            if is_cenum(self.type_):
                if default not in self.type_.values:
                    self._wrong_default_exception(default, self.type_)
            elif is_cclass(self.type_):
                if default not in self.type_.objects:
                    self._wrong_default_exception(default, self.type_)
            elif is_cmetaclass(self.type_):
                if default not in self.type_.classes:
                    self._wrong_default_exception(default, self.type_)
            elif not isinstance(default, self.type_):
                self._wrong_default_exception(default, self.type_)
        else:
            attr_type = get_attribute_type(default)
            if attr_type is None:
                raise CException(f"unknown attribute type: '{default!r}'")
            self.type = attr_type
        self.default_ = default
        if self.classifier_ is not None:
            self.classifier_.update_default_values_of_classifier_(self)

    def check_attribute_value_type_(self, name, value):
        attr_type = get_attribute_type(value)
        if attr_type is None:
            raise CException(f"value for attribute '{name!s}' is not a known attribute type")
        if is_cclassifier(attr_type):
            if attr_type != self.type_ and (self.type_ not in attr_type.all_superclasses):
                raise CException(f"type of '{value!s}' is not matching type of attribute '{name!s}'")
            return
        if attr_type != self.type_:
            if self.type == float and attr_type == int:
                return
            if not (is_cenum(self.type_) and attr_type == str):
                raise CException(f"value type for attribute '{name!s}' does not match attribute type")
        if is_cenum(self.type_) and attr_type == str and (not self.type_.is_legal_value(value)):
            raise CException(f"value '{value!s}' is not element of enumeration")
