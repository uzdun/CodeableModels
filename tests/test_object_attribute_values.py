import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CClass, CObject, CAttribute, CException, CEnum

class TestObjectAttributeValues():
    def setUp(self):
        self.mcl = CMetaclass("MCL")
        self.cl = CClass(self.mcl, "CL")

    def testValuesOnPrimitiveTypeAttributes(self):
        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"]})
        o = CObject(cl, "o")

        eq_(o.getValue("isBoolean"), True)
        eq_(o.getValue("intVal"), 1)
        eq_(o.getValue("floatVal"), 1.1)
        eq_(o.getValue("string"), "abc")
        eq_(o.getValue("list"), ["a", "b"])

        o.setValue("isBoolean", False)
        o.setValue("intVal", 2)
        o.setValue("floatVal", 2.1)
        o.setValue("string", "y")

        eq_(o.getValue("isBoolean"), False)
        eq_(o.getValue("intVal"), 2)
        eq_(o.getValue("floatVal"), 2.1)
        eq_(o.getValue("string"), "y")

        o.setValue("list", [])
        eq_(o.getValue("list"), [])
        o.setValue("list", [1, 2, 3])
        eq_(o.getValue("list"), [1, 2, 3])

    def testAttributeOfValueUnknown(self):
        o = CObject(self.cl, "o")
        try:
            o.getValue("x")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'x' unknown for 'o'")

        self.cl.attributes =  {"isBoolean": True, "intVal": 1}
        try:
            o.setValue("x", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'x' unknown for 'o'")

    def testIntegersAsFloats(self):
        cl = CClass(self.mcl, "C", attributes = {
                "floatVal": float})
        o = CObject(cl, "o")
        o.setValue("floatVal", 15)
        eq_(o.getValue("floatVal"), 15)

    def testAttributeDefinedAfterInstance(self):
        cl = CClass(self.mcl, "C")
        o = CObject(cl, "o")
        cl.attributes = {"floatVal": float}
        o.setValue("floatVal", 15)
        eq_(o.getValue("floatVal"), 15)

    def testObjectTypeAttributeValues(self):
        attrType = CClass(self.mcl, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        self.cl.attributes = {"attrTypeObj" : attrValue}
        objAttr = self.cl.getAttribute("attrTypeObj")
        eq_(objAttr.type, attrType)
        o = CObject(self.cl, "o")
        eq_(o.getValue("attrTypeObj"), attrValue)

        nonAttrValue = CObject(self.cl, "nonAttrValue")
        try:
            o.setValue("attrTypeObj", nonAttrValue)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "type of 'nonAttrValue' is not matching type of attribute 'attrTypeObj'")

    def testClassTypeAttributeValues(self):
        attrType = CMetaclass("AttrType")
        attrValue = CClass(attrType, "attrValue")
        self.cl.attributes = {"attrTypeCl" : attrType}
        clAttr = self.cl.getAttribute("attrTypeCl")
        clAttr.default = attrValue
        eq_(clAttr.type, attrType)
        o = CObject(self.cl, "o")
        eq_(o.getValue("attrTypeCl"), attrValue)

        nonAttrValue = CClass(CMetaclass("MX"), "nonAttrValue")
        try:
            o.setValue("attrTypeCl", nonAttrValue)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "type of 'nonAttrValue' is not matching type of attribute 'attrTypeCl'")

    def testAddObjectAttributeGetSetValue(self):
        attrType = CClass(self.mcl, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        o1 = CObject(self.cl, "o1")
        self.cl.attributes = {
            "attrTypeObj1" : attrType, "attrTypeObj2" : attrValue
        }
        eq_(o1.getValue("attrTypeObj1"), None)
        eq_(o1.getValue("attrTypeObj2"), attrValue)

    def testObjectAttributeOfSuperclassType(self):
        attrSuperType = CClass(self.mcl, "AttrSuperType") 
        attrType = CClass(self.mcl, "AttrType", superclasses = attrSuperType)
        attrValue = CObject(attrType, "attrValue")
        o = CObject(self.cl, "o1")
        self.cl.attributes = {
            "attrTypeObj1" : attrSuperType, "attrTypeObj2" : attrValue
        }
        o.setValue("attrTypeObj1", attrValue)
        o.setValue("attrTypeObj2", attrValue)
        eq_(o.getValue("attrTypeObj1"), attrValue)
        eq_(o.getValue("attrTypeObj2"), attrValue)

    def testValuesOnAttributesWithNoDefaultValues(self):
        attrType = CClass(self.mcl, "AttrType")   
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        cl = CClass(self.mcl, "C", attributes = {
                "b": bool, 
                "i": int,
                "f": float,
                "s": str,
                "l": list,
                "o": attrType,
                "e": enumType})
        o = CObject(cl, "o")
        for n in ["b", "i", "f", "s", "l", "o", "e"]:
            eq_(o.getValue(n), None)

    def testValuesDefinedInConstructor(self):
        objValType = CClass(CMetaclass())
        objVal = CObject(objValType, "objVal")

        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"],
                "obj": objValType})
        o = CObject(cl, "o", values = {
            "isBoolean": False, "intVal": 2, "floatVal": 2.1, 
            "string": "y", "list": [], "obj": objVal})

        eq_(o.getValue("isBoolean"), False)
        eq_(o.getValue("intVal"), 2)
        eq_(o.getValue("floatVal"), 2.1)
        eq_(o.getValue("string"), "y")
        eq_(o.getValue("list"), [])
        eq_(o.getValue("obj"), objVal)

        eq_(o.values, {"isBoolean": False, "intVal": 2, "floatVal": 2.1, 
            "string": "y", "list": [], "obj": objVal})

    def testValuesSetterOverwrite(self):
        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": True, 
                "intVal": 1})
        o = CObject(cl, "o", values = {
            "isBoolean": False, "intVal": 2})
        o.values = {"isBoolean": True, "intVal": 20}
        eq_(o.getValue("isBoolean"), True)
        eq_(o.getValue("intVal"), 20)
        eq_(o.values, {'isBoolean': True, 'intVal': 20})
        o.values = {}
        # values should not delete existing values
        eq_(o.values, {"isBoolean": True, "intVal": 20})

    def testValuesSetterWithSuperclass(self):
        scl = CClass(self.mcl, "SCL", attributes = {
                "intVal": 20, "intVal2": 30})
        cl = CClass(self.mcl, "C", superclasses = scl, attributes = {
                "isBoolean": True, 
                "intVal": 1})
        o = CObject(cl, "o", values = {
            "isBoolean": False})
        eq_(o.values, {"isBoolean": False, "intVal": 1, "intVal2": 30})
        o.setValue("intVal", 12, scl)
        o.setValue("intVal", 15, cl)
        o.setValue("intVal2", 16, scl)
        eq_(o.values, {"isBoolean": False, "intVal": 15, "intVal2": 16})
        eq_(o.getValue("intVal", scl), 12)
        eq_(o.getValue("intVal", cl), 15)

    def testValuesSetterMalformedDescription(self):
        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": True, 
                "intVal": 1})
        o = CObject(cl, "o")
        try:
            o.values = [1, 2, 3]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "malformed attribute values description: '[1, 2, 3]'")

    def testEnumTypeAttributeValues(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        cl = CClass(self.mcl, "C", attributes = {
                "e1": enumType,
                "e2": enumType})
        e2 = cl.getAttribute("e2")
        e2.default = "A"
        o = CObject(cl, "o")
        eq_(o.getValue("e1"), None)
        eq_(o.getValue("e2"), "A")
        o.setValue("e1", "B")
        o.setValue("e2", "C")
        eq_(o.getValue("e1"), "B")
        eq_(o.getValue("e2"), "C")
        try:
            o.setValue("e1", "X")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "value 'X' is not element of enumeration")

    def testDefaultInitAfterInstanceCreation(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        cl = CClass(self.mcl, "C", attributes = {
                "e1": enumType,
                "e2": enumType})
        o = CObject(cl, "o")
        e2 = cl.getAttribute("e2")
        e2.default = "A"
        eq_(o.getValue("e1"), None)
        eq_(o.getValue("e2"), "A")

    def testAttributeValueTypeCheckBool1(self):
        self.cl.attributes = {"t": bool}
        o = CObject(self.cl, "o")
        try:
            o.setValue("t", self.mcl)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value for attribute 't' is not a known attribute type", e.value)

    def testAttributeValueTypeCheckBool2(self):
        self.cl.attributes = {"t": bool}
        o = CObject(self.cl, "o")
        try:
            o.setValue("t", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckInt(self):
        self.cl.attributes = {"t": int}
        o = CObject(self.cl, "o")
        try:
            o.setValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckFloat(self):
        self.cl.attributes = {"t": float}
        o = CObject(self.cl, "o")
        try:
            o.setValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckStr(self):
        self.cl.attributes = {"t": str}
        o = CObject(self.cl, "o")
        try:
            o.setValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckList(self):
        self.cl.attributes = {"t": list}
        o = CObject(self.cl, "o")
        try:
            o.setValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckObject(self):
        attrType = CClass(self.mcl, "AttrType")
        self.cl.attributes = {"t": attrType}
        o = CObject(self.cl, "o")
        try:
            o.setValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckEnum(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        self.cl.attributes = {"t": enumType}
        o = CObject(self.cl, "o")
        try:
            o.setValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeDeleted(self):
        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": True, 
                "intVal": 15})
        o = CObject(cl, "o")
        eq_(o.getValue("intVal"), 15)
        cl.attributes = {
                "isBoolean": False}
        eq_(o.getValue("isBoolean"), True)
        try:
            o.getValue("intVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for 'o'") 
        try:
            o.setValue("intVal", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for 'o'") 

    def testAttributeDeletedNoDefault(self):
        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": bool, 
                "intVal": int})
        cl.attributes = {"isBoolean": bool}
        o = CObject(cl, "o")
        eq_(o.getValue("isBoolean"), None)
        try:
            o.getValue("intVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for 'o'")    
        try:
            o.setValue("intVal", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for 'o'") 

    def testAttributesOverwrite(self):
        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": True, 
                "intVal": 15})
        o = CObject(cl, "o")
        eq_(o.getValue("intVal"), 15)
        try:
            o.getValue("floatVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'floatVal' unknown for 'o'")        
        o.setValue("intVal", 18)
        cl.attributes = {
                "isBoolean": False, 
                "intVal": 19, 
                "floatVal": 25.1}
        eq_(o.getValue("isBoolean"), True)
        eq_(o.getValue("floatVal"), 25.1)
        eq_(o.getValue("intVal"), 18)
        o.setValue("floatVal", 1.2)
        eq_(o.getValue("floatVal"), 1.2)

    def testAttributesOverwriteNoDefaults(self):
        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": bool, 
                "intVal": int})
        o = CObject(cl, "o")
        eq_(o.getValue("isBoolean"), None)   
        o.setValue("isBoolean", False)
        cl.attributes = {
                "isBoolean": bool, 
                "intVal": int, 
                "floatVal": float}
        eq_(o.getValue("isBoolean"), False)
        eq_(o.getValue("floatVal"), None)
        eq_(o.getValue("intVal"), None)
        o.setValue("floatVal", 1.2)
        eq_(o.getValue("floatVal"), 1.2)

    def testAttributesDeletedOnSubclass(self):
        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": True, 
                "intVal": 1})
        cl2 = CClass(self.mcl, "C2", attributes = {
                "isBoolean": False}, superclasses = cl)

        o = CObject(cl2, "o")

        eq_(o.getValue("isBoolean"), False)
        eq_(o.getValue("isBoolean", cl), True)   
        eq_(o.getValue("isBoolean", cl2), False)   

        cl2.attributes = {}

        eq_(o.getValue("isBoolean"), True)
        eq_(o.getValue("intVal"), 1)
        eq_(o.getValue("isBoolean", cl), True)
        try:
            o.getValue("isBoolean", cl2) 
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'isBoolean' unknown for 'C2'")

    def testAttributesDeletedOnSubclassNoDefaults(self):
        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": bool, 
                "intVal": int})
        cl2 = CClass(self.mcl, "C2", attributes = {
                "isBoolean": bool}, superclasses = cl)

        o = CObject(cl2, "o")

        eq_(o.getValue("isBoolean"), None)
        eq_(o.getValue("isBoolean", cl), None)   
        eq_(o.getValue("isBoolean", cl2), None)   

        cl2.attributes = {}

        eq_(o.getValue("isBoolean"), None)
        eq_(o.getValue("intVal"), None)
        eq_(o.getValue("isBoolean", cl), None)
        try:
            o.getValue("isBoolean", cl2) 
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'isBoolean' unknown for 'C2'")

    def testAttributeValuesInheritance(self):
        t1 = CClass(self.mcl, "T1")
        t2 = CClass(self.mcl, "T2")
        c = CClass(self.mcl, "C", superclasses = [t1, t2])
        sc = CClass(self.mcl, "C", superclasses = c)

        t1.attributes = {"i0" : 0}
        t2.attributes = {"i1" : 1}
        c.attributes = {"i2" : 2}
        sc.attributes = {"i3" : 3}

        o = CObject(sc, "o")

        for name, value in {"i0" : 0, "i1" : 1, "i2" : 2, "i3" : 3}.items():
            eq_(o.getValue(name), value)

        eq_(o.getValue("i0", t1), 0)
        eq_(o.getValue("i1", t2), 1)
        eq_(o.getValue("i2", c), 2)
        eq_(o.getValue("i3", sc), 3)

        for name, value in {"i0" : 10, "i1" : 11, "i2" : 12, "i3" : 13}.items():
            o.setValue(name, value)

        for name, value in {"i0" : 10, "i1" : 11, "i2" : 12, "i3" : 13}.items():
            eq_(o.getValue(name), value)

        eq_(o.getValue("i0", t1), 10)
        eq_(o.getValue("i1", t2), 11)
        eq_(o.getValue("i2", c), 12)
        eq_(o.getValue("i3", sc), 13)

    def testAttributeValuesInheritanceAfterDeleteSuperclass(self):
        t1 = CClass(self.mcl, "T1")
        t2 = CClass(self.mcl, "T2")
        c = CClass(self.mcl, "C", superclasses = [t1, t2])
        sc = CClass(self.mcl, "C", superclasses = c)

        t1.attributes = {"i0" : 0}
        t2.attributes = {"i1" : 1}
        c.attributes = {"i2" : 2}
        sc.attributes = {"i3" : 3}

        o = CObject(sc, "o")

        t2.delete()

        for name, value in {"i0" : 0, "i2" : 2, "i3" : 3}.items():
            eq_(o.getValue(name), value)
        try:
            o.getValue("i1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for 'o'")

        eq_(o.getValue("i0", t1), 0)
        try:
            o.getValue("i1", t2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for ''")
        eq_(o.getValue("i2", c), 2)
        eq_(o.getValue("i3", sc), 3)

        for name, value in {"i0" : 10, "i2" : 12, "i3" : 13}.items():
            o.setValue(name, value)
        try:
            o.setValue("i1", 11)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for 'o'")

        for name, value in {"i0" : 10, "i2" : 12, "i3" : 13}.items():
            eq_(o.getValue(name), value)
        try:
            o.getValue("i1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for 'o'")

        eq_(o.getValue("i0", t1), 10)
        try:
            o.getValue("i1", t2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for ''")
        eq_(o.getValue("i2", c), 12)
        eq_(o.getValue("i3", sc), 13)

    def testAttributeValuesSameNameInheritance(self):
        t1 = CClass(self.mcl, "T1")
        t2 = CClass(self.mcl, "T2")
        c = CClass(self.mcl, "C", superclasses = [t1, t2])
        sc = CClass(self.mcl, "C", superclasses = c)

        t1.attributes = {"i" : 0}
        t2.attributes = {"i" : 1}
        c.attributes = {"i" : 2}
        sc.attributes = {"i" : 3}

        o1 = CObject(sc)
        o2 = CObject(c)
        o3 = CObject(t1)

        eq_(o1.getValue("i"), 3) 
        eq_(o2.getValue("i"), 2) 
        eq_(o3.getValue("i"), 0)

        eq_(o1.getValue("i", sc), 3) 
        eq_(o1.getValue("i", c), 2)
        eq_(o1.getValue("i", t2), 1)
        eq_(o1.getValue("i", t1), 0)
        eq_(o2.getValue("i", c), 2)
        eq_(o2.getValue("i", t2), 1)
        eq_(o2.getValue("i", t1), 0)
        eq_(o3.getValue("i", t1), 0)
        
        o1.setValue("i", 10)
        o2.setValue("i", 11)
        o3.setValue("i", 12)

        eq_(o1.getValue("i"), 10) 
        eq_(o2.getValue("i"), 11) 
        eq_(o3.getValue("i"), 12)

        eq_(o1.getValue("i", sc), 10) 
        eq_(o1.getValue("i", c), 2)
        eq_(o1.getValue("i", t2), 1)
        eq_(o1.getValue("i", t1), 0)
        eq_(o2.getValue("i", c), 11)
        eq_(o2.getValue("i", t2), 1)
        eq_(o2.getValue("i", t1), 0)
        eq_(o3.getValue("i", t1), 12)

        o1.setValue("i", 130, sc)
        o1.setValue("i", 100, t1)
        o1.setValue("i", 110, t2)
        o1.setValue("i", 120, c)   

        eq_(o1.getValue("i"), 130) 

        eq_(o1.getValue("i", sc), 130) 
        eq_(o1.getValue("i", c), 120)
        eq_(o1.getValue("i", t2), 110)
        eq_(o1.getValue("i", t1), 100)

    def testValuesMultipleInheritance(self):
        t1 = CClass(self.mcl, "T1")
        t2 = CClass(self.mcl, "T2")
        sta = CClass(self.mcl, "STA", superclasses = [t1, t2])
        suba = CClass(self.mcl, "SubA", superclasses = [sta])
        stb = CClass(self.mcl, "STB", superclasses = [t1, t2])
        subb = CClass(self.mcl, "SubB", superclasses = [stb])
        stc = CClass(self.mcl, "STC")
        subc = CClass(self.mcl, "SubC", superclasses = [stc])

        cl = CClass(self.mcl, "M", superclasses = [suba, subb, subc])
        o = CObject(cl)

        t1.attributes = {"i0" : 0} 
        t2.attributes = {"i1" : 1}
        sta.attributes = {"i2" : 2}
        suba.attributes = {"i3" : 3}
        stb.attributes = {"i4" : 4}
        subb.attributes = {"i5" : 5}
        stc.attributes = {"i6" : 6}
        subc.attributes = {"i7" : 7}

        eq_(o.getValue("i0"), 0)
        eq_(o.getValue("i1"), 1)
        eq_(o.getValue("i2"), 2)
        eq_(o.getValue("i3"), 3)
        eq_(o.getValue("i4"), 4)
        eq_(o.getValue("i5"), 5)
        eq_(o.getValue("i6"), 6)
        eq_(o.getValue("i7"), 7)

        eq_(o.getValue("i0", t1), 0)
        eq_(o.getValue("i1", t2), 1)
        eq_(o.getValue("i2", sta), 2)
        eq_(o.getValue("i3", suba), 3)
        eq_(o.getValue("i4", stb), 4)
        eq_(o.getValue("i5", subb), 5)
        eq_(o.getValue("i6", stc), 6)
        eq_(o.getValue("i7", subc), 7)

        o.setValue("i0", 10)
        o.setValue("i1", 11)
        o.setValue("i2", 12)
        o.setValue("i3", 13)
        o.setValue("i4", 14)
        o.setValue("i5", 15)
        o.setValue("i6", 16)
        o.setValue("i7", 17)

        eq_(o.getValue("i0"), 10)
        eq_(o.getValue("i1"), 11)
        eq_(o.getValue("i2"), 12)
        eq_(o.getValue("i3"), 13)
        eq_(o.getValue("i4"), 14)
        eq_(o.getValue("i5"), 15)
        eq_(o.getValue("i6"), 16)
        eq_(o.getValue("i7"), 17)

    def testDeleteAttributeValues(self):
        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"]})
        o = CObject(cl, "o")
        o.deleteValue("isBoolean")
        o.deleteValue("intVal")
        valueOfList = o.deleteValue("list")
        eq_(o.values, {'floatVal': 1.1, 'string': 'abc'})
        eq_(valueOfList, ['a', 'b'])

    def testDeleteAttributeValuesWithSuperclass(self):
        scl = CClass(self.mcl, "SCL", attributes = {
                "intVal": 20, "intVal2": 30})
        cl = CClass(self.mcl, "C", superclasses = scl, attributes = {
                "isBoolean": True, 
                "intVal": 1})
        o = CObject(cl, "o", values = {
            "isBoolean": False})
        o.deleteValue("isBoolean")
        o.deleteValue("intVal2")
        eq_(o.values, {"intVal": 1})

        o.setValue("intVal", 2, scl)
        o.setValue("intVal", 3, cl)
        eq_(o.values, {"intVal": 3})
        o.deleteValue("intVal")
        eq_(o.values, {"intVal": 2})

        o.setValue("intVal", 2, scl)
        o.setValue("intVal", 3, cl)
        o.deleteValue("intVal", cl)
        eq_(o.values, {"intVal": 2})

        o.setValue("intVal", 2, scl)
        o.setValue("intVal", 3, cl)
        o.deleteValue("intVal", scl)
        eq_(o.values, {"intVal": 3})

    def testAttributeValuesExceptionalCases(self):
        cl = CClass(self.mcl, "C", attributes = {"b": True})
        o1 = CObject(cl, "o")
        o1.delete()

        try:
            o1.getValue("b")                
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't get value 'b' on deleted object")

        try:
            o1.setValue("b", 1)                
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't set value 'b' on deleted object")

        try:
            o1.deleteValue("b")                
            exceptionExpected_()
        except CException as e: 
            eq_(e.value,"can't delete value 'b' on deleted object")

        try:
            o1.values = {"b": 1}                
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't set values on deleted object")

        try:
            o1.values                
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "can't get values on deleted object")

        o = CObject(cl, "o")
        try:
            o.deleteValue("x")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'x' unknown for 'o'")

if __name__ == "__main__":
    nose.main()