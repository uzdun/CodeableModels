import nose
from nose.tools import ok_, eq_
from tests.testing_commons import exception_expected_

from codeable_models import CBundle, CMetaclass, CClass, CException, CEnum


class TestBundlesOfBundles:
    def setup(self):
        self.mcl = CMetaclass("MCL")
        self.b1 = CBundle("B1")
        self.b2 = CBundle("B2")

    def test_bundle_defined_bundles(self):
        eq_(set(self.b1.get_elements()), set())
        b1 = CBundle("B1", bundles=self.b1)
        eq_(set(self.b1.get_elements()), {b1})
        b2 = CBundle("B2", bundles=[self.b1])
        b3 = CBundle("B3", bundles=[self.b1, self.b2])
        mcl = CMetaclass("MCL", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CBundle)), {b1, b2, b3})
        eq_(set(self.b1.elements), {b1, b2, b3, mcl})
        eq_(set(self.b2.get_elements(type=CBundle)), {b3})
        eq_(set(self.b2.elements), {b3})

    def test_bundle_defined_by_bundle_list(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        b3 = CBundle("P3")
        eq_(set(self.b1.get_elements(type=CBundle)), set())
        ba = CBundle("PA", elements=[b1, b2, b3])
        eq_(set(ba.elements), {b1, b2, b3})
        self.mcl.bundles = ba
        eq_(set(ba.elements), {b1, b2, b3, self.mcl})
        eq_(set(ba.get_elements(type=CBundle)), {b1, b2, b3})
        bb = CBundle("PB")
        bb.elements = [b2, b3]
        eq_(set(bb.get_elements(type=CBundle)), {b2, b3})
        eq_(set(b1.bundles), {ba})
        eq_(set(b2.bundles), {ba, bb})
        eq_(set(b3.bundles), {ba, bb})
        eq_(set(ba.bundles), set())
        eq_(set(bb.bundles), set())
        eq_(set(b1.elements), set())
        eq_(set(b2.elements), set())
        eq_(set(b3.elements), set())

    def test_get_bundles_by_name(self):
        eq_(set(self.b1.get_elements(name="B1")), set())
        b1 = CBundle("B1", bundles=self.b1)
        m = CMetaclass("B1", bundles=self.b1)
        eq_(self.b1.get_elements(type=CMetaclass), [m])
        eq_(set(self.b1.get_elements(name="B1", type=CBundle)), {b1})
        b2 = CBundle("B1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="B1", type=CBundle)), {b1, b2})
        ok_(b1 != b2)
        b3 = CBundle("B1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="B1", type=CBundle)), {b1, b2, b3})
        eq_(self.b1.get_element(name="B1", type=CBundle), b1)

    def test_get_bundle_elements_by_name(self):
        eq_(set(self.b1.get_elements(name="B1")), set())
        b1 = CBundle("B1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="B1")), {b1})
        m = CMetaclass("B1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="B1")), {m, b1})
        b2 = CBundle("B1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="B1")), {m, b1, b2})
        ok_(b1 != b2)
        b3 = CBundle("B1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="B1")), {m, b1, b2, b3})
        eq_(self.b1.get_element(name="B1"), b1)

    def test_bundle_defined_bundle_change(self):
        b1 = CBundle("B1", bundles=self.b1)
        b2 = CBundle("B2", bundles=self.b1)
        b3 = CBundle("P3", bundles=self.b1)
        mcl = CMetaclass("MCL", bundles=self.b1)
        b = CBundle()
        b2.bundles = b
        b3.bundles = None
        self.mcl.bundles = b
        eq_(set(self.b1.elements), {mcl, b1})
        eq_(set(self.b1.get_elements(type=CBundle)), {b1})
        eq_(set(b.elements), {b2, self.mcl})
        eq_(set(b.get_elements(type=CBundle)), {b2})
        eq_(b1.bundles, [self.b1])
        eq_(b2.bundles, [b])
        eq_(b3.bundles, [])

    def test_bundle_delete_bundle(self):
        b1 = CBundle("B1", bundles=self.b1)
        b2 = CBundle("B2", bundles=self.b1)
        b3 = CBundle("P3", bundles=self.b1)
        self.b1.delete()
        eq_(set(self.b1.elements), set())
        eq_(b1.get_elements(type=CBundle), [])
        eq_(b1.elements, [])
        eq_(b2.get_elements(type=CBundle), [])
        eq_(b3.get_elements(type=CBundle), [])

    def test_creation_of_unnamed_bundle_in_bundle(self):
        b1 = CBundle()
        b2 = CBundle()
        b3 = CBundle("x")
        mcl = CMetaclass()
        self.b1.elements = [b1, b2, b3, mcl]
        eq_(set(self.b1.get_elements(type=CBundle)), {b1, b2, b3})
        eq_(self.b1.get_element(name=None, type=CBundle), b1)
        eq_(set(self.b1.get_elements(name=None, type=CBundle)), {b1, b2})
        eq_(set(self.b1.get_elements(name=None)), {b1, b2, mcl})

    def test_remove_bundle_from_bundle(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        ba = CBundle("A", bundles=b1)
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
            b2.remove(ba)
            exception_expected_()
        except CException as e:
            eq_("'A' is not an element of the bundle", e.value)
        b1.remove(ba)
        eq_(set(b1.get_elements(type=CBundle)), set())

        mcl1 = CMetaclass("MCL")
        cl1 = CClass(mcl1, "CL")

        ba = CBundle("PA", bundles=b1)
        bb = CBundle("PB", bundles=b1)
        bc = CBundle("PC", bundles=b1, elements=[mcl1, cl1])

        b1.remove(ba)
        try:
            b1.remove(CBundle("PB", bundles=b2))
            exception_expected_()
        except CException as e:
            eq_("'PB' is not an element of the bundle", e.value)
        try:
            b1.remove(ba)
            exception_expected_()
        except CException as e:
            eq_("'PA' is not an element of the bundle", e.value)

        eq_(set(b1.get_elements(type=CBundle)), {bb, bc})
        b1.remove(bc)
        eq_(set(b1.get_elements(type=CBundle)), {bb})

        eq_(bc.get_elements(type=CBundle), [])
        eq_(bc.get_elements(type=CBundle), [])
        eq_(bc.elements, [mcl1, cl1])

    def test_delete_bundle_from_bundle(self):
        b1 = CBundle("B1")
        ba = CBundle("A", bundles=b1)
        ba.delete()
        eq_(set(b1.get_elements(type=CBundle)), set())

        mcl1 = CMetaclass("MCL")
        cl1 = CClass(mcl1, "CL")

        ba = CBundle("PA", bundles=b1)
        bb = CBundle("PB", bundles=b1)
        bc = CBundle("PC", bundles=b1, elements=[mcl1, cl1])

        ba.delete()
        eq_(set(b1.get_elements(type=CBundle)), {bb, bc})
        bc.delete()
        eq_(set(b1.get_elements(type=CBundle)), {bb})

        eq_(bc.get_elements(type=CBundle), [])
        eq_(bc.get_elements(type=CBundle), [])
        eq_(bc.elements, [])

    def test_remove_bundle_from_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        ba = CBundle("ba", bundles=[b1, b2])
        b1.remove(ba)
        eq_(set(b1.get_elements(type=CBundle)), set())
        eq_(set(b2.get_elements(type=CBundle)), {ba})
        eq_(set(ba.bundles), {b2})

    def test_delete_bundle_from_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        ba = CBundle("ba", bundles=[b1, b2])
        b1.delete()
        eq_(set(b1.get_elements(type=CBundle)), set())
        eq_(set(b2.get_elements(type=CBundle)), {ba})
        eq_(set(ba.bundles), {b2})

    def test_delete_bundle_having_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        ba = CBundle("ba", bundles=[b1, b2])
        bb = CBundle("bb", bundles=[b2])
        ba.delete()
        eq_(set(b1.get_elements(type=CBundle)), set())
        eq_(set(b2.get_elements(type=CBundle)), {bb})
        eq_(set(ba.bundles), set())
        eq_(set(bb.bundles), {b2})

    def test_delete_top_level_bundle(self):
        b1 = CBundle("B1")
        ba = CBundle("A", bundles=b1)
        b1.delete()
        eq_(b1.get_elements(type=CBundle), [])
        eq_(ba.get_elements(type=CBundle), [])

        b1 = CBundle("B1")
        mcl1 = CMetaclass("MCL")
        cl1 = CClass(mcl1, "CL")

        ba = CBundle("BA", bundles=b1)
        bb = CBundle("BB", bundles=b1)
        bc = CBundle("BC", bundles=b1, elements=[mcl1, cl1])

        b1.delete()
        eq_(b1.get_elements(type=CBundle), [])
        eq_(b1.elements, [])
        eq_(ba.get_elements(type=CBundle), [])
        eq_(bb.get_elements(type=CBundle), [])
        eq_(bc.get_elements(type=CBundle), [])
        eq_(bc.elements, [mcl1, cl1])
        eq_(bc.get_elements(type=CBundle), [])
        eq_(mcl1.classes, [cl1])
        eq_(mcl1.bundles, [bc])
        eq_(cl1.metaclass, mcl1)
        eq_(cl1.bundles, [bc])

    def test_bundle_that_is_deleted(self):
        b1 = CBundle("B1")
        b1.delete()
        try:
            CBundle("A", bundles=b1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_set_bundle_to_none(self):
        p = CBundle("A", bundles=None)
        eq_(p.get_elements(type=CBundle), [])
        eq_(p.name, "A")


if __name__ == "__main__":
    nose.main()
