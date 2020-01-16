import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeable_models import CMetaclass, CStereotype, CClass, CObject, CAttribute, CException, CEnum, set_links, add_links

class TestStereotypeInstancesOnAssociations():
    def setUp(self):
        self.m1 = CMetaclass("M1")
        self.m2 = CMetaclass("M2")
        self.a = self.m1.association(self.m2, name = "a", multiplicity = "*", role_name = "m1",
            source_multiplicity = "1", source_role_name = "m2")

    def testStereotypeInstancesOnAssociation(self):
        s1 = CStereotype("S1", extended = self.a)
        s2 = CStereotype("S2", extended = self.a)
        s3 = CStereotype("S3", extended = self.a)

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        link_objects = set_links({c1: [c2, c3]})
        l1 = link_objects[0]

        eq_(l1.stereotype_instances, [])
        eq_(s1.extended_instances, [])
        l1.stereotype_instances = [s1]
        eq_(s1.extended_instances, [l1])
        eq_(l1.stereotype_instances, [s1])
        l1.stereotype_instances = [s1, s2, s3]
        eq_(s1.extended_instances, [l1])
        eq_(s2.extended_instances, [l1])
        eq_(s3.extended_instances, [l1])
        eq_(set(l1.stereotype_instances), set([s1, s2, s3]))
        l1.stereotype_instances = s2
        eq_(l1.stereotype_instances, [s2])
        eq_(s1.extended_instances, [])
        eq_(s2.extended_instances, [l1])
        eq_(s3.extended_instances, [])

    def testStereotypeInstancesDoubleAssignment(self):
        s1 = CStereotype("S1", extended = self.a)
        
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = set_links({c1: c2})[0]

        try:
            l.stereotype_instances = [s1, s1]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'S1' is already a stereotype instance on link from 'C1' to 'C2'")
        eq_(l.stereotype_instances, [s1])

    def testStereotypeInstancesNoneAssignment(self):
        s1 = CStereotype("S1", extended = self.a)
        
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = set_links({c1:[c2]})[0]

        try:
            l.stereotype_instances = [None]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'None' is not a stereotype")
        eq_(l.stereotype_instances, [])

    def testStereotypeInstancesWrongTypeInAssignment(self):
        s1 = CStereotype("S1", extended = self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = c1.add_links(c2)[0]
        try:
            l.stereotype_instances = self.a
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "a list or a stereotype is required as input")
        eq_(l.stereotype_instances, [])

    def testMultipleExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.a)
        s2 = CStereotype("S2", extended = self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        c4 = CClass(self.m2, "C4")
        link_objects = set_links({c1: [c2, c3, c4]})
        link_objects[0].stereotype_instances = [s1]
        eq_(s1.extended_instances, [link_objects[0]])
        link_objects[1].stereotype_instances = [s1]
        eq_(set(s1.extended_instances), set([link_objects[0], link_objects[1]]))
        link_objects[2].stereotype_instances = [s1, s2]
        eq_(set(s1.extended_instances), set([link_objects[0], link_objects[1], link_objects[2]]))
        eq_(set(s2.extended_instances), set([link_objects[2]]))
    
    def testDeleteStereotypeOfExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.a)
        s1.delete()
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = set_links({c1: c2})[0]
        try: 
            l.stereotype_instances = [s1]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testDeleteStereotypedElementInstance(self):
        s1 = CStereotype("S1", extended = self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = set_links({c1: c2}, stereotype_instances = [s1])[0]
        eq_(s1.extended_instances, [l])
        eq_(l.stereotype_instances, [s1])
        l.delete()
        eq_(s1.extended_instances, [])
        eq_(l.stereotype_instances, [])

    def testAddStereotypeInstanceWrongAssociation(self):
        otherAssociation = self.m1.association(self.m2, name = "b", multiplicity = "*", role_name = "m1",
            source_multiplicity = "1", source_role_name = "m2")
        s1 = CStereotype("S1", extended = self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = set_links({c1: c2}, association = otherAssociation)[0]
        try:
            l.stereotype_instances = [s1]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype 'S1' cannot be added to link from 'C1' to 'C2': no extension by this stereotype found")   

    def testAddStereotypeOfInheritedMetaclass(self):
        sub1 = CMetaclass("Sub1", superclasses = self.m1)
        sub2 = CMetaclass("Sub2", superclasses = self.m2)
        s = CStereotype("S1", extended = self.a)
        c1 = CClass(sub1, "C1")
        c2 = CClass(sub2, "C2")
        l = add_links({c1: c2}, stereotype_instances = s)[0]
        eq_(s.extended_instances, [l])
        eq_(l.stereotype_instances, [s])

    def testAddStereotypeInstanceCorrectByInheritanceOfStereotype(self):
        s1 = CStereotype("S1", extended = self.a)
        s2 = CStereotype("S2", superclasses = s1)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        l = c1.add_links(c2, stereotype_instances = [s2])[0]
        eq_(s2.extended_instances, [l])
        eq_(l.stereotype_instances, [s2])

    def testAllExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.a)
        s2 = CStereotype("S2", superclasses = s1)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        link_objects = set_links({c1: [c2, c3]})
        link_objects[0].stereotype_instances = s1
        link_objects[1].stereotype_instances = s2
        eq_(s1.extended_instances, [link_objects[0]])
        eq_(s2.extended_instances, [link_objects[1]])
        eq_(s1.all_extended_instances, [link_objects[0], link_objects[1]])
        eq_(s2.all_extended_instances, [link_objects[1]])


if __name__ == "__main__":
    nose.main()