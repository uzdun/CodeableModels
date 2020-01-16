from codeable_models.cassociation import CAssociation
from codeable_models.cclassifier import CClassifier
from codeable_models.cmetaclass import CMetaclass
from codeable_models.internal.commons import *
from codeable_models.internal.var_values import delete_var_value, set_var_value, get_var_value, get_var_values, \
    set_var_values, VarValueKind


def _determine_extended_type_of_list(elements):
    if len(elements) == 0:
        return None
    if is_cmetaclass(elements[0]):
        return CMetaclass
    if is_cassociation(elements[0]):
        return CAssociation
    raise CException(f"unknown type of extend element: '{elements[0]!s}'")


class CStereotype(CClassifier):
    def __init__(self, name=None, **kwargs):
        self.extended_ = []
        self.extended_instances_ = []
        self.default_values_ = {}
        super().__init__(name, **kwargs)

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.append("extended")
        legal_keyword_args.append("default_values")
        super()._init_keyword_args(legal_keyword_args, **kwargs)

    @property
    def extended(self):
        return list(self.extended_)

    @extended.setter
    def extended(self, elements):
        if elements is None:
            elements = []
        for e in self.extended_:
            e.stereotypes_holder.stereotypes_.remove(self)
        self.extended_ = []
        if is_cmetaclass(elements):
            extended_type = CMetaclass
            elements = [elements]
        elif is_cassociation(elements):
            extended_type = CAssociation
            elements = [elements]
        elif not isinstance(elements, list):
            raise CException(f"extended requires a list or a metaclass as input")
        else:
            extended_type = _determine_extended_type_of_list(elements)

        for e in elements:
            if extended_type == CMetaclass:
                check_is_cmetaclass(e)
            elif extended_type == CAssociation:
                check_is_cassociation(e)
            else:
                raise CException(f"type of extend element incompatible: '{e!s}'")
            check_named_element_is_not_deleted(e)
            if e in self.extended_:
                raise CException(f"'{e.name!s}' is already extended by stereotype '{self.name!s}'")
            self.extended_.append(e)
            e.stereotypes_holder.stereotypes_.append(self)

    @property
    def extended_instances(self):
        return list(self.extended_instances_)

    @property
    def all_extended_instances(self):
        all_instances = list(self.extended_instances_)
        for scl in self.all_subclasses:
            for cl in scl.extended_instances_:
                all_instances.append(cl)
        return all_instances

    def delete(self):
        if self.is_deleted:
            return
        for e in self.extended_:
            e.stereotypes_holder.stereotypes_.remove(self)
        self.extended_ = []
        super().delete()

    def update_default_values_of_classifier(self, attribute=None):
        all_classes = [self] + list(self.all_subclasses)
        for sc in all_classes:
            for i in sc.extended_instances_:
                attr_items = self.attributes_.items()
                if attribute is not None:
                    attr_items = {attribute.name_: attribute}.items()
                for attrName, attr in attr_items:
                    if attr.default is not None:
                        if i.get_tagged_value(attrName, self) is None:
                            i.set_tagged_value(attrName, attr.default, self)

    def _remove_attribute_values_of_classifier(self, attributes_to_keep):
        for i in self.extended_instances_:
            for attrName in self.attribute_names:
                if attrName not in attributes_to_keep:
                    i.delete_tagged_value(attrName, self)

    def is_metaclass_extended_by_this_stereotype(self, metaclass):
        if metaclass in self.extended_:
            return True
        for mcSuperclass in metaclass.get_all_superclasses():
            if mcSuperclass in self.extended_:
                return True
        return False

    def is_element_extended_by_stereotype(self, element):
        if is_cclass(element):
            if self.is_metaclass_extended_by_this_stereotype(element.metaclass):
                return True
            for superclass in self.get_all_superclasses():
                if superclass.is_metaclass_extended_by_this_stereotype(element.metaclass):
                    return True
            return False
        elif is_clink(element):
            if element.association in self.extended:
                return True
            for superclass in self.get_all_superclasses():
                if element.association in superclass.extended:
                    return True
            return False
        raise CException("element is neither a metaclass nor an association")

    def association(self, target, descriptor=None, **kwargs):
        if not isinstance(target, CStereotype):
            raise CException(f"stereotype '{self!s}' is not compatible with association target '{target!s}'")
        return super(CStereotype, self).association(target, descriptor, **kwargs)

    def compute_connected(self, context):
        super().compute_connected(context)
        if not context.process_stereotypes:
            return
        connected = []
        for e in self.extended:
            if e not in context.stop_elements_exclusive:
                connected.append(e)
        self.append_connected(context, connected)

    def _get_all_extended_elements(self):
        result = []
        for cl in self.class_path:
            for extendedElement in cl.extended:
                if extendedElement not in result:
                    result.append(extendedElement)
        return result

    def _get_default_value_class_path(self):
        result = []
        for extendedElement in self._get_all_extended_elements():
            if not is_cmetaclass(extendedElement):
                raise CException(f"default values can only be used on a stereotype that extends metaclasses")
            for mcl in extendedElement.class_path:
                if mcl not in result:
                    result.append(mcl)
        return result

    @property
    def default_values(self):
        if self.is_deleted:
            raise CException(f"can't get default values on deleted stereotype")
        class_path = self._get_default_value_class_path()
        return get_var_values(class_path, self.default_values_)

    @default_values.setter
    def default_values(self, new_values):
        if self.is_deleted:
            raise CException(f"can't set default values on deleted stereotype")
        class_path = self._get_default_value_class_path()
        if len(class_path) == 0:
            raise CException(f"default values can only be used on a stereotype that extends metaclasses")
        set_var_values(self, new_values, VarValueKind.DEFAULT_VALUE)

    def get_default_value(self, attribute_name, classifier=None):
        if self.is_deleted:
            raise CException(f"can't get default value '{attribute_name!s}' on deleted stereotype")
        class_path = self._get_default_value_class_path()
        if len(class_path) == 0:
            raise CException(f"default values can only be used on a stereotype that extends metaclasses")
        return get_var_value(self, class_path, self.default_values_, attribute_name, VarValueKind.DEFAULT_VALUE,
                             classifier)

    def delete_default_value(self, attribute_name, classifier=None):
        if self.is_deleted:
            raise CException(f"can't delete default value '{attribute_name!s}' on deleted stereotype")
        class_path = self._get_default_value_class_path()
        if len(class_path) == 0:
            raise CException(f"default values can only be used on a stereotype that extends metaclasses")
        return delete_var_value(self, class_path, self.default_values_, attribute_name, VarValueKind.DEFAULT_VALUE,
                                classifier)

    def set_default_value(self, attribute_name, value, classifier=None):
        if self.is_deleted:
            raise CException(f"can't set default value '{attribute_name!s}' on deleted stereotype")
        class_path = self._get_default_value_class_path()
        if len(class_path) == 0:
            raise CException(f"default values can only be used on a stereotype that extends metaclasses")
        set_var_value(self, class_path, self.default_values_, attribute_name, value, VarValueKind.DEFAULT_VALUE,
                      classifier)
