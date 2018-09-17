import sys
sys.path.append("..")

import re

import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CBundle, CMetaclass, CClass, CObject, CAttribute, CException, CEnum

class TestBundlesOfClasses():
    def setUp(self):
        self.mcl = CMetaclass("MCL")
        self.cl = CClass(self.mcl, "C", attributes = {"i" : 1})
        self.b1 = CBundle("B1")
        self.b2 = CBundle("B2")

    def testObjectNameFail(self):
        try:
            CObject(self.cl, self.b1)
            exceptionExpected_()
        except CException as e:
            ok_(e.value.startswith("is not a name string: '"))
            ok_(e.value.endswith(" B1'"))


    def testObjectDefinedBundles(self):
        eq_(set(self.b1.getElements(type=CObject)), set()) 
        o1 = CObject(self.cl, "O1", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CObject)), set([o1])) 
        o2 = CObject(self.cl, "O2", bundles = [self.b1])
        o3 = CObject(self.cl, "O3", bundles = [self.b1, self.b2])
        mcl = CMetaclass("MCL", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CObject)), set([o1, o2, o3])) 
        eq_(set(self.b1.elements), set([o1, o2, o3, mcl]))     
        eq_(set(self.b2.getElements(type = CObject)), set([o3])) 
        eq_(set(self.b2.elements), set([o3]))   

    def testBundleDefinedObjects(self):
        o1 = CObject(self.cl, "O1")
        o2 = CObject(self.cl, "O2")
        o3 = CObject(self.cl, "O3")
        eq_(set(self.b1.getElements(type=CObject)), set()) 
        b1 = CBundle("B1", elements = [o1, o2, o3])
        eq_(set(b1.elements), set([o1, o2, o3]))
        self.mcl.bundles = b1
        eq_(set(b1.elements), set([o1, o2, o3, self.mcl]))
        eq_(set(b1.getElements(type=CObject)), set([o1, o2, o3])) 
        b2 = CBundle("B2")
        b2.elements = [o2, o3]
        eq_(set(b2.getElements(type=CObject)), set([o2, o3])) 
        eq_(set(o1.bundles), set([b1]))
        eq_(set(o2.bundles), set([b1, b2]))
        eq_(set(o3.bundles), set([b1, b2]))


    def testGetObjectsByName(self):
        eq_(set(self.b1.getElements(type=CObject, name = "O1")), set())
        o1 = CObject(self.cl, "O1", bundles = self.b1)
        m = CMetaclass("O1", bundles = self.b1)
        eq_(self.b1.getElements(type=CMetaclass), [m])
        eq_(set(self.b1.getElements(type=CObject, name = "O1")), set([o1]))
        o2 = CObject(self.cl, "O1", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CObject, name = "O1")), set([o1, o2]))
        ok_(o1 != o2)
        o3 = CObject(self.cl, "O1", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CObject, name = "O1")), set([o1, o2, o3]))
        eq_(self.b1.getElement(type=CObject, name = "O1"), o1)

    def testGetObjectElementsByName(self):
        eq_(set(self.b1.getElements(type=CObject, name = "O1")), set())
        o1 = CObject(self.cl, "O1", bundles = self.b1)
        eq_(set(self.b1.getElements(type=CObject, name = "O1")), set([o1]))
        m = CMetaclass("O1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "O1")), set([m, o1]))       
        o2 = CObject(self.cl, "O1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "O1")), set([m, o1, o2]))
        ok_(o1 != o2)
        o3 = CObject(self.cl, "O1", bundles = self.b1)
        eq_(set(self.b1.getElements(name = "O1")), set([m, o1, o2, o3]))
        eq_(self.b1.getElement(type=CObject, name = "O1"), o1)

    def testObjectDefinedBundleChange(self):
        o1 = CObject(self.cl, "O1", bundles = self.b1)
        o2 = CObject(self.cl, "O2", bundles = self.b1)
        o3 = CObject(self.cl, "O3", bundles = self.b1)
        mcl = CMetaclass("MCL", bundles = self.b1)
        b = CBundle()
        o2.bundles = b
        o3.bundles = None
        self.mcl.bundles = b
        eq_(set(self.b1.elements), set([mcl, o1]))
        eq_(set(self.b1.getElements(type=CObject)), set([o1]))        
        eq_(set(b.elements), set([o2, self.mcl]))
        eq_(set(b.getElements(type=CObject)), set([o2]))
        eq_(o1.bundles, [self.b1])
        eq_(o2.bundles, [b])
        eq_(o3.bundles, [])             
 
    def testBundleDeleteObject(self):
        o1 = CObject(self.cl, "O1", bundles = self.b1)
        o2 = CObject(self.cl, "O2", bundles = self.b1)
        o3 = CObject(self.cl, "O3", bundles = self.b1)
        self.b1.delete()
        eq_(set(self.b1.elements), set())
        eq_(o1.bundles, [])
        eq_(o1.classifier, self.cl)
        eq_(o2.bundles, [])
        eq_(o3.bundles, [])  

    def testCreationOfUnnamedObjectInBundle(self):
        o1 = CObject(self.cl)
        o2 = CObject(self.cl)
        o3 = CObject(self.cl, "x")
        mcl = CMetaclass()
        self.b1.elements = [o1, o2, o3, mcl]
        eq_(set(self.b1.getElements(type=CObject)), set([o1, o2, o3]))
        eq_(self.b1.getElement(type=CObject, name = None), o1)
        eq_(set(self.b1.getElements(type=CObject, name = None)), set([o1, o2]))
        eq_(self.b1.getElement(name = None), o1)
        eq_(set(self.b1.getElements(name = None)), set([o1, o2, mcl]))

    def testRemoveObjectFromBundle(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        o = CObject(self.cl, "O", bundles = b1)
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
            b2.remove(o)
            exceptionExpected_()
        except CException as e: 
            eq_("'O' is not an element of the bundle", e.value)
        b1.remove(o)
        eq_(set(b1.getElements(type=CObject)), set())

        o1 = CObject(self.cl, "O1", bundles = b1)
        o2 = CObject(self.cl, "O2", bundles = b1)
        o3 = CObject(self.cl, "O3", bundles = b1)
        o3.setValue("i", 7)

        b1.remove(o1)
        try:
            b1.remove(CObject(CClass(self.mcl), "Obj2", bundles = b2))
            exceptionExpected_()
        except CException as e: 
            eq_("'Obj2' is not an element of the bundle", e.value)
        try:
            b1.remove(o1)
            exceptionExpected_()
        except CException as e: 
            eq_("'O1' is not an element of the bundle", e.value)

        eq_(set(b1.getElements(type=CObject)), set([o2, o3]))
        b1.remove(o3)
        eq_(b1.getElements(type=CObject), [o2])

        eq_(o3.classifier, self.cl)
        eq_(set(self.cl.objects), set([o, o1, o2, o3]))
        eq_(o3.getValue("i"), 7)
        eq_(o3.name, "O3")
        eq_(o3.bundles, [])
        
    def testDeleteObjectFromBundle(self):
        b1 = CBundle("B1")
        o = CObject(self.cl, "O1", bundles = b1)
        o.delete()
        eq_(set(b1.getElements(type=CObject)), set())

        o1 = CObject(self.cl, "O1", bundles = b1)
        o2 = CObject(self.cl, "O2", bundles = b1)
        o3 = CObject(self.cl, "O3", bundles = b1)
        o3.setValue("i", 7)

        o1.delete()
        eq_(set(b1.getElements(type=CObject)), set([o2, o3]))
        o3.delete()
        eq_(set(b1.getElements(type=CObject)), set([o2]))

        eq_(o3.classifier, None)
        try:
            o3.getValue("i")
            exceptionExpected_()
        except CException as e: 
            eq_("can't get value 'i' on deleted object", e.value)
        eq_(o3.name, None)
        eq_(o3.bundles, [])
        

    def testRemoveBundleFromTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        o1 = CObject(self.cl, "o", bundles =  [b1, b2])
        b1.remove(o1)
        eq_(set(b1.getElements(type=CObject)), set())
        eq_(set(b2.getElements(type=CObject)), set([o1]))
        eq_(set(o1.bundles), set([b2]))

    def testDeleteBundleFromTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        o1 = CObject(self.cl, "o1", bundles = [b1, b2])
        b1.delete()
        eq_(set(b1.getElements(type=CObject)), set())
        eq_(set(b2.getElements(type=CObject)), set([o1]))
        eq_(set(o1.bundles), set([b2]))

    def testDeleteObjectHavingTwoBundles(self):
        b1 = CBundle("B1")
        b2 = CBundle("B2")
        o1 = CObject(self.cl, "o1", bundles = [b1, b2])
        o2 = CObject(self.cl, "o2", bundles = [b2])
        o1.delete()
        eq_(set(b1.getElements(type=CObject)), set())
        eq_(set(b2.getElements(type=CObject)), set([o2]))
        eq_(set(o1.bundles), set())
        eq_(set(o2.bundles), set([b2]))


    def testBundleThatIsDeleted(self):
        b1 = CBundle("B1")
        b1.delete()
        try:
            CObject(self.cl, "O1", bundles = b1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")


    def testSetBundleToNone(self):
        o = CObject(self.cl, "O1", bundles = None)
        eq_(o.bundles, [])
        eq_(o.name, "O1")

if __name__ == "__main__":
    nose.main()



