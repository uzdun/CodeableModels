import nose
from nose.tools import ok_, eq_
from parameterized import parameterized

from codeable_models import CBundle, CMetaclass, CClass, CException, CStereotype
from tests.testing_commons import exception_expected_


class TestMetaclass:
    def test_creation_of_one_metaclass(self):
        mcl = CMetaclass("MCL")
        eq_(mcl.name, "MCL")
        cl = CClass(mcl, "C")
        eq_(cl.metaclass, mcl)

    def test_creation_of_unnamed_metaclass(self):
        mcl = CMetaclass()
        eq_(mcl.name, None)

    def test_delete_metaclass(self):
        m = CMetaclass("M1")
        cl = CClass(m, "C")
        m.delete()
        eq_(cl.metaclass, None)

        m1 = CMetaclass("M1")
        m2 = CMetaclass("M2")
        m3 = CMetaclass("M3", superclasses=m2, attributes={"i": 1}, stereotypes=CStereotype("S"))
        cl = CClass(m3, "C")
        m1.delete()
        eq_(cl.metaclass, m3)
        m3.delete()
        eq_(cl.metaclass, None)

        eq_(m3.superclasses, [])
        eq_(m2.subclasses, [])
        eq_(m3.attributes, [])
        eq_(m3.attribute_names, [])
        eq_(m3.stereotypes, [])
        eq_(m3.classes, [])
        eq_(m3.name, None)
        eq_(m3.bundles, [])

    def test_delete_metaclass_classes_relation(self):
        m1 = CMetaclass()
        m2 = CMetaclass()
        cl1 = CClass(m1)
        cl2 = CClass(m1)
        cl3 = CClass(m2)

        m1.delete()

        eq_(cl1.metaclass, None)
        eq_(cl2.metaclass, None)
        eq_(cl3.metaclass, m2)
        eq_(set(m2.classes), {cl3})
        eq_(m1.classes, [])

    def test_get_classes_by_name(self):
        m1 = CMetaclass()
        eq_(set(m1.get_classes("CL1")), set())
        c1 = CClass(m1, "CL1")
        eq_(m1.classes, [c1])
        eq_(set(m1.get_classes("CL1")), {c1})
        c2 = CClass(m1, "CL1")
        eq_(set(m1.get_classes("CL1")), {c1, c2})
        ok_(c1 != c2)
        c3 = CClass(m1, "CL1")
        eq_(set(m1.get_classes("CL1")), {c1, c2, c3})
        eq_(m1.get_class("CL1"), c1)

    def test_get_stereotypes_by_name(self):
        m1 = CMetaclass()
        eq_(set(m1.get_stereotypes("S1")), set())
        s1 = CStereotype("S1", extended=m1)
        eq_(m1.stereotypes, [s1])
        eq_(set(m1.get_stereotypes("S1")), {s1})
        s2 = CStereotype("S1", extended=m1)
        eq_(set(m1.get_stereotypes("S1")), {s1, s2})
        ok_(s1 != s2)
        s3 = CStereotype("S1", extended=m1)
        eq_(set(m1.get_stereotypes("S1")), {s1, s2, s3})
        eq_(m1.get_stereotype("S1"), s1)

    def test_stereotypes_that_are_deleted(self):
        s1 = CStereotype("S1")
        s1.delete()
        try:
            CMetaclass(stereotypes=[s1])
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_stereotypes_that_are_none(self):
        try:
            CMetaclass(stereotypes=[None])
            exception_expected_()
        except CException as e:
            eq_(e.value, "'None' is not a stereotype")

    def test_get_connected_elements__wrong_keyword_arg(self):
        m1 = CMetaclass("m1")
        try:
            m1.get_connected_elements(a="m1")
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keyword argument 'a', should be one of: " +
                "['add_associations', 'add_stereotypes', 'process_stereotypes', 'add_bundles', 'process_bundles', " +
                "'stop_elements_inclusive', 'stop_elements_exclusive']")

    def test_get_connected_elements_empty(self):
        m1 = CMetaclass("m1")
        eq_(set(m1.get_connected_elements()), {m1})

    m1 = CMetaclass("m1")
    m2 = CMetaclass("m2", superclasses=m1)
    m3 = CMetaclass("m3", superclasses=m2)
    m4 = CMetaclass("m4", superclasses=m2)
    m5 = CMetaclass("m5", superclasses=m4)
    m6 = CMetaclass("m6")
    a1 = m1.association(m6)
    m7 = CMetaclass("m7")
    m8 = CMetaclass("m8")
    a3 = m8.association(m7)
    m9 = CMetaclass("m9")
    a4 = m7.association(m9)
    m10 = CMetaclass("m10")
    m11 = CMetaclass("m11", superclasses=m10)
    m12 = CMetaclass("m12")
    m13 = CMetaclass("m13")
    m12.association(m11)
    b_sub = CBundle("b_sub", elements=[m13])
    b1 = CBundle("b1", elements=[m1, m2, m3, b_sub, m7])
    b2 = CBundle("b2", elements=[m7, m10, m11, m12])

    m14 = CMetaclass("m14")
    s1 = CStereotype("s1")
    s2 = CStereotype("s2", extended=[m7, m14], superclasses=s1)

    all_test_elements = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, b1, b2, b_sub, m14, s1, s2]

    @parameterized.expand([
        (all_test_elements, {"process_stereotypes": True, "process_bundles": True},
         {m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14}),
        (all_test_elements,
         {"process_stereotypes": True, "process_bundles": True, "add_stereotypes": True, "add_bundles": True},
         {m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, b1, b2, b_sub, s1, s2}),
        (all_test_elements, {"process_stereotypes": True, "process_bundles": True, "add_bundles": True},
         {m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, b1, b2, b_sub}),
        (all_test_elements, {"process_stereotypes": True, "process_bundles": True, "add_stereotypes": True},
         {m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, s1, s2}),
        ([m1], {"process_bundles": True}, {m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13}),
        ([m1], {"process_bundles": True, "add_stereotypes": True, "add_bundles": True},
         {m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, b1, b2, b_sub, s1, s2}),
        ([m1], {"process_bundles": True, "add_bundles": True},
         {m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, b1, b2, b_sub}),
        ([m1], {"process_bundles": True, "add_stereotypes": True},
         {m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, s1, s2}),
        ([m7], {"process_stereotypes": True}, {m7, m8, m9, m14}),
        ([m7], {"process_stereotypes": True, "add_stereotypes": True, "add_bundles": True},
         {m7, m8, m9, m14, b1, b2, s1, s2}),
        ([m7], {"process_stereotypes": True, "add_bundles": True}, {m7, m8, m9, m14, b1, b2}),
        ([m7], {"process_stereotypes": True, "add_stereotypes": True}, {m7, m8, m9, m14, s1, s2}),
        ([m7], {}, {m7, m8, m9}),
        ([m7], {"add_stereotypes": True, "add_bundles": True}, {m7, m8, m9, b1, b2, s1, s2}),
        ([m7], {"add_bundles": True}, {m7, m8, m9, b1, b2}),
        ([m7], {"add_stereotypes": True}, {m7, m8, m9, s1, s2})])
    def test_get_connected_elements(self, test_elements, kwargs_dict, connected_elements_result):
        for elt in test_elements:
            eq_(set(elt.get_connected_elements(**kwargs_dict)), connected_elements_result)

    def test_get_connected_elements_stop_elements_inclusive_wrong_types(self):
        m1 = CMetaclass("m1")
        try:
            m1.get_connected_elements(stop_elements_inclusive="m1")
            exception_expected_()
        except CException as e:
            eq_(e.value, "expected one element or a list of stop elements, but got: 'm1'")
        try:
            m1.get_connected_elements(stop_elements_inclusive=["m1"])
            exception_expected_()
        except CException as e:
            eq_(e.value,
                "expected one element or a list of stop elements, but got: '['m1']' with element of wrong type: 'm1'")

    @parameterized.expand([
        ([m1], {"stop_elements_exclusive": [m1]}, set()),
        ([m1], {"stop_elements_inclusive": [m3, m6]}, {m1, m2, m3, m4, m5, m6}),
        ([m1], {"stop_elements_exclusive": [m3, m6]}, {m1, m2, m4, m5}),
        ([m1], {"stop_elements_inclusive": [m3, m6], "stop_elements_exclusive": [m3]}, {m1, m2, m4, m5, m6}),
        ([m7], {"stop_elements_inclusive": [b2, s2], "stop_elements_exclusive": [b1], "process_stereotypes": True,
                "process_bundles": True, "add_stereotypes": True, "add_bundles": True}, {m7, b2, s2, m8, m9}),
        ([m7], {"stop_elements_exclusive": [b1, b2, s2], "process_stereotypes": True, "process_bundles": True,
                "add_stereotypes": True, "add_bundles": True}, {m7, m8, m9}),
        ([b2],
         {"stop_elements_inclusive": [b1, m8, m9], "stop_elements_exclusive": [s1, s2], "process_stereotypes": True,
          "process_bundles": True, "add_stereotypes": True, "add_bundles": True},
         {m7, m10, m11, m12, m8, m9, b1, b2}),
        ([b2],
         {"stop_elements_inclusive": [b1, m8, m9], "stop_elements_exclusive": [s1, s2], "process_stereotypes": True,
          "process_bundles": True}, {m7, m10, m11, m12, m8, m9}),
        ([s1], {"stop_elements_inclusive": [m14, m7], "process_stereotypes": True, "process_bundles": True,
                "add_stereotypes": True, "add_bundles": True}, {s1, s2, m7, m14}),
        ([s1], {"stop_elements_inclusive": [m14, m7], "process_stereotypes": True, "process_bundles": True},
         {m7, m14})
    ])
    def test_get_connected_elements_stop_elements_inclusive(self, test_elements, kwargs_dict,
                                                            connected_elements_result):
        for elt in test_elements:
            eq_(set(elt.get_connected_elements(**kwargs_dict)), connected_elements_result)


if __name__ == "__main__":
    nose.main()
