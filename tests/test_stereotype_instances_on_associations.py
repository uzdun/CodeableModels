import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CStereotype, CClass, CObject, CAttribute, CException, CEnum, setLinks, addLinks

class TestStereotypeInstancesOnAssociations():
    def setUp(self):
        self.m1 = CMetaclass("M1")
        self.m2 = CMetaclass("M2")
        self.a = self.m1.association(self.m2, name = "a", multiplicity = "*", roleName = "m1",  
            sourceMultiplicity = "1", sourceRoleName = "m2")

    def testStereotypeInstancesOnAssociation(self):
        s1 = CStereotype("S1", extended = self.a)
        s2 = CStereotype("S2", extended = self.a)
        s3 = CStereotype("S3", extended = self.a)

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        linkObjects = setLinks({c1: [c2, c3]})
        l1 = linkObjects[0]

        eq_(l1.stereotypeInstances, [])
        eq_(s1.extendedInstances, [])
        l1.stereotypeInstances = [s1]
        eq_(s1.extendedInstances, [l1])
        eq_(l1.stereotypeInstances, [s1])
        l1.stereotypeInstances = [s1, s2, s3]
        eq_(s1.extendedInstances, [l1])
        eq_(s2.extendedInstances, [l1])
        eq_(s3.extendedInstances, [l1])
        eq_(set(l1.stereotypeInstances), set([s1, s2, s3]))
        l1.stereotypeInstances = s2
        eq_(l1.stereotypeInstances, [s2])
        eq_(s1.extendedInstances, [])
        eq_(s2.extendedInstances, [l1])
        eq_(s3.extendedInstances, [])

    def testStereotypeInstancesDoubleAssignment(self):
        s1 = CStereotype("S1", extended = self.a)
        
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = setLinks({c1: c2})[0]

        try:
            l.stereotypeInstances = [s1, s1]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'S1' is already a stereotype instance on link from 'C1' to 'C2'")
        eq_(l.stereotypeInstances, [s1])

    def testStereotypeInstancesNoneAssignment(self):
        s1 = CStereotype("S1", extended = self.a)
        
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = setLinks({c1:[c2]})[0]

        try:
            l.stereotypeInstances = [None]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'None' is not a stereotype")
        eq_(l.stereotypeInstances, [])

    def testStereotypeInstancesWrongTypeInAssignment(self):
        s1 = CStereotype("S1", extended = self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = c1.addLinks(c2)[0]
        try:
            l.stereotypeInstances = self.a
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "a list or a stereotype is required as input")
        eq_(l.stereotypeInstances, [])

    def testMultipleExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.a)
        s2 = CStereotype("S2", extended = self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        c4 = CClass(self.m2, "C4")
        linkObjects = setLinks({c1: [c2, c3, c4]})
        linkObjects[0].stereotypeInstances = [s1]
        eq_(s1.extendedInstances, [linkObjects[0]])
        linkObjects[1].stereotypeInstances = [s1]
        eq_(set(s1.extendedInstances), set([linkObjects[0], linkObjects[1]]))
        linkObjects[2].stereotypeInstances = [s1, s2]
        eq_(set(s1.extendedInstances), set([linkObjects[0], linkObjects[1], linkObjects[2]]))
        eq_(set(s2.extendedInstances), set([linkObjects[2]]))
    
    def testDeleteStereotypeOfExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.a)
        s1.delete()
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = setLinks({c1: c2})[0]
        try: 
            l.stereotypeInstances = [s1]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testDeleteStereotypedElementInstance(self):
        s1 = CStereotype("S1", extended = self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = setLinks({c1: c2}, stereotypeInstances = [s1])[0]
        eq_(s1.extendedInstances, [l])
        eq_(l.stereotypeInstances, [s1])
        l.delete()
        eq_(s1.extendedInstances, [])
        eq_(l.stereotypeInstances, [])

    def testAddStereotypeInstanceWrongAssociation(self):
        otherAssociation = self.m1.association(self.m2, name = "b", multiplicity = "*", roleName = "m1",  
            sourceMultiplicity = "1", sourceRoleName = "m2")
        s1 = CStereotype("S1", extended = self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = setLinks({c1: c2}, association = otherAssociation)[0]
        try:
            l.stereotypeInstances = [s1]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype 'S1' cannot be added to link from 'C1' to 'C2': no extension by this stereotype found")   

    def testAddStereotypeOfInheritedMetaclass(self):
        sub1 = CMetaclass("Sub1", superclasses = self.m1)
        sub2 = CMetaclass("Sub2", superclasses = self.m2)
        s = CStereotype("S1", extended = self.a)
        c1 = CClass(sub1, "C1")
        c2 = CClass(sub2, "C2")
        l = addLinks({c1: c2}, stereotypeInstances = s)[0]
        eq_(s.extendedInstances, [l])
        eq_(l.stereotypeInstances, [s])

    def testAddStereotypeInstanceCorrectByInheritanceOfStereotype(self):
        s1 = CStereotype("S1", extended = self.a)
        s2 = CStereotype("S2", superclasses = s1)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = c1.addLinks(c2, stereotypeInstances = [s2])[0]
        eq_(s2.extendedInstances, [l])
        eq_(l.stereotypeInstances, [s2])

    def testAllExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.a)
        s2 = CStereotype("S2", superclasses = s1)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        linkObjects = setLinks({c1: [c2, c3]})
        linkObjects[0].stereotypeInstances = s1
        linkObjects[1].stereotypeInstances = s2
        eq_(s1.extendedInstances, [linkObjects[0]])
        eq_(s2.extendedInstances, [linkObjects[1]])
        eq_(s1.allExtendedInstances, [linkObjects[0], linkObjects[1]])
        eq_(s2.allExtendedInstances, [linkObjects[1]])


if __name__ == "__main__":
    nose.main()