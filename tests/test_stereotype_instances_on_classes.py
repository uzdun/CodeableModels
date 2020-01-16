import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeable_models import CMetaclass, CStereotype, CClass, CObject, CAttribute, CException, CEnum

class TestStereotypeInstancesOnClasses():
    def setUp(self):
        self.mcl = CMetaclass("MCL")

    def testStereotypeInstancesOnClass(self):
        s1 = CStereotype("S1", extended = self.mcl)
        s2 = CStereotype("S2", extended = self.mcl)
        s3 = CStereotype("S3", extended = self.mcl)
        c = CClass(self.mcl, "C")
        eq_(c.stereotype_instances, [])
        eq_(s1.extended_instances, [])
        c.stereotype_instances = [s1]
        eq_(s1.extended_instances, [c])
        eq_(c.stereotype_instances, [s1])
        c.stereotype_instances = [s1, s2, s3]
        eq_(s1.extended_instances, [c])
        eq_(s2.extended_instances, [c])
        eq_(s3.extended_instances, [c])
        eq_(set(c.stereotype_instances), set([s1, s2, s3]))
        c.stereotype_instances = s2
        eq_(c.stereotype_instances, [s2])
        eq_(s1.extended_instances, [])
        eq_(s2.extended_instances, [c])
        eq_(s3.extended_instances, [])

    def testStereotypeInstancesDoubleAssignment(self):
        s1 = CStereotype("S1", extended = self.mcl)
        c = CClass(self.mcl, "C")
        try:
            c.stereotype_instances = [s1, s1]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'S1' is already a stereotype instance on 'C'")
        eq_(c.stereotype_instances, [s1])

    def testStereotypeInstancesNoneAssignment(self):
        s1 = CStereotype("S1", extended = self.mcl)
        c = CClass(self.mcl, "C")
        try:
            c.stereotype_instances = [None]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'None' is not a stereotype")
        eq_(c.stereotype_instances, [])

    def testStereotypeInstancesWrongTypeInAssignment(self):
        s1 = CStereotype("S1", extended = self.mcl)
        c = CClass(self.mcl, "C")
        try:
            c.stereotype_instances = self.mcl
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "a list or a stereotype is required as input")
        eq_(c.stereotype_instances, [])

    def testMultipleExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.mcl)
        s2 = CStereotype("S2", extended = self.mcl)
        c1 = CClass(self.mcl, "C1", stereotype_instances = [s1])
        eq_(s1.extended_instances, [c1])
        c2 = CClass(self.mcl, "C2", stereotype_instances = s1)
        eq_(set(s1.extended_instances), set([c1, c2]))
        c3 = CClass(self.mcl, "C3", stereotype_instances = [s1, s2])
        eq_(set(s1.extended_instances), set([c1, c2, c3]))
        eq_(set(s2.extended_instances), set([c3]))
    
    def testDeleteStereotypeOfExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.mcl)
        s1.delete()
        try: 
            CClass(self.mcl, "C1", stereotype_instances = [s1])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testDeleteStereotypedElementInstance(self):
        s1 = CStereotype("S1", extended = self.mcl)
        c = CClass(self.mcl, "C1", stereotype_instances = [s1])
        c.delete()
        eq_(s1.extended_instances, [])
        eq_(c.stereotype_instances, [])

    def testAddStereotypeInstanceWrongMetaclass(self):
        otherMCL = CMetaclass()
        s1 = CStereotype("S1", extended = self.mcl)
        try: 
            CClass(otherMCL, "C1", stereotype_instances = [s1])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype 'S1' cannot be added to 'C1': no extension by this stereotype found")   

    def testAddStereotypeInstanceMetaclassCorrectByInheritanceOfMetaclass(self):
        mcl1 = CMetaclass("MCL1")
        mcl2 = CMetaclass("MCL2", superclasses = mcl1)
        s = CStereotype("S1", extended = mcl1)
        c = CClass(mcl2, "CL", stereotype_instances = s)
        eq_(s.extended_instances, [c])
        eq_(c.stereotype_instances, [s])

    def testApplyStereotypeInstancesWrongMetaclassInheritance(self):
        mcl1 = CMetaclass("MCL1", superclasses = self.mcl)
        mcl2 = CMetaclass("MCL2", superclasses = self.mcl) 
        s1 = CStereotype("S1", extended = mcl1)
        s2 = CStereotype("S2", extended = mcl2)
        superST = CStereotype("SuperST", extended = self.mcl)

        c = CClass(self.mcl, "CL")

        try:
            c.stereotype_instances = s1
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype 'S1' cannot be added to 'CL': no extension by this stereotype found")   

        c.stereotype_instances = superST

        mcl1Class = CClass(mcl1, "Mcl1Class", stereotype_instances = s1)
        try:
            mcl1Class.stereotype_instances = [s1, s2]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype 'S2' cannot be added to 'Mcl1Class': no extension by this stereotype found")
        mcl1Class.stereotype_instances = [s1, superST]
        eq_(set(mcl1Class.stereotype_instances), set([s1, superST]))
        eq_(c.stereotype_instances, [superST])

    def testAddStereotypeInstanceMetaclassWrongInheritanceHierarchy(self):
        mcl1 = CMetaclass("MCL1")
        mcl2 = CMetaclass("MCL2", superclasses = mcl1)
        s = CStereotype("S1", extended = mcl2)
        c = CClass(mcl1, "CL")
        try:
            c.stereotype_instances = [s]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype 'S1' cannot be added to 'CL': no extension by this stereotype found")


    def testAddStereotypeInstanceMetaclassCorrectByInheritanceOfStereotype(self):
        s1 = CStereotype("S1", extended = self.mcl)
        s2 = CStereotype("S2", superclasses = s1)
        c = CClass(self.mcl, "CL", stereotype_instances = s2)
        eq_(s2.extended_instances, [c])
        eq_(c.stereotype_instances, [s2])

    def testAllExtendedInstances(self):
        s1 = CStereotype("S1", extended = self.mcl)
        s2 = CStereotype("S2", superclasses = s1)
        c1 = CClass(self.mcl, "C1", stereotype_instances = s1)
        c2 = CClass(self.mcl, "C2", stereotype_instances = s2)
        eq_(s1.extended_instances, [c1])
        eq_(s2.extended_instances, [c2])
        eq_(s1.all_extended_instances, [c1, c2])
        eq_(s2.all_extended_instances, [c2])

    def testDefaultValuesFromStereotypeOnClass(self):
        mcl = CMetaclass("MCL", attributes = {
            "aStr1": str, "aList1": list, "aStr2": "def", "aList2": ["d1", "d2"], "b": bool
        })
        s1 = CStereotype("S1", extended = mcl, default_values = {
            "aStr1": "a", "aList1": ["a"], "aStr2": "def2", "aList2": []
        })

        c1 = CClass(mcl, "C1", stereotype_instances = s1)
        eq_(c1.get_value("aStr1"), "a")
        eq_(c1.get_value("aList1"), ["a"])
        eq_(c1.get_value("aStr2"), "def2")
        eq_(c1.get_value("aList2"), [])

        s1.set_default_value("aStr1", "b")
        eq_(c1.get_value("aStr1"), "a")
        c2 = CClass(mcl, "C2", stereotype_instances = s1)
        eq_(c2.get_value("aStr1"), "b")
        eq_(c2.get_value("aList1"), ["a"])
        eq_(c2.get_value("aStr2"), "def2")
        eq_(c2.get_value("aList2"), [])

        eq_(c1.get_value("b"), None)
        s1.set_default_value("b", True)
        eq_(c1.get_value("b"), None)
        c3 = CClass(mcl, "C3", stereotype_instances = s1)
        eq_(c3.get_value("b"), True)

    def testDefaultValuesFromStereotypeOnClassInheritance1(self):
        mcl = CMetaclass("MCL", attributes = {
            "aStr2": "def", "aList2": ["d1", "d2"], "b": bool
        })
        mcl2 = CMetaclass("MCL2", superclasses = mcl, attributes = {
            "aStr1": str, "aList1": list
        })
        s1 = CStereotype("S1", extended = mcl2, default_values = {
            "aStr1": "a", "aList2": []
        })
        s2 = CStereotype("S2", superclasses = s1, extended = mcl2, default_values = {
            "aList1": ["a"], "aStr2": "def2"
        })

        c1 = CClass(mcl2, "C1", stereotype_instances = s2)
        eq_(c1.get_value("aStr1"), "a")
        eq_(c1.get_value("aList1"), ["a"])
        eq_(c1.get_value("aStr2"), "def2")
        eq_(c1.get_value("aList2"), [])

        c2 = CClass(mcl2, "C2", stereotype_instances = s1)
        eq_(c2.get_value("aStr1"), "a")
        eq_(c2.get_value("aList1"), None)
        eq_(c2.get_value("aStr2"), "def")
        eq_(c2.get_value("aList2"), [])
        
    def testDefaultValuesFromStereotypeOnClassInheritance2(self):
        mcl = CMetaclass("MCL", attributes = {
            "aStr2": "def", "aList2": ["d1", "d2"], "b": bool
        })
        mcl2 = CMetaclass("MCL2", superclasses = mcl, attributes = {
            "aStr1": str, "aList1": list
        })
        s1 = CStereotype("S1", extended = mcl, default_values = {
            "aList2": [], "aStr2": "def2"
        })
        s2 = CStereotype("S2", superclasses = s1, extended = mcl2, default_values = {
            "aStr1": "a", "aList1": ["a"], 
        })

        c1 = CClass(mcl2, "C1", stereotype_instances = s2)
        eq_(c1.get_value("aStr1"), "a")
        eq_(c1.get_value("aList1"), ["a"])
        eq_(c1.get_value("aStr2"), "def2")
        eq_(c1.get_value("aList2"), [])

        c2 = CClass(mcl2, "C2", stereotype_instances = s1)
        eq_(c2.get_value("aStr1"), None)
        eq_(c2.get_value("aList1"), None)
        eq_(c2.get_value("aStr2"), "def2")
        eq_(c2.get_value("aList2"), [])

    def testDefaultValuesFromStereotype_MetaclassDelete(self):
        mcl = CMetaclass("MCL", attributes = {
            "aStr2": "def", "aList2": ["d1", "d2"], "b": bool
        })
        mcl2 = CMetaclass("MCL2", superclasses = mcl, attributes = {
            "aStr1": str, "aList1": list
        })
        s1 = CStereotype("S1", extended = mcl2, default_values = {
            "aStr1": "a", "aList2": []
        })
        s2 = CStereotype("S2", superclasses = s1, extended = mcl2, default_values = {
            "aList1": ["a"], "aStr2": "def2"
        })
        c1 = CClass(mcl2, "C1", stereotype_instances = s2)
        mcl.delete()
        c2 = CClass(mcl2, "C2", stereotype_instances = s1)
        c3 = CClass(mcl2, "C3", stereotype_instances = s2)


        eq_(c1.get_value("aStr1"), "a")
        eq_(c1.get_value("aList1"), ["a"])
        try:
            eq_(c1.get_value("aStr2"), "def2")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'aStr2' unknown for 'C1'") 

        eq_(c2.get_value("aStr1"), "a")
        eq_(c2.get_value("aList1"), None)
        try:
            eq_(c2.get_value("aStr2"), "def2")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'aStr2' unknown for 'C2'") 

        eq_(c3.get_value("aStr1"), "a")
        eq_(c3.get_value("aList1"), ["a"])
        try:
            eq_(c3.get_value("aStr2"), "def2")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'aStr2' unknown for 'C3'") 

    def testDefaultValuesFromStereotype_StereotypeDelete(self):
        mcl = CMetaclass("MCL", attributes = {
            "aStr2": "def", "aList2": ["d1", "d2"], "b": bool
        })
        mcl2 = CMetaclass("MCL2", superclasses = mcl, attributes = {
            "aStr1": str, "aList1": list
        })
        s1 = CStereotype("S1", extended = mcl2, default_values = {
            "aStr1": "a", "aList2": []
        })
        s2 = CStereotype("S2", superclasses = s1, extended = mcl2, default_values = {
            "aList1": ["a"], "aStr2": "def2"
        })
        c1 = CClass(mcl2, "C1", stereotype_instances = s2)
        s1.delete()
        c2 = CClass(mcl2, "C2", stereotype_instances = s2)

        eq_(c1.get_value("aStr1"), "a")
        eq_(c1.get_value("aList1"), ["a"])
        eq_(c1.get_value("aStr2"), "def2")
        eq_(c1.get_value("aList2"), [])

        eq_(c2.get_value("aStr1"), None)
        eq_(c2.get_value("aList1"), ["a"])
        eq_(c2.get_value("aStr2"), "def2")
        eq_(c2.get_value("aList2"), ["d1", "d2"])


if __name__ == "__main__":
    nose.main()