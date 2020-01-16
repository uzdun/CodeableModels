from codeable_models.cclassifier import CClassifier
from codeable_models.cexception import CException
from codeable_models.internal.commons import check_is_cclass
from codeable_models.internal.stereotype_holders import CStereotypesHolder


class CMetaclass(CClassifier):
    def __init__(self, name=None, **kwargs):
        self.classes_ = []
        self.stereotypes_holder = CStereotypesHolder(self)
        super().__init__(name, **kwargs)

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.append("stereotypes")
        super()._init_keyword_args(legal_keyword_args, **kwargs)

    @property
    def classes(self):
        return list(self.classes_)

    @property
    def all_classes(self):
        all_classes = list(self.classes_)
        for scl in self.all_subclasses:
            for cl in scl.classes_:
                all_classes.append(cl)
        return all_classes

    def get_classes(self, name):
        return list(cl for cl in self.classes if cl.name == name)

    def get_class(self, name):
        classes = self.get_classes(name)
        return None if len(classes) == 0 else classes[0]

    def get_stereotypes(self, name):
        return list(cl for cl in self.stereotypes if cl.name == name)

    def get_stereotype(self, name):
        stereotypes = self.get_stereotypes(name)
        return None if len(stereotypes) == 0 else stereotypes[0]

    def add_class(self, cl):
        check_is_cclass(cl)
        if cl in self.classes_:
            raise CException(f"class '{cl!s}' is already a class of the metaclass '{self!s}'")
        self.classes_.append(cl)

    def remove_class(self, cl):
        if cl not in self.classes_:
            raise CException(f"can't remove class instance '{cl!s}' from metaclass '{self!s}': not a class instance")
        self.classes_.remove(cl)

    def delete(self):
        if self.is_deleted:
            return
        classes_to_delete = list(self.classes_)
        for cl in classes_to_delete:
            cl.delete()
        self.classes_ = []
        for s in self.stereotypes_holder.stereotypes_:
            s.extended_.remove(self)
        self.stereotypes_holder.stereotypes_ = []
        super().delete()

    @property
    def stereotypes(self):
        return self.stereotypes_holder.stereotypes

    @stereotypes.setter
    def stereotypes(self, elements):
        self.stereotypes_holder.stereotypes = elements

    def update_default_values_of_classifier(self, attribute=None):
        for i in self.all_classes:
            attr_items = self.attributes_.items()
            if attribute is not None:
                attr_items = {attribute.name_: attribute}.items()
            for attrName, attr in attr_items:
                if attr.default is not None:
                    if i.get_value(attrName, self) is None:
                        i.set_value(attrName, attr.default, self)

    def _remove_attribute_values_of_classifier(self, attributes_to_keep):
        for i in self.all_classes:
            for attrName in self.attribute_names:
                if attrName not in attributes_to_keep:
                    i.delete_value(attrName, self)

    def association(self, target, descriptor=None, **kwargs):
        if not isinstance(target, CMetaclass):
            raise CException(f"metaclass '{self!s}' is not compatible with association target '{target!s}'")
        return super(CMetaclass, self).association(target, descriptor, **kwargs)

    def compute_connected(self, context):
        super().compute_connected(context)
        connected = []
        for s in self.stereotypes:
            if s not in context.stop_elements_exclusive:
                connected.append(s)
        self.append_connected(context, connected)
