import sys
sys.path.append("..")

import re

import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CStereotype, CClass, CObject, CAttribute, CException, CEnum

class TestStereotypeInstancesOnClasses():
    def setUp(self):
        self.mcl = CMetaclass("MCL")

    def testStereotypeInstancesOnClass(self):
        s1 = CStereotype("S1", extended = self.mcl)
        s2 = CStereotype("S2", extended = self.mcl)
        s3 = CStereotype("S3", extended = self.mcl)
        c = CClass(self.mcl, "C")
        eq_(c.stereotypeInstances, [])
        eq_(s1.extendedInstances, [])
        c.stereotypeInstances = [s1]
        eq_(s1.extendedInstances, [c])
        eq_(c.stereotypeInstances, [s1])
        c.stereotypeInstances = [s1, s2, s3]
        eq_(s1.extendedInstances, [c])
        eq_(s2.extendedInstances, [c])
        eq_(s3.extendedInstances, [c])
        eq_(set(c.stereotypeInstances), set([s1, s2, s3]))
        c.stereotypeInstances = s2
        eq_(c.stereotypeInstances, [s2])
        eq_(s1.extendedInstances, [])
        eq_(s2.extendedInstances, [c])
        eq_(s3.extendedInstances, [])

    def testStereotypeInstancesDoubleAssignment(self):
        s1 = CStereotype("S1", extended = self.mcl)
        c = CClass(self.mcl, "C")
        try:
            c.stereotypeInstances = [s1, s1]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'S1' is already a stereotype instance on 'C'")
        eq_(c.stereotypeInstances, [s1])

    def testStereotypeInstancesNoneAssignment(self):
        s1 = CStereotype("S1", extended = self.mcl)
        c = CClass(self.mcl, "C")
        try:
            c.stereotypeInstances = [None]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'None' is not a stereotype")
        eq_(c.stereotypeInstances, [])

    def testStereotypeInstancesWrongTypeInAssignment(self):
        s1 = CStereotype("S1", extended = self.mcl)
        c = CClass(self.mcl, "C")
        try:
            c.stereotypeInstances = self.mcl
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "a list or a stereotype is required as input")
        eq_(c.stereotypeInstances, [])

    def testMultipleExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.mcl)
        s2 = CStereotype("S2", extended = self.mcl)
        c1 = CClass(self.mcl, "C1", stereotypeInstances = [s1])
        eq_(s1.extendedInstances, [c1])
        c2 = CClass(self.mcl, "C2", stereotypeInstances = s1)
        eq_(set(s1.extendedInstances), set([c1, c2]))
        c3 = CClass(self.mcl, "C3", stereotypeInstances = [s1, s2])
        eq_(set(s1.extendedInstances), set([c1, c2, c3]))
        eq_(set(s2.extendedInstances), set([c3]))
    
    def testDeleteStereotypeOfExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.mcl)
        s1.delete()
        try: 
            CClass(self.mcl, "C1", stereotypeInstances = [s1])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testDeleteStereotypedElementInstance(self):
        s1 = CStereotype("S1", extended = self.mcl)
        c = CClass(self.mcl, "C1", stereotypeInstances = [s1])
        c.delete()
        eq_(s1.extendedInstances, [])
        eq_(c.stereotypeInstances, [])

    def testAddStereotypeInstanceWrongMetaclass(self):
        otherMCL = CMetaclass()
        s1 = CStereotype("S1", extended = self.mcl)
        try: 
            CClass(otherMCL, "C1", stereotypeInstances = [s1])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype 'S1' cannot be added to 'C1': no extension by this stereotype found")   

    def testAddStereotypeInstanceMetaclassCorrectByInheritanceOfMetaclass(self):
        mcl1 = CMetaclass("MCL1")
        mcl2 = CMetaclass("MCL2", superclasses = mcl1)
        s = CStereotype("S1", extended = mcl1)
        c = CClass(mcl2, "CL", stereotypeInstances = s)
        eq_(s.extendedInstances, [c])
        eq_(c.stereotypeInstances, [s])

    def testApplyStereotypeInstancesWrongMetaclassInheritance(self):
        mcl1 = CMetaclass("MCL1", superclasses = self.mcl)
        mcl2 = CMetaclass("MCL2", superclasses = self.mcl) 
        s1 = CStereotype("S1", extended = mcl1)
        s2 = CStereotype("S2", extended = mcl2)
        superST = CStereotype("SuperST", extended = self.mcl)

        c = CClass(self.mcl, "CL")

        try:
            c.stereotypeInstances = s1
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype 'S1' cannot be added to 'CL': no extension by this stereotype found")   

        c.stereotypeInstances = superST

        mcl1Class = CClass(mcl1, "Mcl1Class", stereotypeInstances = s1)
        try:
            mcl1Class.stereotypeInstances = [s1, s2]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype 'S2' cannot be added to 'Mcl1Class': no extension by this stereotype found")
        mcl1Class.stereotypeInstances = [s1, superST]
        eq_(set(mcl1Class.stereotypeInstances), set([s1, superST]))
        eq_(c.stereotypeInstances, [superST])

    def testAddStereotypeInstanceMetaclassWrongInheritanceHierarchy(self):
        mcl1 = CMetaclass("MCL1")
        mcl2 = CMetaclass("MCL2", superclasses = mcl1)
        s = CStereotype("S1", extended = mcl2)
        c = CClass(mcl1, "CL")
        try:
            c.stereotypeInstances = [s]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype 'S1' cannot be added to 'CL': no extension by this stereotype found")


    def testAddStereotypeInstanceMetaclassCorrectByInheritanceOfStereotype(self):
        s1 = CStereotype("S1", extended = self.mcl)
        s2 = CStereotype("S2", superclasses = s1)
        c = CClass(self.mcl, "CL", stereotypeInstances = s2)
        eq_(s2.extendedInstances, [c])
        eq_(c.stereotypeInstances, [s2])

    def testAllExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.mcl)
        s2 = CStereotype("S2", superclasses = s1)
        c1 = CClass(self.mcl, "C1", stereotypeInstances = s1)
        c2 = CClass(self.mcl, "C2", stereotypeInstances = s2)
        eq_(s1.extendedInstances, [c1])
        eq_(s2.extendedInstances, [c2])
        eq_(s1.allExtendedInstances, [c1, c2])
        eq_(s2.allExtendedInstances, [c2])

if __name__ == "__main__":
    nose.main()