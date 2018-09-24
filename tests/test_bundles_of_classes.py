import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CBundle, CMetaclass, CClass, CObject, CAttribute, CException, CEnum

class TestBundlesOfClasses():
    def setUp(self):
        self.mcl = CMetaclass("MCL", attributes = {"i" : 1})
        self.b1 = CBundle("B1")
        self.b2 = CBundle("B2")

    def testClassNameFail(self):
        try:
            CClass(self.mcl, self.mcl)
            exceptionExpected_()
        except CException as e:
            ok_(e.value.startswith("is not a name string: '"))
            ok_(e.value.endswith(" MCL'"))

    def testClassDefinedBundles(self):
        eq_(set(self.b1.getElements()), set()) 
        cl1 = CClass(self.mcl, "Class1", bundles = self.b1)
        eq_(set(self.b1.getElements()), set([cl1])) 
        cl2 = CClass(self.mcl, "Class2", bundles = [self.b1])
        cl3 = CClass(self.mcl, "Class3", bundles = [self.b1, self.b2])
        mcl = CMetaclass("MCL", bundles = self.b1)
        eq_(set(self.b1.getElements(type = CClass)), set([cl1, cl2, cl3])) 
        eq_(set(self.b1.elements), set([cl1, cl2, cl3, mcl]))     
        eq_(set(self.b2.getElements(type = CClass)), set([cl3])) 
        eq_(set(self.b2.elements), set([cl3]))

    
    def testBundleDefinedClasses(self):
        cl1 = CClass(self.mcl, "Class1")
        cl2 = CClass(self.mcl, "Class2")
        cl3 = CClass(self.mcl, "Class3")
        eq_(set(self.b1.getElements(type = CClass)), set()) 
        b1 = CBundle("B1", elements = [cl1, cl2, cl3])
        eq_(set(b1.elements), set([cl1, cl2, cl3]))
        self.mcl.bundles = b1
        eq_(set(b1.elements), set([cl1, cl2, cl3, self.mcl]))
        eq_(set(b1.getElements(type = CClass)), set([cl1, cl2, cl3])) 
        b2 = CBundle("B2")
        b2.elements = [cl2, cl3]
        eq_(set(b2.getElements(type = CClass)), set([cl2, cl3])) 
        eq_(set(cl1.bundles), set([b1]))
        eq_(set(cl2.bundles), set([b1, b2]))
        eq_(set(cl3.bundles), set([b1, b2]))

    def testGetClassesByName(self):
        eq_(set(self.b1.getElements(type=CClass, name ="CL1")), set())
        c1 = CClass(self.mcl, "CL1", bundles = self.b1)
        m = CMetaclass("CL1", bundles = self.b1)
        eq_(self.b1.getElements(type=CMetaclass), [m])
        eq_(set(self.b1.getElements(type=CClass, name = "CL1")), set([c1]))
        c2 = CClass(self.mcl, "CL1", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CClass, name = "CL1")), set([c1, c2]))
        ok_(c1 != c2)
        c3 = CClass(self.mcl, "CL1", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CClass, name = "CL1")), set([c1, c2, c3]))
        eq_(self.b1.getElement(type=CClass, name = "CL1"), c1)

    def testGetClassElementsByName(self):
        eq_(set(self.b1.getElements(name = "CL1")), set())
        c1 = CClass(self.mcl, "CL1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "CL1")), set([c1]))
        m = CMetaclass("CL1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "CL1")), set([m, c1]))       
        c2 = CClass(self.mcl, "CL1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "CL1")), set([m, c1, c2]))
        ok_(c1 != c2)
        c3 = CClass(self.mcl, "CL1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "CL1")), set([m, c1, c2, c3]))
        eq_(self.b1.getElement(name = "CL1"), c1)

    def testClassDefinedBundleChange(self):
        cl1 = CClass(self.mcl, "Class1", bundles = self.b1)
        cl2 = CClass(self.mcl, "Class2", bundles = self.b1)
        cl3 = CClass(self.mcl, "Class3", bundles = self.b1)
        mcl = CMetaclass("MCL", bundles = self.b1)
        b = CBundle()
        cl2.bundles = b
        cl3.bundles = None
        self.mcl.bundles = b
        eq_(set(self.b1.elements), set([mcl, cl1]))
        eq_(set(self.b1.getElements(type = CClass)), set([cl1]))        
        eq_(set(b.elements), set([cl2, self.mcl]))
        eq_(set(b.getElements(type = CClass)), set([cl2]))
        eq_(cl1.bundles, [self.b1])
        eq_(cl2.bundles, [b])
        eq_(cl3.bundles, [])             
 
    def testBundleDeleteClass(self):
        cl1 = CClass(self.mcl, "Class1", bundles = self.b1)
        cl2 = CClass(self.mcl, "Class2", bundles = self.b1)
        cl3 = CClass(self.mcl, "Class3", bundles = self.b1)
        self.b1.delete()
        eq_(set(self.b1.elements), set())
        eq_(cl1.bundles, [])
        eq_(cl1.metaclass, self.mcl)
        eq_(cl2.bundles, [])
        eq_(cl3.bundles, [])  

    def testCreationOfUnnamedClassInBundle(self):
        c1 = CClass(self.mcl)
        c2 = CClass(self.mcl)
        c3 = CClass(self.mcl, "x")
        mcl = CMetaclass()
        self.b1.elements = [c1, c2, c3, mcl]
        eq_(set(self.b1.getElements(type=CClass)), set([c1, c2, c3]))
        eq_(self.b1.getElement(type=CClass, name = None), c1)
        eq_(set(self.b1.getElements(type=CClass, name = None)), set([c1, c2]))
        eq_(set(self.b1.getElements(name = None)), set([c1, c2, mcl]))

    def testRemoveClassFromBundle(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        cl1 = CClass(self.mcl, "CL1", bundles = b1)
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
            b2.remove(cl1)
            exceptionExpected_()
        except CException as e: 
            eq_("'CL1' is not an element of the bundle", e.value)
        b1.remove(cl1)
        eq_(set(b1.getElements(type=CClass)), set())

        cl1 = CClass(self.mcl, "CL1", bundles = b1)
        cl2 = CClass(self.mcl, "CL2", bundles = b1)
        cl3 = CClass(self.mcl, "CL3", superclasses = cl2, attributes = {"i" : 1}, bundles = b1)
        cl3.setValue("i", 7)
        o = CObject(cl3, bundles = b1)

        b1.remove(cl1)
        try:
            b1.remove(CClass(CMetaclass("MCL", bundles = b2), "CL2", bundles = b2))
            exceptionExpected_()
        except CException as e: 
            eq_("'CL2' is not an element of the bundle", e.value)
        try:
            b1.remove(cl1)
            exceptionExpected_()
        except CException as e: 
            eq_("'CL1' is not an element of the bundle", e.value)

        eq_(set(b1.getElements(type=CClass)), set([cl2, cl3]))
        b1.remove(cl3)
        eq_(set(b1.getElements(type=CClass)), set([cl2]))

        eq_(cl3.superclasses, [cl2])
        eq_(cl2.subclasses, [cl3])
        eq_(cl3.attributeNames, ["i"])
        eq_(cl3.metaclass, self.mcl)
        eq_(cl3.objects, [o])
        eq_(cl3.name, "CL3")
        eq_(cl3.bundles, [])
        eq_(b1.getElements(type=CObject), [o])
        eq_(cl3.getValue("i"), 7)

    def testDeleteClassFromBundle(self):
        b1 = CBundle("B1")
        cl1 = CClass(self.mcl, "CL1", bundles = b1)
        cl1.delete()
        eq_(set(b1.getElements(type=CClass)), set())

        cl1 = CClass(self.mcl, "CL1", bundles = b1)
        cl2 = CClass(self.mcl, "CL2", bundles = b1)
        cl3 = CClass(self.mcl, "CL3", superclasses = cl2, attributes = {"i" : 1}, bundles = b1)
        cl3.setValue("i", 7)
        CObject(cl3, bundles = b1)
        cl1.delete()
        eq_(set(b1.getElements(type=CClass)), set([cl2, cl3]))
        cl3.delete()
        eq_(set(b1.getElements(type=CClass)), set([cl2]))

        eq_(cl3.superclasses, [])
        eq_(cl2.subclasses, [])
        eq_(cl3.attributes, [])
        eq_(cl3.attributeNames, [])
        eq_(cl3.metaclass, None)
        eq_(cl3.objects, [])
        eq_(cl3.name, None)
        eq_(cl3.bundles, [])
        eq_(b1.getElements(type=CObject), [])
        try:
            cl3.getValue("i")
            exceptionExpected_()
        except CException as e: 
            eq_("can't get value 'i' on deleted object", e.value)


    def testRemoveBundleFromTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        c1 = CClass(self.mcl, "c1", bundles = [b1, b2])
        b1.remove(c1)
        eq_(set(b1.getElements(type=CClass)), set())
        eq_(set(b2.getElements(type=CClass)), set([c1]))
        eq_(set(c1.bundles), set([b2]))

    def testDeleteBundleFromTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        c1 = CClass(self.mcl, "c1", bundles = [b1, b2])
        b1.delete()
        eq_(set(b1.getElements(type=CClass)), set())
        eq_(set(b2.getElements(type=CClass)), set([c1]))
        eq_(set(c1.bundles), set([b2]))

    def testDeleteClassHavingTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        c1 = CClass(self.mcl, "c1", bundles = [b1, b2])
        c2 = CClass(self.mcl, "c2", bundles = [b2])
        c1.delete()
        eq_(set(b1.getElements(type=CClass)), set())
        eq_(set(b2.getElements(type=CClass)), set([c2]))
        eq_(set(c1.bundles), set())
        eq_(set(c2.bundles), set([b2]))

    def testDeleteClassThatIsAnAttributeType(self):
        b1 = CBundle("B1")
        cl1 = CClass(self.mcl, "CL1", bundles = b1)
        cl2 = CClass(self.mcl, "CL2", bundles = b1)
        cl3 = CClass(self.mcl, "CL3", bundles = b1)
        o3 = CObject(cl3, "O3")

        ea1 = CAttribute(type = cl3, default = o3)
        c = CClass(self.mcl, "C", bundles = b1, attributes = {"o" : ea1})
        o = CObject(c)   
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
            o.setValue("o", CObject(cl2))
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)
        try:
            o.getValue("o")
            exceptionExpected_()
        except CException as e: 
            eq_("cannot access named element that has been deleted", e.value)


    def testBundleThatIsDeleted(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        b1.delete()
        try:
            CClass(self.mcl, "CL1", bundles = b1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")


    def testSetBundleToNone(self):
        c = CClass(self.mcl, "C", bundles = None)
        eq_(c.bundles, [])
        eq_(c.name, "C")

    def testBundleElementsThatAreDeleted(self):
        c = CClass(self.mcl, "C")
        c.delete()
        try:
            CBundle("B1", elements = [c])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testBundleElementsThatAreNone(self):
        try:
            CBundle("B1", elements = [None])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'None' cannot be an element of bundle")

if __name__ == "__main__":
    nose.main()



