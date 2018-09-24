import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CBundle, CMetaclass, CClass, CObject, CAttribute, CException, CEnum

class TestBundlesOfMetaclasses():
    def setUp(self):
        self.b1 = CBundle("B1")
        self.b2 = CBundle("B2")

    def testMetaclassNameFail(self):
        try:
            CMetaclass(self.b1)
            exceptionExpected_()
        except CException as e:
            ok_(e.value.startswith("is not a name string: '"))
            ok_(e.value.endswith(" B1'"))

    def testMetaclassDefinedBundles(self):
        eq_(set(self.b1.getElements()), set()) 
        m1 = CMetaclass("M1", bundles = self.b1)
        eq_(set(self.b1.getElements()), set([m1])) 
        m2 = CMetaclass("M2", bundles = [self.b1])
        m3 = CMetaclass("M3", bundles = [self.b1, self.b2])
        cl = CClass(m1, "C", bundles = [self.b1, self.b2])
        eq_(set(self.b1.getElements(type=CMetaclass)), set([m1, m2, m3])) 
        eq_(set(self.b1.elements), set([m1, m2, m3, cl]))     
        eq_(set(self.b2.getElements(type = CMetaclass)), set([m3])) 
        eq_(set(self.b2.elements), set([m3, cl]))   


    def testBundleDefinedMetaclasses(self):
        m1 = CMetaclass("M1")
        m2 = CMetaclass("M2")
        m3 = CMetaclass("M3")
        eq_(set(self.b1.getElements(type=CMetaclass)), set()) 
        b1 = CBundle("B1", elements = [m1, m2, m3])
        eq_(set(b1.elements), set([m1, m2, m3]))
        cl = CClass(m1, "C", bundles = b1)
        eq_(set(b1.elements), set([m1, m2, m3, cl]))
        eq_(set(b1.getElements(type=CMetaclass)), set([m1, m2, m3])) 
        b2 = CBundle("B2")
        b2.elements = [m2, m3]
        eq_(set(b2.getElements(type=CMetaclass)), set([m2, m3])) 
        eq_(set(m1.bundles), set([b1]))
        eq_(set(m2.bundles), set([b1, b2]))
        eq_(set(m3.bundles), set([b1, b2]))

    def testGetMetaclassesByName(self):
        eq_(set(self.b1.getElements(type=CMetaclass, name = "m1")), set())
        m1 = CMetaclass("M1", bundles = self.b1)
        c1 = CClass(m1, "C1", bundles = self.b1)
        eq_(self.b1.getElements(type=CClass), [c1])
        eq_(set(self.b1.getElements(type=CMetaclass, name = "M1")), set([m1]))
        m2 = CMetaclass("M1", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CMetaclass, name = "M1")), set([m1, m2]))
        ok_(m1 != m2)
        m3 = CMetaclass("M1", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CMetaclass, name = "M1")), set([m1, m2, m3]))
        eq_(self.b1.getElement(type=CMetaclass, name = "M1"), m1)

    def testGetMetaclassElementsByName(self):
        eq_(set(self.b1.getElements(name = "M1")), set())
        m1 = CMetaclass("M1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "M1")), set([m1]))
        c1 = CClass(m1, "M1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "M1")), set([m1, c1]))       
        m2 = CMetaclass("M1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "M1")), set([m1, c1, m2]))
        ok_(m1 != m2)
        m3 = CMetaclass("M1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "M1")), set([m1, c1, m2, m3]))
        eq_(self.b1.getElement(name = "M1"), m1)

    def testMetaclassDefinedBundleChange(self):
        m1 = CMetaclass("M1", bundles = self.b1)
        m2 = CMetaclass("M2", bundles = self.b1)
        m3 = CMetaclass("M3", bundles = self.b1)
        cl1 = CClass(m1, "C1", bundles = self.b1)
        cl2 = CClass(m1, "C2", bundles = self.b1)
        b = CBundle()
        m2.bundles = b
        m3.bundles = None
        cl2.bundles = b
        eq_(set(self.b1.elements), set([cl1, m1]))
        eq_(set(self.b1.getElements(type=CMetaclass)), set([m1]))        
        eq_(set(b.elements), set([m2, cl2]))
        eq_(set(b.getElements(type=CMetaclass)), set([m2]))
        eq_(m1.bundles, [self.b1])
        eq_(m2.bundles, [b])
        eq_(m3.bundles, [])             
 
    def testBundleDeleteMetaclass(self):
        m1 = CMetaclass("M1", bundles = self.b1)
        c = CClass(m1)
        eq_(m1.classes, [c])
        m2 = CMetaclass("M2", bundles = self.b1)
        m3 = CMetaclass("M3", bundles = self.b1)
        self.b1.delete()
        eq_(set(self.b1.elements), set())
        eq_(m1.bundles, [])
        eq_(m1.classes, [c])
        eq_(m2.bundles, [])
        eq_(m3.bundles, [])  

    def testCreationOfUnnamedMetaclassInBundle(self):
        m1 = CMetaclass()
        m2 = CMetaclass()
        m3 = CMetaclass("x")
        cl = CClass(m1)
        self.b1.elements = [m1, m2, m3, cl]
        eq_(set(self.b1.getElements(type = CMetaclass)), set([m1, m2, m3]))
        eq_(self.b1.getElement(name = None), m1)
        eq_(set(self.b1.getElements(type = CMetaclass, name = None)), set([m1, m2]))
        eq_(set(self.b1.getElements(name = None)), set([m1, m2, cl]))

    def testRemoveMetaclassFromBundle(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        m1 = CMetaclass("M1", bundles = b1)
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
            b2.remove(m1)
            exceptionExpected_()
        except CException as e: 
            eq_("'M1' is not an element of the bundle", e.value)
        b1.remove(m1)
        eq_(set(b1.getElements(type=CMetaclass)), set())

        m1 = CMetaclass("M1", bundles = b1)
        m2 = CMetaclass("M1", bundles = b1)
        m3 = CMetaclass("M1", superclasses = m2, attributes = {"i" : 1}, bundles = b1)
        c = CClass(m3, bundles = b1)

        b1.remove(m1)
        try:
            b1.remove(CMetaclass("M2", bundles = b2))
            exceptionExpected_()
        except CException as e: 
            eq_("'M2' is not an element of the bundle", e.value)
        try:
            b1.remove(m1)
            exceptionExpected_()
        except CException as e: 
            eq_("'M1' is not an element of the bundle", e.value)

        eq_(set(b1.getElements(type=CMetaclass)), set([m2, m3]))
        b1.remove(m3)
        eq_(set(b1.getElements(type=CMetaclass)), set([m2]))

        eq_(m3.superclasses, [m2])
        eq_(m2.subclasses, [m3])
        eq_(m3.attributeNames, ["i"])
        eq_(m3.classes, [c])
        eq_(m3.name, "M1")
        eq_(m3.bundles, [])
        eq_(b1.getElements(type=CClass), [c])

    def testDeleteMetaclassFromBundle(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        m1 = CMetaclass("M1", bundles = b1)
        m1.delete()
        eq_(set(b1.getElements(type=CMetaclass)), set())

        m1 = CMetaclass("M1", bundles = b1)
        m2 = CMetaclass("M1", bundles = b1)
        m3 = CMetaclass("M1", superclasses = m2, attributes = {"i" : 1}, bundles = b1)
        CClass(m3, bundles = b1)
        m1.delete()
        eq_(set(b1.getElements(type=CMetaclass)), set([m2, m3]))
        m3.delete()
        eq_(set(b1.getElements(type=CMetaclass)), set([m2]))

        eq_(m3.superclasses, [])
        eq_(m2.subclasses, [])
        eq_(m3.attributes, [])
        eq_(m3.attributeNames, [])
        eq_(m3.classes, [])
        eq_(m3.name, None)
        eq_(m3.bundles, [])
        eq_(b1.getElements(type=CClass), [])


    def testRemoveBundleFromTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        m1 = CMetaclass("m1", bundles = [b1, b2])
        b1.remove(m1)
        eq_(set(b1.getElements(type=CMetaclass)), set())
        eq_(set(b2.getElements(type=CMetaclass)), set([m1]))
        eq_(set(m1.bundles), set([b2]))

    def testDeleteBundleFromTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        m1 = CMetaclass("m1", bundles = [b1, b2])
        b1.delete()
        eq_(set(b1.getElements(type=CMetaclass)), set())
        eq_(set(b2.getElements(type=CMetaclass)), set([m1]))
        eq_(set(m1.bundles), set([b2]))

    def testDeleteMetaclassHavingTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        m1 = CMetaclass("m1", bundles = [b1, b2])
        m2 = CMetaclass("m2", bundles = [b2])
        m1.delete()
        eq_(set(b1.getElements(type=CMetaclass)), set())
        eq_(set(b2.getElements(type=CMetaclass)), set([m2]))
        eq_(set(m1.bundles), set())
        eq_(set(m2.bundles), set([b2]))

    def testDeleteClassThatIsAnAttributeType(self):
        b1 = CBundle("B1")
        mcl = CMetaclass("MCL")
        cl1 = CClass(mcl, "CL1", bundles = b1)
        cl2 = CClass(mcl, "CL2", bundles = b1)
        cl3 = CClass(mcl, "CL3", bundles = b1)
        o3 = CObject(cl3, "O3")

        ea1 = CAttribute(type = cl3, default = o3)
        m = CMetaclass("M", bundles = b1, attributes = {"o" : ea1})
        c = CClass(m)   
        cl1.delete()
        cl3.delete()
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
            ea1.type = cl1
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            ea1.type = cl2
            exceptionExpected_()
        except CException as e: 
            eq_("default value '' incompatible with attribute's type 'CL2'", e.value)
        try:
            c.setValue("o", CObject(cl2))
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            c.getValue("o")
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)

    def testBundleThatIsDeleted(self):
        b1 = CBundle("B1")
        b1.delete()
        try:
            CMetaclass("M", bundles = b1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")


    def testSetBundleToNone(self):
        c = CMetaclass("M", bundles = None)
        eq_(c.bundles, [])
        eq_(c.name, "M")

if __name__ == "__main__":
    nose.main()



