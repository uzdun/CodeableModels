from codeable_models.internal.commons import *


class VarValueKind:
    ATTRIBUTE_VALUE = 1
    TAGGED_VALUE = 2
    DEFAULT_VALUE = 3


def _get_var_unknown_exception(value_kind, entity, var_name):
    if value_kind == VarValueKind.TAGGED_VALUE:
        value_kind_str = "tagged value"
    elif value_kind == VarValueKind.ATTRIBUTE_VALUE or value_kind == VarValueKind.DEFAULT_VALUE:
        value_kind_str = "attribute"
    else:
        raise CException("unknown variable kind")

    if value_kind == VarValueKind.DEFAULT_VALUE:
        return CException(
            f"{value_kind_str!s} '{var_name!s}' unknown for metaclasses extended by stereotype '{entity!s}'")
    if is_clink(entity):
        return CException(f"{value_kind_str!s} '{var_name!s}' unknown")
    return CException(f"{value_kind_str!s} '{var_name!s}' unknown for '{entity!s}'")


def _get_and_check_var_classifier(_self, class_path, var_name, value_kind, classifier=None):
    if classifier is None:
        # search on a class path
        for cl in class_path:
            if cl.get_attribute(var_name) is not None:
                return _get_and_check_var_classifier(_self, class_path, var_name, value_kind, cl)
        raise _get_var_unknown_exception(value_kind, _self, var_name)
    else:
        # check only on specified classifier
        attribute = classifier.get_attribute(var_name)
        if attribute is None:
            raise _get_var_unknown_exception(value_kind, classifier, var_name)
        attribute.check_attribute_type_is_not_deleted()
        return attribute


def delete_var_value(_self, class_path, values_dict, var_name, value_kind, classifier=None):
    if _self.is_deleted:
        raise CException(f"can't delete '{var_name!s}' on deleted element")
    attribute = _get_and_check_var_classifier(_self, class_path, var_name, value_kind, classifier)
    try:
        values_of_classifier = values_dict[attribute.classifier]
    except KeyError:
        return None
    try:
        value = values_of_classifier[var_name]
        del values_of_classifier[var_name]
        return value
    except KeyError:
        return None


def set_var_value(_self, class_path, values_dict, var_name, value, value_kind, classifier=None):
    if _self.is_deleted:
        raise CException(f"can't set '{var_name!s}' on deleted element")
    attribute = _get_and_check_var_classifier(_self, class_path, var_name, value_kind, classifier)
    attribute.check_attribute_value_type_(var_name, value)
    try:
        values_dict[attribute.classifier].update({var_name: value})
    except KeyError:
        values_dict[attribute.classifier] = {var_name: value}


def get_var_value(_self, class_path, values_dict, var_name, value_kind, classifier=None):
    if _self.is_deleted:
        raise CException(f"can't get '{var_name!s}' on deleted element")
    attribute = _get_and_check_var_classifier(_self, class_path, var_name, value_kind, classifier)
    try:
        values_of_classifier = values_dict[attribute.classifier]
    except KeyError:
        return None
    try:
        return values_of_classifier[var_name]
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
        if values_kind == VarValueKind.TAGGED_VALUE:
            value_kind_str = "tagged values"
        elif values_kind == VarValueKind.ATTRIBUTE_VALUE:
            value_kind_str = "attribute values"
        elif values_kind == VarValueKind.DEFAULT_VALUE:
            value_kind_str = "default values"
        else:
            raise CException("unknown variable kind")
        raise CException(f"malformed {value_kind_str!s} description: '{new_values!s}'")
    for valueName in new_values:
        if values_kind == VarValueKind.ATTRIBUTE_VALUE:
            _self.set_value(valueName, new_values[valueName])
        elif values_kind == VarValueKind.TAGGED_VALUE:
            _self.set_tagged_value(valueName, new_values[valueName])
        elif values_kind == VarValueKind.DEFAULT_VALUE:
            _self.set_default_value(valueName, new_values[valueName])
        else:
            raise CException("unknown variable kind")
