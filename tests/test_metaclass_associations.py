import nose
from nose.tools import eq_

from codeable_models import CMetaclass, CClass, CException, CBundle, CStereotype
from tests.testing_commons import exception_expected_


class TestMetaclassAssociations:
    def setup(self):
        self.metaclassBundle = CBundle("P")
        self.m1 = CMetaclass("M1", bundles=self.metaclassBundle)
        self.m2 = CMetaclass("M2", bundles=self.metaclassBundle)
        self.m3 = CMetaclass("M3", bundles=self.metaclassBundle)
        self.m4 = CMetaclass("M4", bundles=self.metaclassBundle)
        self.m5 = CMetaclass("M5", bundles=self.metaclassBundle)

    def get_all_associations_in_bundle(self):
        associations = []
        for c in self.metaclassBundle.get_elements(type=CMetaclass):
            for a in c.all_associations:
                if a not in associations:
                    associations.append(a)
        return associations

    def test_association_creation(self):
        a1 = self.m1.association(self.m2, multiplicity="1", role_name="t",
                                 source_multiplicity="*", source_role_name="i")
        a2 = self.m1.association(self.m2, "[o]*->[s]1")
        a3 = self.m1.association(self.m3, "[a] 0..1 <*>- [n]*")
        a4 = self.m1.association(self.m3, multiplicity="*", role_name="e",
                                 source_multiplicity="0..1", source_role_name="a", composition=True)
        a5 = self.m4.association(self.m3, multiplicity="*", role_name="n",
                                 source_multiplicity="0..1", source_role_name="a", aggregation=True)
        a6 = self.m3.association(self.m2, '[a] 3 <>- [e]*')

        eq_(len(self.get_all_associations_in_bundle()), 6)

        eq_(self.m1.associations[0].role_name, "t")
        eq_(a5.role_name, "n")
        eq_(a2.role_name, "s")
        eq_(a1.multiplicity, "1")
        eq_(a1.source_multiplicity, "*")
        eq_(a4.source_multiplicity, "0..1")
        eq_(a6.source_multiplicity, "3")

        eq_(a1.composition, False)
        eq_(a1.aggregation, False)
        eq_(a3.composition, True)
        eq_(a3.aggregation, False)
        eq_(a5.composition, False)
        eq_(a5.aggregation, True)

        a1.aggregation = True
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)
        a1.composition = True
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)

    def test_mixed_association_types(self):
        c1 = CClass(self.m1, "C1")
        s1 = CStereotype("S1")
        try:
            self.m1.association(s1, multiplicity="1", role_name="t",
                                source_multiplicity="*", source_role_name="i")
            exception_expected_()
        except CException as e:
            eq_("metaclass 'M1' is not compatible with association target 'S1'", e.value)

        try:
            self.m1.association(c1, multiplicity="1", role_name="t",
                                source_multiplicity="*", source_role_name="i")
            exception_expected_()
        except CException as e:
            eq_("metaclass 'M1' is not compatible with association target 'C1'", e.value)

    def test_get_association_by_role_name(self):
        self.m1.association(self.m2, multiplicity="1", role_name="t",
                            source_multiplicity="*", source_role_name="i")
        self.m1.association(self.m2, multiplicity="1", role_name="s",
                            source_multiplicity="*", source_role_name="o")
        self.m1.association(self.m3, multiplicity="*", role_name="n",
                            source_multiplicity="0..1", source_role_name="a", composition=True)

        a_2 = next(a for a in self.m1.associations if a.role_name == "s")
        eq_(a_2.multiplicity, "1")
        eq_(a_2.source_role_name, "o")
        eq_(a_2.source_multiplicity, "*")

    def test_get_association_by_name(self):
        self.m1.association(self.m2, name="n1", multiplicity="1", role_name="t",
                            source_multiplicity="*", source_role_name="i")
        self.m1.association(self.m2, name="n2", multiplicity="1", role_name="s",
                            source_multiplicity="*", source_role_name="o")
        self.m1.association(self.m3, "n3: [a] 0..1 <*>- [n] *")

        a_2 = next(a for a in self.m1.associations if a.name == "n2")
        eq_(a_2.multiplicity, "1")
        eq_(a_2.source_role_name, "o")
        eq_(a_2.source_multiplicity, "*")

        a_3 = next(a for a in self.m1.associations if a.name == "n3")
        eq_(a_3.multiplicity, "*")
        eq_(a_3.role_name, "n")
        eq_(a_3.source_multiplicity, "0..1")
        eq_(a_3.source_role_name, "a")
        eq_(a_3.composition, True)

    def test_get_associations(self):
        a1 = self.m1.association(self.m2, multiplicity="1", role_name="t",
                                 source_multiplicity="*", source_role_name="i")
        a2 = self.m1.association(self.m2, multiplicity="1", role_name="s",
                                 source_multiplicity="*", source_role_name="o")
        a3 = self.m1.association(self.m3, multiplicity="*", role_name="n",
                                 source_multiplicity="0..1", source_role_name="a", composition=True)
        a4 = self.m1.association(self.m3, multiplicity="*", role_name="e",
                                 source_multiplicity="0..1", source_role_name="a", composition=True)
        a5 = self.m4.association(self.m3, multiplicity="*", role_name="n",
                                 source_multiplicity="0..1", source_role_name="a", aggregation=True)
        a6 = self.m3.association(self.m2, multiplicity="*", role_name="e",
                                 source_multiplicity="3", source_role_name="a", aggregation=True)
        eq_(self.m1.associations, [a1, a2, a3, a4])
        eq_(self.m2.associations, [a1, a2, a6])
        eq_(self.m3.associations, [a3, a4, a5, a6])
        eq_(self.m4.associations, [a5])
        eq_(self.m5.associations, [])

    def test_delete_associations(self):
        a1 = self.m1.association(self.m2, multiplicity="1", role_name="t",
                                 source_multiplicity="*", source_role_name="i")
        a2 = self.m1.association(self.m2, multiplicity="1", role_name="s",
                                 source_multiplicity="*", source_role_name="o")
        a3 = self.m1.association(self.m3, multiplicity="*", role_name="n",
                                 source_multiplicity="0..1", source_role_name="a", composition=True)
        a4 = self.m1.association(self.m3, multiplicity="*", role_name="e",
                                 source_multiplicity="0..1", source_role_name="a", composition=True)
        a5 = self.m4.association(self.m3, multiplicity="*", role_name="n",
                                 source_multiplicity="0..1", source_role_name="a", aggregation=True)
        a6 = self.m3.association(self.m2, multiplicity="*", role_name="e",
                                 source_multiplicity="3", source_role_name="a", aggregation=True)
        a7 = self.m1.association(self.m1, multiplicity="*", role_name="x",
                                 source_multiplicity="3", source_role_name="y")

        eq_(len(self.get_all_associations_in_bundle()), 7)

        a2.delete()
        a4.delete()

        eq_(len(self.get_all_associations_in_bundle()), 5)

        eq_(self.m1.associations, [a1, a3, a7])
        eq_(self.m2.associations, [a1, a6])
        eq_(self.m3.associations, [a3, a5, a6])
        eq_(self.m4.associations, [a5])
        eq_(self.m5.associations, [])

    def test_delete_class_and_get_associations(self):
        self.m1.association(self.m2, multiplicity="1", role_name="t",
                            source_multiplicity="*", source_role_name="i")
        self.m1.association(self.m2, multiplicity="1", role_name="s",
                            source_multiplicity="*", source_role_name="o")
        self.m1.association(self.m3, multiplicity="*", role_name="n",
                            source_multiplicity="0..1", source_role_name="a", composition=True)
        self.m1.association(self.m3, multiplicity="*", role_name="e",
                            source_multiplicity="0..1", source_role_name="a", composition=True)
        a5 = self.m4.association(self.m3, multiplicity="*", role_name="n",
                                 source_multiplicity="0..1", source_role_name="a", aggregation=True)
        a6 = self.m3.association(self.m2, multiplicity="*", role_name="e",
                                 source_multiplicity="3", source_role_name="a", aggregation=True)
        self.m1.association(self.m1, multiplicity="*", role_name="x",
                            source_multiplicity="3", source_role_name="y")

        eq_(len(self.get_all_associations_in_bundle()), 7)

        self.m1.delete()

        eq_(len(self.get_all_associations_in_bundle()), 2)

        eq_(self.m1.associations, [])
        eq_(self.m2.associations, [a6])
        eq_(self.m3.associations, [a5, a6])
        eq_(self.m4.associations, [a5])
        eq_(self.m5.associations, [])

    def test_all_associations(self):
        s = CMetaclass("S")
        d = CMetaclass("D", superclasses=s)
        a = s.association(d, "is next: [prior s] * -> [next d] *")
        eq_(d.all_associations, [a])
        eq_(s.all_associations, [a])

    def test_get_opposite_classifier(self):
        a = self.m1.association(self.m2, "[o]*->[s]1")
        eq_(a.get_opposite_classifier(self.m1), self.m2)
        eq_(a.get_opposite_classifier(self.m2), self.m1)
        try:
            a.get_opposite_classifier(self.m3)
            exception_expected_()
        except CException as e:
            eq_("can only get opposite if either source or target classifier is provided", e.value)


if __name__ == "__main__":
    nose.main()
