import nose
from nose.tools import eq_

from codeable_models import CMetaclass, CClass, CException
from tests.testing_commons import exception_expected_


class TestAssociationsEndsDescriptor:
    def setup(self):
        self.mcl = CMetaclass("MCL")
        self.c1 = CClass(self.mcl, "C1")
        self.c2 = CClass(self.mcl, "C2")
        self.c3 = CClass(self.mcl, "C3")
        self.c4 = CClass(self.mcl, "C4")
        self.c5 = CClass(self.mcl, "C5")

    def test_ends_string_malformed(self):
        try:
            self.c1.association(self.c2, '')
            exception_expected_()
        except CException as e:
            eq_("association descriptor malformed: ''", e.value)
        try:
            self.c1.association(self.c2, '->->')
            exception_expected_()
        except CException as e:
            eq_("malformed multiplicity: ''", e.value)
        try:
            self.c1.association(self.c2, 'a->b')
            exception_expected_()
        except CException as e:
            eq_("malformed multiplicity: 'a'", e.value)
        try:
            self.c1.association(self.c2, '[]->[]')
            exception_expected_()
        except CException as e:
            eq_("malformed multiplicity: '[]'", e.value)
        try:
            self.c1.association(self.c2, '[]1->[]*')
            exception_expected_()
        except CException as e:
            eq_("malformed multiplicity: '[]1'", e.value)
        try:
            self.c1.association(self.c2, '::1->1')
            exception_expected_()
        except CException as e:
            eq_("malformed multiplicity: ':1'", e.value)
        try:
            self.c1.association(self.c2, '1->1:')
            exception_expected_()
        except CException as e:
            eq_("association descriptor malformed: ''", e.value)

    def test_ends_string_association(self):
        a1 = self.c1.association(self.c2, '[a]1->[b]*')
        eq_(a1.role_name, "b")
        eq_(a1.source_role_name, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, ' [a b]  1   ->  [ b c_()-] * ')
        eq_(a1.role_name, " b c_()-")
        eq_(a1.source_role_name, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, '1..3->    4..*  ')
        eq_(a1.role_name, None)
        eq_(a1.source_role_name, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.source_multiplicity, "1..3")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, '[ax] -> [bx]')
        eq_(a1.role_name, "bx")
        eq_(a1.source_role_name, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)

    def test_ends_string_aggregation(self):
        a1 = self.c1.association(self.c2, '[a]1<>-[b]*')
        eq_(a1.role_name, "b")
        eq_(a1.source_role_name, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)

        a1 = self.c1.association(self.c2, ' [a b]  1   <>-  [ b c_()-] * ')
        eq_(a1.role_name, " b c_()-")
        eq_(a1.source_role_name, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)

        a1 = self.c1.association(self.c2, '1..3<>-    4..*  ')
        eq_(a1.role_name, None)
        eq_(a1.source_role_name, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.source_multiplicity, "1..3")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)

        a1 = self.c1.association(self.c2, '[ax] <>- [bx]')
        eq_(a1.role_name, "bx")
        eq_(a1.source_role_name, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)

    def test_ends_string_composition(self):
        a1 = self.c1.association(self.c2, '[a]1<*>-[b]*')
        eq_(a1.role_name, "b")
        eq_(a1.source_role_name, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, ' [a b]  1   <*>-  [ b c_()-] * ')
        eq_(a1.role_name, " b c_()-")
        eq_(a1.source_role_name, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, '1..3<*>-    4..*  ')
        eq_(a1.role_name, None)
        eq_(a1.source_role_name, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.source_multiplicity, "1..3")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, '[ax] <*>- [bx]')
        eq_(a1.role_name, "bx")
        eq_(a1.source_role_name, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)

    def test_ends_string_association_with_name(self):
        a1 = self.c1.association(self.c2, ' assoc a : [a]1->[b]*')
        eq_(a1.role_name, "b")
        eq_(a1.source_role_name, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)
        eq_(a1.name, "assoc a")

        a1 = self.c1.association(self.c2, 'a: [a b]  1   ->  [ b c_()-] * ')
        eq_(a1.role_name, " b c_()-")
        eq_(a1.source_role_name, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)
        eq_(a1.name, "a")

        a1 = self.c1.association(self.c2, '"legal_name":1..3->    4..*  ')
        eq_(a1.role_name, None)
        eq_(a1.source_role_name, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.source_multiplicity, "1..3")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)
        eq_(a1.name, '"legal_name"')

        a1 = self.c1.association(self.c2, '[ax] -> [bx]:[ax] -> [bx]')
        eq_(a1.role_name, "bx")
        eq_(a1.source_role_name, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)
        eq_(a1.name, '[ax] -> [bx]')

    def test_ends_string_aggregation_with_name(self):
        a1 = self.c1.association(self.c2, ' assoc a : [a]1<>-[b]*')
        eq_(a1.role_name, "b")
        eq_(a1.source_role_name, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)
        eq_(a1.name, "assoc a")

        a1 = self.c1.association(self.c2, ': [a b]  1   <>-  [ b c_()-] * ')
        eq_(a1.role_name, " b c_()-")
        eq_(a1.source_role_name, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.name, "")

        a1 = self.c1.association(self.c2, '"legal_name":1..3<>-    4..*  ')
        eq_(a1.role_name, None)
        eq_(a1.source_role_name, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.source_multiplicity, "1..3")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)
        eq_(a1.name, '"legal_name"')

        a1 = self.c1.association(self.c2, '[ax] <>- [bx]:[ax] <>- [bx]')
        eq_(a1.role_name, "bx")
        eq_(a1.source_role_name, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)
        eq_(a1.name, '[ax] <>- [bx]')

    def test_ends_string_composition_with_name(self):
        a1 = self.c1.association(self.c2, ' assoc a : [a]1<*>-[b]*')
        eq_(a1.role_name, "b")
        eq_(a1.source_role_name, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)
        eq_(a1.name, "assoc a")

        a1 = self.c1.association(self.c2, 'a: [a b]  1   <*>-  [ b c_()-] * ')
        eq_(a1.role_name, " b c_()-")
        eq_(a1.source_role_name, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)
        eq_(a1.name, "a")

        a1 = self.c1.association(self.c2, '"legal_name":1..3<*>-    4..*  ')
        eq_(a1.role_name, None)
        eq_(a1.source_role_name, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.source_multiplicity, "1..3")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)
        eq_(a1.name, '"legal_name"')

        a1 = self.c1.association(self.c2, '[ax] <*>- [bx]:[ax] <*>- [bx]')
        eq_(a1.role_name, "bx")
        eq_(a1.source_role_name, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.source_multiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)
        eq_(a1.name, '[ax] <*>- [bx]')


if __name__ == "__main__":
    nose.main()
