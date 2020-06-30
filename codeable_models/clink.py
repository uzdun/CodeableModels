from codeable_models.cobject import CObject
from codeable_models.internal.commons import *
from codeable_models.internal.stereotype_holders import CStereotypeInstancesHolder
from codeable_models.internal.var_values import delete_var_value, set_var_value, get_var_value, get_var_values, \
    set_var_values, VarValueKind


class CLink(CObject):
    def __init__(self, association, source_object, target_object, **kwargs):
        """``CLink`` is used to define object links.
        Objects can be linked if their respective classes have an association.
        When linking objects, the association definitions are checked for correctness.
        For example, linking three objects to an object in a 1:1 multiplicity relation, yields an exception.

        **Superclasses:**  :py:class:`.CBundlable`

        Args:
            association (CAssociation): The association that defines the link and is the classifier of this link.
            source_object (CObject): The object from which a link to another object shall be created;
                must be an instance of the respective class in the association.
            target_object (CObject): The object to which a link to another object shall be created;
                must be an instance of the respective class in the association.
            **kwargs: Pass in any kwargs acceptable to superclasses. In addition ``CLink`` accepts
                ``stereotype_instances``:

                - ``stereotype_instances``:
                    Any :py:class:`.CStereotype` extending the association of this class can be defined on the link
                    as a stereotype instance. That is, the list of stereotypes on the association defines the possible
                    stereotypes instances of the link. The kwarg accepts a list of stereotype instances or a single
                    stereotype instance as argument.


        **Examples:**

        The following defines for two cart objects links from the cart to its items via
        the :py:func:`.add_links` function.
        It uses a role name to determine the correct association and association direction::

            new_links = add_links({cart1: [item1, item2],
                                   cart2: [item3, item4, item5]}, role_name="item in cart")

        The list of created ``CLink`` objects is returned.

        The same links could be defined using ``add_links`` on :py:class:`.CObject`::

            new_links_1 = cart1.add_links([item1, item2], role_name="item in cart")
            new_links_2 = cart2.add_links([item3, item4, item5], role_name="item in cart")

        Both calls also return the list of created ``CLink`` objects.


        **Main Relations:**

        The main relations of ``CLink`` are shown in the figure below.

        .. image:: ../images/link_model.png

        Each object can be source or target of a link. Links are only valid, if there is an association between
        the classes of the objects to be linked (and multiplicities are correctly set on
        these associations).

        The association is the classifier of the link (thus it inherits from
        :py:class:`.CClassifier`), and the link is treated as
        an instance of the association (thus it inherits from :py:class:`.CObject`).

        Links can have stereotype instances of the stereotypes defined for the :py:class:`.CAssociation` of the link.

        """

        self.is_deleted = False
        self.source_ = source_object
        self.target_ = target_object
        self.label = None
        self.association = association
        self.stereotype_instances_holder = CStereotypeInstancesHolder(self)
        self.tagged_values_ = {}
        super().__init__(association)
        self._init_keyword_args(**kwargs)

    def __str__(self):
        return f"`CLink source = {self.source_!s} -> target = {self.target_!s}`"

    def __repr__(self):
        result = super().__repr__()
        return f"`CLink {result} source = {self.source_!r} -> target = {self.target_!r}`"

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.append("stereotype_instances")
        set_keyword_args(self, legal_keyword_args, **kwargs)

    def get_opposite_object(self, cobject):
        """Given an object, this method returns the opposite in the link,
        i.e. the source if ``object`` is the
        target, and vice versa. Raises an exception if ``object`` is neither source nor target.

        Args:
            cobject: The object from which we want to get the opposite in the link.

        Returns:
            CObject: The opposite object.

        """
        if is_cclass(cobject):
            cobject = cobject.class_object
        if cobject == self.source_:
            return self.target_
        elif cobject == self.target_:
            return self.source_
        else:
            raise CException("can only get opposite if either source or target object is provided")

    def is_class_link(self):
        """Returns ``True`` if this is a link between classes (class objects), else ``False``.

        Returns:
            bool: Result of the check.

        """
        if is_cclass(self.source) or (self.source.class_object_class is not None):
            return True
        return False

    @property
    def role_name(self):
        """str: Getter for the (target) role name of this link.
        """
        return self.association.role_name

    @property
    def source_role_name(self):
        """str: Getter for the source role name of this link.
        """
        return self.association.source_role_name

    @property
    def source(self):
        """CObject: Getter for the source object of this link.
        """
        if self.source_.class_object_class is not None:
            return self.source_.class_object_class
        return self.source_

    @property
    def target(self):
        """CObject: Getter for the target object of this link.
        """
        if self.target_.class_object_class is not None:
            return self.target_.class_object_class
        return self.target_

    def delete(self):
        """Delete the link, delete it from source and target, and delete its stereotype instances.
        Calls ``delete()`` on superclass.

        Returns:
            None

        """
        if self.is_deleted:
            return
        for si in self.stereotype_instances:
            si.extended_instances_.remove(self)
        self.stereotype_instances_holder.stereotypes_ = []
        if self.source_ != self.target_:
            self.target_.links_.remove(self)
        self.source_.links_.remove(self)
        super().delete()
        self.is_deleted = True

    @property
    def stereotype_instances(self):
        """list[CStereotype]|CStereotype: Getter to get and setter to set the stereotype instances of this link.

        The stereotype instances must be stereotypes extending the association of the link.

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
        """dict[str, value]: Getter for getting all tagged values of the link using a dict, and setter of setting
        all tagged values of the link based on a dict. The dict uses key/value pairs.
        The value types must conform to the types defined for the attributes.
        """
        if self.is_deleted:
            raise CException(f"can't get tagged values on deleted link")
        return get_var_values(self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_)

    @tagged_values.setter
    def tagged_values(self, new_values):
        if self.is_deleted:
            raise CException(f"can't set tagged values on deleted link")
        set_var_values(self, new_values, VarValueKind.TAGGED_VALUE)


def _get_target_objects_from_definition(source_obj, targets):
    if targets is None:
        targets = []
    elif not isinstance(targets, list):
        targets = [targets]
    new_targets = []
    for t in targets:
        is_source_a_class = source_obj.class_object_class is not None
        if is_cclass(t):
            if is_clink(source_obj):
                if not is_cmetaclass(source_obj.association.target):
                    raise CException(f"link target '{t!s}' is a class, but source is a not class link")
            elif not is_source_a_class:
                raise CException(f"link target '{t!s}' is a class, but source is an object")
            new_targets.append(t.class_object_)
        elif is_clink(t):
            if is_cmetaclass(t.association.source):
                if is_clink(source_obj):
                    if not is_cmetaclass(source_obj.association.target):
                        raise CException(f"link target is an class link, but source is an object link")
                elif not is_source_a_class:
                    raise CException(f"link target is a class link, but source is an object")
            else:
                if is_clink(source_obj):
                    if not is_cclass(source_obj.association.target):
                        raise CException(f"link target is an object link, but source is an class link")
                elif is_source_a_class:
                    raise CException(f"link target is an object link, but source is a class")
            new_targets.append(t)
        elif is_cobject(t):
            if is_clink(source_obj):
                if not is_cclass(source_obj.association.target):
                    raise CException(f"link target '{t!s}' is an object, but source is not an object link")
            else:
                if is_source_a_class and t.class_object_class is None:
                    raise CException(f"link target '{t!s}' is an object, but source is a class")
                if not is_source_a_class and t.class_object_class is not None:
                    raise CException(f"link target '{t!s}' is a class, but source is an object")
            new_targets.append(t)
        else:
            raise CException(f"link target '{t!s}' is not an object, class, or link")
    return new_targets


def _check_link_definition_and_replace_classes(link_definitions):
    if not isinstance(link_definitions, dict):
        raise CException("link definitions should be of the form " +
                         "{<link source 1>: <link target(s) 1>, ..., <link source n>: <link target(s) n>}")

    new_definitions = {}
    for source in link_definitions:
        source_obj = source
        if source is None or source == []:
            raise CException("link should not contain an empty source")
        if is_cclass(source):
            source_obj = source.class_object_
        elif not is_cobject(source):
            raise CException(f"link source '{source!s}' is not an object, class, or link")
        targets = _get_target_objects_from_definition(source_obj, link_definitions[source])
        new_definitions[source_obj] = targets

    return new_definitions


def _determine_matching_association_and_set_context_info(context, source, targets):
    if source.class_object_class is not None:
        target_classifier_candidates = get_common_metaclasses(
            [co.class_object_class if not is_clink(co) else co for co in targets])
        context.sourceClassifier = source.class_object_class.metaclass
    else:
        target_classifier_candidates = [get_common_classifier(targets)]
        context.sourceClassifier = source.classifier

    if context.association is not None and context.target_classifier is None:
        if context.sourceClassifier.is_classifier_of_type(context.association.source):
            target_classifier_candidates = [context.association.target]
            context.sourceClassifier = context.association.source
        elif context.sourceClassifier.is_classifier_of_type(context.association.target):
            target_classifier_candidates = [context.association.source]
            context.sourceClassifier = context.association.target

    associations = context.sourceClassifier.all_associations
    if context.association is not None:
        associations = [context.association]
    matches_association_order = []
    matches_reverse_association_order = []
    matching_classifier = None

    for association in associations:
        for target_classifierCandidate in target_classifier_candidates:
            if (association.matches_target_(target_classifierCandidate, context.role_name) and
                    association.matches_source_(context.sourceClassifier, None)):
                matches_association_order.append(association)
                matching_classifier = target_classifierCandidate
            elif (association.matches_source_(target_classifierCandidate, context.role_name) and
                  association.matches_target_(context.sourceClassifier, None)):
                matches_reverse_association_order.append(association)
                matching_classifier = target_classifierCandidate
    matches = len(matches_association_order) + len(matches_reverse_association_order)
    if matches == 1:
        if len(matches_association_order) == 1:
            context.association = matches_association_order[0]
            context.matchesInOrder[source] = True
        else:
            context.association = matches_reverse_association_order[0]
            context.matchesInOrder[source] = False
        context.target_classifier = matching_classifier
    elif matches == 0:
        raise CException(f"matching association not found for source '{source!s}' " +
                         f"and targets '{[str(item) for item in targets]!s}'")
    else:
        raise CException(
            f"link specification ambiguous, multiple matching associations found for source '{source!s}' " +
            f"and targets '{[str(item) for item in targets]!s}'")


def link_objects_(context, source, targets):
    new_links = []
    source_obj = source
    if is_cclass(source):
        source_obj = source.class_object_
    for t in targets:
        target = t
        if is_cclass(t):
            target = t.class_object_

        source_for_link = source_obj
        target_for_link = target
        if not context.matchesInOrder[source_obj]:
            source_for_link = target
            target_for_link = source_obj
        for existingLink in source_obj.links_:
            if (existingLink.source_ == source_for_link and existingLink.target_ == target_for_link
                    and existingLink.association == context.association):
                for link in new_links:
                    link.delete()
                raise CException(
                    f"trying to link the same link twice '{source!s} -> {target!s}'' twice for the same association")
        link = CLink(context.association, source_for_link, target_for_link)
        if context.label is not None:
            link.label = context.label

        new_links.append(link)
        source_obj.links_.append(link)
        # for links from this object to itself, store only one link object
        if source_obj != target:
            target.links_.append(link)
        if context.stereotype_instances is not None:
            link.stereotype_instances = context.stereotype_instances
        if context.tagged_values is not None:
            link.tagged_values = context.tagged_values
    return new_links


def remove_links_for_associations_(context, source, targets):
    if source not in context.objectLinksHaveBeenRemoved:
        context.objectLinksHaveBeenRemoved.append(source)
        for link in source.get_links_for_association(context.association):
            link.delete()
    for target in targets:
        if target not in context.objectLinksHaveBeenRemoved:
            context.objectLinksHaveBeenRemoved.append(target)
            for link in target.get_links_for_association(context.association):
                link.delete()


def set_links(link_definitions, do_add_links=False, **kwargs):
    """
    Sets multiple links by first deleting all existing links on the objects to be used in the links and then
    adding the links in the ``link_definitions`` with the same functionality as the :py:func:`.add_links` function.

    As links get deleted first, please use ``set_links()`` with care. Use of :py:func:`.add_links` (and maybe deleting
    only selected links) can be safer.

    Args:
        link_definitions (dict): A dict of link definitions as explained before.
        do_add_links: Optional parameter, used to only add links, without prior deletion. Defaults to False.
        **kwargs: The same keyword arguments as accepted by the :py:func:`.add_links` function.

    Returns:
        List[CLink]: List of newly created links.

    """
    context = LinkKeywordsContext(**kwargs)
    link_definitions = _check_link_definition_and_replace_classes(link_definitions)

    new_links = []
    for source in link_definitions:
        if source.is_deleted:
            raise CException("cannot link to deleted source")
        targets = link_definitions[source]
        for target in targets:
            if target.is_deleted:
                raise CException("cannot link to deleted target")

        _determine_matching_association_and_set_context_info(context, source, targets)
        if not do_add_links:
            remove_links_for_associations_(context, source, targets)
        try:
            new_links.extend(link_objects_(context, source, targets))
        except CException as e:
            for link in new_links:
                link.delete()
            raise e
    try:
        for source in link_definitions:
            targets = link_definitions[source]
            source_len = len(source.get_links_for_association(context.association))
            if len(targets) == 0:
                context.association.check_multiplicity_(source, source_len, 0, context.matchesInOrder[source])
            else:
                for target in targets:
                    target_len = len(target.get_links_for_association(context.association))
                    context.association.check_multiplicity_(source, source_len, target_len,
                                                            context.matchesInOrder[source])
                    context.association.check_multiplicity_(target, target_len, source_len,
                                                            not context.matchesInOrder[source])
    except CException as e:
        for link in new_links:
            link.delete()
        raise e
    return new_links


def add_links(link_definitions, **kwargs):
    """
    Function used to add multiple links at once, maybe to different source objects. The function takes
    a dict of link definitions. With it multiple links can be specified at once. It also supports
    association and role name specifications in the keyword args.
    If those are used, only one kind of link can be specified with one :py:func:`.add_links` call.

    For example, we can use this function to define the links between items and their carts::

            new_links = add_links({cart1: [item1, item2],
                                   cart2: [item3, item4, item5]}, role_name="item in cart")

    The values in the link definitions dict can either be a single object or a list. A list is needed for
    defining links to more than one object. The keys of the link definition must be single objects.
    As a dict can take in a key only once, each object might appear only once as a key.

    ``association`` or ``role_name`` keyword args can be used to specify the association and/or association direction
    for the links to be created. If neither ``association`` nor ``role_name`` are specified,
    the association is guessed based on the source and target objects in the link definitions.
    If association and/or role name are used, the correct association and/or association direction can
    be selected unambiguously.

    Args:
        link_definitions (dict): A dict of link definitions as explained before.
        **kwargs: The following keyword arguments are supported:

                - ``association``:
                    Specify the association to be used as a link classifier for all the links added with
                    this ``add_links`` invocation. Please note that association (alone)
                    can be ambiguous, as a recursive association from an class to itself has two possible link
                    directions for the combination of association and source/target objects of the same type.
                - ``role_name``:
                    Specify the association and its direction by role name to be used as a link classifier
                    for all the links added with this ``add_links`` invocation. Please note that role name alone
                    can be ambiguous, as multiple same-named role names could exist in different associations of
                    a class (and its superclasses).
                - ``stereotype_instances``:
                    Used to set the stereotype instances for the links, using a stereotype or a list of
                    stereotypes as in the ``stereotype_instances`` setter of  :py:class:`.CLink`.
                - ``tagged_values``:
                    Used to set the tagged values for the links, using a values dict
                    as in the ``tagged_values`` setter of  :py:class:`.CLink`.
    Returns:
        List[CLink]: List of newly created links.

    """
    return set_links(link_definitions, True, **kwargs)


def delete_links(link_definitions, **kwargs):
    """
    Function used to delete multiple links, maybe to different source objects.

    Args:
        link_definitions (dict): Link definitions of the links
            to be deleted. Defined in the same way as in the :py:func:`.add_links` function.
        **kwargs: Defines filter criteria for deletion:

                - ``association``:
                    Delete links only if they are based on the specified association.
                - ``role_name``:
                    Delete links only if they are based on an associations having the specified role name
                    either as a target or source role name.

    Returns:
        None

    """

    # stereotype_instances / tagged values is not supported for delete links
    if "stereotype_instances" in kwargs:
        raise CException(f"unknown keywords argument")
    if "tagged_values" in kwargs:
        raise CException(f"unknown keywords argument")

    context = LinkKeywordsContext(**kwargs)
    link_definitions = _check_link_definition_and_replace_classes(link_definitions)

    for source in link_definitions:
        targets = link_definitions[source]

        for target in targets:
            matches_in_order = None
            matching_link = None
            for link in source.links_:
                if context.association is not None and link.association != context.association:
                    continue
                matches_in_order = True
                matches = False
                if source == link.source_ and target == link.target_:
                    matches = True
                    if context.role_name is not None and not link.association.role_name == context.role_name:
                        matches = False
                if target == link.source_ and source == link.target_:
                    matches = True
                    matches_in_order = False
                    if context.role_name is not None and not link.association.source_role_name == context.role_name:
                        matches = False
                if matches:
                    if matching_link is None:
                        matching_link = link
                    else:
                        raise CException("link definition in delete links ambiguous for link " +
                                         f"'{source!s}->{target!s}': found multiple matches")
            if matching_link is None:
                role_name_string = ""
                if context.role_name is not None:
                    role_name_string = f" for given role name '{context.role_name!s}'"
                association_string = ""
                if context.association is not None:
                    association_string = f" for given association"
                    if role_name_string != "":
                        association_string = " and" + association_string
                raise CException(f"no link found for '{source!s} -> {target!s}' " +
                                 "in delete links" + role_name_string + association_string)
            else:
                if matches_in_order is None:
                    raise CException(f"no link found for '{source!s} -> {target!s}' in delete links")
                source_len = len(source.get_links_for_association(matching_link.association)) - 1
                target_len = len(target.get_links_for_association(matching_link.association)) - 1
                matching_link.association.check_multiplicity_(source, source_len, target_len, matches_in_order)
                matching_link.association.check_multiplicity_(target, target_len, source_len, not matches_in_order)
                matching_link.delete()


class LinkKeywordsContext(object):
    def __init__(self, **kwargs):
        self.role_name = kwargs.pop("role_name", None)
        self.association = kwargs.pop("association", None)
        self.stereotype_instances = kwargs.pop("stereotype_instances", None)
        self.label = kwargs.pop("label", None)
        self.tagged_values = kwargs.pop("tagged_values", None)
        if len(kwargs) != 0:
            raise CException(f"unknown keywords argument")
        if self.association is not None:
            check_is_cassociation(self.association)
        self.sourceClassifier = None
        self.target_classifier = None
        self.matchesInOrder = {}
        self.objectLinksHaveBeenRemoved = []
