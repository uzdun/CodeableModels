import nose
from nose.tools import eq_

from codeable_models import CMetaclass, CStereotype, CClass, CException, set_links, add_links
from tests.testing_commons import exception_expected_


class TestStereotypeInstancesOnDerivedAssociations:
    def setup(self):
        self.m1 = CMetaclass("M1")
        self.m2 = CMetaclass("M2")
        self.m3 = CMetaclass("M3")
        self.a = self.m1.association(self.m2, name="a", multiplicity="*", role_name="m2",
                                     source_multiplicity="1..*", source_role_name="m1")

    def test_stereotype_instances_on_derived_association(self):
        s1 = CStereotype("S1", extended=self.a)
        s2 = CStereotype("S2", extended=self.a)
        s3 = CStereotype("S3", extended=self.a)

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a)

        eq_(a1.stereotype_instances, [])
        eq_(s1.extended_instances, [])
        a1.stereotype_instances = [s1]
        eq_(s1.extended_instances, [a1])
        eq_(a1.stereotype_instances, [s1])
        a1.stereotype_instances = [s1, s2, s3]
        eq_(s1.extended_instances, [a1])
        eq_(s2.extended_instances, [a1])
        eq_(s3.extended_instances, [a1])
        eq_(set(a1.stereotype_instances), {s1, s2, s3})
        a1.stereotype_instances = s2
        eq_(a1.stereotype_instances, [s2])
        eq_(s1.extended_instances, [])
        eq_(s2.extended_instances, [a1])
        eq_(s3.extended_instances, [])

        eq_(c1.associations, [a1])
        eq_(c2.associations, [a1])

    def test_stereotype_instances_on_derived_association_and_links_in_combination(self):
        s1 = CStereotype("S1", extended=self.a)
        s2 = CStereotype("S2", extended=self.a)
        s3 = CStereotype("S3", extended=self.a)

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a)
        links = set_links({c1: [c2, c3]})
        l1 = links[0]

        a1.stereotype_instances = [s1]
        l1.stereotype_instances = [s1]
        eq_(set(s1.extended_instances), {a1, l1})
        eq_(a1.stereotype_instances, [s1])
        eq_(l1.stereotype_instances, [s1])
        a1.stereotype_instances = [s1, s2, s3]
        eq_(set(s1.extended_instances), {a1, l1})
        eq_(s2.extended_instances, [a1])
        eq_(s3.extended_instances, [a1])
        eq_(set(a1.stereotype_instances), {s1, s2, s3})
        eq_(set(l1.stereotype_instances), {s1})
        l1.stereotype_instances = [s1, s2, s3]
        eq_(set(s1.extended_instances), {a1, l1})
        eq_(set(s2.extended_instances), {a1, l1})
        eq_(set(s3.extended_instances), {a1, l1})
        eq_(set(a1.stereotype_instances), {s1, s2, s3})
        eq_(set(l1.stereotype_instances), {s1, s2, s3})
        a1.stereotype_instances = s2
        eq_(a1.stereotype_instances, [s2])
        eq_(set(l1.stereotype_instances), {s1, s2, s3})
        eq_(s1.extended_instances, [l1])
        eq_(set(s2.extended_instances), {a1, l1})
        eq_(s3.extended_instances, [l1])
        l1.stereotype_instances = s3
        eq_(a1.stereotype_instances, [s2])
        eq_(l1.stereotype_instances, [s3])
        eq_(s1.extended_instances, [])
        eq_(s2.extended_instances, [a1])
        eq_(s3.extended_instances, [l1])

    def test_stereotype_instances_double_assignment(self):
        s1 = CStereotype("S1", extended=self.a)

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a)

        try:
            a1.stereotype_instances = [s1, s1]
            exception_expected_()
        except CException as e:
            eq_(e.value, "'S1' is already a stereotype instance on association from 'C1' to 'C2'")
        eq_(a1.stereotype_instances, [s1])

    def test_stereotype_instances_none_assignment(self):
        CStereotype("S1", extended=self.a)

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a)

        try:
            a1.stereotype_instances = [None]
            exception_expected_()
        except CException as e:
            eq_(e.value, "'None' is not a stereotype")
        eq_(a1.stereotype_instances, [])

    def test_stereotype_instances_wrong_type_in_assignment(self):
        CStereotype("S1", extended=self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a)

        try:
            a1.stereotype_instances = self.a
            exception_expected_()
        except CException as e:
            eq_(e.value, "a list or a stereotype is required as input")
        eq_(a1.stereotype_instances, [])

    def test_multiple_extended_instances(self):
        s1 = CStereotype("S1", extended=self.a)
        s2 = CStereotype("S2", extended=self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")

        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a)
        a2 = c1.association(c3, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a)
        a3 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a)

        a1.stereotype_instances = [s1]
        eq_(s1.extended_instances, [a1])
        a2.stereotype_instances = [s1]
        eq_(set(s1.extended_instances), {a1, a2})
        a3.stereotype_instances = [s1, s2]
        eq_(set(s1.extended_instances), {a1, a2, a3})
        eq_(set(s2.extended_instances), {a3})

    def test_delete_stereotype_of_extended_instances(self):
        s1 = CStereotype("S1", extended=self.a)
        s1.delete()
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a)
        try:
            a1.stereotype_instances = [s1]
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_delete_stereotyped_element_instance(self):
        s1 = CStereotype("S1", extended=self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a,
                            stereotype_instances=[s1])
        eq_(s1.extended_instances, [a1])
        eq_(a1.stereotype_instances, [s1])
        a1.delete()
        eq_(s1.extended_instances, [])
        eq_(a1.stereotype_instances, [])

    def test_add_stereotype_instance_wrong_association(self):
        other_association = self.m1.association(self.m2, name="b", multiplicity="*", role_name="m1",
                                                source_multiplicity="1", source_role_name="m2")
        s1 = CStereotype("S1", extended=self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=other_association)
        try:
            a1.stereotype_instances = [s1]
            exception_expected_()
        except CException as e:
            eq_(e.value,
                "stereotype 'S1' cannot be added to association from 'C1' to 'C2': " +
                "no extension by this stereotype found")

    def test_add_stereotype_of_inherited_metaclass(self):
        sub1 = CMetaclass("Sub1", superclasses=self.m1)
        sub2 = CMetaclass("Sub2", superclasses=self.m2)
        s = CStereotype("S1", extended=self.a)
        c1 = CClass(sub1, "C1")
        c2 = CClass(sub2, "C2")
        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a,
                            stereotype_instances=s)
        eq_(s.extended_instances, [a1])
        eq_(a1.stereotype_instances, [s])

    def test_add_stereotype_instance_correct_by_inheritance_of_stereotype(self):
        s1 = CStereotype("S1", extended=self.a)
        s2 = CStereotype("S2", superclasses=s1)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a,
                            stereotype_instances=s2)
        eq_(s2.extended_instances, [a1])
        eq_(a1.stereotype_instances, [s2])

    def test_all_extended_instances(self):
        s1 = CStereotype("S1", extended=self.a)
        s2 = CStereotype("S2", superclasses=s1)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a)
        a2 = c1.association(c3, name="a", multiplicity="*", role_name="c3",
                            source_multiplicity="1", source_role_name="c1", derived_from=self.a)
        a1.stereotype_instances = s1
        a2.stereotype_instances = s2
        eq_(s1.extended_instances, [a1])
        eq_(s2.extended_instances, [a2])
        eq_(s1.all_extended_instances, [a1, a2])
        eq_(s2.all_extended_instances, [a2])

    def test_adding_stereotype_before_derived_from_is_used(self):
        sub1 = CMetaclass("Sub1", superclasses=self.m1)
        sub2 = CMetaclass("Sub2", superclasses=self.m2)
        s = CStereotype("S1", extended=self.a)
        c1 = CClass(sub1, "C1")
        c2 = CClass(sub2, "C2")
        try:
            a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                                source_multiplicity="1", source_role_name="c1", stereotype_instances=s,
                                derived_from=self.a)
            exception_expected_()
        except CException as e:
            eq_(e.value,
                "stereotype 'S1' cannot be added to association from 'C1' to 'C2': " +
                "no extension by this stereotype found")

    def test_derived_from_wrong_type(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        try:
            c1.association(c2, name="a", multiplicity="*", role_name="c2",
                           source_multiplicity="*", source_role_name="c1",
                           derived_from=self.m2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "'M2' is not an association")

    def test_derived_from_getters(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a1 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1")
        eq_(a1.derived_from, None)
        eq_(self.a.derived_associations, [])

        a2 = c1.association(c2, name="a", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1",
                            derived_from=self.a)
        eq_(a2.derived_from, self.a)
        eq_(set(self.a.derived_associations), {a2})

        a1.derived_from = self.a
        eq_(a1.derived_from, self.a)
        eq_(set(self.a.derived_associations), {a1, a2})

    def test_source_multiplicities_derived_from_metaclass(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a = self.m1.association(self.m2, "a: [m1] 1 -> [m2] *")
        try:
            c1.association(c2, name="a", multiplicity="*", role_name="c2",
                           source_multiplicity="*", source_role_name="c1",
                           derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "source lower multiplicity '0' smaller than metaclass' source lower " +
                "multiplicity '1' this association is derived from")
        try:
            c1.association(c2, name="a", multiplicity="*", role_name="c2",
                           source_multiplicity="1..*", source_role_name="c1",
                           derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "source upper multiplicity '*' (of this association, maybe combined with other derived " +
                "associations of the same kind) is larger than metaclass' source upper " +
                "multiplicity '1' this association is derived from")

        b = self.m1.association(self.m2, "a: [m1] 2..4 -> [m2] *")

        c1.association(c2, "a: [c1] 2..3 -> [c2] *", derived_from=b)

        try:
            c1.association(c2, "a: [c1] 1..* -> [c2] *", derived_from=b)
            exception_expected_()
        except CException as e:
            eq_(e.value, "source lower multiplicity '1' smaller than metaclass' source lower " +
                "multiplicity '2' this association is derived from")
        try:
            c1.association(c2, "a: [c1] 2..* -> [c2] *", derived_from=b)
            exception_expected_()
        except CException as e:
            eq_(e.value, "source upper multiplicity '*' (of this association, maybe combined with other derived " +
                "associations of the same kind) is larger than metaclass' source upper " +
                "multiplicity '4' this association is derived from")

    def test_target_multiplicities_derived_from_metaclass(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a = self.m1.association(self.m2, "* -> 1")
        try:
            c1.association(c2, name="a", multiplicity="*", role_name="c2",
                           source_multiplicity="*", source_role_name="c1",
                           derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "lower multiplicity '0' smaller than metaclass' lower " +
                "multiplicity '1' this association is derived from")
        try:
            c1.association(c2, name="a", multiplicity="1..*", role_name="c2",
                           source_multiplicity="*", source_role_name="c1",
                           derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "upper multiplicity '*' (of this association, maybe combined with other derived " +
                "associations of the same kind) is larger than metaclass' upper " +
                "multiplicity '1' this association is derived from")

        b = self.m1.association(self.m2, "a: * -> 2..4")

        c1.association(c2, "* -> 2..3", derived_from=b)

        try:
            c1.association(c2, name="a", multiplicity="1..*", role_name="c2",
                           source_multiplicity="*", source_role_name="c1",
                           derived_from=b)
            exception_expected_()
        except CException as e:
            eq_(e.value, "lower multiplicity '1' smaller than metaclass' lower " +
                "multiplicity '2' this association is derived from")
        try:
            c1.association(c2, "* -> 2..*", derived_from=b)
            exception_expected_()
        except CException as e:
            eq_(e.value, "upper multiplicity '*' (of this association, maybe combined with other derived " +
                "associations of the same kind) is larger than metaclass' upper " +
                "multiplicity '4' this association is derived from")

    def test_derived_from_source_multiplicities_on_multiple_associations(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a = self.m1.association(self.m2, "a: [m1] 1 -> [m2] *")
        try:
            c1.association(c2, "a1: [c1] 1 -> [c2] *", derived_from=a)
            c1.association(c2, "a1: [c1] 1 -> [c2] *", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "source upper multiplicity '2' (of this association, maybe combined with other derived " +
                "associations of the same kind) is larger than metaclass' source upper " +
                "multiplicity '1' this association is derived from")

    def test_derived_from_source_multiplicities_multiple_associations_from_different_sources_and_targets(self):
        c1a = CClass(self.m1, "C1A")
        c1b = CClass(self.m1, "C1B")
        c1c = CClass(self.m1, "C1C")
        c2a = CClass(self.m2, "C2A")
        c2b = CClass(self.m2, "C2B")
        c2c = CClass(self.m2, "C2B")

        a = self.m1.association(self.m2, "a: [m1] 1 -> [m2] *")

        # testing to check this does not raise an exception, as association sources/targets are different
        c1a.association(c2a, "a1: [c1a] 1 -> [c2a] *", derived_from=a)
        c1b.association(c2a, "a2: [c1b] 1 -> [c2a] *", derived_from=a)
        c1c.association(c2a, "a3: [c1c] 1 -> [c2a] *", derived_from=a)
        c1a.association(c2b, "a4: [c1a] 1 -> [c2b] *", derived_from=a)
        c1a.association(c2c, "a5: [c1a] 1 -> [c2c] *", derived_from=a)

    def test_derived_from_source_multiplicities_on_multiple_associations_inheritance1(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m1, "C3", superclasses=c1)
        c4 = CClass(self.m2, "C4", superclasses=c2)
        c5 = CClass(self.m3, "C5")

        a = self.m1.association(self.m2, "a: [m1] 1 -> [m2] *")
        b = self.m1.association(self.m3, "b: [m1] 1 -> [m3] *")

        try:
            c1.association(c5, "b1: 1 -> *", derived_from=b)
            c3.association(c4, "a-c3-c4: [c3] 1 -> [c4] *", derived_from=a)
            c1.association(c2, "a-c1-c2: [c1] 1 -> [c2] *", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "source upper multiplicity '2' (of this association, maybe combined with other derived " +
                "associations of the same kind) is larger than metaclass' source upper " +
                "multiplicity '1' this association is derived from")

    def test_derived_from_source_multiplicities_on_multiple_associations_inheritance2(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m1, "C3", superclasses=c1)

        a = self.m1.association(self.m2, "a: [m1] 1 -> [m2] *")

        try:
            c3.association(c2, "a1: [c3] 1 -> [c2] *", derived_from=a)
            c1.association(c2, "a2: [c1] 1..* -> [c2] *", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "source upper multiplicity '*' (of this association, maybe combined with other derived " +
                "associations of the same kind) is larger than metaclass' source upper " +
                "multiplicity '1' this association is derived from")

    def test_derived_from_source_multiplicities_on_multiple_associations_inheritance3(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m1, "C3", superclasses=c1)
        c4 = CClass(self.m2, "C4", superclasses=c2)

        a = self.m1.association(self.m2, "a: [m1] 1 -> [m2] *")

        c1_c2 = c1.association(c2, "a2: [c1] 1 -> [c2] *", derived_from=a)
        try:
            c3.association(c4, "a1: [c3] 1 -> [c4] *", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "source upper multiplicity '2' (of this association, maybe combined with other derived " +
                "associations of the same kind) is larger than metaclass' source upper " +
                "multiplicity '1' this association is derived from")
        eq_(set(a.derived_associations), {c1_c2})

    def test_derived_from_source_multiplicities_on_multiple_associations_other_derived_association(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c5 = CClass(self.m3, "C5")

        a = self.m1.association(self.m2, "a: [m1] 1 -> [m2] *")
        b = self.m1.association(self.m3, "b: [m1] 1 -> [m3] *")

        c1.association(c5, "b1: 1 -> *", derived_from=b)
        # testing to check this does not raise an exception, as other derived association is not
        # counted in source upper multiplicity count
        c1.association(c2, "a: [c1] 1 -> [c2] *", derived_from=a)

    def test_derived_from_target_multiplicities_on_multiple_associations(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a = self.m1.association(self.m2, "a: [m1] * -> [m2] 1")
        try:
            c1.association(c2, "a1: [c1] * -> [c2] 1", derived_from=a)
            c1.association(c2, "a1: [c1] * -> [c2] 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "upper multiplicity '2' (of this association, maybe combined with other derived " +
                "associations of the same kind) is larger than metaclass' upper " +
                "multiplicity '1' this association is derived from")

    def test_derived_from_target_multiplicities_multiple_associations_from_different_sources(self):
        c1a = CClass(self.m1, "C1A")
        c1b = CClass(self.m1, "C1B")
        c1c = CClass(self.m1, "C1C")
        c2a = CClass(self.m2, "C2A")
        c2b = CClass(self.m2, "C2B")
        c2c = CClass(self.m2, "C2B")

        a = self.m1.association(self.m2, "a: [m1] * -> [m2] 1")

        # testing to check this does not raise an exception, as association sources/targets are different
        c1a.association(c2a, "a1: [c1a] * -> [c2a] 1", derived_from=a)
        c1b.association(c2a, "a2: [c1b] * -> [c2a] 1", derived_from=a)
        c1c.association(c2a, "a3: [c1c] * -> [c2a] 1", derived_from=a)
        c1a.association(c2b, "a4: [c1a] * -> [c2b] 1", derived_from=a)
        c1a.association(c2c, "a5: [c1a] * -> [c2c] 1", derived_from=a)

    def test_derived_from_target_multiplicities_on_multiple_associations_inheritance1(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m1, "C3", superclasses=c1)
        c4 = CClass(self.m2, "C4", superclasses=c2)
        c5 = CClass(self.m3, "C5")

        a = self.m1.association(self.m2, "a: [m1] * -> [m2] 1")
        b = self.m1.association(self.m3, "b: [m1] * -> [m3] 1")

        try:
            c1.association(c5, "b1: * -> 1", derived_from=b)
            c3.association(c4, "a-c3-c4: [c3] * -> [c4] 1", derived_from=a)
            c1.association(c2, "a-c1-c2: [c1] * -> [c2] 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "upper multiplicity '2' (of this association, maybe combined with other derived " +
                "associations of the same kind) is larger than metaclass' upper " +
                "multiplicity '1' this association is derived from")

    def test_derived_from_target_multiplicities_on_multiple_associations_inheritance2(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m1, "C3", superclasses=c1)

        a = self.m1.association(self.m2, "a: [m1] * -> [m2] 1")

        try:
            c3.association(c2, "a1: [c3] * -> [c2] 1", derived_from=a)
            c1.association(c2, "a2: [c1] * -> [c2] 1..*", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "upper multiplicity '*' (of this association, maybe combined with other derived " +
                "associations of the same kind) is larger than metaclass' upper " +
                "multiplicity '1' this association is derived from")

    def test_derived_from_target_multiplicities_on_multiple_associations_other_derived_association(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c5 = CClass(self.m3, "C5")

        a = self.m1.association(self.m2, "a: [m1] * -> [m2] 1")
        b = self.m1.association(self.m3, "b: [m1] * -> [m3] 1")

        c1.association(c5, "b1: * -> 1", derived_from=b)
        # testing to check this does not raise an exception, as other derived association is not
        # counted in upper multiplicity count
        c1.association(c2, "a: [c1] * -> [c2] 1", derived_from=a)

    def test_check_derived_association_has_same_aggregation_state(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a = self.m1.association(self.m2, "a: [m1] * -> [m2] 1")
        try:
            c1.association(c2, "ac: [c1] * <>- [c2] 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "derived association is an aggregation, but metaclass association is not")

        a = self.m1.association(self.m2, "a: [m1] * <>- [m2] 1")
        try:
            c1.association(c2, "ac: [c1] * -> [c2] 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "metaclass association is an aggregation, but derived association is not")

        a = self.m1.association(self.m2, "a: [m1] * -> [m2] 1")
        try:
            c1.association(c2, "ac: [c1] * <*>- [c2] 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "derived association is a composition, but metaclass association is not")

        a = self.m1.association(self.m2, "a: [m1] * <*>- [m2] 1")
        try:
            c1.association(c2, "ac: [c1] * -> [c2] 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "metaclass association is a composition, but derived association is not")

        a = self.m1.association(self.m2, "a: [m1] * <*>- [m2] 1")
        try:
            c1.association(c2, "ac: [c1] * <>- [c2] 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "derived association is an aggregation, but metaclass association is not")

        a = self.m1.association(self.m2, "a: [m1] * <>- [m2] 1")
        try:
            c1.association(c2, "ac: [c1] * <*>- [c2] 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "metaclass association is an aggregation, but derived association is not")

        a = self.m1.association(self.m2, "a: [m1] * <>- [m2] 1")
        try:
            c1.association(c2, "ac: [c1] * <*>- [c2] 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "metaclass association is an aggregation, but derived association is not")

        a = self.m1.association(self.m2, "a: [m1] * <*>- [m2] 1")
        try:
            c1.association(c2, "ac: [c1] * <>- [c2] 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "derived association is an aggregation, but metaclass association is not")

    def test_derived_from_reversing_source_and_target_not_supported(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a = self.m1.association(self.m2, "a: [m1] 1 -> [m2] *")
        try:
            c2.association(c1, "a2: [c2] * -> [c1] 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "association source class 'C2' is not derived source metaclass 'M1'")

    def test_check_derived_from_non_metaclass_association(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a = c1.association(c2, "* -> 1")

        try:
            c1.association(c2, "* -> 1", derived_from=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "association used as 'derived_from' parameter is not a metaclass-level association")

    def test_check_derived_association_is_metaclass_association(self):
        m1 = CMetaclass("MC1")
        m2 = CMetaclass("MC2")

        try:
            m1.association(m2, "* -> 1", derived_from=self.a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "association 'derived_from' is called on is not a class-level association")

    def test_changing_single_derived_from_relation(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        ma = self.m1.association(self.m2, "a: [m1] 1 -> [m2] *")
        a1 = c1.association(c2, "1 -> *", derived_from=self.a)
        a1.derived_from = ma

        eq_(a1.derived_from, ma)
        eq_(self.a.derived_associations, [])
        eq_(set(ma.derived_associations), {a1})

    def test_changing_two_derived_from_relation(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        ma = self.m1.association(self.m2, "a: [m1] 1 -> [m2] *")
        a1 = c1.association(c2, "1 -> *", derived_from=self.a)
        a2 = c1.association(c2, "1 -> *", derived_from=self.a)
        a1.derived_from = ma

        eq_(a1.derived_from, ma)
        eq_(a2.derived_from, self.a)
        eq_(set(self.a.derived_associations), {a2})
        eq_(set(ma.derived_associations), {a1})

    def test_setting_derived_from_relation_to_none(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a1 = c1.association(c2, "1 -> *", derived_from=self.a)
        a1.derived_from = None

        eq_(a1.derived_from, None)
        eq_(self.a.derived_associations, [])

    def test_setting_one_of_two_derived_from_relations_to_none(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a1 = c1.association(c2, "1 -> *", derived_from=self.a)
        a2 = c1.association(c2, "1 -> *", derived_from=self.a)
        a1.derived_from = None

        eq_(a1.derived_from, None)
        eq_(a2.derived_from, self.a)
        eq_(set(self.a.derived_associations), {a2})

    def test_delete_derived_association(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        c = c1.association(c2, "ac: [c1] 1 -> [c2] *")
        c.delete()
        eq_(c.derived_from, None)

        b = c1.association(c2, "ac: [c1] 1 -> [c2] *", derived_from=self.a)

        b.delete()

        eq_(b.derived_from, None)
        eq_(self.a.derived_associations, [])

    def test_delete_one_of_two_derived_association(self):
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        b1 = c1.association(c2, "ac: [c1] 1 -> [c2] *", derived_from=self.a)
        b2 = c1.association(c2, "ac: [c1] 1 -> [c2] *", derived_from=self.a)

        b1.delete()

        eq_(b1.derived_from, None)
        eq_(b2.derived_from, self.a)
        eq_(set(self.a.derived_associations), {b2})

    def test_delete_derived_from_metaclass_association(self):
        m = self.m1.association(self.m2, "a: [m1] 1..2 -> [m2] *")
        m.delete()
        eq_(m.derived_associations, [])

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        ma = self.m1.association(self.m2, "a: [m1] 1..2 -> [m2] *")
        b1 = c1.association(c2, "ac: [c1] 1 -> [c2] *", derived_from=ma)
        b2 = c1.association(c2, "ac: [c1] 1 -> [c2] *", derived_from=ma)

        ma.delete()

        eq_(b1.derived_from, None)
        eq_(b2.derived_from, None)
        eq_(ma.derived_associations, [])


if __name__ == "__main__":
    nose.main()
