from codeable_models.internal.commons import *
from codeable_models.cexception import CException
from codeable_models.internal.stereotype_holders import CStereotypeInstancesHolder
from codeable_models.internal.var_values import delete_var_value, set_var_value, get_var_value, get_var_values, \
    set_var_values, VarValueKind


class CLink(object):
    def __init__(self, association, source_object, target_object, **kwargs):
        self.is_deleted = False
        self.source_ = source_object
        self.target_ = target_object
        self.label = None
        self.association = association
        self.stereotype_instances_holder = CStereotypeInstancesHolder(self)
        self.tagged_values_ = {}
        super().__init__()
        self._init_keyword_args(**kwargs)

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.append("stereotype_instances")
        set_keyword_args(self, legal_keyword_args, **kwargs)

    def get_opposite_object(self, object_):
        if object_ == self.source_:
            return self.target_
        else:
            return self.source_

    @property
    def role_name(self):
        return self.association.role_name

    @property
    def source_role_name(self):
        return self.association.source_role_name

    @property
    def source(self):
        if self.source_.class_object_class_ is not None:
            return self.source_.class_object_class_
        return self.source_

    @property
    def target(self):
        if self.target_.class_object_class_ is not None:
            return self.target_.class_object_class_
        return self.target_

    def delete(self):
        if self.is_deleted:
            return
        self.is_deleted = True
        for si in self.stereotype_instances:
            si.extended_instances_.remove(self)
        self.stereotype_instances_holder.stereotypes_ = []
        if self.source_ != self.target_:
            self.target_.link_objects_.remove(self)
        self.source_.link_objects_.remove(self)

    @property
    def stereotype_instances(self):
        return self.stereotype_instances_holder.stereotypes

    @stereotype_instances.setter
    def stereotype_instances(self, elements):
        self.stereotype_instances_holder.stereotypes = elements

    def get_tagged_value(self, name, stereotype=None):
        if self.is_deleted:
            raise CException(f"can't get tagged value '{name!s}' on deleted link")
        return get_var_value(self, self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_,
                             name, VarValueKind.TAGGED_VALUE, stereotype)

    def delete_tagged_value(self, name, stereotype=None):
        if self.is_deleted:
            raise CException(f"can't delete tagged value '{name!s}' on deleted link")
        return delete_var_value(self, self.stereotype_instances_holder.get_stereotype_instance_path(),
                                self.tagged_values_, name, VarValueKind.TAGGED_VALUE, stereotype)

    def set_tagged_value(self, name, value, stereotype=None):
        if self.is_deleted:
            raise CException(f"can't set tagged value '{name!s}' on deleted link")
        return set_var_value(self, self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_,
                             name, value, VarValueKind.TAGGED_VALUE, stereotype)

    @property
    def tagged_values(self):
        if self.is_deleted:
            raise CException(f"can't get tagged values on deleted link")
        return get_var_values(self.stereotype_instances_holder.get_stereotype_instance_path(), self.tagged_values_)

    @tagged_values.setter
    def tagged_values(self, new_values):
        if self.is_deleted:
            raise CException(f"can't set tagged values on deleted link")
        set_var_values(self, new_values, VarValueKind.TAGGED_VALUE)


def _get_target_objects_from_definition(targets, is_class_links):
    if targets is None:
        targets = []
    elif not isinstance(targets, list):
        targets = [targets]
    new_targets = []
    for t in targets:
        if is_cclass(t):
            if not is_class_links:
                raise CException(f"link target '{t!s}' is a class, but source is an object")
            new_targets.append(t.class_object_)
        elif is_cobject(t):
            if is_class_links and t.class_object_class_ is None:
                raise CException(f"link target '{t!s}' is an object, but source is an class")
            if not is_class_links and t.class_object_class_ is not None:
                raise CException(f"link target '{t!s}' is an class, but source is an object")
            new_targets.append(t)
        else:
            raise CException(f"link target '{t!s}' is neither an object nor a class")
    return new_targets


def _check_link_definition_and_replace_classes(link_definitions):
    if not isinstance(link_definitions, dict):
        raise CException("link definitions should be of the form " +
                         "{<link source 1>: <link target(s) 1>, ..., <link source n>: <link target(s) n>}")

    new_defs = {}
    for source in link_definitions:
        source_obj = source
        if source is None or source == []:
            raise CException("link should not contain an empty source")
        if is_cclass(source):
            source_obj = source.class_object_
        elif not is_cobject(source):
            raise CException(f"link source '{source!s}' is neither an object nor a class")
        targets = _get_target_objects_from_definition(link_definitions[source],
                                                      source_obj.class_object_class_ is not None)
        new_defs[source_obj] = targets

    return new_defs


def _determine_matching_association_and_set_context_info(context, source, targets):
    if source.class_object_class_ is not None:
        target_classifier_candidates = get_common_metaclasses([co.class_object_class_ for co in targets])
        context.sourceClassifier = source.class_object_class_.metaclass
    else:
        target_classifier_candidates = [get_common_classifier(targets)]
        context.sourceClassifier = source.classifier

    if context.association is not None and context.target_classifier is None:
        if context.sourceClassifier.conforms_to_type(context.association.source):
            target_classifier_candidates = [context.association.target]
            context.sourceClassifier = context.association.source
        elif context.sourceClassifier.conforms_to_type(context.association.target):
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
            if (association.matches_target(target_classifierCandidate, context.role_name) and
                    association.matches_source(context.sourceClassifier, None)):
                matches_association_order.append(association)
                matching_classifier = target_classifierCandidate
            elif (association.matches_source(target_classifierCandidate, context.role_name) and
                  association.matches_target(context.sourceClassifier, None)):
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
        for existingLink in source_obj.link_objects_:
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
        source_obj.link_objects_.append(link)
        # for links from this object to itself, store only one link object
        if source_obj != target:
            target.link_objects_.append(link)
        if context.stereotype_instances is not None:
            link.stereotype_instances = context.stereotype_instances
        if context.tagged_values is not None:
            link.tagged_values = context.tagged_values
    return new_links


def remove_links_for_associations(context, source, targets):
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
    context = LinkKeywordsContext(**kwargs)
    link_definitions = _check_link_definition_and_replace_classes(link_definitions)

    new_links = []
    for source in link_definitions:
        targets = link_definitions[source]
        _determine_matching_association_and_set_context_info(context, source, targets)
        if not do_add_links:
            remove_links_for_associations(context, source, targets)
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
                context.association.check_multiplicity(source, source_len, 0, context.matchesInOrder[source])
            else:
                for target in targets:
                    target_len = len(target.get_links_for_association(context.association))
                    context.association.check_multiplicity(source, source_len, target_len,
                                                           context.matchesInOrder[source])
                    context.association.check_multiplicity(target, target_len, source_len,
                                                           not context.matchesInOrder[source])
    except CException as e:
        for link in new_links:
            link.delete()
        raise e
    return new_links


def add_links(link_definitions, **kwargs):
    return set_links(link_definitions, True, **kwargs)


def delete_links(link_definitions, **kwargs):
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
            for link in source.link_objects_:
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
                matching_link.association.check_multiplicity(source, source_len, target_len, matches_in_order)
                matching_link.association.check_multiplicity(target, target_len, source_len, not matches_in_order)
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
