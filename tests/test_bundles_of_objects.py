import nose
from nose.tools import ok_, eq_
from tests.testing_commons import exception_expected_

from codeable_models import CBundle, CMetaclass, CClass, CObject, CException, CEnum


class TestBundlesOfClasses:
    def setup(self):
        self.mcl = CMetaclass("MCL")
        self.cl = CClass(self.mcl, "C", attributes={"i": 1})
        self.b1 = CBundle("B1")
        self.b2 = CBundle("B2")

    def test_object_name_fail(self):
        try:
            CObject(self.cl, self.b1)
            exception_expected_()
        except CException as e:
            ok_(e.value.startswith("is not a name string: '"))
            ok_(e.value.endswith(" B1'"))

    def test_object_defined_bundles(self):
        eq_(set(self.b1.get_elements(type=CObject)), set())
        o1 = CObject(self.cl, "O1", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CObject)), {o1})
        o2 = CObject(self.cl, "O2", bundles=[self.b1])
        o3 = CObject(self.cl, "O3", bundles=[self.b1, self.b2])
        mcl = CMetaclass("MCL", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CObject)), {o1, o2, o3})
        eq_(set(self.b1.elements), {o1, o2, o3, mcl})
        eq_(set(self.b2.get_elements(type=CObject)), {o3})
        eq_(set(self.b2.elements), {o3})

    def test_bundle_defined_objects(self):
        o1 = CObject(self.cl, "O1")
        o2 = CObject(self.cl, "O2")
        o3 = CObject(self.cl, "O3")
        eq_(set(self.b1.get_elements(type=CObject)), set())
        b1 = CBundle("B1", elements=[o1, o2, o3])
        eq_(set(b1.elements), {o1, o2, o3})
        self.mcl.bundles = b1
        eq_(set(b1.elements), {o1, o2, o3, self.mcl})
        eq_(set(b1.get_elements(type=CObject)), {o1, o2, o3})
        b2 = CBundle("B2")
        b2.elements = [o2, o3]
        eq_(set(b2.get_elements(type=CObject)), {o2, o3})
        eq_(set(o1.bundles), {b1})
        eq_(set(o2.bundles), {b1, b2})
        eq_(set(o3.bundles), {b1, b2})

    def test_get_objects_by_name(self):
        eq_(set(self.b1.get_elements(type=CObject, name="O1")), set())
        o1 = CObject(self.cl, "O1", bundles=self.b1)
        m = CMetaclass("O1", bundles=self.b1)
        eq_(self.b1.get_elements(type=CMetaclass), [m])
        eq_(set(self.b1.get_elements(type=CObject, name="O1")), {o1})
        o2 = CObject(self.cl, "O1", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CObject, name="O1")), {o1, o2})
        ok_(o1 != o2)
        o3 = CObject(self.cl, "O1", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CObject, name="O1")), {o1, o2, o3})
        eq_(self.b1.get_element(type=CObject, name="O1"), o1)

    def test_get_object_elements_by_name(self):
        eq_(set(self.b1.get_elements(type=CObject, name="O1")), set())
        o1 = CObject(self.cl, "O1", bundles=self.b1)
        eq_(set(self.b1.get_elements(type=CObject, name="O1")), {o1})
        m = CMetaclass("O1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="O1")), {m, o1})
        o2 = CObject(self.cl, "O1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="O1")), {m, o1, o2})
        ok_(o1 != o2)
        o3 = CObject(self.cl, "O1", bundles=self.b1)
        eq_(set(self.b1.get_elements(name="O1")), {m, o1, o2, o3})
        eq_(self.b1.get_element(type=CObject, name="O1"), o1)

    def test_object_defined_bundle_change(self):
        o1 = CObject(self.cl, "O1", bundles=self.b1)
        o2 = CObject(self.cl, "O2", bundles=self.b1)
        o3 = CObject(self.cl, "O3", bundles=self.b1)
        mcl = CMetaclass("MCL", bundles=self.b1)
        b = CBundle()
        o2.bundles = b
        o3.bundles = None
        self.mcl.bundles = b
        eq_(set(self.b1.elements), {mcl, o1})
        eq_(set(self.b1.get_elements(type=CObject)), {o1})
        eq_(set(b.elements), {o2, self.mcl})
        eq_(set(b.get_elements(type=CObject)), {o2})
        eq_(o1.bundles, [self.b1])
        eq_(o2.bundles, [b])
        eq_(o3.bundles, [])

    def test_bundle_delete_object(self):
        o1 = CObject(self.cl, "O1", bundles=self.b1)
        o2 = CObject(self.cl, "O2", bundles=self.b1)
        o3 = CObject(self.cl, "O3", bundles=self.b1)
        self.b1.delete()
        eq_(set(self.b1.elements), set())
        eq_(o1.bundles, [])
        eq_(o1.classifier, self.cl)
        eq_(o2.bundles, [])
        eq_(o3.bundles, [])

    def test_creation_of_unnamed_object_in_bundle(self):
        o1 = CObject(self.cl)
        o2 = CObject(self.cl)
        o3 = CObject(self.cl, "x")
        mcl = CMetaclass()
        self.b1.elements = [o1, o2, o3, mcl]
        eq_(set(self.b1.get_elements(type=CObject)), {o1, o2, o3})
        eq_(self.b1.get_element(type=CObject, name=None), o1)
        eq_(set(self.b1.get_elements(type=CObject, name=None)), {o1, o2})
        eq_(self.b1.get_element(name=None), o1)
        eq_(set(self.b1.get_elements(name=None)), {o1, o2, mcl})

    def test_remove_object_from_bundle(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        o = CObject(self.cl, "O", bundles=b1)
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
            b2.remove(o)
            exception_expected_()
        except CException as e:
            eq_("'O' is not an element of the bundle", e.value)
        b1.remove(o)
        eq_(set(b1.get_elements(type=CObject)), set())

        o1 = CObject(self.cl, "O1", bundles=b1)
        o2 = CObject(self.cl, "O2", bundles=b1)
        o3 = CObject(self.cl, "O3", bundles=b1)
        o3.set_value("i", 7)

        b1.remove(o1)
        try:
            b1.remove(CObject(CClass(self.mcl), "Obj2", bundles=b2))
            exception_expected_()
        except CException as e:
            eq_("'Obj2' is not an element of the bundle", e.value)
        try:
            b1.remove(o1)
            exception_expected_()
        except CException as e:
            eq_("'O1' is not an element of the bundle", e.value)

        eq_(set(b1.get_elements(type=CObject)), {o2, o3})
        b1.remove(o3)
        eq_(b1.get_elements(type=CObject), [o2])

        eq_(o3.classifier, self.cl)
        eq_(set(self.cl.objects), {o, o1, o2, o3})
        eq_(o3.get_value("i"), 7)
        eq_(o3.name, "O3")
        eq_(o3.bundles, [])

    def test_delete_object_from_bundle(self):
        b1 = CBundle("B1")
        o = CObject(self.cl, "O1", bundles=b1)
        o.delete()
        eq_(set(b1.get_elements(type=CObject)), set())

        o1 = CObject(self.cl, "O1", bundles=b1)
        o2 = CObject(self.cl, "O2", bundles=b1)
        o3 = CObject(self.cl, "O3", bundles=b1)
        o3.set_value("i", 7)

        o1.delete()
        eq_(set(b1.get_elements(type=CObject)), {o2, o3})
        o3.delete()
        eq_(set(b1.get_elements(type=CObject)), {o2})

        eq_(o3.classifier, None)
        try:
            o3.get_value("i")
            exception_expected_()
        except CException as e:
            eq_("can't get value 'i' on deleted object", e.value)
        eq_(o3.name, None)
        eq_(o3.bundles, [])

    def test_remove_bundle_from_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        o1 = CObject(self.cl, "o", bundles=[b1, b2])
        b1.remove(o1)
        eq_(set(b1.get_elements(type=CObject)), set())
        eq_(set(b2.get_elements(type=CObject)), {o1})
        eq_(set(o1.bundles), {b2})

    def test_delete_bundle_from_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        o1 = CObject(self.cl, "o1", bundles=[b1, b2])
        b1.delete()
        eq_(set(b1.get_elements(type=CObject)), set())
        eq_(set(b2.get_elements(type=CObject)), {o1})
        eq_(set(o1.bundles), {b2})

    def test_delete_object_having_two_bundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        o1 = CObject(self.cl, "o1", bundles=[b1, b2])
        o2 = CObject(self.cl, "o2", bundles=[b2])
        o1.delete()
        eq_(set(b1.get_elements(type=CObject)), set())
        eq_(set(b2.get_elements(type=CObject)), {o2})
        eq_(set(o1.bundles), set())
        eq_(set(o2.bundles), {b2})

    def test_bundle_that_is_deleted(self):
        b1 = CBundle("B1")
        b1.delete()
        try:
            CObject(self.cl, "O1", bundles=b1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_set_bundle_to_none(self):
        o = CObject(self.cl, "O1", bundles=None)
        eq_(o.bundles, [])
        eq_(o.name, "O1")


if __name__ == "__main__":
    nose.main()
