from codeable_models.cattribute import CAttribute
from codeable_models.cbundlable import CBundlable
from codeable_models.cenum import CEnum
from codeable_models.internal.commons import *


class CClassifier(CBundlable):
    def __init__(self, name=None, **kwargs):
        """``CClassifier`` is superclass of classifiers such as :py:class:`.CClass` and :py:class:`.CMetaclass`
        defining common features for
        classifiers. The class is usually not used directly but its features are used from the subclasses.

        **Superclasses:**  :py:class:`.CBundlable`

        Args:
           name (str): An optional name.
           **kwargs: Pass in any kwargs acceptable to superclasses. In addition, ``CClassifier`` accepts:
                ``attributes``, ``superclasses``.

                - The ``attributes`` kwarg accepts a dict of attributes in the form acceptable
                  to the ``attributes`` property.
                - The ``superclasses`` kwarg accepts a list of superclasses in the form
                  acceptable to the ``superclasses`` property.

        **Examples:**

        The following code uses the ``superclasses`` and ``attributes`` features of ``CClassifier`` during
        a class definition and then uses the ``association`` feature to define an association for a class::

            customer = CClass(domain_metaclass, "Customer", superclasses=person, attributes={
                "id": str,
                "shipping addresses": [],
            })

            customer.association(cart, "shops with: [customer] 1 <*>- [cart] 1")

        **Main Relations:**

        The main relations of ``CClassifier`` are shown in the figure below.

        .. image:: ../images/classifier_model.png

        As can be seen,  :py:class:`.CClass`, :py:class:`.CMetaclass`, and :py:class:`.CStereotype` are
        classifiers, as could be expected.
        In addition, :py:class:`.CAssociation` is a classifier, which might be a less obvious design choice. It is
        a classifier, so that a :py:class:`.CLink` can be an object. That is, the association is the classifier
        of the link. This way links can be referenced and treated as objects.

        The associations, attributes, and inheritance hierarchy of a classifier are managed by
        the methods of ``CClassifier``.

        """
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
        """dict[str, CAttribute | Attribute Type | Default Value] : Property that gets the list of attributes
        of a classifier or sets them using a dictionary.

        All attributes are internally stored as :py:class:`.CAttribute` objects. The getter returns the list of
        all attributes as :py:class:`.CAttribute` objects.

        For the setter, ``None`` or ``{}`` can be used to remove all attributes from the classifier.

        Each attribute in the dict is specified using the form:

        .. code-block:: none

             attributeName: <type|default-value|CAttribute>

        Possible types of attributes are:

            - ``bool``: a boolean
            - ``int``: an integer
            - ``float``: a floating point number
            - ``str``: a string
            - ``list``: a Python list
            - enumeration values: An object of type :py:class:`.CEnum` is the type and enumeration values are used
              as attribute values.
            - objects: A class of type :py:class:`.CClassifier` is the type and :py:class:`.CObject`'s are used as
              attribute values. Please note this might be :py:class:`.CClass` as a type
              with :py:class:`.CObject` objects, or
              :py:class:`.CMetaclass` as a type with :py:class:`.CClass` objects.
            - ``CAttribute`` objects: An :py:class:`.CAttribute` object describes an attribute, i.e., its type and
              default value.

        **Example:** The following code initialized one ``int`` and one ``bool`` attribute,
        each with a default value,
        and it defines another string attribute using the ``str`` type::

            game = CClass(metaclass, "Game", attributes={
                "number_of_players": 1,
                "game_started": False,
                "player_id": str
            })

        ``game.attributes`` returns the list of attributes as :py:class:`.CAttribute` objects.

        More examples are provided in the document :ref:`class_attributes`.
        """
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
        """list[str]: Returns a list of all attribute names defined for this classifier.

        Examples are provided in the document :ref:`class_attributes`.
        """
        return list(self.attributes_.keys())

    def get_attribute(self, attribute_name):
        """Returns the :py:class:`.CAttribute` object that conforms to the provided attribute name. If none is found,
        ``None`` is returned.

        Examples are provided in the document :ref:`class_attributes`.

        Returns:
            CAttribute: The attribute conforming to the attribute name.
        """
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
        """list[CClassifier]: Getter that returns the subclasses of this classifier."""
        return list(self.subclasses_)

    @property
    def superclasses(self):
        """list[CClassifier]: Setter to set and getter to return the superclasses of
        this classifier."""
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
                    if self.is_metaclass_association_():
                        if not is_cmetaclass(scl) or (is_cassociation(scl) and scl.is_metaclass_association_()):
                            raise CException(f"cannot add superclass '{scl!s}':" +
                                             " not a metaclass or metaclass association")
                    else:
                        if not is_cclass(scl) or (is_cassociation(scl) and not scl.is_metaclass_association_()):
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
        """list[CClassifier]: Getter that returns all superclasses of this classifier
        on the inheritance hierarchy."""
        return self.get_all_superclasses_()

    @property
    def all_subclasses(self):
        """list[CClassifier]: Getter that returns all subclasses of this classifier
        on the inheritance hierarchy."""
        return self.get_all_subclasses_()

    def is_classifier_of_type(self, classifier):
        """Checks if the classifier conforms to the provided classifier's type.

        Args:
            classifier: A :py:class:`.CClassifier` to check against.

        Returns:
            bool: Boolean result of the check.

        """
        type_classifiers = classifier.all_subclasses
        type_classifiers.add(classifier)
        if self in type_classifiers:
            return True
        return False

    def get_all_superclasses_(self, iterated_classes=None):
        if iterated_classes is None:
            iterated_classes = set()
        result = set()
        for sc in self.superclasses:
            if sc not in iterated_classes:
                iterated_classes.add(sc)
                result.add(sc)
                result.update(sc.get_all_superclasses_(iterated_classes))
        return result

    def get_all_subclasses_(self, iterated_classes=None):
        if iterated_classes is None:
            iterated_classes = set()
        result = set()
        for sc in self.subclasses:
            if sc not in iterated_classes:
                iterated_classes.add(sc)
                result.add(sc)
                result.update(sc.get_all_subclasses_(iterated_classes))
        return result

    def has_subclass(self, classifier):
        """Returns ``True`` if ``classifier`` is subclass of this classifier, else ``False``.

        Args:
            classifier: The classifier to test.

        Returns:
            bool: Boolean result of the check

        """
        return classifier in self.get_all_subclasses_()

    def has_superclass(self, classifier):
        """Returns ``True`` if ``classifier`` is superclass of this classifier, else ``False``.

        Args:
            classifier: The classifier to test.

        Returns:
            bool: Boolean result of the check

        """
        return classifier in self.get_all_superclasses_()

    def delete(self):
        """Deletes the classifier, removes superclasses, removes it from subclasses,
        removes all associations and attributes, and removes the classifier from bundles.
        Calls ``delete()`` on superclass.
        """
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
        """list[CAssociation]: Getter listing associations of this classifier."""
        return list(self.associations_)

    @property
    def all_associations(self):
        """list[CAssociation]: Getter listing all associations of this classifier including those
        of superclasses."""
        all_associations = self.associations
        for sc in self.all_superclasses:
            for a in sc.associations:
                if a not in all_associations:
                    all_associations.extend([a])
        return all_associations

    def association(self, target, descriptor=None, **kwargs):
        """Method used to create associations on this classifier.
        Returns the :py:class:`.CAssociation` that is created.

        Args:
            target: The association target classifier.
            descriptor: An optional descriptor making it easier to define associations with a simple string.
            **kwargs: Accepts all keyword arguments acceptable to :py:class:`.CAssociation` to define associations.

        Returns:
            CAssociation: The created association.

        For explanation of descriptor syntax and supported keyword arguments see documentation of the
        constructor of :py:class:`.CAssociation`.

        """
        from codeable_models.cassociation import CAssociation
        return CAssociation(self, target, descriptor, **kwargs)

    def compute_connected_(self, context):
        super().compute_connected_(context)
        connected_candidates = []
        connected = []
        for association in self.associations:
            connected_candidates.append(association.get_opposite_classifier(self))
        connected_candidates = self.superclasses + self.subclasses + connected_candidates
        for c in connected_candidates:
            if c not in context.stop_elements_exclusive:
                connected.append(c)
        self.append_connected_(context, connected)

    # get class path starting from this classifier, including this classifier
    def get_class_path_(self):
        class_path = [self]
        for sc in self.superclasses:
            for cl in sc.get_class_path_():
                if cl not in class_path:
                    class_path.append(cl)
        return class_path

    @property
    def class_path(self):
        """list[CClassifier]: Superclasses are processed using a linerarized class path.
        This path unambiguously orders the superclasses for each classifier, from lower-level to higher-level
        classes. At the same level, classes will be ordered in the same order as specified in the ``superclasses``
        definitions. If a classifier appears multiple times on the class path, i.e. it is reachable via
        different paths, the first appearance is chosen.

        This getter returns all superclasses in the order of the class path.
        """
        return self.get_class_path_()
