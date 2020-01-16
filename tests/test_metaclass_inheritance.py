import re

import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeable_models import CMetaclass, CStereotype, CClass, CObject, CAttribute, CException, CEnum

class TestMetaclassInheritance():
    def testMetaclassNoInheritance(self):
        t = CMetaclass("T")
        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set())
        eq_(set(t.all_superclasses), set())
        eq_(set(t.all_subclasses), set())

    def testMetaclassSuperclassesEmptyInput(self):
        m1 = CMetaclass("M1", superclasses = [])
        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())

    def testMetaclassSuperclassesNoneInput(self):
        m1 = CMetaclass("M1", superclasses = None)
        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())

    def testMetaclassSimpleInheritance(self):
        t = CMetaclass("T")
        m1 = CMetaclass("M1", superclasses = t)
        m2 = CMetaclass("M2", superclasses = t)
        b1 = CMetaclass("B1", superclasses = m1)
        b2 = CMetaclass("B2", superclasses = m1)
        b3 = CMetaclass("B3", superclasses = t)

        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set([m1, m2, b3]))
        eq_(set(t.all_superclasses), set())
        eq_(set(t.all_subclasses), set([m1, m2, b1, b2, b3]))

        eq_(set(m1.superclasses), set([t]))
        eq_(set(m1.subclasses), set([b1, b2]))
        eq_(set(m1.all_superclasses), set([t]))
        eq_(set(m1.all_subclasses), set([b1, b2]))

        eq_(set(m2.superclasses), set([t]))
        eq_(set(m2.subclasses), set())
        eq_(set(m2.all_superclasses), set([t]))
        eq_(set(m2.all_subclasses), set())

        eq_(set(b1.superclasses), set([m1]))
        eq_(set(b1.subclasses), set())
        eq_(set(b1.all_superclasses), set([t, m1]))
        eq_(set(b1.all_subclasses), set())

        eq_(set(b2.superclasses), set([m1]))
        eq_(set(b2.subclasses), set())
        eq_(set(b2.all_superclasses), set([t, m1]))
        eq_(set(b2.all_subclasses), set())

        eq_(set(b3.superclasses), set([t]))
        eq_(set(b3.subclasses), set())
        eq_(set(b3.all_superclasses), set([t]))
        eq_(set(b3.all_subclasses), set())

    def testMetaclassInheritanceDoubleAssignment(self):
        t = CMetaclass("T")
        m1 = CMetaclass("M1") 
        try:
            m1.superclasses = [t, t]
            exceptionExpected_()
        except CException as e: 
            eq_("'T' is already a superclass of 'M1'", e.value)       
        eq_(m1.name, "M1")
        eq_(t.name, "T")
        eq_(set(m1.superclasses), set([t]))

    def testMetaclassInheritanceDeleteTopClass(self):
        t = CMetaclass("T")
        m1 = CMetaclass("M1", superclasses = [t])
        m2 = CMetaclass("M2", superclasses = [t])
        b1 = CMetaclass("B1", superclasses = [m1])
        b2 = CMetaclass("B2", superclasses = [m1])
        b3 = CMetaclass("B3", superclasses = [t])

        t.delete()

        eq_(t.name, None)
        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set())
        eq_(set(t.all_superclasses), set())
        eq_(set(t.all_subclasses), set())

        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set([b1, b2]))
        eq_(set(m1.all_superclasses), set())
        eq_(set(m1.all_subclasses), set([b1, b2]))

        eq_(set(m2.superclasses), set())
        eq_(set(m2.subclasses), set())
        eq_(set(m2.all_superclasses), set())
        eq_(set(m2.all_subclasses), set())

        eq_(set(b1.superclasses), set([m1]))
        eq_(set(b1.subclasses), set())
        eq_(set(b1.all_superclasses), set([m1]))
        eq_(set(b1.all_subclasses), set())

        eq_(set(b2.superclasses), set([m1]))
        eq_(set(b2.subclasses), set())
        eq_(set(b2.all_superclasses), set([m1]))
        eq_(set(b2.all_subclasses), set())

        eq_(set(b3.superclasses), set())
        eq_(set(b3.subclasses), set())
        eq_(set(b3.all_superclasses), set())
        eq_(set(b3.all_subclasses), set())

    def testMetaclassInheritanceDeleteInnerClass(self):
        t = CMetaclass("T")
        m1 = CMetaclass("M1", superclasses = [t])
        m2 = CMetaclass("M2", superclasses = [t])
        b1 = CMetaclass("B1", superclasses = [m1])
        b2 = CMetaclass("B2", superclasses = [m1])
        b3 = CMetaclass("B3", superclasses = [t])

        m1.delete()

        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set([m2, b3]))
        eq_(set(t.all_superclasses), set())
        eq_(set(t.all_subclasses), set([m2, b3]))

        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())
        eq_(set(m1.all_superclasses), set())
        eq_(set(m1.all_subclasses), set())

        eq_(set(m2.superclasses), set([t]))
        eq_(set(m2.subclasses), set())
        eq_(set(m2.all_superclasses), set([t]))
        eq_(set(m2.all_subclasses), set())

        eq_(set(b1.superclasses), set())
        eq_(set(b1.subclasses), set())
        eq_(set(b1.all_superclasses), set())
        eq_(set(b1.all_subclasses), set())

        eq_(set(b2.superclasses), set())
        eq_(set(b2.subclasses), set())
        eq_(set(b2.all_superclasses), set())
        eq_(set(b2.all_subclasses), set())

        eq_(set(b3.superclasses), set([t]))
        eq_(set(b3.subclasses), set())
        eq_(set(b3.all_superclasses), set([t]))
        eq_(set(b3.all_subclasses), set())

    def testMetaclassSuperclassesReassignment(self):
        t = CMetaclass("T")
        m1 = CMetaclass("M1", superclasses = [t])
        m2 = CMetaclass("M2", superclasses = [t])
        b1 = CMetaclass("B1", superclasses = [m1])
        b2 = CMetaclass("B2", superclasses = [m1])
        b3 = CMetaclass("B3", superclasses = [t])

        m1.superclasses = []
        b1.superclasses = []
        b2.superclasses = []

        eq_(set(t.superclasses), set())
        eq_(set(t.subclasses), set([m2, b3]))
        eq_(set(t.all_superclasses), set())
        eq_(set(t.all_subclasses), set([m2, b3]))

        eq_(set(m1.superclasses), set())
        eq_(set(m1.subclasses), set())
        eq_(set(m1.all_superclasses), set())
        eq_(set(m1.all_subclasses), set())

        eq_(set(m2.superclasses), set([t]))
        eq_(set(m2.subclasses), set())
        eq_(set(m2.all_superclasses), set([t]))
        eq_(set(m2.all_subclasses), set())

        eq_(set(b1.superclasses), set())
        eq_(set(b1.subclasses), set())
        eq_(set(b1.all_superclasses), set())
        eq_(set(b1.all_subclasses), set())

        eq_(set(b2.superclasses), set())
        eq_(set(b2.subclasses), set())
        eq_(set(b2.all_superclasses), set())
        eq_(set(b2.all_subclasses), set())

        eq_(set(b3.superclasses), set([t]))
        eq_(set(b3.subclasses), set())
        eq_(set(b3.all_superclasses), set([t]))
        eq_(set(b3.all_subclasses), set())

    def testMetaclassMultipleInheritance(self):
        t1 = CMetaclass("T1")
        t2 = CMetaclass("T2")
        t3 = CMetaclass("T3")
        m1 = CMetaclass("M1", superclasses = [t1, t3])
        m2 = CMetaclass("M2", superclasses = [t2, t3])
        b1 = CMetaclass("B1", superclasses = [m1])
        b2 = CMetaclass("B2", superclasses = [m1, m2])
        b3 = CMetaclass("B3", superclasses = [m2, m1])

        eq_(set(t1.superclasses), set())
        eq_(set(t1.subclasses), set([m1]))
        eq_(set(t1.all_superclasses), set())
        eq_(set(t1.all_subclasses), set([m1, b1, b2, b3]))

        eq_(set(t2.superclasses), set())
        eq_(set(t2.subclasses), set([m2]))
        eq_(set(t2.all_superclasses), set())
        eq_(set(t2.all_subclasses), set([m2, b3, b2]))

        eq_(set(t3.superclasses), set())
        eq_(set(t3.subclasses), set([m2, m1]))
        eq_(set(t3.all_superclasses), set())
        eq_(set(t3.all_subclasses), set([m2, m1, b1, b2, b3]))

        eq_(set(m1.superclasses), set([t1, t3]))
        eq_(set(m1.subclasses), set([b1, b2, b3]))
        eq_(set(m1.all_superclasses), set([t1, t3]))
        eq_(set(m1.all_subclasses), set([b1, b2, b3]))

        eq_(set(m2.superclasses), set([t2, t3]))
        eq_(set(m2.subclasses), set([b2, b3]))
        eq_(set(m2.all_superclasses), set([t2, t3]))
        eq_(set(m2.all_subclasses), set([b2, b3]))

        eq_(set(b1.superclasses), set([m1]))
        eq_(set(b1.subclasses), set())
        eq_(set(b1.all_superclasses), set([m1, t1, t3]))
        eq_(set(b1.all_subclasses), set())

        eq_(set(b2.superclasses), set([m1, m2]))
        eq_(set(b2.subclasses), set())
        eq_(set(b2.all_superclasses), set([m1, m2, t1, t2, t3]))
        eq_(set(b2.all_subclasses), set())

        eq_(set(b3.superclasses), set([m1, m2]))
        eq_(set(b3.subclasses), set())
        eq_(set(b3.all_superclasses), set([m1, m2, t1, t2, t3]))
        eq_(set(b3.all_subclasses), set())

    def testMetaclassAsWrongTypeOfSuperclass(self):
        t = CMetaclass("M")
        try:
            CClass(t, "C", superclasses = [t])
            exceptionExpected_()
        except CException as e: 
            ok_(re.match("^cannot add superclass 'M' to 'C': not of type([_ <a-zA-Z.']+)CClass'>$", e.value))
        try:
            CStereotype("S", superclasses = [t])
            exceptionExpected_()
        except CException as e: 
            ok_(re.match("^cannot add superclass 'M' to 'S': not of type([_ <a-zA-Z.']+)CStereotype'>$", e.value))

    def testMetaclass_pathNoInheritance(self):
        t = CMetaclass()
        eq_(set(t.class_path), set([t]))
    
    def testMetaclass_pathSimpleInheritance(self):
        t = CMetaclass("T")
        m1 = CMetaclass("M1", superclasses = [t])
        m2 = CMetaclass("M2", superclasses = [t])
        b1 = CMetaclass("B1", superclasses = [m1])
        b2 = CMetaclass("B2", superclasses = [m1])
        b3 = CMetaclass("B3", superclasses = [t])
        eq_(b1.class_path, [b1, m1, t])
        eq_(b2.class_path, [b2, m1, t])
        eq_(b3.class_path, [b3, t])
        eq_(m1.class_path, [m1, t])
        eq_(m2.class_path, [m2, t])
        eq_(t.class_path, [t])

    def testMetaclass_pathMultipleInheritance(self):
        t = CMetaclass("T")
        m1 = CMetaclass("M1", superclasses = [t])
        m2 = CMetaclass("M2", superclasses = [t])
        b1 = CMetaclass("B1", superclasses = [m1, m2])
        b2 = CMetaclass("B2", superclasses = [t, m1])
        b3 = CMetaclass("B3", superclasses = [t, m1, m2])
        eq_(b1.class_path, [b1, m1, t, m2])
        eq_(b2.class_path, [b2, t, m1])
        eq_(b3.class_path, [b3, t, m1, m2])
        eq_(m1.class_path, [m1, t])
        eq_(m2.class_path, [m2, t])
        eq_(t.class_path, [t])

    def testMetaclassInstanceOf(self):
        a = CMetaclass()
        b = CMetaclass(superclasses = [a])
        c = CMetaclass()
        cl = CClass(b, "C")

        eq_(cl.instance_of(a), True)
        eq_(cl.instance_of(b), True)
        eq_(cl.instance_of(c), False)

        try:
            cl.instance_of(cl)
            exceptionExpected_()
        except CException as e: 
            eq_("'C' is not a metaclass", e.value)

        cl.delete()
        eq_(cl.instance_of(a), False)
    
    def testMetaclassGetAllInstances(self):
        t = CMetaclass("T")
        m1 = CMetaclass("M1", superclasses = [t])
        m2 = CMetaclass("M2", superclasses = [t])
        b1 = CMetaclass("B1", superclasses = [m1, m2])
        to1 = CClass(t)
        to2 = CClass(t)
        m1o1 = CClass(m1)
        m1o2 = CClass(m1)
        m2o = CClass(m2)
        b1o1 = CClass(b1)
        b1o2 = CClass(b1)

        eq_(set(t.classes), set([to1, to2]))
        eq_(set(t.all_classes), set([to1, to2, m1o1, m1o2, b1o1, b1o2, m2o]))
        eq_(set(m1.classes), set([m1o1, m1o2]))
        eq_(set(m1.all_classes), set([m1o1, m1o2, b1o1, b1o2]))
        eq_(set(m2.classes), set([m2o]))
        eq_(set(m2.all_classes), set([m2o, b1o1, b1o2]))
        eq_(set(b1.classes), set([b1o1, b1o2]))
        eq_(set(b1.all_classes), set([b1o1, b1o2]))

    def testMetaclassHasSuperclassHasSubclass(self):
        m1 = CMetaclass("M1")
        m2 = CMetaclass("M2", superclasses = [m1])
        m3 = CMetaclass("M3", superclasses = [m2])
        m4 = CMetaclass("M4", superclasses = [m2])
        m5 = CMetaclass("M5", superclasses = [])

        eq_(m1.has_superclass(m2), False)
        eq_(m5.has_superclass(m2), False)
        eq_(m1.has_superclass(None), False)
        eq_(m5.has_superclass(None), False)
        eq_(m2.has_superclass(m1), True)
        eq_(m3.has_superclass(m2), True)
        eq_(m3.has_superclass(m2), True)
        eq_(m4.has_superclass(m2), True)
        eq_(m3.has_subclass(m2), False)
        eq_(m3.has_subclass(None), False)
        eq_(m5.has_subclass(m2), False)
        eq_(m5.has_subclass(None), False)
        eq_(m1.has_subclass(m3), True)
        eq_(m1.has_subclass(m2), True)

    def testMetaclassUnknownNonPositionalArgument(self):
        t = CMetaclass("T")
        try:
            CMetaclass("ST", superclass = t)
            exceptionExpected_()
        except CException as e: 
            eq_("unknown keyword argument 'superclass', should be one of: ['stereotypes', 'attributes', 'superclasses', 'bundles']", e.value)

    def testSuperMetaclassesThatAreDeleted(self):
        m1 = CMetaclass("M1")
        m1.delete()
        try:
            CMetaclass(superclasses = [m1])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testSuperMetaclassesThatAreNone(self):
        try:
            CMetaclass("M", superclasses = [None])
            exceptionExpected_()
        except CException as e: 
            ok_(e.value.startswith("cannot add superclass 'None' to 'M': not of type"))

if __name__ == "__main__":
    nose.main()



