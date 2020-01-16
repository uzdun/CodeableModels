from codeable_models.internal.commons import *


class ValueKind:
    ATTRIBUTE_VALUE = 1
    TAGGED_VALUE = 2
    DEFAULT_VALUE = 3


def _get_attribute_unknown_exception(value_kind, entity, attribute_name):
    if value_kind == ValueKind.TAGGED_VALUE:
        value_kind_str = "tagged value"
    elif value_kind == ValueKind.ATTRIBUTE_VALUE or value_kind == ValueKind.DEFAULT_VALUE:
        value_kind_str = "attribute"
    else:
        raise CException("unknown attribute kind")

    if value_kind == ValueKind.DEFAULT_VALUE:
        return CException(
            f"{value_kind_str!s} '{attribute_name!s}' unknown for metaclasses extended by stereotype '{entity!s}'")
    if is_clink(entity):
        return CException(f"{value_kind_str!s} '{attribute_name!s}' unknown")
    return CException(f"{value_kind_str!s} '{attribute_name!s}' unknown for '{entity!s}'")


def _get_and_check_attribute_classifier(_self, class_path, attribute_name, value_kind, classifier=None):
    if classifier is None:
        # search on a class path
        for cl in class_path:
            if cl.getAttribute(attribute_name) is not None:
                return _get_and_check_attribute_classifier(_self, class_path, attribute_name, value_kind, cl)
        raise _get_attribute_unknown_exception(value_kind, _self, attribute_name)
    else:
        # check only on specified classifier
        attribute = classifier.getAttribute(attribute_name)
        if attribute is None:
            raise _get_attribute_unknown_exception(value_kind, classifier, attribute_name)
        attribute.check_attribute_type_is_not_deleted()
        return attribute


def delete_var_value(_self, class_path, values_dict, attribute_name, value_kind, classifier=None):
    if _self.is_deleted:
        raise CException(f"can't delete '{attribute_name!s}' on deleted element")
    attribute = _get_and_check_attribute_classifier(_self, class_path, attribute_name, value_kind, classifier)
    try:
        values_of_classifier = values_dict[attribute.classifier]
    except KeyError:
        return None
    try:
        value = values_of_classifier[attribute_name]
        del values_of_classifier[attribute_name]
        return value
    except KeyError:
        return None


def set_var_value(_self, class_path, values_dict, attribute_name, value, value_kind, classifier=None):
    if _self.is_deleted:
        raise CException(f"can't set '{attribute_name!s}' on deleted element")
    attribute = _get_and_check_attribute_classifier(_self, class_path, attribute_name, value_kind, classifier)
    attribute.check_attribute_value_type(attribute_name, value)
    try:
        values_dict[attribute.classifier].update({attribute_name: value})
    except KeyError:
        values_dict[attribute.classifier] = {attribute_name: value}


def get_var_value(_self, class_path, values_dict, attribute_name, value_kind, classifier=None):
    if _self.is_deleted:
        raise CException(f"can't get '{attribute_name!s}' on deleted element")
    attribute = _get_and_check_attribute_classifier(_self, class_path, attribute_name, value_kind, classifier)
    try:
        values_of_classifier = values_dict[attribute.classifier]
    except KeyError:
        return None
    try:
        return values_of_classifier[attribute_name]
    except KeyError:
        return None


def get_var_values(class_path, values_dict):
    result = {}
    for cl in class_path:
        if cl in values_dict:
            for attrName in values_dict[cl]:
                if attrName not in result:
                    result[attrName] = values_dict[cl][attrName]
    return result


def set_var_values(_self, new_values, values_kind):
    if new_values is None:
        new_values = {}
    if not isinstance(new_values, dict):
        if values_kind == ValueKind.TAGGED_VALUE:
            value_kind_str = "tagged values"
        elif values_kind == ValueKind.ATTRIBUTE_VALUE:
            value_kind_str = "attribute values"
        elif values_kind == ValueKind.DEFAULT_VALUE:
            value_kind_str = "default values"
        else:
            raise CException("unknown attribute kind")
        raise CException(f"malformed {value_kind_str!s} description: '{new_values!s}'")
    for valueName in new_values:
        if values_kind == ValueKind.ATTRIBUTE_VALUE:
            _self.setValue(valueName, new_values[valueName])
        elif values_kind == ValueKind.TAGGED_VALUE:
            _self.setTaggedValue(valueName, new_values[valueName])
        elif values_kind == ValueKind.DEFAULT_VALUE:
            _self.setDefaultValue(valueName, new_values[valueName])
        else:
            raise CException("unknown attribute kind")
