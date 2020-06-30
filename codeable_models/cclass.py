from codeable_models.cclassifier import CClassifier
from codeable_models.cexception import CException
from codeable_models.cobject import CObject
from codeable_models.internal.commons import check_is_cmetaclass, check_is_cobject, \
    check_named_element_is_not_deleted
from codeable_models.internal.stereotype_holders import CStereotypeInstancesHolder
from codeable_models.internal.var_values import delete_var_value, set_var_value, get_var_value, get_var_values, \
    set_var_values, VarValueKind


class CClass(CClassifier):
    def __init__(self, metaclass, name=None, **kwargs):
        """``CClass`` is used to define classes. Classes in Codeable Models are instances of metaclasses (defined
        using :py:class:`.CMetaclass`).

        **Superclasses:**  :py:class:`.CClassifier`

        Args:
           metaclass (CMetaclass): The meta-class this class is instantiated from. Each class requires a meta-class,
                defined using :py:class:`.CMetaclass`.
           name (str): An optional name.
           **kwargs: Pass in any kwargs acceptable to superclasses. In addition, ``CClass`` accepts:
                ``stereotype_instances``, ``values``, ``tagged_values``.

                - ``stereotype_instances``:
                    Any :py:class:`.CStereotype` extending the meta-class of this class can be defined on the class
                    as a stereotype instance. That is, the list of stereotypes on the meta-class defines the possible
                    stereotypes instances of the class. The kwarg accepts a list of stereotype instances or a single
                    stereotype instance as argument.
                - ``values``:
                    Just as objects can define ``values`` for attributes defined on their classes, a class
                    can define values for any attribute defined on their meta-class. They can be used via the
                    interface of ``CClass``. Internally, a so-called class object (explained below) is used to
                    store and manage those values. ``values`` accepts a dict of key/value pairs. The value
                    types must conform to the types defined for the attributes.
                - ``tagged_values``:
                    Any attribute on a :py:class:`.CStereotype` extending the meta-class of this class, which is
                    also a stereotype instance of this class, can be set as a tagged value on this class.
                    The keyword arg ``tagged_values`` can be used to set them just like ordinary attribute values.
                    ``tagged_values`` accepts a dict of key/value pairs.
                    The value types must conform to the types defined for the attributes.

        **Examples:**

        An example class definition is::

            cloud = CClass(execution_environment, "Cloud")

        Here is a class that defines a stereotype instance (assuming the meta-class is extended by this stereotype)::

            cloud = CClass(execution_environment, "Cloud", stereotype_instances = cloud_env_type)


        **Main Relations:**

        The main relations of ``CClass`` are shown in the figure below.

        .. image:: ../images/class_model.png

        As can be seen,  each :py:class:`.CClass` is a :py:class:`.CClassifier` and has a :py:class:`.CMetaclass`.
        It has instances of type :py:class:`.CObject`.

        ``CClass`` uses a special object, the *class object*,
        to manage its instance relation to its meta-class.
        That is, classes offer :py:class:`.CObject` capabilities such as attribute values and links via the
        class object. For most purposes, the class object is
        hidden by ``CClass``, i.e. the class object is usually not used by the user directly.

        Each class can have stereotype instances of the stereotypes
        defined on its meta-class.
        """
        self.metaclass_ = None
        self.metaclass = metaclass
        self.objects_ = []
        self.class_object_ = CObject(self.metaclass, name, class_object_class_=self)
        self.stereotype_instances_holder = CStereotypeInstancesHolder(self)
        self.tagged_values_ = {}
        super().__init__(name, **kwargs)
        self.class_object_.init_attribute_values_()

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.append("stereotype_instances")
        legal_keyword_args.append("values")
        legal_keyword_args.append("tagged_values")
        super()._init_keyword_args(legal_keyword_args, **kwargs)

    @property
    def class_object(self):
        """CObject: Getter to get the class object of this class."""
        return self.class_object_

    @property
    def metaclass(self):
        """CMetaclass: Getter and setter to get the meta-class of this class."""
        return self.metaclass_

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
        """list[CObject]: Getter to get the instances of this class."""
        return list(self.objects_)

    @property
    def all_objects(self):
        """list[CObject]: Getter to get all instances of this class, defined directly on the class and on any
        sub-class."""
        all_objects = list(self.objects_)
        for scl in self.all_subclasses:
            for cl in scl.objects_:
                all_objects.append(cl)
        return all_objects

    def add_object_(self, obj):
        if obj in self.objects_:
            raise CException(f"object '{obj!s}' is already an instance of the class '{self!s}'")
        check_is_cobject(obj)
        self.objects_.append(obj)

    def remove_object_(self, obj):
        if obj not in self.objects_:
            raise CException(f"can't remove object '{obj!s}'' from class '{self!s}': not an instance")
        self.objects_.remove(obj)

    def delete(self):
        """
        Delete the class. Also deletes all direct instances of the class. Remove the class from stereotype instance
        relations. Removes it from its meta-class relation. Deletes the class object.
        Calls ``delete()`` on superclass.

        Returns:
            None

        """
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

    def instance_of(self, classifier):
        """Returns ``True`` if this class is instance of the ``classifier``, else ``False``.

        Args:
            classifier: A classifier to check against.

        Returns:
            bool: Boolean result of the test.

        """
        return self.class_object_.instance_of(classifier)

    def update_default_values_of_classifier_(self, attribute=None):
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
                    i.remove_value_(attrName, self)

    def get_value(self, attribute_name, classifier=None):
        """Get the value of an attribute with the given ``attribute_name``. Optionally the classifier
        to consider can be specified. This is needed, if one or more attributes of the same name are defined
        on the inheritance hierarchy. Then a shadowed attribute can be accessed by specifying its classifier.

        Args:
            attribute_name: The name of the attribute.
            classifier: The optional classifier on which the attribute is defined.

        Returns:
            Supported Attribute Types: Value of the attribute.
        """
        return self.class_object_.get_value(attribute_name, classifier)

    def delete_value(self, attribute_name, classifier=None):
        """Delete the value of an attribute with the given ``attribute_name``. Optionally the classifier
        to consider can be specified. This is needed, if one or more attributes of the same name are defined
        on the inheritance hierarchy. Then a shadowed attribute can be accessed by specifying its classifier.

        Args:
            attribute_name: The name of the attribute.
            classifier: The optional classifier on which the attribute is defined.

        Returns:
            Supported Attribute Types: Value of the attribute.
        """
        return self.class_object_.delete_value(attribute_name, classifier)

    def set_value(self, attribute_name, value, classifier=None):
        """Set the value of an attribute with the given ``attribute_name`` to ``value``. Optionally the classifier
        to consider can be specified. This is needed, if one or more attributes of the same name are defined
        on the inheritance hierarchy. Then a shadowed attribute can be accessed by specifying its classifier.

        Args:
            attribute_name: The name of the attribute.
            value: The new value.
            classifier: The optional classifier on which the attribute is defined.

        Returns:
            None
        """
        return self.class_object_.set_value(attribute_name, value, classifier)

    @property
    def values(self):
        """dict[str, value]: Getter for getting all values of the object using a dict, and setter of setting
        all values of the object based on a dict. The dict uses key/value pairs.
        The value types must conform to the types defined for the attributes.
        """
        return self.class_object_.values

    @values.setter
    def values(self, new_values):
        self.class_object_.values = new_values

    def get_objects(self, name):
        """
        Returns all objects with a given name with are instances of this classifier.

        Args:
            name: The object name to search for

        Returns:
            list[CObject]: The objects with the given name.

        """
        return list(o for o in self.objects if o.name == name)

    def get_object(self, name):
        """
        Returns an object with the given name with is instance of this classifier, or if not present ``None``.
        If multiple objects are found, the first found object is returned.

        Args:
            name: The object name to search for

        Returns:
            CObject: An object with the given name or None.

        """
        objects = self.get_objects(name)
        return None if len(objects) == 0 else objects[0]

    @property
    def stereotype_instances(self):
        """list[CStereotype]|CStereotype: Getter to get and setter to set the stereotype instances of this class.

        The stereotype instances must be stereotypes extending the meta-class of the class.

        The setter takes a list of stereotype instances or a single stereotype instance as argument.
        The getter always returns a list.
        """
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
        """Get the tagged value of a stereotype attribute with the given ``name``. Optionally the stereotype
        to consider can be specified. This is needed, if one or more attributes of the same name are defined
        on the inheritance hierarchy. Then a shadowed attribute can be accessed by specifying its stereotype.

        Args:
            name: The name of the attribute.
            stereotype: The optional stereotype on which the attribute is defined.

        Returns:
            Supported Attribute Types: Value of the attribute.
        """
        if self.is_deleted:
            raise CException(f"can't get tagged value '{name!s}' on deleted class")
        return get_var_value(self, self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_,
                             name, VarValueKind.TAGGED_VALUE, stereotype)

    def delete_tagged_value(self, name, stereotype=None):
        """Delete tagged value of a stereotype attribute with the given ``name``.  Optionally the stereotype
        to consider can be specified. This is needed, if one or more attributes of the same name are defined
        on the inheritance hierarchy. Then a shadowed attribute can be accessed by specifying its stereotype.

        Args:
            name: The name of the attribute.
            stereotype: The optional stereotype on which the attribute is defined.

        Returns:
            Supported Attribute Types: Value of the attribute.
        """
        if self.is_deleted:
            raise CException(f"can't delete tagged value '{name!s}' on deleted class")
        return delete_var_value(self, self.stereotype_instances_holder.get_stereotype_instance_path(),
                                self.tagged_values_,
                                name, VarValueKind.TAGGED_VALUE, stereotype)

    def set_tagged_value(self, name, value, stereotype=None):
        """Set the tagged value of a stereotype attribute with the given ``name`` to ``value``.  Optionally the
        stereotype to consider can be specified. This is needed, if one or more attributes of the same name are defined
        on the inheritance hierarchy. Then a shadowed attribute can be accessed by specifying its stereotype.

        Args:
            name: The name of the attribute.
            value: The new value.
            stereotype: The optional stereotype on which the attribute is defined.

        Returns:
            None
        """
        if self.is_deleted:
            raise CException(f"can't set tagged value '{name!s}' on deleted class")
        return set_var_value(self, self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_,
                             name, value, VarValueKind.TAGGED_VALUE, stereotype)

    @property
    def tagged_values(self):
        """dict[str, value]: Getter for getting all tagged values of the class using a dict, and setter of setting
        all tagged values of the class based on a dict. The dict uses key/value pairs.
        The value types must conform to the types defined for the attributes.
        """
        if self.is_deleted:
            raise CException(f"can't get tagged values on deleted class")
        return get_var_values(self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_)

    @tagged_values.setter
    def tagged_values(self, new_values):
        if self.is_deleted:
            raise CException(f"can't set tagged values on deleted class")
        set_var_values(self, new_values, VarValueKind.TAGGED_VALUE)

    def association(self, target, descriptor=None, **kwargs):
        """Method used to create associations on this class. See documentation of method ``association``
        on :py:class:`.CClassifier` for details.

        Args:
            target: The association target classifier.
            descriptor: An optional descriptor making it easier to define associations with a simple string.
            **kwargs: Accepts all keyword arguments acceptable to :py:class:`.CAssociation` to define associations.

        Returns:
            CAssociation: The created association.

        """
        if not isinstance(target, CClass):
            raise CException(f"class '{self!s}' is not compatible with association target '{target!s}'")
        return super(CClass, self).association(target, descriptor, **kwargs)

    @property
    def links(self):
        """list[CLink]: Getter for getting the links defined for this class. Class links are based on the
        associations defined for the class' meta-class."""
        return self.class_object_.links

    @property
    def linked(self):
        """list[CClass]: Getter for getting the linked classes defined for this class."""
        return self.class_object_.linked

    def get_linked(self, **kwargs):
        """Method to get the linked classes defined for this class filtered using criteria specified in kwargs.

        Args:
            **kwargs:
                Defines filter criteria.

                - ``association``:
                    Include links only if they are based on the specified association.
                - ``role_name``:
                    Include links only if they are based on an associations having the specified role name
                    either as a target or source role name.

        Returns:
            list[CClass]: List of linked classes

        """
        return self.class_object_.get_linked(**kwargs)

    def get_links_for_association(self, association):
        """
        Method to get all link objects which are defined based on the given association.

        Args:
            association: Association used to filter the links.

        Returns:
            list[CLink]: The list of link objects.

        """
        return self.class_object_.get_links_for_association(association)

    def add_links(self, links, **kwargs):
        """
        Add links on this class (which are based on associations defined on the class' meta-class).
        Uses the function :py:func:`.add_links`. That is, it is possible to use the following equivalently::

            add_links({<this_class>: <links>}, <**kwargs>)

        Args:
            links: The new links to be defined.
            **kwargs: Any keyword arg acceptable to :py:func:`.add_links`.

        Returns:
            list[CLink]: List of created link objects.

        """
        return self.class_object_.add_links(links, **kwargs)

    def delete_links(self, links, **kwargs):
        """
        Delete links on this class (which are based on associations defined on the class' meta-class).
        Uses the function :py:func:`.delete_links`. That is, it is possible
        to use the following equivalently::

            delete_links({<this_class>: <links>}, <**kwargs>)

        Args:
            links: The links to be deleted.
            **kwargs: Any keyword arg acceptable to :py:func:`.delete_links`.

        Returns:
            list[CLink]: List of deleted link objects.

        """
        return self.class_object_.delete_links(links, **kwargs)
