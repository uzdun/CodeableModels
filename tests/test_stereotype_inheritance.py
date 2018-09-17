import sys
sys.path.append("..")

import re

import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CStereotype, CClass, CObject, CAttribute, CException, CEnum

class TestStereotypeInheritance():
    def setUp(self):
        self.mcl = CMetaclass("MCL")

    def testStereotypeNoInheritance(self):
        t = CStereotype("T")
        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set())
        eq_(set(t.allSuperclasses), set())
        eq_(set(t.allSubclasses), set())

    def testStereotypeSuperclassesEmptyInput(self):
        m1 = CStereotype("M1", superclasses = [])
        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())

    def testStereotypeSuperclassesNoneInput(self):
        m1 = CStereotype("M1", superclasses = None)
        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())

    def testStereotypeSimpleInheritance(self):
        t = CStereotype("T")
        m1 = CStereotype("M1", superclasses = t)
        m2 = CStereotype("M2", superclasses = t)
        b1 = CStereotype("B1", superclasses = m1)
        b2 = CStereotype("B2", superclasses = m1)
        b3 = CStereotype("B3", superclasses = t)

        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set([m1, m2, b3]))
        eq_(set(t.allSuperclasses), set())
        eq_(set(t.allSubclasses), set([m1, m2, b1, b2, b3]))

        eq_(set(m1.superclasses), set([t]))
        eq_(set(m1.subclasses), set([b1, b2]))
        eq_(set(m1.allSuperclasses), set([t]))
        eq_(set(m1.allSubclasses), set([b1, b2]))

        eq_(set(m2.superclasses), set([t]))
        eq_(set(m2.subclasses), set())
        eq_(set(m2.allSuperclasses), set([t]))
        eq_(set(m2.allSubclasses), set())

        eq_(set(b1.superclasses), set([m1]))
        eq_(set(b1.subclasses), set())
        eq_(set(b1.allSuperclasses), set([t, m1]))
        eq_(set(b1.allSubclasses), set())

        eq_(set(b2.superclasses), set([m1]))
        eq_(set(b2.subclasses), set())
        eq_(set(b2.allSuperclasses), set([t, m1]))
        eq_(set(b2.allSubclasses), set())

        eq_(set(b3.superclasses), set([t]))
        eq_(set(b3.subclasses), set())
        eq_(set(b3.allSuperclasses), set([t]))
        eq_(set(b3.allSubclasses), set())

    def testStereotypeInheritanceDoubleAssignment(self):
        m = CMetaclass("M")
        t = CStereotype("T")
        try:
            CStereotype("S1", extended = m, superclasses = [t, t])
            exceptionExpected_()
        except CException as e: 
            eq_("'T' is already a superclass of 'S1'", e.value)
        s1 = m.getStereotype("S1")
        eq_(s1.name, "S1")
        eq_(set(s1.superclasses), set([t]))

    def testStereotypeInheritanceDeleteTopClass(self):
        t = CStereotype("T")
        m1 = CStereotype("M1", superclasses = [t])
        m2 = CStereotype("M2", superclasses = [t])
        b1 = CStereotype("B1", superclasses = [m1])
        b2 = CStereotype("B2", superclasses = [m1])
        b3 = CStereotype("B3", superclasses = [t])

        t.delete()

        eq_(t.name, None)
        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set())
        eq_(set(t.allSuperclasses), set())
        eq_(set(t.allSubclasses), set())

        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set([b1, b2]))
        eq_(set(m1.allSuperclasses), set())
        eq_(set(m1.allSubclasses), set([b1, b2]))

        eq_(set(m2.superclasses), set())
        eq_(set(m2.subclasses), set())
        eq_(set(m2.allSuperclasses), set())
        eq_(set(m2.allSubclasses), set())

        eq_(set(b1.superclasses), set([m1]))
        eq_(set(b1.subclasses), set())
        eq_(set(b1.allSuperclasses), set([m1]))
        eq_(set(b1.allSubclasses), set())

        eq_(set(b2.superclasses), set([m1]))
        eq_(set(b2.subclasses), set())
        eq_(set(b2.allSuperclasses), set([m1]))
        eq_(set(b2.allSubclasses), set())

        eq_(set(b3.superclasses), set())
        eq_(set(b3.subclasses), set())
        eq_(set(b3.allSuperclasses), set())
        eq_(set(b3.allSubclasses), set())

    def testStereotypeInheritanceDeleteInnerClass(self):
        t = CStereotype("T")
        m1 = CStereotype("M1", superclasses = [t])
        m2 = CStereotype("M2", superclasses = [t])
        b1 = CStereotype("B1", superclasses = [m1])
        b2 = CStereotype("B2", superclasses = [m1])
        b3 = CStereotype("B3", superclasses = [t])

        m1.delete()

        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set([m2, b3]))
        eq_(set(t.allSuperclasses), set())
        eq_(set(t.allSubclasses), set([m2, b3]))

        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())
        eq_(set(m1.allSuperclasses), set())
        eq_(set(m1.allSubclasses), set())

        eq_(set(m2.superclasses), set([t]))
        eq_(set(m2.subclasses), set())
        eq_(set(m2.allSuperclasses), set([t]))
        eq_(set(m2.allSubclasses), set())

        eq_(set(b1.superclasses), set())
        eq_(set(b1.subclasses), set())
        eq_(set(b1.allSuperclasses), set())
        eq_(set(b1.allSubclasses), set())

        eq_(set(b2.superclasses), set())
        eq_(set(b2.subclasses), set())
        eq_(set(b2.allSuperclasses), set())
        eq_(set(b2.allSubclasses), set())

        eq_(set(b3.superclasses), set([t]))
        eq_(set(b3.subclasses), set())
        eq_(set(b3.allSuperclasses), set([t]))
        eq_(set(b3.allSubclasses), set())

    def testStereotypeSuperclassesReassignment(self):
        t = CStereotype("T")
        m1 = CStereotype("M1", superclasses = [t])
        m2 = CStereotype("M2", superclasses = [t])
        b1 = CStereotype("B1", superclasses = [m1])
        b2 = CStereotype("B2", superclasses = [m1])
        b3 = CStereotype("B3", superclasses = [t])

        m1.superclasses = []
        b1.superclasses = []
        b2.superclasses = []

        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set([m2, b3]))
        eq_(set(t.allSuperclasses), set())
        eq_(set(t.allSubclasses), set([m2, b3]))

        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())
        eq_(set(m1.allSuperclasses), set())
        eq_(set(m1.allSubclasses), set())

        eq_(set(m2.superclasses), set([t]))
        eq_(set(m2.subclasses), set())
        eq_(set(m2.allSuperclasses), set([t]))
        eq_(set(m2.allSubclasses), set())

        eq_(set(b1.superclasses), set())
        eq_(set(b1.subclasses), set())
        eq_(set(b1.allSuperclasses), set())
        eq_(set(b1.allSubclasses), set())

        eq_(set(b2.superclasses), set())
        eq_(set(b2.subclasses), set())
        eq_(set(b2.allSuperclasses), set())
        eq_(set(b2.allSubclasses), set())

        eq_(set(b3.superclasses), set([t]))
        eq_(set(b3.subclasses), set())
        eq_(set(b3.allSuperclasses), set([t]))
        eq_(set(b3.allSubclasses), set())

    def testStereotypeMultipleInheritance(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        t3 = CStereotype("T3")
        m1 = CStereotype("M1", superclasses = [t1, t3])
        m2 = CStereotype("M2", superclasses = [t2, t3])
        b1 = CStereotype("B1", superclasses = [m1])
        b2 = CStereotype("B2", superclasses = [m1, m2])
        b3 = CStereotype("B3", superclasses = [m2, m1])

        eq_(set(t1.superclasses), set())
        eq_(set(t1.subclasses), set([m1]))
        eq_(set(t1.allSuperclasses), set())
        eq_(set(t1.allSubclasses), set([m1, b1, b2, b3]))

        eq_(set(t2.superclasses), set())
        eq_(set(t2.subclasses), set([m2]))
        eq_(set(t2.allSuperclasses), set())
        eq_(set(t2.allSubclasses), set([m2, b3, b2]))

        eq_(set(t3.superclasses), set())
        eq_(set(t3.subclasses), set([m2, m1]))
        eq_(set(t3.allSuperclasses), set())
        eq_(set(t3.allSubclasses), set([m2, m1, b1, b2, b3]))

        eq_(set(m1.superclasses), set([t1, t3]))
        eq_(set(m1.subclasses), set([b1, b2, b3]))
        eq_(set(m1.allSuperclasses), set([t1, t3]))
        eq_(set(m1.allSubclasses), set([b1, b2, b3]))

        eq_(set(m2.superclasses), set([t2, t3]))
        eq_(set(m2.subclasses), set([b2, b3]))
        eq_(set(m2.allSuperclasses), set([t2, t3]))
        eq_(set(m2.allSubclasses), set([b2, b3]))

        eq_(set(b1.superclasses), set([m1]))
        eq_(set(b1.subclasses), set())
        eq_(set(b1.allSuperclasses), set([m1, t1, t3]))
        eq_(set(b1.allSubclasses), set())

        eq_(set(b2.superclasses), set([m1, m2]))
        eq_(set(b2.subclasses), set())
        eq_(set(b2.allSuperclasses), set([m1, m2, t1, t2, t3]))
        eq_(set(b2.allSubclasses), set())

        eq_(set(b3.superclasses), set([m1, m2]))
        eq_(set(b3.subclasses), set())
        eq_(set(b3.allSuperclasses), set([m1, m2, t1, t2, t3]))
        eq_(set(b3.allSubclasses), set())       

    def testStereotypeAsWrongTypeOfSuperclass(self):
        t = CStereotype("S") 
        try:
            CMetaclass("M", superclasses = [t])
            exceptionExpected_()
        except CException as e: 
            ok_(re.match("^cannot add superclass 'S' to 'M': not of type([ <a-zA-Z.']+)CMetaclass'>$", e.value))
        try:
            CClass(CMetaclass(), "C", superclasses = [t])
            exceptionExpected_()
        except CException as e: 
            ok_(re.match("^cannot add superclass 'S' to 'C': not of type([ <a-zA-Z.']+)CClass'>$", e.value))

    def testExtendedClassesOfInheritingStereotypes_SuperclassHasNone(self):
        m1 = CMetaclass()
        m2 = CMetaclass(superclasses = [m1])
        s1 = CStereotype()
        s2 = CStereotype(superclasses = [s1])
        m2.stereotypes = s2
        eq_(len(s1.extended), 0)
        eq_(set(m2.stereotypes), set([s2]))

    def testExtendedClassesOfInheritingStereotypes_SuperclassHasTheSame(self):
        m1 = CMetaclass()
        s1 = CStereotype(extended = [m1])
        s2 = CStereotype(superclasses = [s1], extended = [m1])
        eq_(set(s1.extended), set([m1]))
        eq_(set(s2.extended), set([m1]))
        eq_(set(m1.stereotypes), set([s2, s1]))

    def testExtendedClassesOfInheritingStereotypes_RemoveSuperclassStereotype(self):
        m1 = CMetaclass()
        s1 = CStereotype(extended = [m1])
        s2 = CStereotype(superclasses = [s1], extended = [m1])
        m1.stereotypes = s2
        eq_(set(s1.extended), set())
        eq_(set(s2.extended), set([m1]))
        eq_(set(m1.stereotypes), set([s2]))    

    def testExtendedClassesOfInheritingStereotypes_SuperclassIsSetToTheSame(self):
        m1 = CMetaclass("M1")
        s1 = CStereotype("S1")
        s2 = CStereotype("S2", extended = [m1], superclasses = [s1])
        m1.stereotypes = [s2,s1]
        eq_(set(s1.extended), set([m1]))
        eq_(set(s2.extended), set([m1]))
        eq_(set(m1.stereotypes), set([s2, s1]))  

    def testExtendedClassesOfInheritingStereotypes_SuperclassHasMetaclassesSuperclass(self):
        m1 = CMetaclass()
        m2 = CMetaclass(superclasses = [m1])
        s1 = CStereotype(extended = [m1])
        s2 = CStereotype(superclasses = [s1], extended = [m2])
        eq_(set(s1.extended), set([m1]))
        eq_(set(s2.extended), set([m2]))
        eq_(set(m1.stereotypes), set([s1]))  
        eq_(set(m2.stereotypes), set([s2])) 

    def testExtendedClassesOfInheritingStereotypes_SuperclassHasMetaclassesSuperclassIndirectly(self):
        m1 = CMetaclass()
        m2 = CMetaclass(superclasses = [m1])
        m3 = CMetaclass(superclasses = [m2])
        s1 = CStereotype(extended = [m1])
        s2 = CStereotype(superclasses = [s1], extended = [m3])
        eq_(set(s1.extended), set([m1]))
        eq_(set(s2.extended), set([m3]))
        eq_(set(m1.stereotypes), set([s1]))  
        eq_(set(m3.stereotypes), set([s2])) 

    def testExtendedClassesOfInheritingStereotypes_SuperclassIsSetToMetaclassesSuperclassIndirectly(self):
        m1 = CMetaclass()
        m2 = CMetaclass(superclasses = [m1])
        m3 = CMetaclass(superclasses = [m2])
        s1 = CStereotype()
        s2 = CStereotype(superclasses = [s1], extended = [m3])
        m1.stereotypes = s1
        eq_(set(s1.extended), set([m1]))
        eq_(set(s2.extended), set([m3]))
        eq_(set(m1.stereotypes), set([s1]))  
        eq_(set(m3.stereotypes), set([s2])) 

    def testStereotypeHasSuperclassHasSubclass(self):
        c1 = CStereotype("C1")
        c2 = CStereotype("C2", superclasses = [c1])
        c3 = CStereotype("C3", superclasses = [c2])
        c4 = CStereotype("C4", superclasses = [c2])
        c5 = CStereotype("C5", superclasses = [])

        eq_(c1.hasSuperclass(c2), False)
        eq_(c5.hasSuperclass(c2), False)
        eq_(c1.hasSuperclass(None), False)
        eq_(c5.hasSuperclass(None), False)
        eq_(c2.hasSuperclass(c1), True)
        eq_(c3.hasSuperclass(c2), True)
        eq_(c3.hasSuperclass(c2), True)  
        eq_(c4.hasSuperclass(c2), True)
        eq_(c3.hasSubclass(c2), False)
        eq_(c3.hasSubclass(None), False)
        eq_(c5.hasSubclass(c2), False)
        eq_(c5.hasSubclass(None), False)
        eq_(c1.hasSubclass(c3), True)
        eq_(c1.hasSubclass(c2), True)

    def testStereotypeUnknownNonPositionalArgument(self):
        t = CStereotype("T")
        try:
            CStereotype("ST", superclass = t)
            exceptionExpected_()
        except CException as e: 
            eq_("unknown keyword argument 'superclass', should be one of: ['extended', 'attributes', 'superclasses', 'bundles']", e.value)

    def testSuperStereotypesThatAreDeleted(self):
        s1 = CStereotype("S1")
        s1.delete()
        try:
            CStereotype(superclasses = [s1])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testSuperStereotypesThatAreNone(self):
        try:
            CStereotype("S", superclasses = [None])
            exceptionExpected_()
        except CException as e: 
            ok_(e.value.startswith("cannot add superclass 'None' to 'S': not of type"))

if __name__ == "__main__":
    nose.main()



