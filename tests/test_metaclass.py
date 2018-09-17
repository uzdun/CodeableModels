import sys
sys.path.append("..")

import re

import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CBundle, CMetaclass, CClass, CObject, CAttribute, CException, CEnum, CStereotype

class TestMetaclass():
    def testCreationOfOneMetaclass(self):
        mcl = CMetaclass("MCL")
        eq_(mcl.name, "MCL")
        cl = CClass(mcl, "C")
        eq_(cl.metaclass, mcl) 
 
    def testCreationOfUnnamedMetaclass(self):
        mcl = CMetaclass()
        eq_(mcl.name, None)

    def testDeleteMetaclass(self):
        m = CMetaclass("M1")
        cl = CClass(m, "C")
        m.delete()
        eq_(cl.metaclass, None) 
        
        m1 = CMetaclass("M1")
        m2 = CMetaclass("M2")
        m3 = CMetaclass("M3", superclasses = m2, attributes = {"i" : 1}, stereotypes = CStereotype("S"))
        cl = CClass(m3, "C")
        m1.delete()
        eq_(cl.metaclass, m3)
        m3.delete()
        eq_(cl.metaclass, None) 
       
        eq_(m3.superclasses, [])
        eq_(m2.subclasses, [])
        eq_(m3.attributes, [])
        eq_(m3.attributeNames, [])
        eq_(m3.stereotypes, [])
        eq_(m3.classes, [])
        eq_(m3.name, None)
        eq_(m3.bundles, [])

    def testDeleteMetaclassClassesRelation(self):
        m1 = CMetaclass()
        m2 = CMetaclass()
        cl1 = CClass(m1)
        cl2 = CClass(m1)
        cl3 = CClass(m2)

        m1.delete()

        eq_(cl1.metaclass, None)
        eq_(cl2.metaclass, None)
        eq_(cl3.metaclass, m2)
        eq_(set(m2.classes), set([cl3]))
        eq_(m1.classes, [])
        
    def testGetClassesByName(self):
        m1 = CMetaclass()
        eq_(set(m1.getClasses("CL1")), set())
        c1 = CClass(m1, "CL1")
        eq_(m1.classes, [c1])
        eq_(set(m1.getClasses("CL1")), set([c1]))
        c2 = CClass(m1, "CL1")
        eq_(set(m1.getClasses("CL1")), set([c1, c2]))
        ok_(c1 != c2)
        c3 = CClass(m1, "CL1")
        eq_(set(m1.getClasses("CL1")), set([c1, c2, c3]))
        eq_(m1.getClass("CL1"), c1)

    def testGetStereotypesByName(self):
        m1 = CMetaclass()
        eq_(set(m1.getStereotypes("S1")), set())
        s1 = CStereotype("S1", extended = m1)
        eq_(m1.stereotypes, [s1])
        eq_(set(m1.getStereotypes("S1")), set([s1]))
        s2 = CStereotype("S1", extended = m1)
        eq_(set(m1.getStereotypes("S1")), set([s1, s2]))
        ok_(s1 != s2)
        s3 = CStereotype("S1", extended = m1)
        eq_(set(m1.getStereotypes("S1")), set([s1, s2, s3]))
        eq_(m1.getStereotype("S1"), s1)

    def testStereotypesThatAreDeleted(self):
        s1 = CStereotype("S1")
        s1.delete()
        try:
            CMetaclass(stereotypes = [s1])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testStereotypesThatAreNone(self):
        try:
            CMetaclass(stereotypes = [None])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'None' is not a stereotype")

    def testGetConnectedElements_WrongKeywordArg(self):
        m1 = CMetaclass("m1")
        try:
            m1.getConnectedElements(a = "m1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keyword argument 'a', should be one of: ['addStereotypes', 'processStereotypes', 'addBundles', 'processBundles', 'stopElementsInclusive', 'stopElementsExclusive']")


    def testGetConnectedElementsEmpty(self):
        m1 = CMetaclass("m1")
        eq_(set(m1.getConnectedElements()), set([m1]))

    m1 = CMetaclass("m1")
    m2 = CMetaclass("m2", superclasses = m1)
    m3 = CMetaclass("m3", superclasses = m2)
    m4 = CMetaclass("m4", superclasses = m2)
    m5 = CMetaclass("m5", superclasses = m4)
    m6 = CMetaclass("m6")
    a1 = m1.association(m6)
    m7 = CMetaclass("m7")
    m8 = CMetaclass("m8")
    a3 = m8.association(m7)
    m9 = CMetaclass("m9")
    a4 = m7.association(m9)
    m10 = CMetaclass("m10")
    m11 = CMetaclass("m11", superclasses = m10)
    m12 = CMetaclass("m12")
    m13 = CMetaclass("m13")
    m12.association(m11)
    bsub = CBundle("bsub", elements = [m13])
    b1 = CBundle("b1", elements = [m1, m2, m3, bsub, m7])
    b2 = CBundle("b2", elements = [m7, m10, m11, m12])

    m14 = CMetaclass("m14")
    s1 = CStereotype("s1")
    s2 = CStereotype("s2", extended = [m7, m14], superclasses = s1)

    allTestElts = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, b1, b2, bsub, m14, s1, s2]

    @parameterized.expand([
        (allTestElts, {"processStereotypes": True, "processBundles": True}, set([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14])),
        (allTestElts, {"processStereotypes": True, "processBundles": True, "addStereotypes": True, "addBundles": True}, set([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, b1, b2, bsub, s1, s2])),
        (allTestElts, {"processStereotypes": True, "processBundles": True, "addBundles": True}, set([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, b1, b2, bsub])),
        (allTestElts, {"processStereotypes": True, "processBundles": True, "addStereotypes": True}, set([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, s1, s2])),
        ([m1], {"processBundles": True}, set([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13])),
        ([m1], {"processBundles": True, "addStereotypes": True, "addBundles": True}, set([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, b1, b2, bsub, s1, s2])),
        ([m1], {"processBundles": True, "addBundles": True}, set([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, b1, b2, bsub])),
        ([m1], {"processBundles": True, "addStereotypes": True}, set([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, s1, s2])),
        ([m7], {"processStereotypes": True}, set([m7, m8, m9, m14])),
        ([m7], {"processStereotypes": True, "addStereotypes": True, "addBundles": True}, set([m7, m8, m9, m14, b1, b2, s1, s2])),
        ([m7], {"processStereotypes": True, "addBundles": True}, set([m7, m8, m9, m14, b1, b2])),
        ([m7], {"processStereotypes": True, "addStereotypes": True}, set([m7, m8, m9, m14, s1, s2])),
        ([m7], {}, set([m7, m8, m9])),
        ([m7], {"addStereotypes": True, "addBundles": True}, set([m7, m8, m9, b1, b2, s1, s2])),
        ([m7], {"addBundles": True}, set([m7, m8, m9, b1, b2])),
        ([m7], {"addStereotypes": True}, set([m7, m8, m9, s1, s2]))])
    def testGetConnectedElements(self, testElements, kwargsDict, connectedElementsResult):
        for elt in testElements:
             eq_(set(elt.getConnectedElements(**kwargsDict)), connectedElementsResult)

    def testGetConnectedElements_StopElementsInclusiveWrongTypes(self):
        m1 = CMetaclass("m1")
        try:
            m1.getConnectedElements(stopElementsInclusive = "m1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "expected one element or a list of stop elements, but got: 'm1'")
        try:
            m1.getConnectedElements(stopElementsInclusive = ["m1"])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "expected one element or a list of stop elements, but got: '['m1']' with element of wrong type: 'm1'")

    @parameterized.expand([
        ([m1], {"stopElementsExclusive" : [m1]}, set()),
        ([m1], {"stopElementsInclusive" : [m3, m6]}, set([m1, m2, m3, m4, m5, m6])),
        ([m1], {"stopElementsExclusive" : [m3, m6]}, set([m1, m2, m4, m5])),
        ([m1], {"stopElementsInclusive" : [m3, m6], "stopElementsExclusive" : [m3]}, set([m1, m2, m4, m5, m6])),
        ([m7], {"stopElementsInclusive" : [b2, s2], "stopElementsExclusive" : [b1], "processStereotypes": True, "processBundles": True, "addStereotypes": True, "addBundles": True}, set([m7, b2, s2, m8, m9])),
        ([m7], {"stopElementsExclusive" : [b1, b2, s2], "processStereotypes": True, "processBundles": True, "addStereotypes": True, "addBundles": True}, set([m7, m8, m9])),
        ([b2], {"stopElementsInclusive" : [b1, m8, m9], "stopElementsExclusive" : [s1, s2], "processStereotypes": True, "processBundles": True, "addStereotypes": True, "addBundles": True}, set([m7, m10, m11, m12, m8, m9, b1, b2])),
        ([b2], {"stopElementsInclusive" : [b1, m8, m9], "stopElementsExclusive" : [s1, s2], "processStereotypes": True, "processBundles": True}, set([m7, m10, m11, m12, m8, m9])),
        ([s1], {"stopElementsInclusive" : [m14, m7], "processStereotypes": True, "processBundles": True, "addStereotypes": True, "addBundles": True}, set([s1, s2, m7, m14])),
        ([s1], {"stopElementsInclusive" : [m14, m7], "processStereotypes": True, "processBundles": True}, set([m7, m14]))
    ])
    def testGetConnectedElements_StopElementsInclusive(self, testElements, kwargsDict, connectedElementsResult):
        for elt in testElements:
             eq_(set(elt.getConnectedElements(**kwargsDict)), connectedElementsResult)


if __name__ == "__main__":
    nose.main()