import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CClass, CObject, CAttribute, CException, CEnum, CBundle

class TestClass():
    def setUp(self):
        self.mcl = CMetaclass("MCL", attributes = {"i" : 1})

    def testCreationOfOneClass(self):
        eq_(self.mcl.classes, [])
        cl = CClass(self.mcl, "CL")
        cl2 = self.mcl.classes[0]
        eq_(cl2.name, "CL")
        eq_(cl, cl2)
        eq_(cl2.metaclass, self.mcl)

    def testCreateClassWrongArgTypes(self):
        try:
            CClass("MCL", "CL")
            exceptionExpected_()
        except CException as e: 
            eq_("'MCL' is not a metaclass", e.value)
        try:
            cl = CClass(self.mcl, "TC")
            CClass(cl, "CL")
            exceptionExpected_()
        except CException as e: 
            eq_("'TC' is not a metaclass", e.value)

    def testCreationOf3Classes(self):
        c1 = CClass(self.mcl, "CL1")
        c2 = CClass(self.mcl, "CL2")
        c3 = CClass(self.mcl, "CL3")
        eq_(set(self.mcl.classes), set([c1, c2, c3]))
        
    def testCreationOfUnnamedClass(self):
        c1 = CClass(self.mcl)
        c2 = CClass(self.mcl)
        c3 = CClass(self.mcl, "x")
        eq_(set(self.mcl.classes), set([c1, c2, c3]))
        eq_(c1.name, None)
        eq_(c2.name, None)
        eq_(c3.name, "x")

    def testGetObjectsByName(self):
        c1 = CClass(self.mcl)
        eq_(set(c1.getObjects("o1")), set())
        o1 = CObject(c1, "o1")
        eq_(c1.objects, [o1])
        eq_(set(c1.getObjects("o1")), set([o1]))
        o2 = CObject(c1, "o1")
        eq_(set(c1.getObjects("o1")), set([o1, o2]))
        ok_(o1 != o2)
        o3 = CObject(c1, "o1")
        eq_(set(c1.getObjects("o1")), set([o1, o2, o3]))
        eq_(c1.getObject("o1"), o1)

    def testDeleteClass(self):
        cl1 = CClass(self.mcl, "CL1")
        cl1.delete()
        eq_(set(self.mcl.classes), set())
        
        cl1 = CClass(self.mcl, "CL1")
        cl2 = CClass(self.mcl, "CL2")
        cl3 = CClass(self.mcl, "CL3", superclasses = cl2, attributes = {"i" : 1})
        cl3.setValue("i", 7)
        CObject(cl3)
        
        cl1.delete()
        eq_(set(self.mcl.classes), set([cl2, cl3]))
        cl3.delete()
        eq_(set(self.mcl.classes), set([cl2]))
       
        eq_(cl3.superclasses, [])
        eq_(cl2.subclasses, [])
        eq_(cl3.attributes, [])
        eq_(cl3.attributeNames, [])
        eq_(cl3.metaclass, None)
        eq_(cl3.objects, [])
        eq_(cl3.name, None)
        eq_(cl3.bundles, [])
        try:
            cl3.getValue("i")
            exceptionExpected_()
        except CException as e: 
            eq_("can't get value 'i' on deleted object", e.value)

    def testDeleteClassInstanceRelation(self):
        cl1 = CClass(self.mcl, "CL1")
        cl2 = CClass(self.mcl, "CL2")
        obj1 = CObject(cl1, "O1")
        obj2 = CObject(cl1, "O2")
        obj3 = CObject(cl2, "O3")

        cl1.delete()

        eq_(obj1.classifier, None)
        eq_(obj2.classifier, None)
        eq_(obj3.classifier, cl2)
        eq_(set(cl2.objects), set([obj3]))
        eq_(cl1.objects, [])

    def testMetaclassChange(self):
        m1 = CMetaclass("M1")
        m2 = CMetaclass("M2")
        c1 = CClass(m1, "C1")
        c1.metaclass = m2
        eq_(c1.metaclass, m2)
        eq_(m1.classes, [])
        eq_(m2.classes, [c1])

    def testMetaclassChangeNoneInput(self):
        m1 = CMetaclass("M1")
        m2 = CMetaclass("M2")
        c1 = CClass(m1, "C1")
        try:
            c1.metaclass = None
            exceptionExpected_()
        except CException as e: 
            eq_("'None' is not a metaclass", e.value)

    def testMetaclassChangeWrongInputType(self):
        m1 = CMetaclass("M1")
        m2 = CMetaclass("M2")
        c1 = CClass(m1, "C1")
        try:
            c1.metaclass = CClass(m1)
            exceptionExpected_()
        except CException as e: 
            ok_(e.value.endswith("' is not a metaclass"))

    def testMetaclassIsDeletedInConstructor(self):
        m1 = CMetaclass("M1")
        m1.delete()
        try:
            CClass(m1, "C1")
            exceptionExpected_()
        except CException as e: 
            ok_(e.value.endswith("cannot access named element that has been deleted"))

    def testMetaclassIsDeletedInMetaclassMethod(self):
        m1 = CMetaclass("M1")
        m2 = CMetaclass("M2")
        c1 = CClass(m2, "C1")
        m1.delete()
        try:
            c1.metaclass = m1
            exceptionExpected_()
        except CException as e: 
            ok_(e.value.endswith("cannot access named element that has been deleted"))

    def testMetaclassIsNoneInConstructor(self):
        try:
            CClass(None, "C1")
            exceptionExpected_()
        except CException as e: 
            ok_(e.value.endswith("'None' is not a metaclass"))

    def testGetClassObject(self):
        cl = CClass(self.mcl, "CX")
        eq_(cl.classObject.name, cl.name)
        eq_(cl.classObject.classifier, self.mcl)
        eq_(cl.classObject._classObjectClass, cl)


    def testGetConnectedElements_WrongKeywordArg(self):
        c1 = CClass(self.mcl, "c1")
        try:
            c1.getConnectedElements(a = "c1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keyword argument 'a', should be one of: ['addBundles', 'processBundles', 'stopElementsInclusive', 'stopElementsExclusive']")

    def testGetConnectedElementsEmpty(self):
        c1 = CClass(self.mcl, "c1")
        eq_(set(c1.getConnectedElements()), set([c1]))

    mcl = CMetaclass("MCL")
    c1 = CClass(mcl, "c1")
    c2 = CClass(mcl, "c2", superclasses = c1)
    c3 = CClass(mcl, "c3", superclasses = c2)
    c4 = CClass(mcl, "c4", superclasses = c2)
    c5 = CClass(mcl, "c5", superclasses = c4)
    c6 = CClass(mcl, "c6")
    a1 = c1.association(c6)
    c7 = CClass(mcl, "c7")
    c8 = CClass(mcl, "c8")
    a3 = c8.association(c7)
    c9 = CClass(mcl, "c9")
    a4 = c7.association(c9)
    c10 = CClass(mcl, "c10")
    c11 = CClass(mcl, "c11", superclasses = c10)
    c12 = CClass(mcl, "c12")
    c13 = CClass(mcl, "c13")
    c12.association(c11)
    bsub = CBundle("bsub", elements = [c13])
    b1 = CBundle("b1", elements = [c1, c2, c3, bsub, c7])
    b2 = CBundle("b2", elements = [c7, c10, c11, c12])

    allTestElts = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, b1, b2, bsub]

    @parameterized.expand([
        (allTestElts, {"processBundles": True}, set([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13])),
        (allTestElts, {"processBundles": True, "addBundles": True}, set([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, b1, b2, bsub])),
        ([c1], {"processBundles": True}, set([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13])),
        ([c1], {"processBundles": True, "addBundles": True}, set([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, b1, b2, bsub])),
        ([c7], {}, set([c7, c8, c9])),
        ([c7], {"addBundles": True}, set([c7, c8, c9, b1, b2])),
    ])
    def testGetConnectedElements(self, testElements, kwargsDict, connectedElementsResult):
        for elt in testElements:
             eq_(set(elt.getConnectedElements(**kwargsDict)), connectedElementsResult)

    def testGetConnectedElements_StopElementsInclusiveWrongTypes(self):
        c1 = CClass(self.mcl, "c1")
        try:
            c1.getConnectedElements(stopElementsInclusive = "c1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "expected one element or a list of stop elements, but got: 'c1'")
        try:
            c1.getConnectedElements(stopElementsInclusive = ["c1"])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "expected one element or a list of stop elements, but got: '['c1']' with element of wrong type: 'c1'")

    @parameterized.expand([
        ([c1], {"stopElementsExclusive" : [c1]}, set()),
        ([c1], {"stopElementsInclusive" : [c3, c6]}, set([c1, c2, c3, c4, c5, c6])),
        ([c1], {"stopElementsExclusive" : [c3, c6]}, set([c1, c2, c4, c5])),
        ([c1], {"stopElementsInclusive" : [c3, c6], "stopElementsExclusive" : [c3]}, set([c1, c2, c4, c5, c6])),
        ([c7], {"stopElementsInclusive" : [b2], "stopElementsExclusive" : [b1], "processBundles": True, "addBundles": True}, set([c7, b2, c8, c9])),
        ([c7], {"stopElementsExclusive" : [b1, b2], "processBundles": True, "addBundles": True}, set([c7, c8, c9])),
    ])
    def testGetConnectedElements_StopElementsInclusive(self, testElements, kwargsDict, connectedElementsResult):
        for elt in testElements:
             eq_(set(elt.getConnectedElements(**kwargsDict)), connectedElementsResult)



if __name__ == "__main__":
    nose.main()



