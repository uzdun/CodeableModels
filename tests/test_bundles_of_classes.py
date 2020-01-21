import nose
from nose.tools import ok_, eq_

from codeable_models import CBundle, CMetaclass, CClass, CObject, CAttribute, CException, CEnum
from tests.testing_commons import exception_expected_


class TestBundlesOfClasses:
    def setup(self):
        self.mcl = CMetaclass("MCL", attributes={"i": 1})
        self.b1 = CBundle("B1")
        self.b2 = CBundle("B2")

    def test_class_name_fail(self):
        try:
            CClass(self.mcl, self.mcl)
            exception_expected_()
        except CException as e:
            ok_(e.value.startswith("is not a name string: '"))
            ok_(e.value.endswith(" MCL'"))

    def test_class_defined_bundles(self):
        eq_(set(self.b1.get_elements()), set())
        cl1 = CClass(self.mcl, "Class1", bundles=self.b1)
        eq_(set(self.b1.get_elements()), {cl1})
        cl2 = CClass(self.mcl, "Class2", bundles=[self.b1])
        cl3 = CClass(self.mcl, "Class3", bundles=[self.b1, self.b2])
        mcl = CMetaclass("MCL", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CClass)), {cl1, cl2, cl3})
        eq_(set(self.b1.elements), {cl1, cl2, cl3, mcl})
        eq_(set(self.b2.get_elements(type=CClass)), {cl3})
        eq_(set(self.b2.elements), {cl3})

    def test_bundle_defined_classes(self):
        cl1 = CClass(self.mcl, "Class1")
        cl2 = CClass(self.mcl, "Class2")
        cl3 = CClass(self.mcl, "Class3")
        eq_(set(self.b1.get_elements(type=CClass)), set())
        b1 = CBundle("B1", elements=[cl1, cl2, cl3])
        eq_(set(b1.elements), {cl1, cl2, cl3})
        self.mcl.bundles = b1
        eq_(set(b1.elements), {cl1, cl2, cl3, self.mcl})
        eq_(set(b1.get_elements(type=CClass)), {cl1, cl2, cl3})
        b2 = CBundle("B2")
        b2.elements = [cl2, cl3]
        eq_(set(b2.get_elements(type=CClass)), {cl2, cl3})
        eq_(set(cl1.bundles), {b1})
        eq_(set(cl2.bundles), {b1, b2})
        eq_(set(cl3.bundles), {b1, b2})

    def test_get_classes_by_name(self):
        eq_(set(self.b1.get_elements(type=CClass, name="CL1")), set())
        c1 = CClass(self.mcl, "CL1", bundles=self.b1)
        m = CMetaclass("CL1", bundles=self.b1)
        eq_(self.b1.get_elements(type=CMetaclass), [m])
        eq_(set(self.b1.get_elements(type=CClass, name="CL1")), {c1})
        c2 = CClass(self.mcl, "CL1", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CClass, name="CL1")), {c1, c2})
        ok_(c1 != c2)
        c3 = CClass(self.mcl, "CL1", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CClass, name="CL1")), {c1, c2, c3})
        eq_(self.b1.get_element(type=CClass, name="CL1"), c1)

    def test_get_class_elements_by_name(self):
        eq_(set(self.b1.get_elements(name="CL1")), set())
        c1 = CClass(self.mcl, "CL1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="CL1")), {c1})
        m = CMetaclass("CL1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="CL1")), {m, c1})
        c2 = CClass(self.mcl, "CL1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="CL1")), {m, c1, c2})
        ok_(c1 != c2)
        c3 = CClass(self.mcl, "CL1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="CL1")), {m, c1, c2, c3})
        eq_(self.b1.get_element(name="CL1"), c1)

    def test_class_defined_bundle_change(self):
        cl1 = CClass(self.mcl, "Class1", bundles=self.b1)
        cl2 = CClass(self.mcl, "Class2", bundles=self.b1)
        cl3 = CClass(self.mcl, "Class3", bundles=self.b1)
        mcl = CMetaclass("MCL", bundles=self.b1)
        b = CBundle()
        cl2.bundles = b
        cl3.bundles = None
        self.mcl.bundles = b
        eq_(set(self.b1.elements), {mcl, cl1})
        eq_(set(self.b1.get_elements(type=CClass)), {cl1})
        eq_(set(b.elements), {cl2, self.mcl})
        eq_(set(b.get_elements(type=CClass)), {cl2})
        eq_(cl1.bundles, [self.b1])
        eq_(cl2.bundles, [b])
        eq_(cl3.bundles, [])

    def test_bundle_delete_class(self):
        cl1 = CClass(self.mcl, "Class1", bundles=self.b1)
        cl2 = CClass(self.mcl, "Class2", bundles=self.b1)
        cl3 = CClass(self.mcl, "Class3", bundles=self.b1)
        self.b1.delete()
        eq_(set(self.b1.elements), set())
        eq_(cl1.bundles, [])
        eq_(cl1.metaclass, self.mcl)
        eq_(cl2.bundles, [])
        eq_(cl3.bundles, [])

    def test_creation_of_unnamed_class_in_bundle(self):
        c1 = CClass(self.mcl)
        c2 = CClass(self.mcl)
        c3 = CClass(self.mcl, "x")
        mcl = CMetaclass()
        self.b1.elements = [c1, c2, c3, mcl]
        eq_(set(self.b1.get_elements(type=CClass)), {c1, c2, c3})
        eq_(self.b1.get_element(type=CClass, name=None), c1)
        eq_(set(self.b1.get_elements(type=CClass, name=None)), {c1, c2})
        eq_(set(self.b1.get_elements(name=None)), {c1, c2, mcl})

    def test_remove_class_from_bundle(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        cl1 = CClass(self.mcl, "CL1", bundles=b1)
        try:
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
            b2.remove(cl1)
            exception_expected_()
        except CException as e:
            eq_("'CL1' is not an element of the bundle", e.value)
        b1.remove(cl1)
        eq_(set(b1.get_elements(type=CClass)), set())

        cl1 = CClass(self.mcl, "CL1", bundles=b1)
        cl2 = CClass(self.mcl, "CL2", bundles=b1)
        cl3 = CClass(self.mcl, "CL3", superclasses=cl2, attributes={"i": 1}, bundles=b1)
        cl3.set_value("i", 7)
        o = CObject(cl3, bundles=b1)

        b1.remove(cl1)
        try:
            b1.remove(CClass(CMetaclass("MCL", bundles=b2), "CL2", bundles=b2))
            exception_expected_()
        except CException as e:
            eq_("'CL2' is not an element of the bundle", e.value)
        try:
            b1.remove(cl1)
            exception_expected_()
        except CException as e:
            eq_("'CL1' is not an element of the bundle", e.value)

        eq_(set(b1.get_elements(type=CClass)), {cl2, cl3})
        b1.remove(cl3)
        eq_(set(b1.get_elements(type=CClass)), {cl2})

        eq_(cl3.superclasses, [cl2])
        eq_(cl2.subclasses, [cl3])
        eq_(cl3.attribute_names, ["i"])
        eq_(cl3.metaclass, self.mcl)
        eq_(cl3.objects, [o])
        eq_(cl3.name, "CL3")
        eq_(cl3.bundles, [])
        eq_(b1.get_elements(type=CObject), [o])
        eq_(cl3.get_value("i"), 7)

    def test_delete_class_from_bundle(self):
        b1 = CBundle("B1")
        cl1 = CClass(self.mcl, "CL1", bundles=b1)
        cl1.delete()
        eq_(set(b1.get_elements(type=CClass)), set())

        cl1 = CClass(self.mcl, "CL1", bundles=b1)
        cl2 = CClass(self.mcl, "CL2", bundles=b1)
        cl3 = CClass(self.mcl, "CL3", superclasses=cl2, attributes={"i": 1}, bundles=b1)
        cl3.set_value("i", 7)
        CObject(cl3, bundles=b1)
        cl1.delete()
        eq_(set(b1.get_elements(type=CClass)), {cl2, cl3})
        cl3.delete()
        eq_(set(b1.get_elements(type=CClass)), {cl2})

        eq_(cl3.superclasses, [])
        eq_(cl2.subclasses, [])
        eq_(cl3.attributes, [])
        eq_(cl3.attribute_names, [])
        eq_(cl3.metaclass, None)
        eq_(cl3.objects, [])
        eq_(cl3.name, None)
        eq_(cl3.bundles, [])
        eq_(b1.get_elements(type=CObject), [])
        try:
            cl3.get_value("i")
            exception_expected_()
        except CException as e:
            eq_("can't get value 'i' on deleted class", e.value)

    def test_remove_bundle_from_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        c1 = CClass(self.mcl, "c1", bundles=[b1, b2])
        b1.remove(c1)
        eq_(set(b1.get_elements(type=CClass)), set())
        eq_(set(b2.get_elements(type=CClass)), {c1})
        eq_(set(c1.bundles), {b2})

    def test_delete_bundle_from_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        c1 = CClass(self.mcl, "c1", bundles=[b1, b2])
        b1.delete()
        eq_(set(b1.get_elements(type=CClass)), set())
        eq_(set(b2.get_elements(type=CClass)), {c1})
        eq_(set(c1.bundles), {b2})

    def test_delete_class_having_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        c1 = CClass(self.mcl, "c1", bundles=[b1, b2])
        c2 = CClass(self.mcl, "c2", bundles=[b2])
        c1.delete()
        eq_(set(b1.get_elements(type=CClass)), set())
        eq_(set(b2.get_elements(type=CClass)), {c2})
        eq_(set(c1.bundles), set())
        eq_(set(c2.bundles), {b2})

    def test_delete_class_that_is_an_attribute_type(self):
        b1 = CBundle("B1")
        cl1 = CClass(self.mcl, "CL1", bundles=b1)
        cl2 = CClass(self.mcl, "CL2", bundles=b1)
        cl3 = CClass(self.mcl, "CL3", bundles=b1)
        o3 = CObject(cl3, "O3")

        ea1 = CAttribute(type=cl3, default=o3)
        c = CClass(self.mcl, "C", bundles=b1, attributes={"o": ea1})
        o = CObject(c)
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
            o.set_value("o", CObject(cl2))
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            o.get_value("o")
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)

    def test_bundle_that_is_deleted(self):
        b1 = CBundle("B1")
        CBundle("B2")
        b1.delete()
        try:
            CClass(self.mcl, "CL1", bundles=b1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_set_bundle_to_none(self):
        c = CClass(self.mcl, "C", bundles=None)
        eq_(c.bundles, [])
        eq_(c.name, "C")

    def test_bundle_elements_that_are_deleted(self):
        c = CClass(self.mcl, "C")
        c.delete()
        try:
            CBundle("B1", elements=[c])
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_bundle_elements_that_are_none(self):
        try:
            CBundle("B1", elements=[None])
            exception_expected_()
        except CException as e:
            eq_(e.value, "'None' cannot be an element of bundle")


if __name__ == "__main__":
    nose.main()
