import re

from codeable_models.cexception import CException
from codeable_models.cnamedelement import CNamedElement
from codeable_models.internal.commons import is_cmetaclass, is_cstereotype
from codeable_models.internal.stereotype_holders import CStereotypesHolder


def _check_for_classifier_and_role_name_match(classifier, role_name, association_classifier, association_role_name):
    if classifier is None and role_name is None:
        return False
    matches = True
    if role_name is not None:
        if role_name != association_role_name:
            matches = False
    if matches and classifier is not None:
        if not classifier.conforms_to_type(association_classifier):
            matches = False
    if matches:
        return True
    return False


class CAssociation(CNamedElement):
    STAR_MULTIPLICITY = -1

    def __init__(self, source, target, descriptor=None, **kwargs):
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
        name = kwargs.pop("name", None)
        self.ends = None
        super().__init__(name, **kwargs)
        if descriptor is not None:
            self._eval_descriptor(descriptor)

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.extend(["multiplicity", "role_name", "source_multiplicity",
                                   "source_role_name", "aggregation", "composition", "stereotypes"])
        super()._init_keyword_args(legal_keyword_args, **kwargs)

    def __str__(self):
        return super(CAssociation, self).__str__()

    def __repr__(self):
        name = ""
        if self.name is not None:
            name = self.name
        return f"CAssociation name = {name!s}, source = {self.source!s} -> target = {self.target!s}"

    def get_opposite_class(self, cl):
        if cl == self.source:
            return self.target
        else:
            return self.source

    def matches_target(self, classifier, role_name):
        return _check_for_classifier_and_role_name_match(classifier, role_name, self.target, self.role_name)

    def matches_source(self, classifier, role_name):
        return _check_for_classifier_and_role_name_match(classifier, role_name, self.source, self.source_role_name)

    @property
    def aggregation(self):
        return self.aggregation_

    @aggregation.setter
    def aggregation(self, aggregation):
        if aggregation:
            self.composition_ = False
        self.aggregation_ = aggregation

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
        return self.multiplicity_

    @multiplicity.setter
    def multiplicity(self, multiplicity):
        self.multiplicity_ = multiplicity
        self._set_multiplicity(multiplicity, True)

    @property
    def source_multiplicity(self):
        return self.source_multiplicity_

    @source_multiplicity.setter
    def source_multiplicity(self, multiplicity):
        self.source_multiplicity_ = multiplicity
        self._set_multiplicity(multiplicity, False)

    @property
    def composition(self):
        return self.composition_

    @composition.setter
    def composition(self, composition):
        if composition:
            self.aggregation_ = False
        self.composition_ = composition

    @property
    def stereotypes(self):
        return self.stereotypes_holder.stereotypes

    @stereotypes.setter
    def stereotypes(self, elements):
        self.stereotypes_holder.stereotypes = elements

    def delete(self):
        if self.is_deleted:
            return
        if is_cmetaclass(self.source):
            all_instances = self.source.all_classes
        elif is_cstereotype(self.source):
            all_instances = self.source.all_extended_instances
        else:
            all_instances = self.source.all_objects
        for instance in all_instances:
            for link in instance.link_objects:
                link.delete()
        self.source.associations_.remove(self)
        if self.source != self.target:
            self.target.associations_.remove(self)
        for s in self.stereotypes_holder.stereotypes:
            s.extended_.remove(self)
        self.stereotypes_holder.stereotypes_ = []
        super().delete()

    def check_multiplicity(self, obj, actual_length, actual_opposite_length, check_target_multiplicity):
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
