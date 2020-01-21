import nose
from nose.tools import eq_

from codeable_models import CStereotype, CMetaclass, CException, CBundle
from tests.testing_commons import exception_expected_


class TestStereotypesOnAssociations:
    def setup(self):
        self.m1 = CMetaclass("M1")
        self.m2 = CMetaclass("M2")
        self.a = self.m1.association(self.m2, name="A", multiplicity="1", role_name="m1",
                                     source_multiplicity="*", source_role_name="m2")

    def test_creation_of_one_stereotype(self):
        s = CStereotype("S", extended=self.a)
        eq_(s.name, "S")
        eq_(self.a.stereotypes, [s])
        eq_(s.extended, [self.a])

    def test_wrongs_types_in_list_of_extended_element_types(self):
        try:
            CStereotype("S", extended=[self.a, self.m1])
            exception_expected_()
        except CException as e:
            eq_("'M1' is not a association", e.value)
        try:
            CStereotype("S", extended=[self.a, CBundle("P")])
            exception_expected_()
        except CException as e:
            eq_("'P' is not a association", e.value)
        try:
            CStereotype("S", extended=[CBundle("P"), self.a])
            exception_expected_()
        except CException as e:
            eq_("unknown type of extend element: 'P'", e.value)

    def test_creation_of_3_stereotypes(self):
        s1 = CStereotype("S1")
        s2 = CStereotype("S2")
        s3 = CStereotype("S3")
        self.a.stereotypes = [s1, s2, s3]
        eq_(s1.extended, [self.a])
        eq_(s2.extended, [self.a])
        eq_(s3.extended, [self.a])
        eq_(set(self.a.stereotypes), {s1, s2, s3})

    def test_creation_of_unnamed_stereotype(self):
        s = CStereotype()
        eq_(s.name, None)
        eq_(self.a.stereotypes, [])
        eq_(s.extended, [])

    def test_delete_stereotype(self):
        s1 = CStereotype("S1")
        s1.delete()
        eq_(s1.name, None)
        eq_(self.a.stereotypes, [])
        s1 = CStereotype("S1", extended=self.a)
        s1.delete()
        eq_(s1.name, None)
        eq_(self.a.stereotypes, [])

        s1 = CStereotype("S1", extended=self.a)
        s2 = CStereotype("S2", extended=self.a)
        s3 = CStereotype("s1", superclasses=s2, attributes={"i": 1}, extended=self.a)

        s1.delete()
        eq_(set(self.a.stereotypes), {s2, s3})
        s3.delete()
        eq_(set(self.a.stereotypes), {s2})

        eq_(s3.superclasses, [])
        eq_(s2.subclasses, [])
        eq_(s3.attributes, [])
        eq_(s3.attribute_names, [])
        eq_(s3.extended, [])
        eq_(s3.name, None)
        eq_(s3.bundles, [])

    def test_stereotype_extension_add_remove(self):
        s1 = CStereotype("S1")
        eq_(set(s1.extended), set())
        a1 = self.m1.association(self.m2, multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2", stereotypes=[s1])
        eq_(set(s1.extended), {a1})
        eq_(set(a1.stereotypes), {s1})
        a2 = self.m1.association(self.m2, multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2", stereotypes=s1)
        eq_(set(s1.extended), {a1, a2})
        eq_(set(a1.stereotypes), {s1})
        eq_(set(a2.stereotypes), {s1})
        s1.extended = [a2]
        eq_(set(s1.extended), {a2})
        eq_(set(a1.stereotypes), set())
        eq_(set(a2.stereotypes), {s1})
        s2 = CStereotype("S2", extended=[a2])
        eq_(set(a2.stereotypes), {s2, s1})
        eq_(set(s1.extended), {a2})
        eq_(set(s2.extended), {a2})
        a2.stereotypes = []
        eq_(set(a2.stereotypes), set())
        eq_(set(s1.extended), set())
        eq_(set(s2.extended), set())

    def test_stereotype_remove_stereotype_or_association(self):
        a1 = self.m1.association(self.m2, multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2")
        s1 = CStereotype("S1", extended=[a1])
        s2 = CStereotype("S2", extended=[a1])
        s3 = CStereotype("S3", extended=[a1])
        s4 = CStereotype("S4", extended=[a1])
        eq_(set(a1.stereotypes), {s1, s2, s3, s4})
        s2.delete()
        eq_(set(a1.stereotypes), {s1, s3, s4})
        eq_(set(s2.extended), set())
        eq_(set(s1.extended), {a1})
        a1.delete()
        eq_(set(a1.stereotypes), set())
        eq_(set(s1.extended), set())

    def test_stereotypes_wrong_type(self):
        a1 = self.m1.association(self.m2, name="a1", multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2")
        try:
            a1.stereotypes = [a1]
            exception_expected_()
        except CException as e:
            eq_("'a1' is not a stereotype", e.value)

    def test_association_stereotypes_null_input(self):
        s = CStereotype()
        a1 = self.m1.association(self.m2, name="a1", multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2", stereotypes=None)
        eq_(a1.stereotypes, [])
        eq_(s.extended, [])

    def test_association_stereotypes_non_list_input(self):
        s = CStereotype()
        a1 = self.m1.association(self.m2, name="a1", multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2", stereotypes=s)
        eq_(a1.stereotypes, [s])
        eq_(s.extended, [a1])

    def test_association_stereotypes_non_list_input_wrong_type(self):
        try:
            a1 = self.m1.association(self.m2, name="a1", multiplicity="1", role_name="m1",
                                     source_multiplicity="*", source_role_name="m2")
            a1.stereotypes = a1
            exception_expected_()
        except CException as e:
            eq_("a list or a stereotype is required as input", e.value)

    def test_metaclass_stereotypes_append(self):
        s1 = CStereotype()
        s2 = CStereotype()
        a1 = self.m1.association(self.m2, name="a1", multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2", stereotypes=s1)
        # should have no effect, as setter must be used
        a1.stereotypes.append(s2)
        eq_(a1.stereotypes, [s1])
        eq_(s1.extended, [a1])
        eq_(s2.extended, [])

    def test_stereotype_extended_null_input(self):
        a1 = self.m1.association(self.m2, name="a1", multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2")
        s = CStereotype(extended=None)
        eq_(a1.stereotypes, [])
        eq_(s.extended, [])

    def test_stereotype_extended_non_list_input(self):
        a1 = self.m1.association(self.m2, name="a1", multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2")
        s = CStereotype(extended=a1)
        eq_(a1.stereotypes, [s])
        eq_(s.extended, [a1])

    def test_stereotype_extended_append(self):
        a1 = self.m1.association(self.m2, name="a1", multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2")
        a2 = self.m1.association(self.m2, name="a2", multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2")
        s = CStereotype(extended=[a1])
        # should have no effect, as setter must be used
        s.extended.append(a2)
        eq_(a1.stereotypes, [s])
        eq_(a2.stereotypes, [])
        eq_(s.extended, [a1])

    def test_extended_association_that_is_deleted(self):
        a1 = self.m1.association(self.m2, name="a1", multiplicity="1", role_name="m1",
                                 source_multiplicity="*", source_role_name="m2")
        a1.delete()
        try:
            CStereotype(extended=[a1])
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")


if __name__ == "__main__":
    nose.main()
