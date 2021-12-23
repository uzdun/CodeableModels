from codeable_models.cclass import CClass
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
        """``CStereotype`` is used to define stereotypes and stereotype instances. Meta-classes and meta-class
        associations can be extended with stereotypes.

        **Superclasses:**  :py:class:`.CClassifier`

        Args:
           name (str): An optional name.
           **kwargs: Pass in any kwargs acceptable to superclasses. In addition, ``CStereotype`` accepts:
                ``extended``, ``default_values``.

                - ``extended``:
                    Takes a single or a list of either :py:class:`.CMetaclass` objects or
                    :py:class:`.CAssociation` objects to be extended with this stereotype.
                    Association objects must be  meta-class associations. Using the ``stereotypes``
                    property on the meta-classes or association is an alternative method
                    for defining the ``extended`` relation.
                - ``default_values``:
                    Takes a dict of default values for the values of the extended meta-classes or
                    meta-class associations. Those default values  shadow any default value
                    defined for attributes on the meta-classes or
                    meta-class associations themselves. That is, with ``default_values`` the stereotype
                    can add or change default values of the extended classifiers.

        **Examples:**

        Consider a simple component meta-model is defined like this::

            component = CMetaclass("Component")
            connectors_relation = component.association(component,
                                                        "connected to: [source] * -> [target] *")

        If we want to use stereotypes to distinguish component types, we can extend the meta-class with::

            component_type = CStereotype("Component Type", extended=component)

        Now more specific component types can be defined as sub-classes of the stereotype::

            service = CStereotype("Service", superclasses=component_type)
            database = CStereotype("Database", superclasses=component_type)

        We can also extend the meta-class association with stereotypes, e.g.::

            connector_type = CStereotype("Connector Type", extended=connectors_relation)

        Now we can introduce more specific connector types based on this stereotype as sub-classes::

            jdbc = CStereotype("JDBC", superclasses=connector_type)
            mongo_wire = CStereotype("Mongo Wire", superclasses=connector_type)
            restful_http = CStereotype("RESTful HTTP", superclasses=connector_type)
            soap = CStereotype("SOAP", superclasses=connector_type)

        **Main Relations:**

        The main relations of ``CStereotype`` are shown in the figure below.

        .. image:: ../images/stereotype_model.png

        As can be seen,  each :py:class:`.CStereotype` is a :py:class:`.CClassifier`.
        Meta-classes and meta-class
        associations can be extended with stereotypes.
        If this is the case,
        those stereotypes can be used as stereotype instances on the classes of the meta-class or links of
        the association, respectively.
        """
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
        """CMetaclass | list[CMetaclass]: Getter and setter for extended classifiers.
            Takes a single or a list of either :py:class:`.CMetaclass` objects or
            :py:class:`.CAssociation` objects to be extended with this stereotype.
            Association objects must be  meta-class associations. Using the ``stereotypes``
            property on the meta-classes or association is an alternative method
            for defining the extended relation."""
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
            raise CException(f"extended requires a list, a metaclass, an association as input")
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
        """list[CClass] | list[CLink]: Getter for the extended instances, i.e. the classes or class links
        extended by this stereotype."""
        return list(self.extended_instances_)

    @property
    def all_extended_instances(self):
        """list[CClass] | list[CLink]: Getter for all the extended instances, i.e. the classes or class links
        extended by this stereotype, including those on subclasses."""
        all_instances = list(self.extended_instances_)
        for scl in self.all_subclasses:
            for cl in scl.extended_instances_:
                all_instances.append(cl)
        return all_instances

    def delete(self):
        """Deletes the stereotype. Removes it from all meta-classes or meta-class associations
        it extends.
        Calls ``delete()`` on superclass.

        Returns:
            None
        """
        if self.is_deleted:
            return
        for e in self.extended_:
            e.stereotypes_holder.stereotypes_.remove(self)
        self.extended_ = []
        super().delete()

    def update_default_values_of_classifier_(self, attribute=None):
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

    def is_metaclass_extended_by_this_stereotype_(self, metaclass):
        if metaclass in self.extended_:
            return True
        for mcSuperclass in metaclass.get_all_superclasses_():
            if mcSuperclass in self.extended_:
                return True
        return False

    def is_element_extended_by_stereotype_(self, element):
        if is_cclass(element):
            if self.is_metaclass_extended_by_this_stereotype_(element.metaclass):
                return True
            for superclass in self.get_all_superclasses_():
                if superclass.is_metaclass_extended_by_this_stereotype_(element.metaclass):
                    return True
            return False
        elif is_clink(element):
            if element.association in self.extended:
                return True
            for superclass in self.get_all_superclasses_():
                if element.association in superclass.extended:
                    return True
            return False
        elif is_cassociation(element):
            if element.derived_from in self.extended:
                return True
            for superclass in self.get_all_superclasses_():
                if element.derived_from in superclass.extended:
                    return True
            return False

        raise CException("element is neither a class, nor a link, " +
                         "nor an association derived from a meta-class association")

    def association(self, target, descriptor=None, **kwargs):
        """Method used to create associations on this stereotype. See documentation of method ``association``
        on :py:class:`.CClassifier` for details.

        Args:
            target: The association target classifier.
            descriptor: An optional descriptor making it easier to define associations with a simple string.
            **kwargs: Accepts all keyword arguments acceptable to :py:class:`.CAssociation` to define associations.

        Returns:
            CAssociation: The created association.

        """
        if not isinstance(target, CStereotype):
            raise CException(f"stereotype '{self!s}' is not compatible with association target '{target!s}'")
        return super(CStereotype, self).association(target, descriptor, **kwargs)

    def compute_connected_(self, context):
        super().compute_connected_(context)
        if not context.process_stereotypes:
            return
        connected = []
        for e in self.extended:
            if e not in context.stop_elements_exclusive:
                connected.append(e)
        self.append_connected_(context, connected)

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
        """dict[str, value]: Getter and setter for default values.
        Takes a dict of default values for the values of the extended meta-classes or
        meta-class associations. Those default values shadow any default value
        defined for attributes on the meta-classes or
        meta-class associations themselves. That is, with ``default_values`` the stereotype
        can add or change default values of the extended classifiers.

        Stereotypes, as subclasses of :py:class:`.CClassifier`, can also define attributes,
        which are the definitions of the tagged values of the stereotype. Default values should not be
        confused with those tagged value attributes (and their defaults). The default values concern the attributes
        values defined on the meta-class that is extended by the stereotype.
        """
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
        """Get a default value defined on the stereotype or its superclasses
        with the given ``attribute_name``. Optionally the classifier
        to consider can be specified. This is needed, if one or more attributes of the same name are defined
        on the inheritance hierarchy. Then a shadowed attribute can be accessed by specifying its classifier.

        Stereotypes, as subclasses of :py:class:`.CClassifier`, can also define attributes,
        which are the definitions of the tagged values of the stereotype. Default values should not be
        confused with those tagged value attributes (and their defaults). The default values concern the attributes
        values defined on the meta-class that is extended by the stereotype.

        Args:
            attribute_name: The name of the attribute.
            classifier: The optional classifier on which the attribute is defined.

        Returns:
            Supported Attribute Types: Value of the attribute.
        """
        if self.is_deleted:
            raise CException(f"can't get default value '{attribute_name!s}' on deleted stereotype")
        class_path = self._get_default_value_class_path()
        if len(class_path) == 0:
            raise CException(f"default values can only be used on a stereotype that extends metaclasses")
        return get_var_value(self, class_path, self.default_values_, attribute_name, VarValueKind.DEFAULT_VALUE,
                             classifier)

    def delete_default_value(self, attribute_name, classifier=None):
        """Deletes a default value defined on the stereotype or its superclasses
        with the given ``attribute_name``. Optionally the classifier
        to consider can be specified. This is needed, if one or more attributes of the same name are defined
        on the inheritance hierarchy. Then a shadowed attribute can be accessed by specifying its classifier.

        Args:
            attribute_name: The name of the attribute.
            classifier: The optional classifier on which the attribute is defined.

        Returns:
            Supported Attribute Types: Value of the attribute.
        """
        if self.is_deleted:
            raise CException(f"can't delete default value '{attribute_name!s}' on deleted stereotype")
        class_path = self._get_default_value_class_path()
        if len(class_path) == 0:
            raise CException(f"default values can only be used on a stereotype that extends metaclasses")
        return delete_var_value(self, class_path, self.default_values_, attribute_name, VarValueKind.DEFAULT_VALUE,
                                classifier)

    def set_default_value(self, attribute_name, value, classifier=None):
        """Set a default value defined on the stereotype or its superclasses
        with the given ``attribute_name`` to ``value``. Optionally the classifier
        to consider can be specified. This is needed, if one or more attributes of the same name are defined
        on the inheritance hierarchy. Then a shadowed attribute can be accessed by specifying its classifier.

        Stereotypes, as subclasses of :py:class:`.CClassifier`, can also define attributes,
        which are the definitions of the tagged values of the stereotype. Default values should not be
        confused with those tagged value attributes (and their defaults). The default values concern the attributes
        values defined on the meta-class that is extended by the stereotype.

        Args:
            attribute_name: The name of the attribute.
            value: The new value.
            classifier: The optional classifier on which the attribute is defined.

        Returns:
            None
        """
        if self.is_deleted:
            raise CException(f"can't set default value '{attribute_name!s}' on deleted stereotype")
        class_path = self._get_default_value_class_path()
        if len(class_path) == 0:
            raise CException(f"default values can only be used on a stereotype that extends metaclasses")
        set_var_value(self, class_path, self.default_values_, attribute_name, value, VarValueKind.DEFAULT_VALUE,
                      classifier)
