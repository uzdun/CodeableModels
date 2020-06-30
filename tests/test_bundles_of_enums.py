import nose
from nose.tools import ok_, eq_

from codeable_models import CBundle, CMetaclass, CClass, CObject, CAttribute, CException, CEnum
from tests.testing_commons import exception_expected_


class TestBundlesOfEnums:
    def setup(self):
        self.mcl = CMetaclass("MCL")
        self.b1 = CBundle("B1")
        self.b2 = CBundle("B2")

    def test_enum_name_fail(self):
        try:
            # noinspection PyTypeChecker
            CEnum(self.mcl)
            exception_expected_()
        except CException as e:
            ok_(e.value.startswith("is not a name string: '"))
            ok_(e.value.endswith(" MCL'"))

    def test_enum_defined_bundles(self):
        eq_(set(self.b1.get_elements()), set())
        e1 = CEnum("E1", values=["A", "B", "C"], bundles=self.b1)
        eq_(set(self.b1.get_elements()), {e1})
        e2 = CEnum("E2", values=["A", "B", "C"], bundles=[self.b1])
        e3 = CEnum("E3", values=["A", "B", "C"], bundles=[self.b1, self.b2])
        mcl = CMetaclass("MCL", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CEnum)), {e1, e2, e3})
        eq_(set(self.b1.elements), {e1, e2, e3, mcl})
        eq_(set(self.b2.get_elements(type=CEnum)), {e3})
        eq_(set(self.b2.elements), {e3})

    def test_bundle_defined_enums(self):
        e1 = CEnum("E1", values=["A", "B", "C"])
        e2 = CEnum("E2", values=["A", "B", "C"])
        e3 = CEnum("E3", values=["A", "B", "C"])
        eq_(set(self.b1.get_elements(type=CEnum)), set())
        b1 = CBundle("B1", elements=[e1, e2, e3])
        eq_(set(b1.elements), {e1, e2, e3})
        self.mcl.bundles = b1
        eq_(set(b1.elements), {e1, e2, e3, self.mcl})
        eq_(set(b1.get_elements(type=CEnum)), {e1, e2, e3})
        b2 = CBundle("B2")
        b2.elements = [e2, e3]
        eq_(set(b2.get_elements(type=CEnum)), {e2, e3})
        eq_(set(e1.bundles), {b1})
        eq_(set(e2.bundles), {b1, b2})
        eq_(set(e3.bundles), {b1, b2})

    def test_get_enums_by_name(self):
        eq_(set(self.b1.get_elements(type=CEnum, name="E1")), set())
        e1 = CEnum("E1", bundles=self.b1)
        m = CMetaclass("E1", bundles=self.b1)
        eq_(self.b1.get_elements(type=CMetaclass), [m])
        eq_(set(self.b1.get_elements(type=CEnum, name="E1")), {e1})
        e2 = CEnum("E1", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CEnum, name="E1")), {e1, e2})
        ok_(e1 != e2)
        e3 = CEnum("E1", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CEnum, name="E1")), {e1, e2, e3})
        eq_(self.b1.get_element(type=CEnum, name="E1"), e1)

    def test_get_enum_elements_by_name(self):
        eq_(set(self.b1.get_elements(name="E1")), set())
        e1 = CEnum("E1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="E1")), {e1})
        m = CMetaclass("E1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="E1")), {m, e1})
        e2 = CEnum("E1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="E1")), {m, e1, e2})
        ok_(e1 != e2)
        e3 = CEnum("E1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="E1")), {m, e1, e2, e3})
        eq_(self.b1.get_element(name="E1"), e1)

    def test_enum_defined_bundle_change(self):
        e1 = CEnum("E1", bundles=self.b1)
        e2 = CEnum("E2", bundles=self.b1)
        e3 = CEnum("E3", bundles=self.b1)
        mcl = CMetaclass("MCL", bundles=self.b1)
        b = CBundle()
        e2.bundles = b
        e3.bundles = None
        self.mcl.bundles = b
        eq_(set(self.b1.elements), {mcl, e1})
        eq_(set(self.b1.get_elements(type=CEnum)), {e1})
        eq_(set(b.elements), {e2, self.mcl})
        eq_(set(b.get_elements(type=CEnum)), {e2})
        eq_(e1.bundles, [self.b1])
        eq_(e2.bundles, [b])
        eq_(e3.bundles, [])

    def test_bundle_delete_enum(self):
        e1 = CEnum("E1", bundles=self.b1)
        e2 = CEnum("E2", bundles=self.b1)
        e3 = CEnum("E3", bundles=self.b1)
        self.b1.delete()
        eq_(set(self.b1.elements), set())
        eq_(e1.bundles, [])
        eq_(e1.name, "E1")
        eq_(e2.bundles, [])
        eq_(e3.bundles, [])

    def test_creation_of_unnamed_enum_in_bundle(self):
        e1 = CEnum()
        e2 = CEnum()
        e3 = CEnum("x")
        mcl = CMetaclass()
        self.b1.elements = [e1, e2, e3, mcl]
        eq_(set(self.b1.get_elements(type=CEnum)), {e1, e2, e3})
        eq_(self.b1.get_element(type=CEnum, name=None), e1)
        eq_(set(self.b1.get_elements(type=CEnum, name=None)), {e1, e2})
        eq_(set(self.b1.get_elements(name=None)), {e1, e2, mcl})

    def test_remove_enum_from_bundle(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        e1 = CEnum("E1", bundles=b1)
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
            b2.remove(e1)
            exception_expected_()
        except CException as e:
            eq_("'E1' is not an element of the bundle", e.value)
        b1.remove(e1)
        eq_(set(b1.get_elements(type=CEnum)), set())

        e1 = CEnum("E1", bundles=b1)
        e2 = CEnum("E2", bundles=b1)
        e3 = CEnum("E3", values=["1", "2"], bundles=b1)

        b1.remove(e1)
        try:
            b1.remove(CEnum("E2", bundles=b2))
            exception_expected_()
        except CException as e:
            eq_("'E2' is not an element of the bundle", e.value)
        try:
            b1.remove(e1)
            exception_expected_()
        except CException as e:
            eq_("'E1' is not an element of the bundle", e.value)

        eq_(set(b1.get_elements(type=CEnum)), {e2, e3})
        b1.remove(e3)
        eq_(set(b1.get_elements(type=CEnum)), {e2})

        eq_(e3.name, "E3")
        eq_(e3.bundles, [])
        eq_(e3.values, ["1", "2"])

    def test_delete_enum_from_bundle(self):
        b1 = CBundle("B1")
        e1 = CEnum("E1", bundles=b1)
        e1.delete()
        eq_(set(b1.get_elements(type=CEnum)), set())

        e1 = CEnum("E1", bundles=b1)
        e2 = CEnum("E2", bundles=b1)
        e3 = CEnum("E3", values=["1", "2"], bundles=b1)
        ea1 = CAttribute(type=e3, default="1")
        ea2 = CAttribute(type=e3)
        cl = CClass(self.mcl, attributes={"letters1": ea1, "letters2": ea2})
        o = CObject(cl, "o")

        e1.delete()
        eq_(set(b1.get_elements(type=CEnum)), {e2, e3})
        e3.delete()
        eq_(set(b1.get_elements(type=CEnum)), {e2})

        eq_(e3.name, None)
        eq_(e3.bundles, [])
        eq_(e3.values, [])
        eq_(set(cl.attributes), {ea1, ea2})
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
            ea1.type = e1
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type = e2
            exception_expected_()
        except CException as e:
            eq_("default value '1' incompatible with attribute's type 'E2'", e.value)
        try:
            o.set_value("letters1", "1")
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            o.get_value("letters1")
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)

    def test_remove_bundle_from_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        e1 = CEnum("e1", bundles=[b1, b2])
        b1.remove(e1)
        eq_(set(b1.get_elements(type=CEnum)), set())
        eq_(set(b2.get_elements(type=CEnum)), {e1})
        eq_(set(e1.bundles), {b2})

    def test_delete_bundle_from_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        e1 = CEnum("e1", bundles=[b1, b2])
        b1.delete()
        eq_(set(b1.get_elements(type=CEnum)), set())
        eq_(set(b2.get_elements(type=CEnum)), {e1})
        eq_(set(e1.bundles), {b2})

    def test_delete_enum_having_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        e1 = CEnum("e1", bundles=[b1, b2])
        e2 = CEnum("e2", bundles=[b2])
        e1.delete()
        eq_(set(b1.get_elements(type=CEnum)), set())
        eq_(set(b2.get_elements(type=CEnum)), {e2})
        eq_(set(e1.bundles), set())
        eq_(set(e2.bundles), {b2})

    def test_delete_enum_that_is_an_attribute_type(self):
        b1 = CBundle("B1")
        CBundle("B2")
        e1 = CEnum("E1", bundles=b1)
        e2 = CEnum("E2", bundles=b1)
        e3 = CEnum("E3", values=["1", "2"], bundles=b1)
        ea1 = CAttribute(type=e3, default="1")
        ea2 = CAttribute(type=e3)
        cl = CClass(self.mcl, attributes={"letters1": ea1, "letters2": ea2})
        o = CObject(cl, "o")
        e1.delete()
        e3.delete()
        try:
            ea1.default = "3"
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type = e1
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.default = "3"
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type = e1
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type = e2
            exception_expected_()
        except CException as e:
            eq_("default value '1' incompatible with attribute's type 'E2'", e.value)
        try:
            o.set_value("letters1", "1")
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)
        try:
            o.get_value("letters1")
            exception_expected_()
        except CException as e:
            eq_("cannot access named element that has been deleted", e.value)

    def test_bundle_that_is_deleted(self):
        b1 = CBundle("B1")
        b1.delete()
        try:
            CEnum("E1", bundles=b1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_set_bundle_to_none(self):
        c = CEnum("E1", bundles=None)
        eq_(c.bundles, [])
        eq_(c.name, "E1")


if __name__ == "__main__":
    nose.main()
