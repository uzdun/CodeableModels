from codeable_models.cattribute import CAttribute
from codeable_models.cbundlable import CBundlable
from codeable_models.cenum import CEnum
from codeable_models.internal.commons import *


class CClassifier(CBundlable):
    def __init__(self, name=None, **kwargs):
        self.superclasses_ = []
        self.subclasses_ = []
        self.attributes_ = {}
        self.associations_ = []
        super().__init__(name, **kwargs)

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.append("attributes")
        legal_keyword_args.append("superclasses")
        super()._init_keyword_args(legal_keyword_args, **kwargs)

    @property
    def attributes(self):
        return list(self.attributes_.values())

    def _set_attribute(self, name, value):
        if name in self.attributes_.keys():
            raise CException(f"duplicate attribute name: '{name!s}'")
        if is_cattribute(value):
            attr = value
        elif is_known_attribute_type(value) or isinstance(value, CEnum) or is_cclassifier(value):
            # if value is a CClass, we interpret it as the type for a CObject attribute, not the default 
            # value of a CMetaclass type attribute: if you need to set a metaclass type default value, use 
            # CAttribute's default instead
            attr = CAttribute(type=value)
        else:
            attr = CAttribute(default=value)
        attr.name_ = name
        attr.classifier_ = self
        self.attributes_.update({name: attr})

    @attributes.setter
    def attributes(self, attribute_descriptions):
        if attribute_descriptions is None:
            attribute_descriptions = {}
        self._remove_attribute_values_of_classifier(attribute_descriptions.keys())
        self.attributes_ = {}
        if not isinstance(attribute_descriptions, dict):
            raise CException(f"malformed attribute description: '{attribute_descriptions!s}'")
        for attributeName in attribute_descriptions:
            self._set_attribute(attributeName, attribute_descriptions[attributeName])
        self.update_default_values_of_classifier_()

    @property
    def attribute_names(self):
        return list(self.attributes_.keys())

    def get_attribute(self, attribute_name):
        if attribute_name is None or not isinstance(attribute_name, str):
            return None
        try:
            return self.attributes_[attribute_name]
        except KeyError:
            return None

    def _remove_attribute_values_of_classifier(self, attributes_to_keep):
        raise CException("should be overridden by subclasses to update defaults on instances")

    def update_default_values_of_classifier_(self, attribute=None):
        raise CException("should be overridden by subclasses to update defaults on instances")

    def _check_same_type_as_self(self, cl):
        return isinstance(cl, self.__class__)

    @property
    def subclasses(self):
        return list(self.subclasses_)

    @property
    def superclasses(self):
        return list(self.superclasses_)

    @superclasses.setter
    def superclasses(self, elements):
        if elements is None:
            elements = []
        for sc in self.superclasses_:
            sc.subclasses_.remove(self)
        self.superclasses_ = []
        if is_cclassifier(elements):
            elements = [elements]
        for scl in elements:
            if scl is not None:
                check_named_element_is_not_deleted(scl)
            if not isinstance(scl, self.__class__):
                if is_cassociation(self):
                    if self.is_metaclass_association():
                        if not is_cmetaclass(scl) or (is_cassociation(scl) and scl.is_metaclass_association()):
                            raise CException(f"cannot add superclass '{scl!s}':" +
                                             " not a metaclass or metaclass association")
                    else:
                        if not is_cclass(scl) or (is_cassociation(scl) and not scl.is_metaclass_association()):
                            raise CException(f"cannot add superclass '{scl!s}':" +
                                             " not a class or class association")
                else:
                    raise CException(f"cannot add superclass '{scl!s}' to '{self!s}': not of type {self.__class__!s}")
            if scl in self.superclasses_:
                raise CException(f"'{scl.name!s}' is already a superclass of '{self.name!s}'")
            self.superclasses_.append(scl)
            scl.subclasses_.append(self)

    @property
    def all_superclasses(self):
        return self.get_all_superclasses()

    @property
    def all_subclasses(self):
        return self.get_all_subclasses()

    def conforms_to_type(self, classifier):
        type_classifiers = classifier.all_subclasses
        type_classifiers.add(classifier)
        if self in type_classifiers:
            return True
        return False

    def get_all_superclasses(self, iterated_classes=None):
        if iterated_classes is None:
            iterated_classes = set()
        result = set()
        for sc in self.superclasses:
            if sc not in iterated_classes:
                iterated_classes.add(sc)
                result.add(sc)
                result.update(sc.get_all_superclasses(iterated_classes))
        return result

    def get_all_subclasses(self, iterated_classes=None):
        if iterated_classes is None:
            iterated_classes = set()
        result = set()
        for sc in self.subclasses:
            if sc not in iterated_classes:
                iterated_classes.add(sc)
                result.add(sc)
                result.update(sc.get_all_subclasses(iterated_classes))
        return result

    def has_subclass(self, cl):
        return cl in self.get_all_subclasses()

    def has_superclass(self, cl):
        return cl in self.get_all_superclasses()

    def delete(self):
        if self.is_deleted:
            return
        super().delete()

        # self.superclasses removes the self subclass from the superclasses
        self.superclasses = []

        for subclass in self.subclasses_:
            # for each cl, remove superclass cl
            if self not in subclass.superclasses_:
                raise CException(f"can't remove superclass '{self!s}' from classifier '{subclass!s}': not a superclass")
            subclass.superclasses_.remove(self)
        self.subclasses_ = []

        # remove all associations
        associations = self.associations.copy()
        for association in associations:
            association.delete()

        for a in self.attributes:
            a.name_ = None
            a.classifier_ = None
        self.attributes_ = {}

    @property
    def associations(self):
        return list(self.associations_)

    @property
    def all_associations(self):
        all_associations = self.associations
        for sc in self.all_superclasses:
            for a in sc.associations:
                if a not in all_associations:
                    all_associations.extend([a])
        return all_associations

    def association(self, target, descriptor=None, **kwargs):
        from codeable_models.cassociation import CAssociation
        a = CAssociation(self, target, descriptor, **kwargs)
        self.associations_.append(a)
        if self != target:
            target.associations_.append(a)
        return a

    def compute_connected_(self, context):
        super().compute_connected_(context)
        connected_candidates = []
        connected = []
        for association in self.associations:
            connected_candidates.append(association.get_opposite_class(self))
        connected_candidates = self.superclasses + self.subclasses + connected_candidates
        for c in connected_candidates:
            if c not in context.stop_elements_exclusive:
                connected.append(c)
        self.append_connected_(context, connected)

    # get class path starting from this classifier, including this classifier
    def get_class_path(self):
        class_path = [self]
        for sc in self.superclasses:
            for cl in sc.get_class_path():
                if cl not in class_path:
                    class_path.append(cl)
        return class_path

    @property
    def class_path(self):
        return self.get_class_path()
