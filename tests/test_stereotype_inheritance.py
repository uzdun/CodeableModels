import re

import nose
from nose.tools import ok_, eq_

from codeable_models import CMetaclass, CStereotype, CClass, CException
from tests.testing_commons import exception_expected_


class TestStereotypeInheritance:
    def setup(self):
        self.mcl = CMetaclass("MCL")

    def test_stereotype_no_inheritance(self):
        t = CStereotype("T")
        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set())
        eq_(set(t.all_superclasses), set())
        eq_(set(t.all_subclasses), set())

    def test_stereotype_superclasses_empty_input(self):
        m1 = CStereotype("M1", superclasses=[])
        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())

    def test_stereotype_superclasses_none_input(self):
        m1 = CStereotype("M1", superclasses=None)
        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())

    def test_stereotype_simple_inheritance(self):
        t = CStereotype("T")
        m1 = CStereotype("M1", superclasses=t)
        m2 = CStereotype("M2", superclasses=t)
        b1 = CStereotype("B1", superclasses=m1)
        b2 = CStereotype("B2", superclasses=m1)
        b3 = CStereotype("B3", superclasses=t)

        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), {m1, m2, b3})
        eq_(set(t.all_superclasses), set())
        eq_(set(t.all_subclasses), {m1, m2, b1, b2, b3})

        eq_(set(m1.superclasses), {t})
        eq_(set(m1.subclasses), {b1, b2})
        eq_(set(m1.all_superclasses), {t})
        eq_(set(m1.all_subclasses), {b1, b2})

        eq_(set(m2.superclasses), {t})
        eq_(set(m2.subclasses), set())
        eq_(set(m2.all_superclasses), {t})
        eq_(set(m2.all_subclasses), set())

        eq_(set(b1.superclasses), {m1})
        eq_(set(b1.subclasses), set())
        eq_(set(b1.all_superclasses), {t, m1})
        eq_(set(b1.all_subclasses), set())

        eq_(set(b2.superclasses), {m1})
        eq_(set(b2.subclasses), set())
        eq_(set(b2.all_superclasses), {t, m1})
        eq_(set(b2.all_subclasses), set())

        eq_(set(b3.superclasses), {t})
        eq_(set(b3.subclasses), set())
        eq_(set(b3.all_superclasses), {t})
        eq_(set(b3.all_subclasses), set())

    def test_stereotype_inheritance_double_assignment(self):
        m = CMetaclass("M")
        t = CStereotype("T")
        try:
            CStereotype("S1", extended=m, superclasses=[t, t])
            exception_expected_()
        except CException as e:
            eq_("'T' is already a superclass of 'S1'", e.value)
        s1 = m.get_stereotype("S1")
        eq_(s1.name, "S1")
        eq_(set(s1.superclasses), {t})

    def test_stereotype_inheritance_delete_top_class(self):
        t = CStereotype("T")
        m1 = CStereotype("M1", superclasses=[t])
        m2 = CStereotype("M2", superclasses=[t])
        b1 = CStereotype("B1", superclasses=[m1])
        b2 = CStereotype("B2", superclasses=[m1])
        b3 = CStereotype("B3", superclasses=[t])

        t.delete()

        eq_(t.name, None)
        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set())
        eq_(set(t.all_superclasses), set())
        eq_(set(t.all_subclasses), set())

        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), {b1, b2})
        eq_(set(m1.all_superclasses), set())
        eq_(set(m1.all_subclasses), {b1, b2})

        eq_(set(m2.superclasses), set())
        eq_(set(m2.subclasses), set())
        eq_(set(m2.all_superclasses), set())
        eq_(set(m2.all_subclasses), set())

        eq_(set(b1.superclasses), {m1})
        eq_(set(b1.subclasses), set())
        eq_(set(b1.all_superclasses), {m1})
        eq_(set(b1.all_subclasses), set())

        eq_(set(b2.superclasses), {m1})
        eq_(set(b2.subclasses), set())
        eq_(set(b2.all_superclasses), {m1})
        eq_(set(b2.all_subclasses), set())

        eq_(set(b3.superclasses), set())
        eq_(set(b3.subclasses), set())
        eq_(set(b3.all_superclasses), set())
        eq_(set(b3.all_subclasses), set())

    def test_stereotype_inheritance_delete_inner_class(self):
        t = CStereotype("T")
        m1 = CStereotype("M1", superclasses=[t])
        m2 = CStereotype("M2", superclasses=[t])
        b1 = CStereotype("B1", superclasses=[m1])
        b2 = CStereotype("B2", superclasses=[m1])
        b3 = CStereotype("B3", superclasses=[t])

        m1.delete()

        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), {m2, b3})
        eq_(set(t.all_superclasses), set())
        eq_(set(t.all_subclasses), {m2, b3})

        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())
        eq_(set(m1.all_superclasses), set())
        eq_(set(m1.all_subclasses), set())

        eq_(set(m2.superclasses), {t})
        eq_(set(m2.subclasses), set())
        eq_(set(m2.all_superclasses), {t})
        eq_(set(m2.all_subclasses), set())

        eq_(set(b1.superclasses), set())
        eq_(set(b1.subclasses), set())
        eq_(set(b1.all_superclasses), set())
        eq_(set(b1.all_subclasses), set())

        eq_(set(b2.superclasses), set())
        eq_(set(b2.subclasses), set())
        eq_(set(b2.all_superclasses), set())
        eq_(set(b2.all_subclasses), set())

        eq_(set(b3.superclasses), {t})
        eq_(set(b3.subclasses), set())
        eq_(set(b3.all_superclasses), {t})
        eq_(set(b3.all_subclasses), set())

    def test_stereotype_superclasses_reassignment(self):
        t = CStereotype("T")
        m1 = CStereotype("M1", superclasses=[t])
        m2 = CStereotype("M2", superclasses=[t])
        b1 = CStereotype("B1", superclasses=[m1])
        b2 = CStereotype("B2", superclasses=[m1])
        b3 = CStereotype("B3", superclasses=[t])

        m1.superclasses = []
        b1.superclasses = []
        b2.superclasses = []

        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), {m2, b3})
        eq_(set(t.all_superclasses), set())
        eq_(set(t.all_subclasses), {m2, b3})

        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())
        eq_(set(m1.all_superclasses), set())
        eq_(set(m1.all_subclasses), set())

        eq_(set(m2.superclasses), {t})
        eq_(set(m2.subclasses), set())
        eq_(set(m2.all_superclasses), {t})
        eq_(set(m2.all_subclasses), set())

        eq_(set(b1.superclasses), set())
        eq_(set(b1.subclasses), set())
        eq_(set(b1.all_superclasses), set())
        eq_(set(b1.all_subclasses), set())

        eq_(set(b2.superclasses), set())
        eq_(set(b2.subclasses), set())
        eq_(set(b2.all_superclasses), set())
        eq_(set(b2.all_subclasses), set())

        eq_(set(b3.superclasses), {t})
        eq_(set(b3.subclasses), set())
        eq_(set(b3.all_superclasses), {t})
        eq_(set(b3.all_subclasses), set())

    def test_stereotype_multiple_inheritance(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        t3 = CStereotype("T3")
        m1 = CStereotype("M1", superclasses=[t1, t3])
        m2 = CStereotype("M2", superclasses=[t2, t3])
        b1 = CStereotype("B1", superclasses=[m1])
        b2 = CStereotype("B2", superclasses=[m1, m2])
        b3 = CStereotype("B3", superclasses=[m2, m1])

        eq_(set(t1.superclasses), set())
        eq_(set(t1.subclasses), {m1})
        eq_(set(t1.all_superclasses), set())
        eq_(set(t1.all_subclasses), {m1, b1, b2, b3})

        eq_(set(t2.superclasses), set())
        eq_(set(t2.subclasses), {m2})
        eq_(set(t2.all_superclasses), set())
        eq_(set(t2.all_subclasses), {m2, b3, b2})

        eq_(set(t3.superclasses), set())
        eq_(set(t3.subclasses), {m2, m1})
        eq_(set(t3.all_superclasses), set())
        eq_(set(t3.all_subclasses), {m2, m1, b1, b2, b3})

        eq_(set(m1.superclasses), {t1, t3})
        eq_(set(m1.subclasses), {b1, b2, b3})
        eq_(set(m1.all_superclasses), {t1, t3})
        eq_(set(m1.all_subclasses), {b1, b2, b3})

        eq_(set(m2.superclasses), {t2, t3})
        eq_(set(m2.subclasses), {b2, b3})
        eq_(set(m2.all_superclasses), {t2, t3})
        eq_(set(m2.all_subclasses), {b2, b3})

        eq_(set(b1.superclasses), {m1})
        eq_(set(b1.subclasses), set())
        eq_(set(b1.all_superclasses), {m1, t1, t3})
        eq_(set(b1.all_subclasses), set())

        eq_(set(b2.superclasses), {m1, m2})
        eq_(set(b2.subclasses), set())
        eq_(set(b2.all_superclasses), {m1, m2, t1, t2, t3})
        eq_(set(b2.all_subclasses), set())

        eq_(set(b3.superclasses), {m1, m2})
        eq_(set(b3.subclasses), set())
        eq_(set(b3.all_superclasses), {m1, m2, t1, t2, t3})
        eq_(set(b3.all_subclasses), set())

    def test_stereotype_as_wrong_type_of_superclass(self):
        t = CStereotype("S")
        try:
            CMetaclass("M", superclasses=[t])
            exception_expected_()
        except CException as e:
            ok_(re.match("^cannot add superclass 'S' to 'M': not of type([_ <a-zA-Z.']+)CMetaclass'>$", e.value))
        try:
            CClass(CMetaclass(), "C", superclasses=[t])
            exception_expected_()
        except CException as e:
            ok_(re.match("^cannot add superclass 'S' to 'C': not of type([_ <a-zA-Z.']+)CClass'>$", e.value))

    def test_extended_classes_of_inheriting_stereotypes__superclass_has_none(self):
        m1 = CMetaclass()
        m2 = CMetaclass(superclasses=[m1])
        s1 = CStereotype()
        s2 = CStereotype(superclasses=[s1])
        m2.stereotypes = s2
        eq_(len(s1.extended), 0)
        eq_(set(m2.stereotypes), {s2})

    def test_extended_classes_of_inheriting_stereotypes__superclass_has_the_same(self):
        m1 = CMetaclass()
        s1 = CStereotype(extended=[m1])
        s2 = CStereotype(superclasses=[s1], extended=[m1])
        eq_(set(s1.extended), {m1})
        eq_(set(s2.extended), {m1})
        eq_(set(m1.stereotypes), {s2, s1})

    def test_extended_classes_of_inheriting_stereotypes__remove_superclass_stereotype(self):
        m1 = CMetaclass()
        s1 = CStereotype(extended=[m1])
        s2 = CStereotype(superclasses=[s1], extended=[m1])
        m1.stereotypes = s2
        eq_(set(s1.extended), set())
        eq_(set(s2.extended), {m1})
        eq_(set(m1.stereotypes), {s2})

    def test_extended_classes_of_inheriting_stereotypes__superclass_is_set_to_the_same(self):
        m1 = CMetaclass("M1")
        s1 = CStereotype("S1")
        s2 = CStereotype("S2", extended=[m1], superclasses=[s1])
        m1.stereotypes = [s2, s1]
        eq_(set(s1.extended), {m1})
        eq_(set(s2.extended), {m1})
        eq_(set(m1.stereotypes), {s2, s1})

    def test_extended_classes_of_inheriting_stereotypes__superclass_has_metaclasses_superclass(self):
        m1 = CMetaclass()
        m2 = CMetaclass(superclasses=[m1])
        s1 = CStereotype(extended=[m1])
        s2 = CStereotype(superclasses=[s1], extended=[m2])
        eq_(set(s1.extended), {m1})
        eq_(set(s2.extended), {m2})
        eq_(set(m1.stereotypes), {s1})
        eq_(set(m2.stereotypes), {s2})

    def test_extended_classes_of_inheriting_stereotypes__superclass_has_metaclasses_superclass_indirectly(self):
        m1 = CMetaclass()
        m2 = CMetaclass(superclasses=[m1])
        m3 = CMetaclass(superclasses=[m2])
        s1 = CStereotype(extended=[m1])
        s2 = CStereotype(superclasses=[s1], extended=[m3])
        eq_(set(s1.extended), {m1})
        eq_(set(s2.extended), {m3})
        eq_(set(m1.stereotypes), {s1})
        eq_(set(m3.stereotypes), {s2})

    def test_extended_classes_of_inheriting_stereotypes__superclass_is_set_to_metaclasses_superclass_indirectly(self):
        m1 = CMetaclass()
        m2 = CMetaclass(superclasses=[m1])
        m3 = CMetaclass(superclasses=[m2])
        s1 = CStereotype()
        s2 = CStereotype(superclasses=[s1], extended=[m3])
        m1.stereotypes = s1
        eq_(set(s1.extended), {m1})
        eq_(set(s2.extended), {m3})
        eq_(set(m1.stereotypes), {s1})
        eq_(set(m3.stereotypes), {s2})

    def test_stereotype_has_superclass_has_subclass(self):
        c1 = CStereotype("C1")
        c2 = CStereotype("C2", superclasses=[c1])
        c3 = CStereotype("C3", superclasses=[c2])
        c4 = CStereotype("C4", superclasses=[c2])
        c5 = CStereotype("C5", superclasses=[])

        eq_(c1.has_superclass(c2), False)
        eq_(c5.has_superclass(c2), False)
        eq_(c1.has_superclass(None), False)
        eq_(c5.has_superclass(None), False)
        eq_(c2.has_superclass(c1), True)
        eq_(c3.has_superclass(c2), True)
        eq_(c3.has_superclass(c2), True)
        eq_(c4.has_superclass(c2), True)
        eq_(c3.has_subclass(c2), False)
        eq_(c3.has_subclass(None), False)
        eq_(c5.has_subclass(c2), False)
        eq_(c5.has_subclass(None), False)
        eq_(c1.has_subclass(c3), True)
        eq_(c1.has_subclass(c2), True)

    def test_stereotype_unknown_non_positional_argument(self):
        t = CStereotype("T")
        try:
            CStereotype("ST", superclass=t)
            exception_expected_()
        except CException as e:
            eq_("unknown keyword argument 'superclass', should be one of: " +
                "['extended', 'default_values', 'attributes', 'superclasses', 'bundles']",
                e.value)

    def test_super_stereotypes_that_are_deleted(self):
        s1 = CStereotype("S1")
        s1.delete()
        try:
            CStereotype(superclasses=[s1])
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_super_stereotypes_that_are_none(self):
        try:
            CStereotype("S", superclasses=[None])
            exception_expected_()
        except CException as e:
            ok_(e.value.startswith("cannot add superclass 'None' to 'S': not of type"))


if __name__ == "__main__":
    nose.main()
