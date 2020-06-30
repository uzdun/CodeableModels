from codeable_models.cassociation import CAssociation
from codeable_models.cbundlable import CBundlable
from codeable_models.cmetaclass import CMetaclass
from codeable_models.internal.commons import *
from codeable_models.internal.var_values import delete_var_value, set_var_value, get_var_value, get_var_values, \
    set_var_values, VarValueKind


class CObject(CBundlable):
    def __init__(self, cl, name=None, **kwargs):
        """``CObject`` is used to define objects. Objects in Codeable Models are instances of classes (defined
        using :py:class:`.CClass`).

        **Superclasses:**  :py:class:`.CBundlable`

        Args:
           cl (CClass): The class this object is instantiated from. Each object requires a class,
                defined using :py:class:`.CClass`.
           name (str): An optional name.
           **kwargs: Pass in any kwargs acceptable to superclasses.

        **Examples:**

        An example object definition is::

            basic_pen = CObject(product, values={"id": "P001", "name": "Basic Pen", "price": 1.50})

        Here an unnamed object is derived from class ``product`` with two string values ``id`` and ``name``,
        as well as a float value ``price``. The following defines the same object, except that it uses
        an object name instead of defining a name as an attribute value::

            basic_pen = CObject(product, "Basic Pen", values={"id": "P001", "price": 1.50})

        **Main Relations:**

        The main relations of ``CObject`` are shown in the figure below.

        .. image:: ../images/object_model.png

        Each :py:class:`.CObject` can be used in bundles through its superclass
        :py:class:`.CBundlable`.
        Objects are instances of type :py:class:`.CClass`.

        Each :py:class:`.CClass` has one ``class object``, a
        special object to manage the instance relation of a class to its meta-class. For instance, the
        values of meta-class attributes and links for meta-class associations are stored and managed via
        wrapper methods on :py:class:`.CClass` that call the respective methods of the ``class object``.

        Each object can be source or target of a link. Links are only valid, if there is an association between
        the classes of the objects to be linked (and multiplicities are correctly set on
        these associations). The association is the classifier of the link (thus it inherits from
        :py:class:`.CClassifier`), and the link is interpreted as an instance of the association (thus it
        inherits from :py:class:`.CObject`).

        """
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
                self.classifier_.add_object_(self)
            # do not init default attributes of a class object, the class constructor 
            # does it after stereotype instances are added, who defining defaults first 
            self.init_attribute_values_()
        self.links_ = []

        if values is not None:
            self.values = values

    def init_attribute_values_(self):
        # init default values of attributes
        for cl in self.classifier.class_path:
            for attrName, attr in cl.attributes_.items():
                if attr.default is not None:
                    if self.get_value(attrName, cl) is None:
                        self.set_value(attrName, attr.default, cl)

    @property
    def class_object_class(self):
        """CClass: Getter for the class that has this object as a class object. Returns ``None`` if this
        object is not a class object."""
        return self.class_object_class_

    @property
    def classifier(self):
        """CClassifier: Get/set the classifier of this object. For the setter, changes to the classifier
        (i.e., the association) of a link should not be performed with ``CObject`` methods."""
        return self.classifier_

    @classifier.setter
    def classifier(self, cl):
        if is_clink(self):
            raise CException(
                f"Changes to the classifier (i.e., the association) of a link" +
                " should not be performed with CObject methods")
        check_is_cclass(cl)
        if self.classifier_ is not None:
            self.classifier_.remove_object_(self)
        if cl is not None:
            check_named_element_is_not_deleted(cl)
        self.classifier_ = cl
        self.classifier_.add_object_(self)

    def delete(self):
        """Delete the object and delete it from its classifier. Delete all links of the object.
        Calls ``delete()`` on superclass.

        Returns:
            None
        """
        if self.is_deleted:
            return
        if not (isinstance(self.classifier, CMetaclass) or isinstance(self.classifier, CAssociation)):
            # for class objects, the class cleanup removes the instance
            # link instances are removed by the association
            self.classifier_.remove_object_(self)
        self.classifier_ = None
        super().delete()
        links = self.links_.copy()
        for link in links:
            link.delete()

    def instance_of(self, classifier):
        """Tests whether this object is an instance of ``classifier`` or not.

        Args:
            classifier (CClassifier): The classifier to test against.

        Returns:
            bool: The result of the test.

        """
        if self.classifier is None:
            return False
        if classifier is None:
            raise CException(f"'None' is not a valid argument")
        if is_clink(self):
            # noinspection PyUnresolvedReferences
            if self.is_class_link():
                if not (is_cmetaclass(classifier) or is_cassociation(classifier)):
                    raise CException(f"'{classifier!s}' is not an association or a metaclass")
            else:
                if not (is_cclass(classifier) or is_cassociation(classifier)):
                    raise CException(f"'{classifier!s}' is not an association or a class")
        else:
            if isinstance(self.classifier, CMetaclass):
                # this is a class object
                if not is_cmetaclass(classifier):
                    raise CException(f"'{classifier!s}' is not a metaclass")
            else:
                if not is_cclass(classifier):
                    raise CException(f"'{classifier!s}' is not a class")

        if self.classifier == classifier:
            return True
        if classifier in self.classifier.all_superclasses:
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
        """Get the value of an attribute with the given ``attribute_name``. Optionally the classifier
        to consider can be specified. This is needed, if one or more attributes of the same name are defined
        on the inheritance hierarchy. Then a shadowed attribute can be accessed by specifying its classifier.

        Args:
            attribute_name: The name of the attribute.
            classifier: The optional classifier on which the attribute is defined.

        Returns:
            Supported Attribute Types: Value of the attribute.
        """
        if self.is_deleted:
            raise CException(f"can't get value '{attribute_name!s}' on deleted {self._get_kind_str()!s}")
        return get_var_value(self, self.classifier.class_path, self.attribute_values, attribute_name,
                             VarValueKind.ATTRIBUTE_VALUE, classifier)

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
        if self.is_deleted:
            raise CException(f"can't delete value '{attribute_name!s}' on deleted {self._get_kind_str()!s}")
        return delete_var_value(self, self.classifier.class_path, self.attribute_values, attribute_name,
                                VarValueKind.ATTRIBUTE_VALUE, classifier)

    def set_value(self, attribute_name, value, classifier=None):
        """Set the value of an attribute with the given ``attribute_name`` to ``value``. Optionally the classifier
        to consider can be specified. This is needed, if one or more attributes of the same name are defined
        on the inheritance hierarchy. Then a shadowed attribute can be accessed by specifying its classifier.

        Args:
            attribute_name: The name of the attribute.
            value: The new value.
            classifier: The optional classifier on which the attribute is defined.

        Returns:
            ``None``
        """
        if self.is_deleted:
            raise CException(f"can't set value '{attribute_name!s}' on deleted {self._get_kind_str()!s}")
        set_var_value(self, self.classifier.class_path, self.attribute_values, attribute_name, value,
                      VarValueKind.ATTRIBUTE_VALUE, classifier)

    @property
    def values(self):
        """dict[str, value]: Getter for getting all values of the object using a dict, and setter of setting
        all values of the object based on a dict. The dict uses key/value pairs.
        The value types must conform to the types defined for the attributes.
        """
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
        """list[CLink]: Getter for getting the links defined for this object. Object links are based on the
        associations defined for the object's class."""
        return list(self.links_)

    @property
    def linked(self):
        """list[CObject]: Getter for getting the linked objects defined for this object."""
        result = []
        for link in self.links_:
            opposite = link.get_opposite_object(self)
            if opposite.class_object_class_ is None:
                result.append(opposite)
            else:
                result.append(opposite.class_object_class_)
        return result

    def get_links_for_association(self, association):
        """
        Method to get all link objects which are defined based on the given association.

        Args:
            association: Association used to filter the links.

        Returns:
            list[CLink]: The list of link objects.

        """
        association_links = []
        for link in list(self.links_):
            if link.association == association:
                association_links.extend([link])
        return association_links

    def get_linked(self, **kwargs):
        """Method to get the linked objects defined for this object filtered using criteria specified in kwargs.

        Args:
            **kwargs:
                Defines filter criteria.

                - ``association``:
                    Include links only if they are based on the specified association.
                - ``role_name``:
                    Include links only if they are based on an associations having the specified role name
                    either as a target or source role name.

        Returns:
            list[CObject]: List of linked objects

        """
        from codeable_models.clink import LinkKeywordsContext
        context = LinkKeywordsContext(**kwargs)

        result = []
        for link in self.links_:
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
        """
        Add links on this object (which are based on associations defined on the object's class).
        Uses the function  :py:func:`.add_links`. That is, it is possible to use the following equivalently::

            add_links({<this_object>: <links>}, <**kwargs>)

        Args:
            links: The new links to be defined.
            **kwargs: Any keyword arg acceptable to :py:func:`.add_links`.

        Returns:
            list[CLink]: List of created link objects.

        """
        from codeable_models.clink import add_links
        return add_links({self: links}, **kwargs)

    def delete_links(self, links, **kwargs):
        """
        Delete links on this object (which are based on associations defined on the object's class).
        Uses the function  :py:func:`.delete_links`. That is, it is possible
        to use the following equivalently::

            delete_links({<this_object>: <links>}, <**kwargs>)

        Args:
            links: The links to be deleted.
            **kwargs: Any keyword arg acceptable to :py:func:`.delete_links`.

        Returns:
            list[CLink]: List of deleted link objects.

        """
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
