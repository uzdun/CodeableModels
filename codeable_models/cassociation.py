import re

from codeable_models.cexception import CException
from codeable_models.cclassifier import CClassifier
from codeable_models.internal.commons import is_cmetaclass, is_cstereotype, is_cassociation, check_is_cmetaclass, \
    check_is_cclass
from codeable_models.internal.stereotype_holders import CStereotypesHolder, CStereotypeInstancesHolder
from codeable_models.internal.var_values import get_var_value, VarValueKind, delete_var_value, set_var_value, \
    get_var_values, set_var_values


def _check_for_classifier_and_role_name_match(classifier, role_name, association_classifier, association_role_name):
    if classifier is None and role_name is None:
        return False
    matches = True
    if role_name is not None:
        if role_name != association_role_name:
            matches = False
    if matches and classifier is not None:
        if not classifier.is_classifier_of_type(association_classifier):
            matches = False
    if matches:
        return True
    return False


class CAssociation(CClassifier):
    STAR_MULTIPLICITY = -1

    def __init__(self, source, target, descriptor=None, **kwargs):
        """
        ``CAssociation`` is used for representing associations. Usually associations are created using the
        ``association`` method of :py:class:`.CClassifier` which calls the constructor of ``CAssociation``
        to actually create the association (i.e., ``CAssociation`` could also be used directly).

        **Superclasses:**  :py:class:`.CClassifier`

        Args:
            source (:py:class:`.CClassifier`): The source classifier of the association.
            target (:py:class:`.CClassifier`): The target classifier of the association.
            descriptor: An optional descriptor making it easier to define associations with a simple string. The
                descriptor syntax is described below.
            **kwargs: Pass in any kwargs acceptable to superclasses. In addition, ``CAssociation`` accepts:
                ``multiplicity``, ``role_name``, ``source_multiplicity``,
                ``source_role_name``, ``aggregation``, ``composition``, ``stereotypes``.

                - ``multiplicity``:
                    Used to provide the target multiplicity of the association. Defaults to ``*``.
                    See documentation of the property ``multiplicity`` for the accepted syntax.
                - ``role_name``:
                    Takes a string specifying the target role name and stores it in the same-named
                    attribute. Defaults to ``None``.
                - ``source_multiplicity``:
                    Used to provide the source multiplicity of the association.
                    Defaults to ``1``. See documentation of the property ``multiplicity``
                    for the accepted syntax.
                - ``source_role_name``:
                    Takes a string specifying the source role name and stores it in the same-named
                    attribute. Defaults to ``None``.
                - ``aggregation``:
                    Takes a boolean argument. If set to ``True``, this association is set to be
                    an aggregation, else it is not. Also, if set to ``True``, it sets the property
                    ``composition`` to ``False``.
                - ``composition``:
                    Takes a boolean argument. If set to ``True``, this association is set to be
                    a composition,  else it is not. Also, if set to ``True``, it sets the property
                    ``aggregation`` to ``False``.
                - ``stereotypes``:
                    Takes a single or a list of :py:class:`.CStereotype` objects which extend this
                    association. Extension is only possible, if this association is an association
                    between meta-classes.

        Attributes:
            role_name: A string specifying the target role name.
            source_role_name: A string specifying the source role name.

        Please note that the  ``name`` property derived from :py:class:`.CNamedElement`
        is interpreted as the label of the association.

        **Descriptor Syntax:**

        The ``descriptor`` has the following syntax:

        .. code-block:: none

            ?<label>:? \\
                ?[<source_role_name>]? <source_multiplicity> ->|<>-|<*>- \\
                ?[<target_role_name>]? <target_multiplicity>

        With it, first the label of the association can be optionally specified.
        Source and target multiplicity strings, in the same form as accepted by the ``multiplicity``
        property, must be specified, too.
        They are divided by an arrow determining the type of association: ``->`` for ordinary
        associations, ``<>-`` for aggregations, and ``<*>-`` for compositions.
        Optionally in square brackets the source and target role names can be specified right before
        the multiplicities.

        Please note that first the keyword arguments are evaluated and then the descriptor. So the descriptor
        would override settings made in the keyword arguments.

        **Examples:**

        The following specifies a ``0..1`` to ``*`` association from a class ``cart`` to a class ``item`` labelled
        ``in cart`` with source role name ``cart`` and target role name ``item in cart``::

            cart.association(item, "in cart: [cart] 0..1 -> [item in cart] *")

        The same can be specified more verbosely with kwargs::

            cart.association(item, name="in cart", role_name="item in cart", multiplicity="*",
                 source_role_name="cart", source_multiplicity="0..1")


        **Main Relations:**

        The main relations of ``CAssociation`` are shown in the figure below.

        .. image:: ../images/association_model.png

        A ``CAssociation`` is need in order to derive :py:class:`.CLink` objects, which link objects
        in an object model.  The ``CAssociation`` is  the classifier of the  :py:class:`.CLink`.

        As can be seen,  a ``CAssociation`` can be extended by stereotypes. A :py:class:`.CLink` can have
        stereotype instances of any :py:class:`.CStereotype` defined on the link's association.

        The :py:class:`.CClassifier` can be introspected for its ``associations``. The association stores its ``source``
        and ``target`` classifiers.

        """
        self.source = source
        self.target = target
        self.role_name = None
        self.source_role_name = None
        self.source_multiplicity_ = "1"
        self.source_lower_multiplicity = 1
        self.source_upper_multiplicity = 1
        self.multiplicity_ = "*"
        self.lower_multiplicity = 0
        self.upper_multiplicity = self.STAR_MULTIPLICITY
        self.aggregation_ = False
        self.composition_ = False
        self.stereotypes_holder = CStereotypesHolder(self)
        self.derived_from_ = None
        self.derived_associations_ = []
        self.stereotype_instances_holder = CStereotypeInstancesHolder(self)
        self.tagged_values_ = {}
        # we set the name here already so that either the name=... name or the descriptor name go into
        # super().__init__(self.name, ...)
        self.name = kwargs.pop("name", None)
        self.ends = None
        if descriptor is not None:
            # note that descriptor might overwrite self.name, if it has the form "name: ..."
            self._eval_descriptor(descriptor)
        super().__init__(self.name, **kwargs)

        source.associations_.append(self)
        if source != target:
            target.associations_.append(self)

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.extend(["multiplicity", "role_name", "source_multiplicity",
                                   "source_role_name", "aggregation", "composition", "stereotypes",
                                   "derived_from", "stereotype_instances", "tagged_values"])
        super()._init_keyword_args(legal_keyword_args, **kwargs)

    def __str__(self):
        return super(CAssociation, self).__str__()

    def __repr__(self):
        name = ""
        if self.name is not None:
            name = self.name
        return f"CAssociation name = {name!s}, source = {self.source!s} -> target = {self.target!s}"

    def get_opposite_classifier(self, classifier):
        """Given a classifier, this method returns the opposite in the association,
        i.e. the source if ``classifier`` is the
        target, and vice versa. Raises an exception if ``classifier`` is neither source nor target.

        Args:
            classifier: The classifier from which we want to get the opposite in the association.

        Returns:
            CClassifier: The opposite classifier.

        """
        if classifier == self.source:
            return self.target
        elif classifier == self.target:
            return self.source
        else:
            raise CException("can only get opposite if either source or target classifier is provided")

    def is_metaclass_association_(self):
        if is_cmetaclass(self.source):
            return True
        return False

    def matches_target_(self, classifier, role_name):
        return _check_for_classifier_and_role_name_match(classifier, role_name, self.target, self.role_name)

    def matches_source_(self, classifier, role_name):
        return _check_for_classifier_and_role_name_match(classifier, role_name, self.source, self.source_role_name)

    @property
    def aggregation(self):
        """bool: Takes a boolean argument. If set to ``True``, this association is set to be
        an aggregation, else it is not. Also, if set to ``True``, it sets the property ``composition`` to ``False``."""
        return self.aggregation_

    @aggregation.setter
    def aggregation(self, aggregation):
        if aggregation:
            self.composition_ = False
        self.aggregation_ = aggregation

    @property
    def composition(self):
        """bool: Takes a boolean argument. If set to ``True``, this association is set to be
        a composition,  else it is not. Also, if set to ``True``, it sets the property ``aggregation`` to ``False``."""
        return self.composition_

    @composition.setter
    def composition(self, composition):
        if composition:
            self.aggregation_ = False
        self.composition_ = composition

    def _set_multiplicity(self, multiplicity, is_target_multiplicity):
        if not isinstance(multiplicity, str):
            raise CException("multiplicity must be provided as a string")

        try:
            dots_pos = multiplicity.find("..")
            if dots_pos != -1:
                lower_match = multiplicity[:dots_pos]
                upper_match = multiplicity[dots_pos + 2:]
                lower = int(lower_match)
                if lower < 0:
                    raise CException(f"negative multiplicity in '{multiplicity!s}'")
                if upper_match.strip() == "*":
                    upper = self.STAR_MULTIPLICITY
                else:
                    upper = int(upper_match)
                    if lower < 0 or upper < 0:
                        raise CException(f"negative multiplicity in '{multiplicity!s}'")
            elif multiplicity.strip() == "*":
                lower = 0
                upper = self.STAR_MULTIPLICITY
            else:
                lower = int(multiplicity)
                if lower < 0:
                    raise CException(f"negative multiplicity in '{multiplicity!s}'")
                upper = lower
        except Exception as e:
            if isinstance(e, CException):
                raise e
            raise CException(f"malformed multiplicity: '{multiplicity!s}'")

        if is_target_multiplicity:
            self.upper_multiplicity = upper
            self.lower_multiplicity = lower
        else:
            self.source_upper_multiplicity = upper
            self.source_lower_multiplicity = lower

    @property
    def multiplicity(self):
        """str: Getter and setter for the target multiplicity of the association. The multiplicity string
        has the following syntax: ``<lower_multiplicity>..<higher_multiplicity>|<single_multiplicity>``.

        The multiplicity is either specified as a range or using a ``<single_multiplicity>``. Accepted
        ``<single_multiplicity>`` values are any positive number, zero, or ``*``.  ``*`` denotes
        unbounded multiplicity.

        For multiplicity ranges, ``<lower_multiplicity>`` is zero or any positive number specifying the lower end
        of the accepted multiplicity range. ``<higher_multiplicity>``
        is a number specifying the higher end of the accepted multiplicity range. It must be higher than
        ``<lower_multiplicity>``. It can also be ``*`` meaning
        unbounded higher multiplicity.

        ``*`` multiplicity is equal to the range ``0..*``.
        """
        return self.multiplicity_

    @multiplicity.setter
    def multiplicity(self, multiplicity):
        self.multiplicity_ = multiplicity
        self._set_multiplicity(multiplicity, True)

    @property
    def source_multiplicity(self):
        """str: Getter and setter for the source multiplicity of the association. Syntax is equal to the syntax
        defined in the documentation of the ``multiplicity`` property."""
        return self.source_multiplicity_

    @source_multiplicity.setter
    def source_multiplicity(self, multiplicity):
        self.source_multiplicity_ = multiplicity
        self._set_multiplicity(multiplicity, False)

    @property
    def stereotypes(self):
        """CStereotype|list[CStereotype]: The setter takes a single or a list of :py:class:`.CStereotype`
        objects which extend this association. Extension is only possible, if this association is an association
        between meta-classes. The getter returns the stereotypes that extend this association."""
        return self.stereotypes_holder.stereotypes

    @stereotypes.setter
    def stereotypes(self, elements):
        if not self.is_metaclass_association_():
            raise CException("stereotypes on associations can only be defined for metaclass associations")
        self.stereotypes_holder.stereotypes = elements

    @property
    def stereotype_instances(self):
        """list[CStereotype]|CStereotype: Getter to get and setter to set the stereotype instances of this association.

        The stereotype instances must be stereotypes extending an association that this association is derived from.

        The setter takes a list of stereotype instances or a single stereotype instance as argument.
        The getter always returns a list.
        """
        return self.stereotype_instances_holder.stereotypes

    @stereotype_instances.setter
    def stereotype_instances(self, elements):
        self.stereotype_instances_holder.stereotypes = elements

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
            raise CException(f"can't get tagged value '{name!s}' on deleted link")
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
            raise CException(f"can't delete tagged value '{name!s}' on deleted link")
        return delete_var_value(self, self.stereotype_instances_holder.get_stereotype_instance_path(),
                                self.tagged_values_, name, VarValueKind.TAGGED_VALUE, stereotype)

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
            raise CException(f"can't set tagged value '{name!s}' on deleted link")
        return set_var_value(self, self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_,
                             name, value, VarValueKind.TAGGED_VALUE, stereotype)

    @property
    def tagged_values(self):
        """dict[str, value]: Getter for getting all tagged values of the association using a dict, and setter of
        setting all tagged values of the association based on a dict. The dict uses key/value pairs.
        The value types must conform to the types defined for the attributes.
        """
        if self.is_deleted:
            raise CException("can't get tagged values on deleted link")
        return get_var_values(self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_)

    @tagged_values.setter
    def tagged_values(self, new_values):
        if self.is_deleted:
            raise CException("can't set tagged values on deleted link")
        set_var_values(self, new_values, VarValueKind.TAGGED_VALUE)

    @staticmethod
    def _check_association_class_derived_from_association_metaclass(class_, metaclass_, direction_string):
        try:
            check_is_cclass(class_)
        except CException:
            raise CException("association 'derived_from' is called on is not a class-level association")
        try:
            check_is_cmetaclass(metaclass_)
        except CException:
            raise CException("association used as 'derived_from' parameter is not a metaclass-level association")

        if not class_.metaclass.is_classifier_of_type(metaclass_):
            raise CException(f"association {direction_string!s} class '{class_!s}' is not " +
                             f"derived {direction_string!s} metaclass '{metaclass_!s}'")

    def check_derived_association_multiplicities_(self, metaclass_association, add_to_source_upper=0,
                                                  add_to_upper=0):
        # Before we can check the multiplicities we need to collect other derived associations of the
        # same kind (= same classes or their superclasses are used, derived from the same metaclass association).
        # All their upper multiplicities and upper source multiplicities need to be added to the
        # upper multiplicities and upper source multiplicities of self, respectively.
        # For example, an consider a meta-class association
        #   a = m1.association(m2, "a: [m1] * -> [m2] 1")
        # If we would derive two associations from it:
        #   c1.association(c2, "a1: [c1] * -> [c2] 1", derived_from=a)
        #   c1.association(c2, "a1: [c1] * -> [c2] 1", derived_from=a)
        # without adding up the multiplicities, an upper (target) multiplicity of 2 could be reached, violating
        # the meta-class target upper multiplicity of 1.
        other_derived_associations_requiring_checking = []
        source_upper_multiplicity = self.source_upper_multiplicity + add_to_source_upper
        if add_to_source_upper == CAssociation.STAR_MULTIPLICITY:
            source_upper_multiplicity = CAssociation.STAR_MULTIPLICITY
        upper_multiplicity = self.upper_multiplicity + add_to_upper
        if add_to_upper == CAssociation.STAR_MULTIPLICITY:
            upper_multiplicity = CAssociation.STAR_MULTIPLICITY

        for derived_association in metaclass_association.derived_associations:
            if derived_association == self:
                continue
            if self.source in derived_association.source.class_path and \
                    self.target in derived_association.target.class_path:
                if upper_multiplicity != CAssociation.STAR_MULTIPLICITY:
                    if derived_association.upper_multiplicity == CAssociation.STAR_MULTIPLICITY:
                        upper_multiplicity = CAssociation.STAR_MULTIPLICITY
                    else:
                        upper_multiplicity += derived_association.upper_multiplicity
                if source_upper_multiplicity != CAssociation.STAR_MULTIPLICITY:
                    if derived_association.source_upper_multiplicity == CAssociation.STAR_MULTIPLICITY:
                        source_upper_multiplicity = CAssociation.STAR_MULTIPLICITY
                    else:
                        source_upper_multiplicity += derived_association.source_upper_multiplicity

            # if the derived association is composed out of superclasses of self's source and target,
            # it needs to be checked, too; else we might add a violation by adding the superclass association
            # later on, e.g. on a metaclass association:
            #         a = self.m1.association(self.m2, "a: [m1] 1 -> [m2] *")
            # we add an unproblematic association:
            #         c1_c2 = c1.association(c2, "a2: [c1] 1 -> [c2] *", derived_from=a)
            # but, by adding another association that is composed out of superclasses of self's source and target,
            # a violation is created:
            #        c3.association(c4, "a1: [c3] 1 -> [c4] *", derived_from=a)
            if derived_association.source in self.source.all_superclasses and \
                    derived_association.target in self.target.all_superclasses:
                other_derived_associations_requiring_checking.append(derived_association)

        # Check each multiplicity value (lower and upper for source and target multiplicities)
        if self.lower_multiplicity < metaclass_association.lower_multiplicity:
            raise CException(f"lower multiplicity '{self.lower_multiplicity!s}' smaller than metaclass' lower " +
                             f"multiplicity '{metaclass_association.lower_multiplicity!s}' " +
                             "this association is derived from")
        if metaclass_association.upper_multiplicity != CAssociation.STAR_MULTIPLICITY:
            if upper_multiplicity == CAssociation.STAR_MULTIPLICITY or \
                    upper_multiplicity > metaclass_association.upper_multiplicity:
                upper = "*" if upper_multiplicity == self.STAR_MULTIPLICITY else upper_multiplicity
                meta_upper = "*" if metaclass_association.upper_multiplicity == self.STAR_MULTIPLICITY \
                    else metaclass_association.upper_multiplicity
                raise CException(f"upper multiplicity '{upper!s}' (of this association, maybe combined with " +
                                 f"other derived associations of the same kind) is larger than metaclass' upper " +
                                 f"multiplicity '{meta_upper!s}' " +
                                 "this association is derived from")

        if self.source_lower_multiplicity < metaclass_association.source_lower_multiplicity:
            raise CException(f"source lower multiplicity '{self.source_lower_multiplicity!s}' smaller than " +
                             "metaclass' source lower multiplicity " +
                             f"'{metaclass_association.source_lower_multiplicity!s}' this association is derived from")
        if metaclass_association.source_upper_multiplicity != CAssociation.STAR_MULTIPLICITY:
            if source_upper_multiplicity == CAssociation.STAR_MULTIPLICITY or \
                    source_upper_multiplicity > metaclass_association.source_upper_multiplicity:
                upper = "*" if source_upper_multiplicity == self.STAR_MULTIPLICITY else source_upper_multiplicity
                meta_upper = "*" if metaclass_association.source_upper_multiplicity == self.STAR_MULTIPLICITY \
                    else metaclass_association.source_upper_multiplicity
                raise CException(f"source upper multiplicity '{upper!s}' (of this association, maybe combined with " +
                                 f"other derived associations of the same kind) is larger than " +
                                 f"metaclass' source upper multiplicity '{meta_upper!s}' " +
                                 "this association is derived from")

        # perform the check for associations that are composed out of superclasses of self's source and target
        # we need to add self.source_upper_multiplicity and self.upper_multiplicity to the multiplicities,
        # as self is not yet added in derived_from
        for other_association in other_derived_associations_requiring_checking:
            other_association.check_derived_association_multiplicities_(metaclass_association,
                                                                        self.source_upper_multiplicity,
                                                                        self.upper_multiplicity)

    def _check_derived_association_has_same_aggregation_state(self, metaclass_association):
        if metaclass_association.aggregation and not self.aggregation:
            raise CException(f"metaclass association is an aggregation, but derived association is not")
        if self.aggregation and not metaclass_association.aggregation:
            raise CException(f"derived association is an aggregation, but metaclass association is not")
        if metaclass_association.composition and not self.composition:
            raise CException(f"metaclass association is a composition, but derived association is not")
        if self.composition and not metaclass_association.composition:
            raise CException(f"derived association is a composition, but metaclass association is not")

    @property
    def derived_from(self):
        """CAssociation: Getter to get and setter to set a metaclass association this class-level association
        is derived from.

        Please note that parameter has to be a metaclass association, and this association needs to be a
        class-level association. An association can be derived from a metaclass association, if the association
        is of the same type as the metaclass association, i.e., both are
        either ``association``, ``composition``, or ``aggregation``.

        Both for source and target multiplicities,the lower multiplicity must be equal or higher than the
        metaclass association's lower multiplicity, and the upper multiplicity must be equal or lower than
        the metaclass association's upper multiplicity.

        For the upper multiplicities (source and target), we need to consider other derived associations of the
        same kind (i.e., same classes or their superclasses are used, derived from the same metaclass association),
        as well. For example, an consider a meta-class association::

            a = m1.association(m2, "a: [m1] * -> [m2] 1")

        If we would derive two associations from it::

            c1.association(c2, "a1: [c1] * -> [c2] 1", derived_from=a)
            c1.association(c2, "a1: [c1] * -> [c2] 1", derived_from=a)

        without adding up the multiplicities of all those associations, an upper (target) multiplicity of
        2 could be reached, violating the meta-class target upper multiplicity of 1.

        The stereotype instances must be stereotypes extending an association that this association is derived from.

        The setter takes a CAssociation as argument. Can be ``None`` (the default value) to remove the
        ``derived_from`` relation.
        The getter always returns a CAssociation or ``None``.
        """
        return self.derived_from_

    @derived_from.setter
    def derived_from(self, metaclass_association):
        if metaclass_association is not None:
            if not is_cassociation(metaclass_association):
                raise CException(f"'{metaclass_association!s}' is not an association")
            self._check_association_class_derived_from_association_metaclass(self.source, metaclass_association.source,
                                                                             "source")
            self._check_association_class_derived_from_association_metaclass(self.target, metaclass_association.target,
                                                                             "target")

            self.check_derived_association_multiplicities_(metaclass_association)
            self._check_derived_association_has_same_aggregation_state(metaclass_association)

        if self.derived_from_ is not None:
            self.derived_from_.derived_associations_.remove(self)
            self.derived_from_ = None

        self.derived_from_ = metaclass_association
        if metaclass_association is not None:
            metaclass_association.derived_associations_.append(self)

    @property
    def derived_associations(self):
        """list[CAssociation]: Getter for the list of associations this association is derived from."""
        return self.derived_associations_

    def delete(self):
        """Deletes this association. Removes the association from all classifiers, links, and derived associations.
        Removes it from all stereotypes, too. Removes it from associations it is derived from.
        Calls ``delete()`` on superclass.

        Returns:
            None.

        """
        if self.is_deleted:
            return
        if is_cmetaclass(self.source):
            all_instances = self.source.all_classes
        elif is_cstereotype(self.source):
            all_instances = self.source.all_extended_instances
        else:
            all_instances = self.source.all_objects
        for instance in all_instances:
            for link in instance.links:
                link.delete()
        self.source.associations_.remove(self)
        if self.source != self.target:
            self.target.associations_.remove(self)
        for s in self.stereotypes_holder.stereotypes:
            s.extended_.remove(self)
        self.stereotypes_holder.stereotypes_ = []
        for si in self.stereotype_instances:
            si.extended_instances_.remove(self)
        self.stereotype_instances_holder.stereotypes_ = []
        if self.derived_from_ is not None:
            self.derived_from_.derived_associations_.remove(self)
            self.derived_from_ = None
        if self.derived_associations_:
            for a in self.derived_associations_:
                a.derived_from_ = None
            self.derived_associations_ = []
        super().delete()

    def check_multiplicity_(self, obj, actual_length, actual_opposite_length, check_target_multiplicity):
        if check_target_multiplicity:
            upper = self.upper_multiplicity
            lower = self.lower_multiplicity
            other_side_lower = self.source_lower_multiplicity
            multiplicity_string = self.multiplicity_
        else:
            upper = self.source_upper_multiplicity
            lower = self.source_lower_multiplicity
            other_side_lower = self.lower_multiplicity
            multiplicity_string = self.source_multiplicity_

        if (upper != CAssociation.STAR_MULTIPLICITY and actual_length > upper) or actual_length < lower:
            # if there is actually no link as actualOppositeLength is zero, this is ok, if the otherLower 
            # including zero:
            if not (actual_opposite_length == 0 and other_side_lower == 0):
                raise CException(f"links of object '{obj}' have wrong multiplicity " +
                                 f"'{actual_length!s}': should be '{multiplicity_string!s}'")

    def _eval_descriptor(self, descriptor):
        # handle name only if a ':' is found in the descriptor
        index = descriptor.find(":")
        if index != -1:
            name = descriptor[0:index]
            descriptor = descriptor[index + 1:]
            self.name = name.strip()

        # handle type of relation
        aggregation = False
        composition = False
        index = descriptor.find("->")
        length = 2
        if index == -1:
            index = descriptor.find("<>-")
            if index != -1:
                length = 3
                aggregation = True
            else:
                index = descriptor.find("<*>-")
                length = 4
                composition = True
                if index == -1:
                    raise CException("association descriptor malformed: '" + descriptor + "'")

        # handle role names and multiplicities
        source_str = descriptor[0:index]
        target_str = descriptor[index + length:]
        regexp_with_role_name = r'\s*\[([^\]]+)\]\s*(\S*)\s*'
        regexp_only_multiplicity = r'\s*(\S*)\s*'

        m = re.search(regexp_with_role_name, source_str)
        if m is not None:
            self.source_role_name = m.group(1)
            if m.group(2) != '':
                self.source_multiplicity = m.group(2)
        else:
            m = re.search(regexp_only_multiplicity, source_str)
            self.source_multiplicity = m.group(1)

        m = re.search(regexp_with_role_name, target_str)
        if m is not None:
            self.role_name = m.group(1)
            if m.group(2) != '':
                self.multiplicity = m.group(2)
        else:
            m = re.search(regexp_only_multiplicity, target_str)
            self.multiplicity = m.group(1)

        if aggregation:
            self.aggregation = True
        elif composition:
            self.composition = True

    # overridden methods from CClassifier
    @property
    def attributes(self):
        """Overridden method from :py:class:`.CClassifier`. Attributes on associations are not supported."""
        return super().attributes

    def _set_attribute(self, name, value):
        raise CException("setting of attributes not supported for associations")

    @attributes.setter
    def attributes(self, attribute_descriptions):
        raise CException("setting of attributes not supported for associations")
