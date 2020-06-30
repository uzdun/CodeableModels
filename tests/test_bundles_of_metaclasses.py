import nose
from nose.tools import ok_, eq_

from codeable_models import CBundle, CMetaclass, CClass, CObject, CAttribute, CException, CEnum
from tests.testing_commons import exception_expected_


class TestBundlesOfMetaclasses:
    def setup(self):
        self.b1 = CBundle("B1")
        self.b2 = CBundle("B2")

    def test_metaclass_name_fail(self):
        try:
            # noinspection PyTypeChecker
            CMetaclass(self.b1)
            exception_expected_()
        except CException as e:
            ok_(e.value.startswith("is not a name string: '"))
            ok_(e.value.endswith(" B1'"))

    def test_metaclass_defined_bundles(self):
        eq_(set(self.b1.get_elements()), set())
        m1 = CMetaclass("M1", bundles=self.b1)
        eq_(set(self.b1.get_elements()), {m1})
        m2 = CMetaclass("M2", bundles=[self.b1])
        m3 = CMetaclass("M3", bundles=[self.b1, self.b2])
        cl = CClass(m1, "C", bundles=[self.b1, self.b2])
        eq_(set(self.b1.get_elements(type=CMetaclass)), {m1, m2, m3})
        eq_(set(self.b1.elements), {m1, m2, m3, cl})
        eq_(set(self.b2.get_elements(type=CMetaclass)), {m3})
        eq_(set(self.b2.elements), {m3, cl})

    def test_bundle_defined_metaclasses(self):
        m1 = CMetaclass("M1")
        m2 = CMetaclass("M2")
        m3 = CMetaclass("M3")
        eq_(set(self.b1.get_elements(type=CMetaclass)), set())
        b1 = CBundle("B1", elements=[m1, m2, m3])
        eq_(set(b1.elements), {m1, m2, m3})
        cl = CClass(m1, "C", bundles=b1)
        eq_(set(b1.elements), {m1, m2, m3, cl})
        eq_(set(b1.get_elements(type=CMetaclass)), {m1, m2, m3})
        b2 = CBundle("B2")
        b2.elements = [m2, m3]
        eq_(set(b2.get_elements(type=CMetaclass)), {m2, m3})
        eq_(set(m1.bundles), {b1})
        eq_(set(m2.bundles), {b1, b2})
        eq_(set(m3.bundles), {b1, b2})

    def test_get_metaclasses_by_name(self):
        eq_(set(self.b1.get_elements(type=CMetaclass, name="m1")), set())
        m1 = CMetaclass("M1", bundles=self.b1)
        c1 = CClass(m1, "C1", bundles=self.b1)
        eq_(self.b1.get_elements(type=CClass), [c1])
        eq_(set(self.b1.get_elements(type=CMetaclass, name="M1")), {m1})
        m2 = CMetaclass("M1", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CMetaclass, name="M1")), {m1, m2})
        ok_(m1 != m2)
        m3 = CMetaclass("M1", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CMetaclass, name="M1")), {m1, m2, m3})
        eq_(self.b1.get_element(type=CMetaclass, name="M1"), m1)

    def test_get_metaclass_elements_by_name(self):
        eq_(set(self.b1.get_elements(name="M1")), set())
        m1 = CMetaclass("M1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="M1")), {m1})
        c1 = CClass(m1, "M1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="M1")), {m1, c1})
        m2 = CMetaclass("M1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="M1")), {m1, c1, m2})
        ok_(m1 != m2)
        m3 = CMetaclass("M1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="M1")), {m1, c1, m2, m3})
        eq_(self.b1.get_element(name="M1"), m1)

    def test_metaclass_defined_bundle_change(self):
        m1 = CMetaclass("M1", bundles=self.b1)
        m2 = CMetaclass("M2", bundles=self.b1)
        m3 = CMetaclass("M3", bundles=self.b1)
        cl1 = CClass(m1, "C1", bundles=self.b1)
        cl2 = CClass(m1, "C2", bundles=self.b1)
        b = CBundle()
        m2.bundles = b
        m3.bundles = None
        cl2.bundles = b
        eq_(set(self.b1.elements), {cl1, m1})
        eq_(set(self.b1.get_elements(type=CMetaclass)), {m1})
        eq_(set(b.elements), {m2, cl2})
        eq_(set(b.get_elements(type=CMetaclass)), {m2})
        eq_(m1.bundles, [self.b1])
        eq_(m2.bundles, [b])
        eq_(m3.bundles, [])

    def test_bundle_delete_metaclass(self):
        m1 = CMetaclass("M1", bundles=self.b1)
        c = CClass(m1)
        eq_(m1.classes, [c])
        m2 = CMetaclass("M2", bundles=self.b1)
        m3 = CMetaclass("M3", bundles=self.b1)
        self.b1.delete()
        eq_(set(self.b1.elements), set())
        eq_(m1.bundles, [])
        eq_(m1.classes, [c])
        eq_(m2.bundles, [])
        eq_(m3.bundles, [])

    def test_creation_of_unnamed_metaclass_in_bundle(self):
        m1 = CMetaclass()
        m2 = CMetaclass()
        m3 = CMetaclass("x")
        cl = CClass(m1)
        self.b1.elements = [m1, m2, m3, cl]
        eq_(set(self.b1.get_elements(type=CMetaclass)), {m1, m2, m3})
        eq_(self.b1.get_element(name=None), m1)
        eq_(set(self.b1.get_elements(type=CMetaclass, name=None)), {m1, m2})
        eq_(set(self.b1.get_elements(name=None)), {m1, m2, cl})

    def test_remove_metaclass_from_bundle(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        m1 = CMetaclass("M1", bundles=b1)
        try:
            # noinspection PyTypeChecker
            b1.remove(None)
            exception_expected_()
        except CException as e:
            eq_("'None' is not an element of the bundle", e.value)
        try:
            b1.remove(CEnum("A"))
            exception_expected_()
        except CException as e:
            eq_("'A' is not an element of the bundle", e.value)
        try:
            b2.remove(m1)
            exception_expected_()
        except CException as e:
            eq_("'M1' is not an element of the bundle", e.value)
        b1.remove(m1)
        eq_(set(b1.get_elements(type=CMetaclass)), set())

        m1 = CMetaclass("M1", bundles=b1)
        m2 = CMetaclass("M1", bundles=b1)
        m3 = CMetaclass("M1", superclasses=m2, attributes={"i": 1}, bundles=b1)
        c = CClass(m3, bundles=b1)

        b1.remove(m1)
        try:
            b1.remove(CMetaclass("M2", bundles=b2))
            exception_expected_()
        except CException as e:
            eq_("'M2' is not an element of the bundle", e.value)
        try:
            b1.remove(m1)
            exception_expected_()
        except CException as e:
            eq_("'M1' is not an element of the bundle", e.value)

        eq_(set(b1.get_elements(type=CMetaclass)), {m2, m3})
        b1.remove(m3)
        eq_(set(b1.get_elements(type=CMetaclass)), {m2})

        eq_(m3.superclasses, [m2])
        eq_(m2.subclasses, [m3])
        eq_(m3.attribute_names, ["i"])
        eq_(m3.classes, [c])
        eq_(m3.name, "M1")
        eq_(m3.bundles, [])
        eq_(b1.get_elements(type=CClass), [c])

    def test_delete_metaclass_from_bundle(self):
        b1 = CBundle("B1")
        CBundle("B2")
        m1 = CMetaclass("M1", bundles=b1)
        m1.delete()
        eq_(set(b1.get_elements(type=CMetaclass)), set())

        m1 = CMetaclass("M1", bundles=b1)
        m2 = CMetaclass("M1", bundles=b1)
        m3 = CMetaclass("M1", superclasses=m2, attributes={"i": 1}, bundles=b1)
        CClass(m3, bundles=b1)
        m1.delete()
        eq_(set(b1.get_elements(type=CMetaclass)), {m2, m3})
        m3.delete()
        eq_(set(b1.get_elements(type=CMetaclass)), {m2})

        eq_(m3.superclasses, [])
        eq_(m2.subclasses, [])
        eq_(m3.attributes, [])
        eq_(m3.attribute_names, [])
        eq_(m3.classes, [])
        eq_(m3.name, None)
        eq_(m3.bundles, [])
        eq_(b1.get_elements(type=CClass), [])

    def test_remove_bundle_from_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        m1 = CMetaclass("m1", bundles=[b1, b2])
        b1.remove(m1)
        eq_(set(b1.get_elements(type=CMetaclass)), set())
        eq_(set(b2.get_elements(type=CMetaclass)), {m1})
        eq_(set(m1.bundles), {b2})

    def test_delete_bundle_from_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        m1 = CMetaclass("m1", bundles=[b1, b2])
        b1.delete()
        eq_(set(b1.get_elements(type=CMetaclass)), set())
        eq_(set(b2.get_elements(type=CMetaclass)), {m1})
        eq_(set(m1.bundles), {b2})

    def test_delete_metaclass_having_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        m1 = CMetaclass("m1", bundles=[b1, b2])
        m2 = CMetaclass("m2", bundles=[b2])
        m1.delete()
        eq_(set(b1.get_elements(type=CMetaclass)), set())
        eq_(set(b2.get_elements(type=CMetaclass)), {m2})
        eq_(set(m1.bundles), set())
        eq_(set(m2.bundles), {b2})

    def test_delete_class_that_is_an_attribute_type(self):
        b1 = CBundle("B1")
        mcl = CMetaclass("MCL")
        cl1 = CClass(mcl, "CL1", bundles=b1)
        cl2 = CClass(mcl, "CL2", bundles=b1)
        cl3 = CClass(mcl, "CL3", bundles=b1)
        o3 = CObject(cl3, "O3")

        ea1 = CAttribute(type=cl3, default=o3)
        m = CMetaclass("M", bundles=b1, attributes={"o": ea1})
        c = CClass(m)
        cl1.delete()
        cl3.delete()
        try:
            # we just use list here, in order to not get a warning that ea1.default has no effect
            list([ea1.default])
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            # we just use list here, in order to not get a warning that ea1.type has no effect
            list([ea1.type])
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.default = "3"
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type = cl1
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type = cl2
            exception_expected_()
        except CException as e:
            eq_("default value '' incompatible with attribute's type 'CL2'", e.value)
        try:
            c.set_value("o", CObject(cl2))
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            c.get_value("o")
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)

    def test_bundle_that_is_deleted(self):
        b1 = CBundle("B1")
        b1.delete()
        try:
            CMetaclass("M", bundles=b1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_set_bundle_to_none(self):
        c = CMetaclass("M", bundles=None)
        eq_(c.bundles, [])
        eq_(c.name, "M")


if __name__ == "__main__":
    nose.main()
