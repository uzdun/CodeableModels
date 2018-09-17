import sys
sys.path.append("..")

import re

import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CBundle, CMetaclass, CClass, CObject, CAttribute, CException, CEnum

class TestBundlesOfEnums():
    def setUp(self):
        self.mcl = CMetaclass("MCL")
        self.b1 = CBundle("B1")
        self.b2 = CBundle("B2")

    def testEnumNameFail(self):
        try:
            CEnum(self.mcl)
            exceptionExpected_()
        except CException as e:
            ok_(e.value.startswith("is not a name string: '"))
            ok_(e.value.endswith(" MCL'"))

    def testEnumDefinedBundles(self):
        eq_(set(self.b1.getElements()), set()) 
        e1 = CEnum("E1", values = ["A", "B", "C"], bundles = self.b1)
        eq_(set(self.b1.getElements()), set([e1])) 
        e2 = CEnum("E2", values = ["A", "B", "C"], bundles = [self.b1])
        e3 = CEnum("E3", values = ["A", "B", "C"], bundles = [self.b1, self.b2])
        mcl = CMetaclass("MCL", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CEnum)), set([e1, e2, e3])) 
        eq_(set(self.b1.elements), set([e1, e2, e3, mcl]))
        eq_(set(self.b2.getElements(type = CEnum)), set([e3])) 
        eq_(set(self.b2.elements), set([e3]))   

    def testBundleDefinedEnums(self):
        e1 = CEnum("E1", values = ["A", "B", "C"])
        e2 = CEnum("E2", values = ["A", "B", "C"])
        e3 = CEnum("E3", values = ["A", "B", "C"])
        eq_(set(self.b1.getElements(type=CEnum)), set()) 
        b1 = CBundle("B1", elements = [e1, e2, e3])
        eq_(set(b1.elements), set([e1, e2, e3]))
        self.mcl.bundles = b1
        eq_(set(b1.elements), set([e1, e2, e3, self.mcl]))
        eq_(set(b1.getElements(type=CEnum)), set([e1, e2, e3])) 
        b2 = CBundle("B2")
        b2.elements = [e2, e3]
        eq_(set(b2.getElements(type=CEnum)), set([e2, e3]))
        eq_(set(e1.bundles), set([b1]))
        eq_(set(e2.bundles), set([b1, b2]))
        eq_(set(e3.bundles), set([b1, b2]))
    def testGetEnumsByName(self):
        eq_(set(self.b1.getElements(type=CEnum, name = "E1")), set())
        e1 = CEnum("E1", bundles = self.b1)
        m = CMetaclass("E1", bundles = self.b1)
        eq_(self.b1.getElements(type = CMetaclass), [m])
        eq_(set(self.b1.getElements(type=CEnum, name = "E1")), set([e1]))
        e2 = CEnum("E1", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CEnum, name = "E1")), set([e1, e2]))
        ok_(e1 != e2)
        e3 = CEnum("E1", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CEnum, name = "E1")), set([e1, e2, e3]))
        eq_(self.b1.getElement(type=CEnum, name ="E1"), e1)

    def testgetEnumElementsByName(self):
        eq_(set(self.b1.getElements(name = "E1")), set())
        e1 = CEnum("E1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "E1")), set([e1]))
        m = CMetaclass("E1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "E1")), set([m, e1]))       
        e2 = CEnum("E1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "E1")), set([m, e1, e2]))
        ok_(e1 != e2)
        e3 = CEnum("E1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "E1")), set([m, e1, e2, e3]))
        eq_(self.b1.getElement(name = "E1"), e1)

    def testEnumDefinedBundleChange(self):
        e1 = CEnum("E1", bundles = self.b1)
        e2 = CEnum("E2", bundles = self.b1)
        e3 = CEnum("E3", bundles = self.b1)
        mcl = CMetaclass("MCL", bundles = self.b1)
        b = CBundle()
        e2.bundles = b
        e3.bundles = None
        self.mcl.bundles = b
        eq_(set(self.b1.elements), set([mcl, e1]))
        eq_(set(self.b1.getElements(type=CEnum)), set([e1]))        
        eq_(set(b.elements), set([e2, self.mcl]))
        eq_(set(b.getElements(type=CEnum)), set([e2]))
        eq_(e1.bundles, [self.b1])
        eq_(e2.bundles, [b])
        eq_(e3.bundles, [])             
 
    def testBundleDeleteEnum(self):
        e1 = CEnum("E1", bundles = self.b1)
        e2 = CEnum("E2", bundles = self.b1)
        e3 = CEnum("E3", bundles = self.b1)
        self.b1.delete()
        eq_(set(self.b1.elements), set())
        eq_(e1.bundles, [])
        eq_(e1.name, "E1")
        eq_(e2.bundles, [])
        eq_(e3.bundles, [])  

    def testCreationOfUnnamedEnumInBundle(self):
        e1 = CEnum()
        e2 = CEnum()
        e3 = CEnum("x")
        mcl = CMetaclass()
        self.b1.elements = [e1, e2, e3, mcl]
        eq_(set(self.b1.getElements(type=CEnum)), set([e1, e2, e3]))
        eq_(self.b1.getElement(type=CEnum, name = None), e1)
        eq_(set(self.b1.getElements(type=CEnum, name = None)), set([e1, e2]))
        eq_(set(self.b1.getElements(name = None)), set([e1, e2, mcl]))

    def testRemoveEnumFromBundle(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        e1 = CEnum("E1", bundles = b1)
        try:
            b1.remove(None)
            exceptionExpected_()
        except CException as e: 
            eq_("'None' is not an element of the bundle", e.value)
        try:
            b1.remove(CEnum("A"))
            exceptionExpected_()
        except CException as e: 
            eq_("'A' is not an element of the bundle", e.value)
        try:
            b2.remove(e1)
            exceptionExpected_()
        except CException as e: 
            eq_("'E1' is not an element of the bundle", e.value)
        b1.remove(e1)
        eq_(set(b1.getElements(type = CEnum)), set())

        e1 = CEnum("E1", bundles = b1)
        e2 = CEnum("E2", bundles = b1)
        e3 = CEnum("E3", values = ["1", "2"], bundles = b1)

        b1.remove(e1)
        try:
            b1.remove(CEnum("E2", bundles = b2))
            exceptionExpected_()
        except CException as e: 
            eq_("'E2' is not an element of the bundle", e.value)
        try:
            b1.remove(e1)
            exceptionExpected_()
        except CException as e: 
            eq_("'E1' is not an element of the bundle", e.value)

        eq_(set(b1.getElements(type = CEnum)), set([e2, e3]))
        b1.remove(e3)
        eq_(set(b1.getElements(type = CEnum)), set([e2]))

        eq_(e3.name, "E3")
        eq_(e3.bundles, [])
        eq_(e3.values, ["1", "2"])

    def testDeleteEnumFromBundle(self):
        b1 = CBundle("B1")
        e1 = CEnum("E1", bundles = b1)
        e1.delete()
        eq_(set(b1.getElements(type = CEnum)), set())

        e1 = CEnum("E1", bundles = b1)
        e2 = CEnum("E2", bundles = b1)
        e3 = CEnum("E3", values = ["1", "2"], bundles = b1)
        ea1 = CAttribute(type = e3, default = "1")
        ea2 = CAttribute(type = e3)
        cl = CClass(self.mcl, attributes = {"letters1": ea1, "letters2": ea2})
        o = CObject(cl, "o")

        e1.delete()
        eq_(set(b1.getElements(type = CEnum)), set([e2, e3]))
        e3.delete()
        eq_(set(b1.getElements(type = CEnum)), set([e2]))

        eq_(e3.name, None)
        eq_(e3.bundles, [])
        eq_(e3.values, [])
        eq_(set(cl.attributes), {ea1, ea2})
        try:
            ea1.default
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.default = "3"
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type = e1
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type = e2
            exceptionExpected_()
        except CException as e: 
            eq_("default value '1' incompatible with attribute's type 'E2'", e.value)
        try:
            o.setValue("letters1", "1")
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            o.getValue("letters1")
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)


    def testRemoveBundleFromTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        e1 = CEnum("e1", bundles = [b1, b2])
        b1.remove(e1)
        eq_(set(b1.getElements(type=CEnum)), set())
        eq_(set(b2.getElements(type=CEnum)), set([e1]))
        eq_(set(e1.bundles), set([b2]))

    def testDeleteBundleFromTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        e1 = CEnum("e1", bundles = [b1, b2])
        b1.delete()
        eq_(set(b1.getElements(type=CEnum)), set())
        eq_(set(b2.getElements(type=CEnum)), set([e1]))
        eq_(set(e1.bundles), set([b2]))

    def testDeleteEnumHavingTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        e1 = CEnum("e1", bundles = [b1, b2])
        e2 = CEnum("e2", bundles = [b2])
        e1.delete()
        eq_(set(b1.getElements(type=CEnum)), set())
        eq_(set(b2.getElements(type=CEnum)), set([e2]))
        eq_(set(e1.bundles), set())
        eq_(set(e2.bundles), set([b2]))

    def testDeleteEnumThatIsAnAttributeType(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        e1 = CEnum("E1", bundles = b1)
        e2 = CEnum("E2", bundles = b1)
        e3 = CEnum("E3", values = ["1", "2"], bundles = b1)
        ea1 = CAttribute(type = e3, default = "1")
        ea2 = CAttribute(type = e3)
        cl = CClass(self.mcl, attributes = {"letters1": ea1, "letters2": ea2})
        o = CObject(cl, "o")
        e1.delete()
        e3.delete()
        try:
            ea1.default
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.default = "3"
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type = e1
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type = e2
            exceptionExpected_()
        except CException as e: 
            eq_("default value '1' incompatible with attribute's type 'E2'", e.value)
        try:
            o.setValue("letters1", "1")
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            o.getValue("letters1")
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)

    def testBundleThatIsDeleted(self):
        b1 = CBundle("B1")
        b1.delete()
        try:
            CEnum("E1", bundles = b1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")


    def testSetBundleToNone(self):
        c = CEnum("E1", bundles = None)
        eq_(c.bundles, [])
        eq_(c.name, "E1")

if __name__ == "__main__":
    nose.main()



