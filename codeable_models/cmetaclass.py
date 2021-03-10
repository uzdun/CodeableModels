from codeable_models.cclassifier import CClassifier
from codeable_models.cexception import CException
from codeable_models.internal.commons import check_is_cclass
from codeable_models.internal.stereotype_holders import CStereotypesHolder


class CMetaclass(CClassifier):
    def __init__(self, name=None, **kwargs):
        """``CMetaclass`` is used to define meta-classes. All classes (defined
        using :py:class:`.CClass`) in Codeable Models are instances of metaclasses.

        **Superclasses:**  :py:class:`.CClassifier`

        Args:
           name (str): An optional name.
           **kwargs: Pass in any kwargs acceptable to superclasses. In addition, ``CMetaclass`` accepts:
                ``stereotypes``.

                - ``stereotypes``:
                    Takes a single or a list of :py:class:`.CStereotype` objects which extend this
                    meta-class.

        **Examples:**

        An example meta-class definition is::

            component = CMetaclass("Component")

        Using a simple relation we can use the meta-class to define component and connector del::

            connectors_relation = component.association(component,
                                                        "connected to: [source] * -> [target] *")

        **Main Relations:**

        The main relations of ``CMetaclass`` are shown in the figure below.

        .. image:: ../images/metaclass_model.png

        As can be seen,  each :py:class:`.CMetaclass` is a :py:class:`.CClassifier` and has
        :py:class:`.CClass` instances. Stereotypes can extend the meta-class. If this is the case,
        those stereotypes can be used as stereotype instances on the classes of the meta-class.
        """
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
        """list[CClass]: Getter for the list of classes (directly) derived from this meta-class."""
        return list(self.classes_)

    @property
    def all_classes(self):
        """list[CClass]: Getter for the list of classes derived from this meta-class, either directly
        or in one of the sub-classes of the meta-class."""
        all_classes = list(self.classes_)
        for scl in self.all_subclasses:
            if isinstance(scl, CMetaclass):
                for cl in scl.classes_:
                    all_classes.append(cl)
        return all_classes

    def get_classes(self, name):
        """Gets all classes directly derived from this meta-class that have the specified name.

        Args:
            name: Class name to search for.

        Returns:
            list[CClass]: The classes with the given name.

        """
        return list(cl for cl in self.classes if cl.name == name)

    def get_class(self, name):
        """Gets the class directly derived from this meta-class that has the specified name. If more than one
        such classes exist, the first one is returned.

        Args:
            name: Class name to search for.

        Returns:
            CClass: The class with the given name.

        """
        classes = self.get_classes(name)
        return None if len(classes) == 0 else classes[0]

    def get_stereotypes(self, name):
        """Gets all stereotypes extending this meta-class that have the specified name.

        Args:
            name: Stereotype name to search for.

        Returns:
            list[CClass]: The stereotypes with the given name.

        """
        return list(cl for cl in self.stereotypes if cl.name == name)

    def get_stereotype(self, name):
        """Gets the stereotype extending this meta-class that has the specified name. If more than one
        such stereotypes exist, the first one is returned.

        Args:
            name: Stereotype name to search for.

        Returns:
            CClass: The stereotype with the given name.

        """
        stereotypes = self.get_stereotypes(name)
        return None if len(stereotypes) == 0 else stereotypes[0]

    def add_class(self, cl):
        """Add the class ``cl`` to the classes of this meta-class.

        Args:
            cl (CClass): A class to add.

        Returns:
            None

        """
        check_is_cclass(cl)
        if cl in self.classes_:
            raise CException(f"class '{cl!s}' is already a class of the metaclass '{self!s}'")
        self.classes_.append(cl)

    def remove_class(self, cl):
        """Remove the class ``cl`` from the classes of this meta-class. Raises an exception, if ``cl`` is
        not a class derived from  this meta-class.

        Args:
            cl (CClass): A class to remove.

        Returns:
            None

        """
        if cl not in self.classes_:
            raise CException(f"can't remove class instance '{cl!s}' from metaclass '{self!s}': not a class instance")
        self.classes_.remove(cl)

    def delete(self):
        """
        Delete the meta-class. Delete all classes derived from the meta-class. Remove the class from
        stereotypes that extend this meta-class. Calls ``delete()`` on superclass.

        Returns:
            None

        """
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
        """CStereotype | list[CStereotype]: Getter and setter for the stereotypes which extend this
        meta-class."""
        return self.stereotypes_holder.stereotypes

    @stereotypes.setter
    def stereotypes(self, elements):
        self.stereotypes_holder.stereotypes = elements

    def update_default_values_of_classifier_(self, attribute=None):
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
        """Method used to create associations on this meta-class. See documentation of method ``association``
        on :py:class:`.CClassifier` for details.

        Args:
            target: The association target classifier.
            descriptor: An optional descriptor making it easier to define associations with a simple string.
            **kwargs: Accepts all keyword arguments acceptable to :py:class:`.CAssociation` to define associations.

        Returns:
            CAssociation: The created association.

        """
        if not isinstance(target, CMetaclass):
            raise CException(f"metaclass '{self!s}' is not compatible with association target '{target!s}'")
        return super(CMetaclass, self).association(target, descriptor, **kwargs)

    def compute_connected_(self, context):
        super().compute_connected_(context)
        connected = []
        for s in self.stereotypes:
            if s not in context.stop_elements_exclusive:
                connected.append(s)
        self.append_connected_(context, connected)
