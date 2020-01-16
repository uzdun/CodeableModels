import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeable_models import CMetaclass, CClass, CObject, CAttribute, CException, CEnum

class TestClassAttributeValues():
    def setUp(self):
        self.mcl = CMetaclass("MCL")

    def testValuesOnPrimitiveTypeAttributes(self):
        mcl = CMetaclass("M", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"]})
        cl = CClass(mcl, "C")

        eq_(cl.get_value("isBoolean"), True)
        eq_(cl.get_value("intVal"), 1)
        eq_(cl.get_value("floatVal"), 1.1)
        eq_(cl.get_value("string"), "abc")
        eq_(cl.get_value("list"), ["a", "b"])

        cl.set_value("isBoolean", False)
        cl.set_value("intVal", 2)
        cl.set_value("floatVal", 2.1)
        cl.set_value("string", "y")

        eq_(cl.get_value("isBoolean"), False)
        eq_(cl.get_value("intVal"), 2)
        eq_(cl.get_value("floatVal"), 2.1)
        eq_(cl.get_value("string"), "y")

        cl.set_value("list", [])
        eq_(cl.get_value("list"), [])
        cl.set_value("list", [1, 2, 3])
        eq_(cl.get_value("list"), [1, 2, 3])

    def testAttributeOfValueUnknown(self):
        cl = CClass(self.mcl, "C")
        try:
            cl.get_value("x")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'x' unknown for 'C'")

        self.mcl.attributes =  {"isBoolean": True, "intVal": 1}
        try:
            cl.set_value("x", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'x' unknown for 'C'")

    def testIntegersAsFloats(self):
        mcl = CMetaclass("C", attributes = {
                "floatVal": float})
        cl = CClass(mcl, "C")
        cl.set_value("floatVal", 15)
        eq_(cl.get_value("floatVal"), 15)

    def testAttributeDefinedAfterInstance(self):
        mcl = CMetaclass("C")
        cl = CClass(mcl, "C")
        mcl.attributes = {"floatVal": float}
        cl.set_value("floatVal", 15)
        eq_(cl.get_value("floatVal"), 15)

    def testObjectTypeAttributeValues(self):
        attrType = CClass(self.mcl, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        self.mcl.attributes = {"attrTypeObj" : attrValue}
        objAttr = self.mcl.get_attribute("attrTypeObj")
        eq_(objAttr.type, attrType)
        cl = CClass(self.mcl, "C")
        eq_(cl.get_value("attrTypeObj"), attrValue)

        nonAttrValue = CObject(CClass(self.mcl), "nonAttrValue")
        try:
            cl.set_value("attrTypeObj", nonAttrValue)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "type of 'nonAttrValue' is not matching type of attribute 'attrTypeObj'")

    def testClassTypeAttributeValues(self):
        attrType = CMetaclass("AttrType")
        attrValue = CClass(attrType, "attrValue")
        self.mcl.attributes = {"attrTypeCl" : attrType}
        clAttr = self.mcl.get_attribute("attrTypeCl")
        clAttr.default = attrValue
        eq_(clAttr.type, attrType)
        cl = CClass(self.mcl, "C")
        eq_(cl.get_value("attrTypeCl"), attrValue)

        nonAttrValue = CClass(CMetaclass("MX"), "nonAttrValue")
        try:
            cl.set_value("attrTypeCl", nonAttrValue)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "type of 'nonAttrValue' is not matching type of attribute 'attrTypeCl'")

    def testAddObjectAttributeGetSetValue(self):
        attrType = CClass(self.mcl, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        cl = CClass(self.mcl)
        self.mcl.attributes = {
            "attrTypeObj1" : attrType, "attrTypeObj2" : attrValue
        }
        eq_(cl.get_value("attrTypeObj1"), None)
        eq_(cl.get_value("attrTypeObj2"), attrValue)

    def testObjectAttributeOfSuperclassType(self):
        attrSuperType = CClass(self.mcl, "AttrSuperType") 
        attrType = CClass(self.mcl, "AttrType", superclasses = attrSuperType)
        attrValue = CObject(attrType, "attrValue")
        cl = CClass(self.mcl)
        self.mcl.attributes = {
            "attrTypeObj1" : attrSuperType, "attrTypeObj2" : attrValue
        }
        cl.set_value("attrTypeObj1", attrValue)
        cl.set_value("attrTypeObj2", attrValue)
        eq_(cl.get_value("attrTypeObj1"), attrValue)
        eq_(cl.get_value("attrTypeObj2"), attrValue)

    def testValuesOnAttributesWithNoDefaultValues(self):
        attrType = CClass(self.mcl, "AttrType")
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        mcl = CMetaclass("M", attributes = {
                "b": bool, 
                "i": int,
                "f": float,
                "s": str,
                "l": list,
                "C": attrType,
                "e": enumType})
        cl = CClass(mcl, "C")
        for n in ["b", "i", "f", "s", "l", "C", "e"]:
            eq_(cl.get_value(n), None)

    def testValuesDefinedInConstructor(self):
        objValType = CClass(CMetaclass())
        objVal = CObject(objValType, "objVal")

        mcl = CMetaclass("M", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"],
                "obj": objValType})
        cl = CClass(mcl, "C", values = {
            "isBoolean": False, "intVal": 2, "floatVal": 2.1, 
            "string": "y", "list": [], "obj": objVal})

        eq_(cl.get_value("isBoolean"), False)
        eq_(cl.get_value("intVal"), 2)
        eq_(cl.get_value("floatVal"), 2.1)
        eq_(cl.get_value("string"), "y")
        eq_(cl.get_value("list"), [])
        eq_(cl.get_value("obj"), objVal)

        eq_(cl.values, {"isBoolean": False, "intVal": 2, "floatVal": 2.1, 
            "string": "y", "list": [], "obj": objVal})

    def testValuesSetterOverwrite(self):
        mcl = CMetaclass("M", attributes = {
                "isBoolean": True, 
                "intVal": 1})
        cl = CClass(mcl, "C", values = {
            "isBoolean": False, "intVal": 2})
        cl.values = {"isBoolean": True, "intVal": 20}
        eq_(cl.get_value("isBoolean"), True)
        eq_(cl.get_value("intVal"), 20)
        eq_(cl.values, {'isBoolean': True, 'intVal': 20})
        cl.values = {}
        # values should not delete existing values
        eq_(cl.values, {"isBoolean": True, "intVal": 20})

    def testValuesSetterWithSuperclass(self):
        smcl = CMetaclass("SMCL", attributes = {
                "intVal": 20, "intVal2": 30})
        mcl = CMetaclass("M", superclasses = smcl, attributes = {
                "isBoolean": True, 
                "intVal": 1})
        cl = CClass(mcl, "C", values = {
            "isBoolean": False})
        eq_(cl.values, {"isBoolean": False, "intVal": 1, "intVal2": 30})
        cl.set_value("intVal", 12, smcl)
        cl.set_value("intVal", 15, mcl)
        cl.set_value("intVal2", 16, smcl)
        eq_(cl.values, {"isBoolean": False, "intVal": 15, "intVal2": 16})
        eq_(cl.get_value("intVal", smcl), 12)
        eq_(cl.get_value("intVal", mcl), 15)

    def testValuesSetterMalformedDescription(self):
        mcl = CMetaclass("M", attributes = {
                "isBoolean": True, 
                "intVal": 1})
        cl = CClass(mcl, "C")
        try:
            cl.values = [1, 2, 3]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "malformed attribute values description: '[1, 2, 3]'")

    def testEnumTypeAttributeValues(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        mcl = CMetaclass(attributes = {
                "e1": enumType,
                "e2": enumType})
        e2 = mcl.get_attribute("e2")
        e2.default = "A"
        cl = CClass(mcl, "C")
        eq_(cl.get_value("e1"), None)
        eq_(cl.get_value("e2"), "A")
        cl.set_value("e1", "B")
        cl.set_value("e2", "C")
        eq_(cl.get_value("e1"), "B")
        eq_(cl.get_value("e2"), "C")
        try:
            cl.set_value("e1", "X")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "value 'X' is not element of enumeration")

    def testDefaultInitAfterInstanceCreation(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        mcl = CMetaclass(attributes = {
                "e1": enumType,
                "e2": enumType})
        cl = CClass(mcl, "C")
        e2 = mcl.get_attribute("e2")
        e2.default = "A"
        eq_(cl.get_value("e1"), None)
        eq_(cl.get_value("e2"), "A")

    def testAttributeValueTypeCheckBool1(self):
        self.mcl.attributes = {"t": bool}
        cl = CClass(self.mcl, "C")
        try:
            cl.set_value("t", self.mcl)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value for attribute 't' is not a known attribute type", e.value)

    def testAttributeValueTypeCheckBool2(self):
        self.mcl.attributes = {"t": bool}
        cl = CClass(self.mcl, "C")
        try:
            cl.set_value("t", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckInt(self):
        self.mcl.attributes = {"t": int}
        cl = CClass(self.mcl, "C")
        try:
            cl.set_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckFloat(self):
        self.mcl.attributes = {"t": float}
        cl = CClass(self.mcl, "C")
        try:
            cl.set_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckStr(self):
        self.mcl.attributes = {"t": str}
        cl = CClass(self.mcl, "C")
        try:
            cl.set_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckList(self):
        self.mcl.attributes = {"t": list}
        cl = CClass(self.mcl, "C")
        try:
            cl.set_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckObject(self):
        attrType = CMetaclass("AttrType")
        self.mcl.attributes = {"t": attrType}
        cl = CClass(self.mcl, "C")
        try:
            cl.set_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckEnum(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        self.mcl.attributes = {"t": enumType}
        cl = CClass(self.mcl, "C")
        try:
            cl.set_value("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeDeleted(self):
        mcl = CMetaclass(attributes = {
                "isBoolean": True, 
                "intVal": 15})
        cl = CClass(mcl, "C")
        eq_(cl.get_value("intVal"), 15)
        mcl.attributes = {
                "isBoolean": False}
        eq_(cl.get_value("isBoolean"), True)
        try:
            cl.get_value("intVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for 'C'") 
        try:
            cl.set_value("intVal", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for 'C'") 

    def testAttributeDeletedNoDefault(self):
        mcl = CMetaclass( attributes = {
                "isBoolean": bool, 
                "intVal": int})
        mcl.attributes = {"isBoolean": bool}
        cl = CClass(mcl, "C")
        eq_(cl.get_value("isBoolean"), None)
        try:
            cl.get_value("intVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for 'C'")    
        try:
            cl.set_value("intVal", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for 'C'") 

    def testAttributesOverwrite(self):
        mcl = CMetaclass(attributes = {
                "isBoolean": True, 
                "intVal": 15})
        cl = CClass(mcl, "C")
        eq_(cl.get_value("intVal"), 15)
        try:
            cl.get_value("floatVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'floatVal' unknown for 'C'")        
        cl.set_value("intVal", 18)
        mcl.attributes = {
                "isBoolean": False, 
                "intVal": 19, 
                "floatVal": 25.1}
        eq_(cl.get_value("isBoolean"), True)
        eq_(cl.get_value("floatVal"), 25.1)
        eq_(cl.get_value("intVal"), 18)
        cl.set_value("floatVal", 1.2)
        eq_(cl.get_value("floatVal"), 1.2)

    def testAttributesOverwriteNoDefaults(self):
        mcl = CMetaclass(attributes = {
                "isBoolean": bool, 
                "intVal": int})
        cl = CClass(mcl, "C")
        eq_(cl.get_value("isBoolean"), None)
        cl.set_value("isBoolean", False)
        mcl.attributes = {
                "isBoolean": bool, 
                "intVal": int, 
                "floatVal": float}
        eq_(cl.get_value("isBoolean"), False)
        eq_(cl.get_value("floatVal"), None)
        eq_(cl.get_value("intVal"), None)
        cl.set_value("floatVal", 1.2)
        eq_(cl.get_value("floatVal"), 1.2)

    def testAttributesDeletedOnSubclass(self):
        mcl = CMetaclass("M", attributes = {
                "isBoolean": True, 
                "intVal": 1})
        mcl2 = CMetaclass("M2", attributes = {
                "isBoolean": False}, superclasses = mcl)

        cl = CClass(mcl2, "C")

        eq_(cl.get_value("isBoolean"), False)
        eq_(cl.get_value("isBoolean", mcl), True)
        eq_(cl.get_value("isBoolean", mcl2), False)

        mcl2.attributes = {}

        eq_(cl.get_value("isBoolean"), True)
        eq_(cl.get_value("intVal"), 1)
        eq_(cl.get_value("isBoolean", mcl), True)
        try:
            cl.get_value("isBoolean", mcl2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'isBoolean' unknown for 'M2'")

    def testAttributesDeletedOnSubclassNoDefaults(self):
        mcl = CMetaclass("M", attributes = {
                "isBoolean": bool, 
                "intVal": int})
        mcl2 = CMetaclass("M2", attributes = {
                "isBoolean": bool}, superclasses = mcl)

        cl = CClass(mcl2, "C")

        eq_(cl.get_value("isBoolean"), None)
        eq_(cl.get_value("isBoolean", mcl), None)
        eq_(cl.get_value("isBoolean", mcl2), None)

        mcl2.attributes = {}

        eq_(cl.get_value("isBoolean"), None)
        eq_(cl.get_value("intVal"), None)
        eq_(cl.get_value("isBoolean", mcl), None)
        try:
            cl.get_value("isBoolean", mcl2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'isBoolean' unknown for 'M2'")


    def testAttributeValuesInheritance(self):
        t1 = CMetaclass("T1")
        t2 = CMetaclass("T2")
        c = CMetaclass("C", superclasses = [t1, t2])
        sc = CMetaclass("C", superclasses = c)

        t1.attributes = {"i0" : 0}
        t2.attributes = {"i1" : 1}
        c.attributes = {"i2" : 2}
        sc.attributes = {"i3" : 3}

        cl = CClass(sc, "C")

        for name, value in {"i0" : 0, "i1" : 1, "i2" : 2, "i3" : 3}.items():
            eq_(cl.get_value(name), value)

        eq_(cl.get_value("i0", t1), 0)
        eq_(cl.get_value("i1", t2), 1)
        eq_(cl.get_value("i2", c), 2)
        eq_(cl.get_value("i3", sc), 3)

        for name, value in {"i0" : 10, "i1" : 11, "i2" : 12, "i3" : 13}.items():
            cl.set_value(name, value)

        for name, value in {"i0" : 10, "i1" : 11, "i2" : 12, "i3" : 13}.items():
            eq_(cl.get_value(name), value)

        eq_(cl.get_value("i0", t1), 10)
        eq_(cl.get_value("i1", t2), 11)
        eq_(cl.get_value("i2", c), 12)
        eq_(cl.get_value("i3", sc), 13)

    def testAttributeValuesInheritanceAfterDeleteSuperclass(self):
        t1 = CMetaclass("T1")
        t2 = CMetaclass("T2")
        c = CMetaclass("C", superclasses = [t1, t2])
        sc = CMetaclass("C", superclasses = c)

        t1.attributes = {"i0" : 0}
        t2.attributes = {"i1" : 1}
        c.attributes = {"i2" : 2}
        sc.attributes = {"i3" : 3}

        cl = CClass(sc, "C")

        t2.delete()

        for name, value in {"i0" : 0, "i2" : 2, "i3" : 3}.items():
            eq_(cl.get_value(name), value)
        try:
            cl.get_value("i1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for 'C'")

        eq_(cl.get_value("i0", t1), 0)
        try:
            cl.get_value("i1", t2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for ''")
        eq_(cl.get_value("i2", c), 2)
        eq_(cl.get_value("i3", sc), 3)

        for name, value in {"i0" : 10, "i2" : 12, "i3" : 13}.items():
            cl.set_value(name, value)
        try:
            cl.set_value("i1", 11)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for 'C'")

        for name, value in {"i0" : 10, "i2" : 12, "i3" : 13}.items():
            eq_(cl.get_value(name), value)
        try:
            cl.get_value("i1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for 'C'")

        eq_(cl.get_value("i0", t1), 10)
        try:
            cl.get_value("i1", t2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for ''")
        eq_(cl.get_value("i2", c), 12)
        eq_(cl.get_value("i3", sc), 13)


    def testAttributeValuesSameNameInheritance(self):
        t1 = CMetaclass("T1")
        t2 = CMetaclass("T2")
        c = CMetaclass("C", superclasses = [t1, t2])
        sc = CMetaclass("C", superclasses = c)

        t1.attributes = {"i" : 0}
        t2.attributes = {"i" : 1}
        c.attributes = {"i" : 2}
        sc.attributes = {"i" : 3}

        cl1 = CClass(sc)
        cl2 = CClass(c)
        cl3 = CClass(t1)

        eq_(cl1.get_value("i"), 3)
        eq_(cl2.get_value("i"), 2)
        eq_(cl3.get_value("i"), 0)

        eq_(cl1.get_value("i", sc), 3)
        eq_(cl1.get_value("i", c), 2)
        eq_(cl1.get_value("i", t2), 1)
        eq_(cl1.get_value("i", t1), 0)
        eq_(cl2.get_value("i", c), 2)
        eq_(cl2.get_value("i", t2), 1)
        eq_(cl2.get_value("i", t1), 0)
        eq_(cl3.get_value("i", t1), 0)
        
        cl1.set_value("i", 10)
        cl2.set_value("i", 11)
        cl3.set_value("i", 12)

        eq_(cl1.get_value("i"), 10)
        eq_(cl2.get_value("i"), 11)
        eq_(cl3.get_value("i"), 12)

        eq_(cl1.get_value("i", sc), 10)
        eq_(cl1.get_value("i", c), 2)
        eq_(cl1.get_value("i", t2), 1)
        eq_(cl1.get_value("i", t1), 0)
        eq_(cl2.get_value("i", c), 11)
        eq_(cl2.get_value("i", t2), 1)
        eq_(cl2.get_value("i", t1), 0)
        eq_(cl3.get_value("i", t1), 12)

        cl1.set_value("i", 130, sc)
        cl1.set_value("i", 100, t1)
        cl1.set_value("i", 110, t2)
        cl1.set_value("i", 120, c)

        eq_(cl1.get_value("i"), 130)

        eq_(cl1.get_value("i", sc), 130)
        eq_(cl1.get_value("i", c), 120)
        eq_(cl1.get_value("i", t2), 110)
        eq_(cl1.get_value("i", t1), 100)


    def testValuesMultipleInheritance(self):
        t1 = CMetaclass("T1")
        t2 = CMetaclass("T2")
        sta = CMetaclass("STA", superclasses = [t1, t2])
        suba = CMetaclass("SubA", superclasses = [sta])
        stb = CMetaclass("STB", superclasses = [t1, t2])
        subb = CMetaclass("SubB", superclasses = [stb])
        stc = CMetaclass("STC")
        subc = CMetaclass("SubC", superclasses = [stc])

        mcl = CMetaclass("M", superclasses = [suba, subb, subc])
        cl = CClass(mcl, "C")

        t1.attributes = {"i0" : 0} 
        t2.attributes = {"i1" : 1}
        sta.attributes = {"i2" : 2}
        suba.attributes = {"i3" : 3}
        stb.attributes = {"i4" : 4}
        subb.attributes = {"i5" : 5}
        stc.attributes = {"i6" : 6}
        subc.attributes = {"i7" : 7}

        eq_(cl.get_value("i0"), 0)
        eq_(cl.get_value("i1"), 1)
        eq_(cl.get_value("i2"), 2)
        eq_(cl.get_value("i3"), 3)
        eq_(cl.get_value("i4"), 4)
        eq_(cl.get_value("i5"), 5)
        eq_(cl.get_value("i6"), 6)
        eq_(cl.get_value("i7"), 7)

        eq_(cl.get_value("i0", t1), 0)
        eq_(cl.get_value("i1", t2), 1)
        eq_(cl.get_value("i2", sta), 2)
        eq_(cl.get_value("i3", suba), 3)
        eq_(cl.get_value("i4", stb), 4)
        eq_(cl.get_value("i5", subb), 5)
        eq_(cl.get_value("i6", stc), 6)
        eq_(cl.get_value("i7", subc), 7)

        cl.set_value("i0", 10)
        cl.set_value("i1", 11)
        cl.set_value("i2", 12)
        cl.set_value("i3", 13)
        cl.set_value("i4", 14)
        cl.set_value("i5", 15)
        cl.set_value("i6", 16)
        cl.set_value("i7", 17)

        eq_(cl.get_value("i0"), 10)
        eq_(cl.get_value("i1"), 11)
        eq_(cl.get_value("i2"), 12)
        eq_(cl.get_value("i3"), 13)
        eq_(cl.get_value("i4"), 14)
        eq_(cl.get_value("i5"), 15)
        eq_(cl.get_value("i6"), 16)
        eq_(cl.get_value("i7"), 17)

    def testDeleteAttributeValues(self):
        mcl = CMetaclass("M", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"]})
        cl = CClass(mcl, "C")
        cl.delete_value("isBoolean")
        cl.delete_value("intVal")
        valueOfList = cl.delete_value("list")
        eq_(cl.values, {'floatVal': 1.1, 'string': 'abc'})
        eq_(valueOfList, ['a', 'b'])

    def testDeleteAttributeValuesWithSuperclass(self):
        smcl = CMetaclass("SCL_M",  attributes = {
                "intVal": 20, "intVal2": 30})
        mcl = CMetaclass("M", superclasses = smcl, attributes = {
                "isBoolean": True, 
                "intVal": 1})
        cl = CClass(mcl, "C", values = {
            "isBoolean": False})
        cl.delete_value("isBoolean")
        cl.delete_value("intVal2")
        eq_(cl.values, {"intVal": 1})

        cl.set_value("intVal", 2, smcl)
        cl.set_value("intVal", 3, mcl)
        eq_(cl.values, {"intVal": 3})
        cl.delete_value("intVal")
        eq_(cl.values, {"intVal": 2})

        cl.set_value("intVal", 2, smcl)
        cl.set_value("intVal", 3, mcl)
        cl.delete_value("intVal", mcl)
        eq_(cl.values, {"intVal": 2})

        cl.set_value("intVal", 2, smcl)
        cl.set_value("intVal", 3, mcl)
        cl.delete_value("intVal", smcl)
        eq_(cl.values, {"intVal": 3})

    def testAttributeValuesExceptionalCases(self):
        mcl = CMetaclass("M", attributes = {"b": True})
        cl1 = CClass(mcl, "C")
        cl1.delete()

        try:
            cl1.get_value("b")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't get value 'b' on deleted class")

        try:
            cl1.set_value("b", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't set value 'b' on deleted class")

        try:
            cl1.delete_value("b")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value,"can't delete value 'b' on deleted class")

        try:
            cl1.values = {"b": 1}                
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't set values on deleted class")

        try:
            cl1.values                
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't get values on deleted class")

        cl = CClass(mcl, "C")
        try:
            cl.delete_value("x")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'x' unknown for 'C'")

if __name__ == "__main__":
    nose.main()