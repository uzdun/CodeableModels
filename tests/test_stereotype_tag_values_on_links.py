import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeable_models import *

class TestStereotypeTagValuesOnLinks():
    def setUp(self):
        self.st = CStereotype("ST")      
        self.m1 = CMetaclass("M1")
        self.m2 = CMetaclass("M2")
        self.a = self.m1.association(self.m2, name = "a", multiplicity = "*", role_name = "m1",
            source_multiplicity = "1", source_role_name = "m2")
        self.a.stereotypes = self.st
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        c4 = CClass(self.m2, "C4")
        self.link_objects = set_links({c1: [c2, c3, c4]})
        self.l = self.link_objects[0]
        self.l2 = self.link_objects[1]
        self.l3 = self.link_objects[2]
        self.l.stereotype_instances = self.st


    def testTaggedValuesOnPrimitiveTypeAttributes(self):
        s = CStereotype("S", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"]})
        self.a.stereotypes = s
        self.l.stereotype_instances = s

        eq_(self.l.get_tagged_value("isBoolean"), True)
        eq_(self.l.get_tagged_value("intVal"), 1)
        eq_(self.l.get_tagged_value("floatVal"), 1.1)
        eq_(self.l.get_tagged_value("string"), "abc")
        eq_(self.l.get_tagged_value("list"), ["a", "b"])

        self.l.set_tagged_value("isBoolean", False)
        self.l.set_tagged_value("intVal", 2)
        self.l.set_tagged_value("floatVal", 2.1)
        self.l.set_tagged_value("string", "y")

        eq_(self.l.get_tagged_value("isBoolean"), False)
        eq_(self.l.get_tagged_value("intVal"), 2)
        eq_(self.l.get_tagged_value("floatVal"), 2.1)
        eq_(self.l.get_tagged_value("string"), "y")

        self.l.set_tagged_value("list", [])
        eq_(self.l.get_tagged_value("list"), [])
        self.l.set_tagged_value("list", [1, 2, 3])
        eq_(self.l.get_tagged_value("list"), [1, 2, 3])

    def testAttributeOfTaggedValueUnknown(self):
        try:
            self.l.get_tagged_value("x")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'x' unknown")

    def testIntegersAsFloatTaggedValues(self):
        self.st.attributes = {"floatVal": float}
        self.l.set_tagged_value("floatVal", 15)
        eq_(self.l.get_tagged_value("floatVal"), 15)

    def testObjectTypeAttributeTaggedValues(self):
        attrType = CClass(self.m1, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        self.st.attributes = {"attrTypeObj" : attrValue}
        objAttr = self.st.get_attribute("attrTypeObj")
        eq_(objAttr.type, attrType)
        eq_(self.l.get_tagged_value("attrTypeObj"), attrValue)

        nonAttrValue = CObject(CClass(self.m1), "nonAttrValue")
        try:
            self.l.set_tagged_value("attrTypeObj", nonAttrValue)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "type of 'nonAttrValue' is not matching type of attribute 'attrTypeObj'")

    def testClassTypeAttributeTaggedValues(self):
        attrType = CMetaclass("AttrType")
        attrValue = CClass(attrType, "attrValue")
        self.st.attributes = {"attrTypeCl" : attrType}
        clAttr = self.st.get_attribute("attrTypeCl")
        clAttr.default = attrValue
        eq_(clAttr.type, attrType)
        eq_(self.l.get_tagged_value("attrTypeCl"), attrValue)

        nonAttrValue = CClass(CMetaclass("MX"), "nonAttrValue")
        try:
            self.l.set_tagged_value("attrTypeCl", nonAttrValue)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "type of 'nonAttrValue' is not matching type of attribute 'attrTypeCl'")

    def testAddObjectAttributeGetSetTaggedValue(self):
        attrType = CClass(self.m1, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        self.st.attributes = {
            "attrTypeObj1" : attrType, "attrTypeObj2" : attrValue
        }
        eq_(self.l.get_tagged_value("attrTypeObj1"), None)
        eq_(self.l.get_tagged_value("attrTypeObj2"), attrValue)

    def testObjectAttributeTaggedValueOfSuperclassType(self):
        attrSuperType = CClass(self.m1, "AttrSuperType") 
        attrType = CClass(self.m1, "AttrType", superclasses = attrSuperType)
        attrValue = CObject(attrType, "attrValue")
        self.st.attributes = {
            "attrTypeObj1" : attrSuperType, "attrTypeObj2" : attrValue
        }
        self.l.set_tagged_value("attrTypeObj1", attrValue)
        self.l.set_tagged_value("attrTypeObj2", attrValue)
        eq_(self.l.get_tagged_value("attrTypeObj1"), attrValue)
        eq_(self.l.get_tagged_value("attrTypeObj2"), attrValue)

    def testTaggedValuesOnAttributesWithNoDefaultValues(self):
        attrType = CClass(self.m1, "AttrType")
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        st = CStereotype("S", attributes = {
                "b": bool, 
                "i": int,
                "f": float,
                "s": str,
                "l": list,
                "C": attrType,
                "e": enumType})
        self.a.stereotypes = st
        self.l.stereotype_instances = st
        for n in ["b", "i", "f", "s", "l", "C", "e"]:
            eq_(self.l.get_tagged_value(n), None)

    def testTaggedValuesSetter(self):
        objValType = CClass(CMetaclass())
        objVal = CObject(objValType, "objVal")

        st = CStereotype("S", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"],
                "obj": objValType})
        self.a.stereotypes = st
        self.l.stereotype_instances = st
        self.l.tagged_values = {
            "isBoolean": False, "intVal": 2, "floatVal": 2.1, 
            "string": "y", "list": [], "obj": objVal}

        eq_(self.l.get_tagged_value("isBoolean"), False)
        eq_(self.l.get_tagged_value("intVal"), 2)
        eq_(self.l.get_tagged_value("floatVal"), 2.1)
        eq_(self.l.get_tagged_value("string"), "y")
        eq_(self.l.get_tagged_value("list"), [])
        eq_(self.l.get_tagged_value("obj"), objVal)

        eq_(self.l.tagged_values, {"isBoolean": False, "intVal": 2, "floatVal": 2.1,
            "string": "y", "list": [], "obj": objVal})

    def testTaggedValuesSetterOverwrite(self):
        st = CStereotype("S", attributes = {
                "isBoolean": True, 
                "intVal": 1})
        self.a.stereotypes = st
        self.l.stereotype_instances = st
        self.l.tagged_values = {"isBoolean": False, "intVal": 2}
        self.l.tagged_values = {"isBoolean": True, "intVal": 20}
        eq_(self.l.get_tagged_value("isBoolean"), True)
        eq_(self.l.get_tagged_value("intVal"), 20)
        eq_(self.l.tagged_values, {'isBoolean': True, 'intVal': 20})
        self.l.tagged_values = {}
        # tagged values should not delete existing values
        eq_(self.l.tagged_values, {"isBoolean": True, "intVal": 20})

    def testTaggedValuesSetterWithSuperclass(self):
        sst = CStereotype("SST", attributes = {
                "intVal": 20, "intVal2": 30})
        st = CStereotype("S", superclasses = sst, attributes = {
                "isBoolean": True, 
                "intVal": 1})
        self.a.stereotypes = st
        self.l.stereotype_instances = st
        self.l.tagged_values = {"isBoolean": False}
        eq_(self.l.tagged_values, {"isBoolean": False, "intVal": 1, "intVal2": 30})
        self.l.set_tagged_value("intVal", 12, sst)
        self.l.set_tagged_value("intVal", 15, st)
        self.l.set_tagged_value("intVal2", 16, sst)
        eq_(self.l.tagged_values, {"isBoolean": False, "intVal": 15, "intVal2": 16})
        eq_(self.l.get_tagged_value("intVal", sst), 12)
        eq_(self.l.get_tagged_value("intVal", st), 15)

    def testTaggedValuesSetterMalformedDescription(self):
        try:
            self.l.tagged_values = [1, 2, 3]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "malformed tagged values description: '[1, 2, 3]'")

    def testEnumTypeAttributeValues(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        self.st.attributes = {
                "e1": enumType,
                "e2": enumType}
        e2 = self.st.get_attribute("e2")
        e2.default = "A"
        eq_(self.l.get_tagged_value("e1"), None)
        eq_(self.l.get_tagged_value("e2"), "A")
        self.l.set_tagged_value("e1", "B")
        self.l.set_tagged_value("e2", "C")
        eq_(self.l.get_tagged_value("e1"), "B")
        eq_(self.l.get_tagged_value("e2"), "C")
        try:
            self.l.set_tagged_value("e1", "X")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "value 'X' is not element of enumeration")

    def testDefaultInitAfterInstanceCreation(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        self.st.attributes = {
                "e1": enumType,
                "e2": enumType}
        e2 = self.st.get_attribute("e2")
        e2.default = "A"
        eq_(self.l.get_tagged_value("e1"), None)
        eq_(self.l.get_tagged_value("e2"), "A")

    def testAttributeValueTypeCheckBool1(self):
        self.st.attributes = {"t": bool}
        self.stereotype_instances = self.st
        try:
            self.l.set_tagged_value("t", self.m1)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value for attribute 't' is not a known attribute type", e.value)

    def testAttributeValueTypeCheckBool2(self):
        self.st.attributes = {"t": bool}
        self.l.stereotype_instances = self.st
        try:
            self.l.set_tagged_value("t", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckInt(self):
        self.st.attributes = {"t": int}
        self.l.stereotype_instances = self.st
        try:
            self.l.set_tagged_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckFloat(self):
        self.st.attributes = {"t": float}
        self.l.stereotype_instances = self.st
        try:
            self.l.set_tagged_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckStr(self):
        self.st.attributes = {"t": str}
        self.l.stereotype_instances = self.st
        try:
            self.l.set_tagged_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckList(self):
        self.st.attributes = {"t": list}
        self.l.stereotype_instances = self.st
        try:
            self.l.set_tagged_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckObject(self):
        attrType = CClass(CMetaclass(), "AttrType")
        self.st.attributes = {"t": attrType}
        self.l.stereotype_instances = self.st
        try:
            self.l.set_tagged_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckEnum(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        self.st.attributes = {"t": enumType}
        self.l.stereotype_instances = self.st
        try:
            self.l.set_tagged_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeDeleted(self):
        self.st.attributes = {
                "isBoolean": True, 
                "intVal": 15}
        self.l.stereotype_instances = self.st
        eq_(self.l.get_tagged_value("intVal"), 15)
        self.st.attributes = {
                "isBoolean": False}
        eq_(self.l.get_tagged_value("isBoolean"), True)
        try:
            self.l.get_tagged_value("intVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'intVal' unknown") 
        try:
            self.l.set_tagged_value("intVal", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'intVal' unknown") 

    def testAttributeDeletedNoDefault(self):
        self.st.attributes = {
                "isBoolean": bool, 
                "intVal": int}
        self.st.attributes = {"isBoolean": bool}
        eq_(self.l.get_tagged_value("isBoolean"), None)
        try:
            self.l.get_tagged_value("intVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'intVal' unknown")    
        try:
            self.l.set_tagged_value("intVal", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'intVal' unknown") 

    def testAttributesOverwrite(self):
        self.st.attributes = {
                "isBoolean": True, 
                "intVal": 15}
        self.l.stereotype_instances = self.st
        eq_(self.l.get_tagged_value("intVal"), 15)
        try:
            self.l.get_tagged_value("floatVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'floatVal' unknown")        
        self.l.set_tagged_value("intVal", 18)
        self.st.attributes = {
                "isBoolean": False, 
                "intVal": 19, 
                "floatVal": 25.1}
        eq_(self.l.get_tagged_value("isBoolean"), True)
        eq_(self.l.get_tagged_value("floatVal"), 25.1)
        eq_(self.l.get_tagged_value("intVal"), 18)
        self.l.set_tagged_value("floatVal", 1.2)
        eq_(self.l.get_tagged_value("floatVal"), 1.2)

    def testAttributesOverwriteNoDefaults(self):
        self.st.attributes = {
                "isBoolean": bool, 
                "intVal": int}
        eq_(self.l.get_tagged_value("isBoolean"), None)
        self.l.set_tagged_value("isBoolean", False)
        self.st.attributes = {
                "isBoolean": bool, 
                "intVal": int, 
                "floatVal": float}
        eq_(self.l.get_tagged_value("isBoolean"), False)
        eq_(self.l.get_tagged_value("floatVal"), None)
        eq_(self.l.get_tagged_value("intVal"), None)
        self.l.set_tagged_value("floatVal", 1.2)
        eq_(self.l.get_tagged_value("floatVal"), 1.2)

    def testAttributesDeletedOnSubclass(self):
        self.st.attributes = {
                "isBoolean": True, 
                "intVal": 1}
        st2 = CStereotype("S2", attributes = {
                "isBoolean": False}, superclasses = self.st)
        self.a.stereotypes = st2
        self.l.stereotype_instances = st2

        eq_(self.l.get_tagged_value("isBoolean"), False)
        eq_(self.l.get_tagged_value("isBoolean", self.st), True)
        eq_(self.l.get_tagged_value("isBoolean", st2), False)

        st2.attributes = {}

        eq_(self.l.get_tagged_value("isBoolean"), True)
        eq_(self.l.get_tagged_value("intVal"), 1)
        eq_(self.l.get_tagged_value("isBoolean", self.st), True)
        try:
            self.l.get_tagged_value("isBoolean", st2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'isBoolean' unknown for 'S2'")

    def testAttributesDeletedOnSubclassNoDefaults(self):
        self.st.attributes = {
                "isBoolean": bool, 
                "intVal": int}
        st2 = CStereotype("S2", attributes = {
                "isBoolean": bool}, superclasses = self.st)
        self.a.stereotypes = st2
        self.l.stereotype_instances = st2

        eq_(self.l.get_tagged_value("isBoolean"), None)
        eq_(self.l.get_tagged_value("isBoolean", self.st), None)
        eq_(self.l.get_tagged_value("isBoolean", st2), None)

        st2.attributes = {}

        eq_(self.l.get_tagged_value("isBoolean"), None)
        eq_(self.l.get_tagged_value("intVal"), None)
        eq_(self.l.get_tagged_value("isBoolean", self.st), None)
        try:
            self.l.get_tagged_value("isBoolean", st2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'isBoolean' unknown for 'S2'")

    def testWrongStereotypeInTaggedValue(self):
        self.st.attributes = {
                "isBoolean": True}
        st2 = CStereotype("S2", attributes = {
                "isBoolean": True})
        self.a.stereotypes = st2
        self.l.stereotype_instances = st2

        self.l.set_tagged_value("isBoolean", False)

        try:
            self.l.set_tagged_value("isBoolean", False, st2)
        except CException as e: 
            eq_(e.value, "stereotype 'S2' is not a stereotype of element")

        eq_(self.l.get_tagged_value("isBoolean"), False)

        try:
            self.l.get_tagged_value("isBoolean", st2)
        except CException as e: 
            eq_(e.value, "stereotype 'S2' is not a stereotype of element")


    def testAttributeValuesInheritance(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        c = CStereotype("C", superclasses = [t1, t2])
        sc = CStereotype("C", superclasses = c)

        t1.attributes = {"i0" : 0}
        t2.attributes = {"i1" : 1}
        c.attributes = {"i2" : 2}
        sc.attributes = {"i3" : 3}

        self.a.stereotypes = sc
        self.l.stereotype_instances = sc

        for name, value in {"i0" : 0, "i1" : 1, "i2" : 2, "i3" : 3}.items():
            eq_(self.l.get_tagged_value(name), value)

        eq_(self.l.get_tagged_value("i0", t1), 0)
        eq_(self.l.get_tagged_value("i1", t2), 1)
        eq_(self.l.get_tagged_value("i2", c), 2)
        eq_(self.l.get_tagged_value("i3", sc), 3)

        for name, value in {"i0" : 10, "i1" : 11, "i2" : 12, "i3" : 13}.items():
            self.l.set_tagged_value(name, value)

        for name, value in {"i0" : 10, "i1" : 11, "i2" : 12, "i3" : 13}.items():
            eq_(self.l.get_tagged_value(name), value)

        eq_(self.l.get_tagged_value("i0", t1), 10)
        eq_(self.l.get_tagged_value("i1", t2), 11)
        eq_(self.l.get_tagged_value("i2", c), 12)
        eq_(self.l.get_tagged_value("i3", sc), 13)

    def testAttributeValuesInheritanceAfterDeleteSuperclass(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        c = CStereotype("C", superclasses = [t1, t2])
        sc = CStereotype("C", superclasses = c)

        t1.attributes = {"i0" : 0}
        t2.attributes = {"i1" : 1}
        c.attributes = {"i2" : 2}
        sc.attributes = {"i3" : 3}

        self.a.stereotypes = sc
        self.l.stereotype_instances = sc
        
        t2.delete()

        for name, value in {"i0" : 0, "i2" : 2, "i3" : 3}.items():
            eq_(self.l.get_tagged_value(name), value)
        try:
            self.l.get_tagged_value("i1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'i1' unknown")

        eq_(self.l.get_tagged_value("i0", t1), 0)
        try:
            self.l.get_tagged_value("i1", t2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'i1' unknown for ''")
        eq_(self.l.get_tagged_value("i2", c), 2)
        eq_(self.l.get_tagged_value("i3", sc), 3)

        for name, value in {"i0" : 10, "i2" : 12, "i3" : 13}.items():
            self.l.set_tagged_value(name, value)
        try:
            self.l.set_tagged_value("i1", 11)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'i1' unknown")

        for name, value in {"i0" : 10, "i2" : 12, "i3" : 13}.items():
            eq_(self.l.get_tagged_value(name), value)
        try:
            self.l.get_tagged_value("i1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'i1' unknown")

        eq_(self.l.get_tagged_value("i0", t1), 10)
        try:
            self.l.get_tagged_value("i1", t2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'i1' unknown for ''")
        eq_(self.l.get_tagged_value("i2", c), 12)
        eq_(self.l.get_tagged_value("i3", sc), 13)


    def testAttributeValuesSameNameInheritance(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        c = CStereotype("C", superclasses = [t1, t2])
        sc = CStereotype("C", superclasses = c)

        t1.attributes = {"i" : 0}
        t2.attributes = {"i" : 1}
        c.attributes = {"i" : 2}
        sc.attributes = {"i" : 3}

        self.a.stereotypes = t1
        self.l.stereotype_instances = sc
        self.l2.stereotype_instances = c
        self.l3.stereotype_instances = t1

        eq_(self.l.get_tagged_value("i"), 3)
        eq_(self.l2.get_tagged_value("i"), 2)
        eq_(self.l3.get_tagged_value("i"), 0)

        eq_(self.l.get_tagged_value("i", sc), 3)
        eq_(self.l.get_tagged_value("i", c), 2)
        eq_(self.l.get_tagged_value("i", t2), 1)
        eq_(self.l.get_tagged_value("i", t1), 0)
        eq_(self.l2.get_tagged_value("i", c), 2)
        eq_(self.l2.get_tagged_value("i", t2), 1)
        eq_(self.l2.get_tagged_value("i", t1), 0)
        eq_(self.l3.get_tagged_value("i", t1), 0)
        
        self.l.set_tagged_value("i", 10)
        self.l2.set_tagged_value("i", 11)
        self.l3.set_tagged_value("i", 12)

        eq_(self.l.get_tagged_value("i"), 10)
        eq_(self.l2.get_tagged_value("i"), 11)
        eq_(self.l3.get_tagged_value("i"), 12)

        eq_(self.l.get_tagged_value("i", sc), 10)
        eq_(self.l.get_tagged_value("i", c), 2)
        eq_(self.l.get_tagged_value("i", t2), 1)
        eq_(self.l.get_tagged_value("i", t1), 0)
        eq_(self.l2.get_tagged_value("i", c), 11)
        eq_(self.l2.get_tagged_value("i", t2), 1)
        eq_(self.l2.get_tagged_value("i", t1), 0)
        eq_(self.l3.get_tagged_value("i", t1), 12)

        self.l.set_tagged_value("i", 130, sc)
        self.l.set_tagged_value("i", 100, t1)
        self.l.set_tagged_value("i", 110, t2)
        self.l.set_tagged_value("i", 120, c)

        eq_(self.l.get_tagged_value("i"), 130)

        eq_(self.l.get_tagged_value("i", sc), 130)
        eq_(self.l.get_tagged_value("i", c), 120)
        eq_(self.l.get_tagged_value("i", t2), 110)
        eq_(self.l.get_tagged_value("i", t1), 100)


    def testTaggedValuesInheritanceMultipleStereotypes(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        sta = CStereotype("STA", superclasses = [t1, t2])
        suba = CStereotype("SubA", superclasses = [sta])
        stb = CStereotype("STB", superclasses = [t1, t2])
        subb = CStereotype("SubB", superclasses = [stb])
        stc = CStereotype("STC")
        subc = CStereotype("SubC", superclasses = [stc])

        self.a.stereotypes = [t1, stc]
        self.l.stereotype_instances = [suba, subb, subc]

        t1.attributes = {"i0" : 0} 
        t2.attributes = {"i1" : 1}
        sta.attributes = {"i2" : 2}
        suba.attributes = {"i3" : 3}
        stb.attributes = {"i4" : 4}
        subb.attributes = {"i5" : 5}
        stc.attributes = {"i6" : 6}
        subc.attributes = {"i7" : 7}

        eq_(self.l.get_tagged_value("i0"), 0)
        eq_(self.l.get_tagged_value("i1"), 1)
        eq_(self.l.get_tagged_value("i2"), 2)
        eq_(self.l.get_tagged_value("i3"), 3)
        eq_(self.l.get_tagged_value("i4"), 4)
        eq_(self.l.get_tagged_value("i5"), 5)
        eq_(self.l.get_tagged_value("i6"), 6)
        eq_(self.l.get_tagged_value("i7"), 7)

        eq_(self.l.get_tagged_value("i0", t1), 0)
        eq_(self.l.get_tagged_value("i1", t2), 1)
        eq_(self.l.get_tagged_value("i2", sta), 2)
        eq_(self.l.get_tagged_value("i3", suba), 3)
        eq_(self.l.get_tagged_value("i4", stb), 4)
        eq_(self.l.get_tagged_value("i5", subb), 5)
        eq_(self.l.get_tagged_value("i6", stc), 6)
        eq_(self.l.get_tagged_value("i7", subc), 7)

        self.l.set_tagged_value("i0", 10)
        self.l.set_tagged_value("i1", 11)
        self.l.set_tagged_value("i2", 12)
        self.l.set_tagged_value("i3", 13)
        self.l.set_tagged_value("i4", 14)
        self.l.set_tagged_value("i5", 15)
        self.l.set_tagged_value("i6", 16)
        self.l.set_tagged_value("i7", 17)

        eq_(self.l.get_tagged_value("i0"), 10)
        eq_(self.l.get_tagged_value("i1"), 11)
        eq_(self.l.get_tagged_value("i2"), 12)
        eq_(self.l.get_tagged_value("i3"), 13)
        eq_(self.l.get_tagged_value("i4"), 14)
        eq_(self.l.get_tagged_value("i5"), 15)
        eq_(self.l.get_tagged_value("i6"), 16)
        eq_(self.l.get_tagged_value("i7"), 17)

        self.l.set_tagged_value("i0", 210, t1)
        self.l.set_tagged_value("i1", 211, t2)
        self.l.set_tagged_value("i2", 212, sta)
        self.l.set_tagged_value("i3", 213, suba)
        self.l.set_tagged_value("i4", 214, stb)
        self.l.set_tagged_value("i5", 215, subb)
        self.l.set_tagged_value("i6", 216, stc)
        self.l.set_tagged_value("i7", 217, subc)

        eq_(self.l.get_tagged_value("i0"), 210)
        eq_(self.l.get_tagged_value("i1"), 211)
        eq_(self.l.get_tagged_value("i2"), 212)
        eq_(self.l.get_tagged_value("i3"), 213)
        eq_(self.l.get_tagged_value("i4"), 214)
        eq_(self.l.get_tagged_value("i5"), 215)
        eq_(self.l.get_tagged_value("i6"), 216)
        eq_(self.l.get_tagged_value("i7"), 217)


    def testTaggedValuesNonPosArgument_ObjectAddLinks(self):
        s = CStereotype("S", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"]})
        self.a.stereotypes = s

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")

        links = c1.add_links([c2, c3], stereotype_instances = s, tagged_values = {
            "isBoolean": True, "intVal": 1, "floatVal": 1.1, "string": "abc", "list": ["a", "b"]
        })
        link = links[0]

        eq_(link.stereotype_instances, [s])
        eq_(link.get_tagged_value("isBoolean"), True)
        eq_(link.get_tagged_value("intVal"), 1)
        eq_(link.get_tagged_value("floatVal"), 1.1)
        eq_(link.get_tagged_value("string"), "abc")
        eq_(link.get_tagged_value("list"), ["a", "b"])

    def testTaggedValuesNonPosArgument_AddLinksFunction(self):
        s = CStereotype("S", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"]})
        self.a.stereotypes = s

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")

        links = add_links({c1: [c2, c3]}, stereotype_instances = s, tagged_values = {
            "isBoolean": True, "intVal": 1, "floatVal": 1.1, "string": "abc", "list": ["a", "b"]
        })
        link = links[0]

        eq_(link.stereotype_instances, [s])
        eq_(link.get_tagged_value("isBoolean"), True)
        eq_(link.get_tagged_value("intVal"), 1)
        eq_(link.get_tagged_value("floatVal"), 1.1)
        eq_(link.get_tagged_value("string"), "abc")
        eq_(link.get_tagged_value("list"), ["a", "b"])

    def testDeleteTaggedValues(self):
        s = CStereotype("S", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"]})
        self.a.stereotypes = s
        self.l.stereotype_instances = s
        self.l.delete_tagged_value("isBoolean")
        self.l.delete_tagged_value("intVal")
        valueOfList = self.l.delete_tagged_value("list")
        eq_(self.l.tagged_values, {'floatVal': 1.1, 'string': 'abc'})
        eq_(valueOfList, ['a', 'b'])

    def testDeleteTaggedValuesWithSuperclass(self):
        sst = CStereotype("SST", attributes = {
                "intVal": 20, "intVal2": 30})
        st = CStereotype("ST", superclasses = sst, attributes = {
                "isBoolean": True, 
                "intVal": 1})
        self.a.stereotypes = st
        self.l.stereotype_instances = st

        self.l.delete_tagged_value("isBoolean")
        self.l.delete_tagged_value("intVal2")
        eq_(self.l.tagged_values, {"intVal": 1})

        self.l.set_tagged_value("intVal", 2, sst)
        self.l.set_tagged_value("intVal", 3, st)
        eq_(self.l.tagged_values, {"intVal": 3})
        self.l.delete_tagged_value("intVal")
        eq_(self.l.tagged_values, {"intVal": 2})

        self.l.set_tagged_value("intVal", 2, sst)
        self.l.set_tagged_value("intVal", 3, st)
        self.l.delete_tagged_value("intVal", st)
        eq_(self.l.tagged_values, {"intVal": 2})

        self.l.set_tagged_value("intVal", 2, sst)
        self.l.set_tagged_value("intVal", 3, st)
        self.l.delete_tagged_value("intVal", sst)
        eq_(self.l.tagged_values, {"intVal": 3})

    def testDeleteTaggedValuesExceptionalCases(self):
        s = CStereotype("S", attributes = {"b": True})
        self.a.stereotypes = s
        self.l.stereotype_instances = s
        self.l2.delete()

        try:
            self.l2.get_tagged_value("b")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't get tagged value 'b' on deleted link")

        try:
            self.l2.set_tagged_value("b", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't set tagged value 'b' on deleted link")

        try:
            self.l2.delete_tagged_value("b")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value,"can't delete tagged value 'b' on deleted link")

        try:
            self.l2.tagged_values = {"b": 1}
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't set tagged values on deleted link")

        try:
            self.l2.tagged_values
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't get tagged values on deleted link")

        self.l.stereotype_instances = s
        try:
            self.l.delete_tagged_value("x")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'x' unknown")

if __name__ == "__main__":
    nose.main()