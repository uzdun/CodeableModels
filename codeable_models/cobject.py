from codeable_models.cassociation import CAssociation
from codeable_models.cbundlable import CBundlable
from codeable_models.cmetaclass import CMetaclass
from codeable_models.internal.commons import *
from codeable_models.internal.var_values import delete_var_value, set_var_value, get_var_value, get_var_values, \
    set_var_values, VarValueKind


class CObject(CBundlable):
    def __init__(self, cl, name=None, **kwargs):
        self.class_object_class_ = None
        if 'class_object_class_' in kwargs:
            class_object_class = kwargs.pop('class_object_class_', None)
            self.class_object_class_ = class_object_class
        elif cl.__class__ is CAssociation:
            pass
        else:
            # don't check if this is a class object, as classifier is then a metaclass 
            check_is_cclass(cl)

        values = kwargs.pop('values', None)

        if cl is not None:
            check_named_element_is_not_deleted(cl)
        self.classifier_ = cl
        self.attribute_values = {}
        super().__init__(name, **kwargs)
        if self.class_object_class_ is None:
            # don't add instance if this is a class object or association
            if cl.__class__ is not CAssociation:
                self.classifier_.add_object(self)
            # do not init default attributes of a class object, the class constructor 
            # does it after stereotype instances are added, who defining defaults first 
            self.init_attribute_values()
        self.links_ = []

        if values is not None:
            self.values = values

    def init_attribute_values(self):
        # init default values of attributes
        for cl in self.classifier.class_path:
            for attrName, attr in cl.attributes_.items():
                if attr.default is not None:
                    if self.get_value(attrName, cl) is None:
                        self.set_value(attrName, attr.default, cl)

    @property
    def class_object_class(self):
        return self.class_object_class_

    @property
    def classifier(self):
        return self.classifier_

    @classifier.setter
    def classifier(self, cl):
        if is_clink(self):
            raise CException(
                f"Changes to classifier (i.e., the association) of a link" +
                " should not be performed with CObject methods")
        check_is_cclass(cl)
        if self.classifier_ is not None:
            self.classifier_.remove_object(self)
        if cl is not None:
            check_named_element_is_not_deleted(cl)
        self.classifier_ = cl
        self.classifier_.add_object(self)

    def delete(self):
        if self.is_deleted:
            return
        if not (isinstance(self.classifier, CMetaclass) or isinstance(self.classifier, CAssociation)):
            # for class objects, the class cleanup removes the instance
            # link instances are removed by the association
            self.classifier_.remove_object(self)
        self.classifier_ = None
        super().delete()
        links = self.links_.copy()
        for link in links:
            link.delete()

    def instance_of(self, cl):
        if self.classifier is None:
            return False
        if cl is None:
            raise CException(f"'None' is not a valid argument")
        if is_clink(self):
            # noinspection PyUnresolvedReferences
            if self.is_class_link():
                if not (is_cmetaclass(cl) or is_cassociation(cl)):
                    raise CException(f"'{cl!s}' is not an association or a metaclass")
            else:
                if not (is_cclass(cl) or is_cassociation(cl)):
                    raise CException(f"'{cl!s}' is not an association or a class")
        else:
            if isinstance(self.classifier, CMetaclass):
                # this is a class object
                if not is_cmetaclass(cl):
                    raise CException(f"'{cl!s}' is not a metaclass")
            else:
                if not is_cclass(cl):
                    raise CException(f"'{cl!s}' is not a class")

        if self.classifier == cl:
            return True
        if cl in self.classifier.all_superclasses:
            return True
        return False

    def _get_kind_str(self):
        kind_str = "object"
        if is_clink(self):
            kind_str = "link"
        elif self.class_object_class_ is not None:
            kind_str = "class"
        return kind_str

    def get_value(self, attribute_name, classifier=None):
        if self.is_deleted:
            raise CException(f"can't get value '{attribute_name!s}' on deleted {self._get_kind_str()!s}")
        return get_var_value(self, self.classifier.class_path, self.attribute_values, attribute_name,
                             VarValueKind.ATTRIBUTE_VALUE, classifier)

    def delete_value(self, attribute_name, classifier=None):
        if self.is_deleted:
            raise CException(f"can't delete value '{attribute_name!s}' on deleted {self._get_kind_str()!s}")
        return delete_var_value(self, self.classifier.class_path, self.attribute_values, attribute_name,
                                VarValueKind.ATTRIBUTE_VALUE, classifier)

    def set_value(self, attribute_name, value, classifier=None):
        if self.is_deleted:
            raise CException(f"can't set value '{attribute_name!s}' on deleted {self._get_kind_str()!s}")
        set_var_value(self, self.classifier.class_path, self.attribute_values, attribute_name, value,
                      VarValueKind.ATTRIBUTE_VALUE, classifier)

    @property
    def values(self):
        if self.is_deleted:
            raise CException(f"can't get values on deleted {self._get_kind_str()!s}")
        return get_var_values(self.classifier.class_path, self.attribute_values)

    @values.setter
    def values(self, new_values):
        if self.is_deleted:
            raise CException(f"can't set values on deleted {self._get_kind_str()!s}")
        set_var_values(self, new_values, VarValueKind.ATTRIBUTE_VALUE)

    def remove_value_(self, attribute_name, classifier):
        try:
            self.attribute_values[classifier].pop(attribute_name, None)
        except KeyError:
            return

    @property
    def links(self):
        return list(self.links_)

    @property
    def linked(self):
        result = []
        for link in self.links_:
            opposite = link.get_opposite_object(self)
            if opposite.class_object_class_ is None:
                result.append(opposite)
            else:
                result.append(opposite.class_object_class_)
        return result

    def get_links_for_association(self, association):
        association_links = []
        for link in list(self.links_):
            if link.association == association:
                association_links.extend([link])
        return association_links

    def get_linked(self, **kwargs):
        from codeable_models.clink import LinkKeywordsContext
        context = LinkKeywordsContext(**kwargs)

        result = []
        for link in self.links_:
            # if link.is_deleted:

            append = True
            if context.association is not None:
                if link.association != context.association:
                    append = False
            if context.role_name is not None:
                append = False
                if link.association.role_name == context.role_name:
                    if self == link.source_:
                        append = True
                if link.association.source_role_name == context.role_name:
                    if self == link.target_:
                        append = True

            if append:
                opposite = link.get_opposite_object(self)
                if opposite.class_object_class_ is None:
                    result.append(opposite)
                else:
                    result.append(opposite.class_object_class_)
        return result

    def add_links(self, links, **kwargs):
        from codeable_models.clink import add_links
        return add_links({self: links}, **kwargs)

    def delete_links(self, links, **kwargs):
        from codeable_models.clink import delete_links
        return delete_links({self: links}, **kwargs)

    def compute_connected_(self, context):
        super().compute_connected_(context)
        connected = []
        for link in self.links_:
            opposite = link.get_opposite_object(self)
            if opposite not in context.stop_elements_exclusive:
                connected.append(opposite)
        self.append_connected_(context, connected)
