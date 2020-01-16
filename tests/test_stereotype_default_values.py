import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized
import re

from codeable_models import CMetaclass, CClass, CObject, CAttribute, CException, CEnum, CStereotype

class TestStereotypeDefaultValues():
    def setUp(self):
        self.mcl = CMetaclass("MCL")
        self.stereotype = CStereotype("S", extended = self.mcl)
        self.m1 = CMetaclass("M1")
        self.m2 = CMetaclass("M2")
        self.a = self.m1.association(self.m2, name = "a", multiplicity = "*", role_name = "m1",
            source_multiplicity = "1", source_role_name = "m2")


    def testDefaultValuesOnStereotype(self):
        mcl = CMetaclass("MCL", attributes = {
            "aStr1": str, "aList1": list, "aStr2": "def", "aList2": ["d1", "d2"], "b": bool
        })
        s1 = CStereotype("S1", extended = mcl, default_values = {
            "aStr1": "a", "aList1": ["a"], "aStr2": "def2", "aList2": []
        })
        eq_(s1.default_values, {"aStr1": "a", "aList1": ["a"], "aStr2": "def2", "aList2": []})
        eq_(s1.get_default_value("aStr1"), "a")
        s1.set_default_value("aStr1", "b")
        eq_(s1.get_default_value("aStr1"), "b")

        s1.default_values = {}
        # default_values should not delete existing values
        eq_(s1.default_values, {'aStr1': 'b', 'aList1': ['a'], 'aStr2': 'def2', 'aList2': []})

        s1.default_values = {"b": True}
        eq_(s1.default_values, {'aStr1': 'b', 'aList1': ['a'], 'aStr2': 'def2', 'aList2': [], 'b': True})
        eq_(s1.get_default_value("b"), True)

    def testDefaultValuesOnStereotype_InitializedInClassConstructor(self):
        mcl = CMetaclass("MCL", attributes = {
            "aStr1": str, "aList1": list, "aStr2": "def", "aList2": ["d1", "d2"], "b": True
        })
        s = CStereotype("S", extended = mcl, default_values = {
            "aStr1": "a", "aList1": ["a"], "aStr2": "def2", "aList2": []
        })
        c1 = CClass(mcl, "C1", stereotype_instances = s)
        # metaclass defaults are initialized at the end of construction, stereotype_instances runs before
        # and thus overwrites metaclass defaults
        eq_(c1.values, {"aStr1": "a", "aList1": ["a"], "aStr2": "def2", "aList2": [], "b": True})

    def testDefaultValuesOnStereotype_InitializeAfterClassConstructor(self):
        mcl = CMetaclass("MCL", attributes = {
            "aStr1": str, "aList1": list, "aStr2": "def", "aList2": ["d1", "d2"], "b": True
        })
        s = CStereotype("S", extended = mcl, default_values = {
            "aStr1": "a", "aList1": ["a"], "aStr2": "def2", "aList2": []
        })
        c1 = CClass(mcl, "C1")
        c1.stereotype_instances = s
        # after construction, metaclass defaults are set. The stereotype defaults are set only for 
        # values not yet set
        eq_(c1.values, {'aStr2': 'def', 'aList2': ['d1', 'd2'], 'b': True, 'aStr1': 'a', 'aList1': ['a']})

    def testDefaultValuesOnStereotypeExceptions(self):
        mcl = CMetaclass("MCL", attributes = {
            "aStr1": str, "aList1": list, "aStr2": "def", "aList2": ["d1", "d2"], "b": bool
        })
        s1 = CStereotype("S1", extended = mcl, default_values = {
            "aStr1": "a", "aList1": ["a"], "aStr2": "def2", "aList2": []
        })
        try:
            s1.default_values = {"x": bool}
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'x' unknown for metaclasses extended by stereotype 'S1'")   

        try:
            s1.default_values = {"b": bool}
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "value for attribute 'b' is not a known attribute type")  

        try:
            s1.default_values = {"b": []}
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "value type for attribute 'b' does not match attribute type") 

        try:
            s1.default_values = []
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "malformed default values description: '[]'")     

    def testDefaultValuesOnStereotypeInheritance1(self):
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

        eq_(s1.default_values, {"aStr1": "a", "aList2": []})
        eq_(s2.default_values, {"aList1": ["a"], "aStr2": "def2"})
        eq_(s1.get_default_value("aStr1"), "a")
        eq_(s2.get_default_value("aStr2"), "def2")
        eq_(s2.get_default_value("aStr1"), None)
        eq_(s1.get_default_value("aStr2"), None)

    def testDefaultValuesOnStereotypeInheritance2(self):
        mcl = CMetaclass("MCL", attributes = {
            "aStr2": "def", "aList2": ["d1", "d2"], "b": bool
        })
        mcl2 = CMetaclass("MCL2", superclasses = mcl, attributes = {
            "aStr1": str, "aList1": list
        })
        try:
            s1 = CStereotype("S1", extended = mcl, default_values = {
                "aStr1": "a", "aList2": []
            })
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'aStr1' unknown for metaclasses extended by stereotype 'S1'")   

        s2 = CStereotype("S2", extended = mcl2, default_values = {
            "aList1": ["a"], "aStr2": "def2"
        })
        eq_(s2.default_values, {"aList1": ["a"], "aStr2": "def2"})

    def testDefaultValuesOnStereotype_MetaclassDelete(self):
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
        mcl.delete()

        eq_(s1.default_values, {"aStr1": "a"})
        eq_(s2.default_values, {"aList1": ["a"]})
        eq_(s1.get_default_value("aStr1"), "a")
        try:
            eq_(s2.get_default_value("aStr2"), "def2")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'aStr2' unknown for metaclasses extended by stereotype 'S2'")   
        eq_(s2.get_default_value("aStr1"), None)

    def testDeleteDefaultValues(self):
        mcl = CMetaclass("MCL", attributes = {
                "isBoolean": True, 
                "intVal": int,
                "floatVal": 1.1,
                "string": "def",
                "list": list})    
        s = CStereotype("S", extended = mcl, default_values = {
                "isBoolean": False, 
                "intVal": 1,
                "string": "abc",
                "list": ["a", "b"]})
        c1 = CClass(mcl, "C1", stereotype_instances = s)
        s.delete_default_value("isBoolean")
        s.delete_default_value("intVal")
        valueOfList = s.delete_default_value("list")
        eq_(s.default_values, {"string": "abc"})
        eq_(valueOfList, ['a', 'b'])
        c2 = CClass(mcl, "C2", stereotype_instances = s)
        eq_(c1.values, {'isBoolean': False, 'floatVal': 1.1, 'string': 'abc', 'intVal': 1, 'list': ['a', 'b']})
        eq_(c2.values, {'isBoolean': True, 'floatVal': 1.1, 'string': 'abc'})

    def testDeleteDefaultValuesWithSuperclass(self):
        smcl = CMetaclass("sMCL", attributes = {
                "isBoolean": False, 
                "intVal": int,
                "intVal2": int})
        mcl = CMetaclass("MCL", superclasses = smcl, attributes = {
                "isBoolean": False, 
                "intVal": int,
                "intVal2": int}) 
        sst = CStereotype("SST", extended = mcl, default_values = {
            "intVal": 20, "intVal2": 30})
        st = CStereotype("ST", superclasses = sst, default_values = {
                "isBoolean": True, 
                "intVal": 1})
        c1 = CClass(mcl, "C1", stereotype_instances = st)
        eq_(c1.values, {'isBoolean': True, 'intVal': 1, 'intVal2': 30})
        st.delete_default_value("isBoolean")
        sst.delete_default_value("intVal2")
        st.delete_default_value("intVal")
        eq_(st.default_values, {})
        eq_(sst.default_values, {"intVal": 20})
        c2 = CClass(mcl, "C2", stereotype_instances = st)
        eq_(c1.values, {'isBoolean': True, 'intVal': 1, 'intVal2': 30})
        eq_(c2.values, {'isBoolean': False, 'intVal': 20})

        sst.set_default_value("intVal", 2, smcl)
        sst.set_default_value("intVal", 3, mcl)
        eq_(sst.default_values, {"intVal": 3})
        sst.delete_default_value("intVal")
        eq_(sst.default_values, {"intVal": 2})

        sst.set_default_value("intVal", 2, smcl)
        sst.set_default_value("intVal", 3, mcl)
        sst.delete_default_value("intVal", mcl)
        eq_(sst.default_values, {"intVal": 2})

        sst.set_default_value("intVal", 2, smcl)
        sst.set_default_value("intVal", 3, mcl)
        sst.delete_default_value("intVal", smcl)
        eq_(sst.default_values, {"intVal": 3})

    def testDefaultValuesExceptionalCases(self):
        mcl = CMetaclass("MCL", attributes = {
                "isBoolean": True, 
                "intVal": int,
                "floatVal": 1.1,
                "string": "def",
                "list": list})    
        s1 = CStereotype("S", extended = mcl, default_values = {
                "isBoolean": False, 
                "intVal": 1,
                "string": "abc",
                "list": ["a", "b"]})
        s1.delete()
        
        try:
            s1.get_default_value("b")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't get default value 'b' on deleted stereotype")

        try:
            s1.set_default_value("b", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't set default value 'b' on deleted stereotype")

        try:
            s1.delete_default_value("b")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't delete default value 'b' on deleted stereotype")

        try:
            s1.default_values = {"b": 1}
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't set default values on deleted stereotype")

        try:
            s1.default_values
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't get default values on deleted stereotype")

        s = CStereotype("S", extended = mcl, default_values = {
                "isBoolean": False, 
                "intVal": 1,
                "string": "abc",
                "list": ["a", "b"]})
        try:
            s.delete_default_value("x")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'x' unknown for metaclasses extended by stereotype 'S'")

    def testDefaultValuesFromStereotypeOnAssociationFails(self):
        try:
            s1 = CStereotype("S1", extended = self.a, default_values = {
                "aStr1": "a", "aList1": ["a"], "aStr2": "def2", "aList2": []
            })
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "default values can only be used on a stereotype that extends metaclasses")

    def testSetDefaultValueFromStereotypeOnAssociationFails(self):
        try:
            s1 = CStereotype("S1", extended = self.a)
            s1.set_default_value("a", "1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "default values can only be used on a stereotype that extends metaclasses")

    def testGetDefaultValueFromStereotypeOnAssociationFails(self):
        try:
            s1 = CStereotype("S1", extended = self.a)
            s1.get_default_value("a")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "default values can only be used on a stereotype that extends metaclasses")

    def testDeleteDefaultValueFromStereotypeOnAssociationFails(self):
        try:
            s1 = CStereotype("S1", extended = self.a)
            s1.delete_default_value("a")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "default values can only be used on a stereotype that extends metaclasses")

    def testDefaultValuesFromStereotypeOnNoExtensionFails(self):
        try:
            s1 = CStereotype("S1", default_values = {
                "aStr1": "a", "aList1": ["a"], "aStr2": "def2", "aList2": []
            })
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "default values can only be used on a stereotype that extends metaclasses")

    def testSetDefaultValueFromStereotypeOnNoExtensionFails(self):
        try:
            s1 = CStereotype("S1")
            s1.set_default_value("a", "1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "default values can only be used on a stereotype that extends metaclasses")

    def testGetDefaultValueFromStereotypeOnNoExtensionFails(self):
        try:
            s1 = CStereotype("S1")
            s1.get_default_value("a")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "default values can only be used on a stereotype that extends metaclasses")

    def testDeleteDefaultValueFromStereotypeOnNoExtensionFails(self):
        try:
            s1 = CStereotype("S1")
            s1.delete_default_value("a")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "default values can only be used on a stereotype that extends metaclasses")


if __name__ == "__main__":
    nose.main()


