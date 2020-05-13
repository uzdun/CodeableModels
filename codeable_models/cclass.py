from codeable_models.cclassifier import CClassifier
from codeable_models.cexception import CException
from codeable_models.cobject import CObject
from codeable_models.internal.commons import check_is_cmetaclass, check_is_cobject, check_named_element_is_not_deleted
from codeable_models.internal.stereotype_holders import CStereotypeInstancesHolder
from codeable_models.internal.var_values import delete_var_value, set_var_value, get_var_value, get_var_values, \
    set_var_values, VarValueKind


class CClass(CClassifier):
    def __init__(self, metaclass, name=None, **kwargs):
        self.metaclass_ = None
        self.metaclass = metaclass
        self.objects_ = []
        self.class_object_ = CObject(self.metaclass, name, class_object_class_=self)
        self.stereotype_instances_holder = CStereotypeInstancesHolder(self)
        self.tagged_values_ = {}
        super().__init__(name, **kwargs)
        self.class_object_.init_attribute_values()

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.append("stereotype_instances")
        legal_keyword_args.append("values")
        legal_keyword_args.append("tagged_values")
        super()._init_keyword_args(legal_keyword_args, **kwargs)

    @property
    def metaclass(self):
        return self.metaclass_

    @property
    def class_object(self):
        return self.class_object_

    @metaclass.setter
    def metaclass(self, mcl):
        check_is_cmetaclass(mcl)
        if self.metaclass_ is not None:
            self.metaclass_.remove_class(self)
        if mcl is not None:
            check_named_element_is_not_deleted(mcl)
        self.metaclass_ = mcl
        self.metaclass_.add_class(self)

    @property
    def objects(self):
        return list(self.objects_)

    @property
    def all_objects(self):
        all_objects = list(self.objects_)
        for scl in self.all_subclasses:
            for cl in scl.objects_:
                all_objects.append(cl)
        return all_objects

    def add_object(self, obj):
        if obj in self.objects_:
            raise CException(f"object '{obj!s}' is already an instance of the class '{self!s}'")
        check_is_cobject(obj)
        self.objects_.append(obj)

    def remove_object(self, obj):
        if obj not in self.objects_:
            raise CException(f"can't remove object '{obj!s}'' from class '{self!s}': not an instance")
        self.objects_.remove(obj)

    def delete(self):
        if self.is_deleted:
            return

        objects_to_delete = list(self.objects_)
        for obj in objects_to_delete:
            obj.delete()
        self.objects_ = []

        for si in self.stereotype_instances:
            si.extended_instances_.remove(self)
        self.stereotype_instances_holder.stereotypes_ = []

        self.metaclass.remove_class(self)
        self.metaclass_ = None

        super().delete()

        self.class_object_.delete()

    def instance_of(self, cl):
        return self.class_object_.instance_of(cl)

    def update_default_values_of_classifier(self, attribute=None):
        for i in self.all_objects:
            attr_items = self.attributes_.items()
            if attribute is not None:
                attr_items = {attribute.name_: attribute}.items()
            for attrName, attr in attr_items:
                if attr.default is not None:
                    if i.get_value(attrName, self) is None:
                        i.set_value(attrName, attr.default, self)

    def _remove_attribute_values_of_classifier(self, attributes_to_keep):
        for i in self.all_objects:
            for attrName in self.attribute_names:
                if attrName not in attributes_to_keep:
                    i.remove_value(attrName, self)

    def get_value(self, attribute_name, cl=None):
        return self.class_object_.get_value(attribute_name, cl)

    def delete_value(self, attribute_name, cl=None):
        return self.class_object_.delete_value(attribute_name, cl)

    def set_value(self, attribute_name, value, cl=None):
        return self.class_object_.set_value(attribute_name, value, cl)

    @property
    def values(self):
        return self.class_object_.values

    @values.setter
    def values(self, new_values):
        self.class_object_.values = new_values

    def get_objects(self, name):
        return list(o for o in self.objects if o.name == name)

    def get_object(self, name):
        objects = self.get_objects(name)
        return None if len(objects) == 0 else objects[0]

    @property
    def stereotype_instances(self):
        return self.stereotype_instances_holder.stereotypes

    @stereotype_instances.setter
    def stereotype_instances(self, elements):
        self.stereotype_instances_holder.stereotypes = elements
        self._init_stereotype_default_values()

    def _init_stereotype_default_values(self):
        # stereotype instances applies all stereotype defaults, if the value has not
        # yet been set. as this runs during initialization before the metaclass default
        # initialization, stereotypes have priority. If stereotype_instances is called after
        # class initialization has finished, other values like metaclass defaults might have
        # been set. Then the stereotype defaults will not overwrite existing values (you need to
        # delete them explicitly in order for them to be replaced by stereotype defaults)
        existing_attribute_names = []
        for mcl in self.metaclass.class_path:
            for attrName in mcl.attribute_names:
                if attrName not in existing_attribute_names:
                    existing_attribute_names.append(attrName)
        for stereotypeInstance in self.stereotype_instances:
            for st in stereotypeInstance.class_path:
                for name in st.default_values:
                    if name in existing_attribute_names:
                        if self.get_value(name) is None:
                            self.set_value(name, st.default_values[name])

    def get_tagged_value(self, name, stereotype=None):
        if self.is_deleted:
            raise CException(f"can't get tagged value '{name!s}' on deleted class")
        return get_var_value(self, self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_,
                             name, VarValueKind.TAGGED_VALUE, stereotype)

    def delete_tagged_value(self, name, stereotype=None):
        if self.is_deleted:
            raise CException(f"can't delete tagged value '{name!s}' on deleted class")
        return delete_var_value(self, self.stereotype_instances_holder.get_stereotype_instance_path(),
                                self.tagged_values_,
                                name, VarValueKind.TAGGED_VALUE, stereotype)

    def set_tagged_value(self, name, value, stereotype=None):
        if self.is_deleted:
            raise CException(f"can't set tagged value '{name!s}' on deleted class")
        return set_var_value(self, self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_,
                             name, value, VarValueKind.TAGGED_VALUE, stereotype)

    @property
    def tagged_values(self):
        if self.is_deleted:
            raise CException(f"can't get tagged values on deleted class")
        return get_var_values(self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_)

    @tagged_values.setter
    def tagged_values(self, new_values):
        if self.is_deleted:
            raise CException(f"can't set tagged values on deleted class")
        set_var_values(self, new_values, VarValueKind.TAGGED_VALUE)

    def association(self, target, descriptor=None, **kwargs):
        if not isinstance(target, CClass):
            raise CException(f"class '{self!s}' is not compatible with association target '{target!s}'")
        return super(CClass, self).association(target, descriptor, **kwargs)

    @property
    def link_objects(self):
        return self.class_object_.link_objects

    @property
    def links(self):
        return self.class_object_.links

    def get_links(self, **kwargs):
        return self.class_object_.get_links(**kwargs)

    def get_link_objects_for_association(self, association):
        return self.class_object_.get_link_objects_for_association(association)

    # returns a list of tuples of the form: (from, to, stereotype_instance), listing all such relations for the
    # an association
    def get_link_stereotype_instances_for_association(self, association):
        result = []
        for link in self.get_link_objects_for_association(association):
            for link_type in link.stereotype_instances:
                from_object = link.source
                to_object = self
                if link.source == self:
                    from_object = self
                    to_object = link.target
                result.append((from_object, to_object, link_type))
        return result

    def add_links(self, links, **kwargs):
        return self.class_object_.add_links(links, **kwargs)

    def delete_links(self, links, **kwargs):
        return self.class_object_.delete_links(links, **kwargs)
