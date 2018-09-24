import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CClass, CObject, CAttribute, CException, CEnum

class TestClassAttributeValues():
    def setUp(self):
        self.mcl = CMetaclass("MCL")

    def testValuesOnPrimitiveTypeAttributes(self):
        mcl = CMetaclass("M", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc"})
        cl = CClass(mcl, "C")

        eq_(cl.getValue("isBoolean"), True)
        eq_(cl.getValue("intVal"), 1)
        eq_(cl.getValue("floatVal"), 1.1)
        eq_(cl.getValue("string"), "abc")

        cl.setValue("isBoolean", False)
        cl.setValue("intVal", 2)
        cl.setValue("floatVal", 2.1)
        cl.setValue("string", "y")

        eq_(cl.getValue("isBoolean"), False)
        eq_(cl.getValue("intVal"), 2)
        eq_(cl.getValue("floatVal"), 2.1)
        eq_(cl.getValue("string"), "y")

    def testAttributeOfValueUnknown(self):
        cl = CClass(self.mcl, "C")
        try:
            cl.getValue("x")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'x' unknown for object 'C'")

        self.mcl.attributes =  {"isBoolean": True, "intVal": 1}
        try:
            cl.setValue("x", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'x' unknown for object 'C'")

    def testIntegersAsFloats(self):
        cl = CMetaclass("C", attributes = {
                "floatVal": float})
        o = CClass(cl, "C")
        o.setValue("floatVal", 15)
        eq_(o.getValue("floatVal"), 15)

    def testAttributeDefinedAfterInstance(self):
        cl = CMetaclass("C")
        o = CClass(cl, "C")
        cl.attributes = {"floatVal": float}
        o.setValue("floatVal", 15)
        eq_(o.getValue("floatVal"), 15)

    def testObjectTypeAttributeValues(self):
        attrType = CClass(self.mcl, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        self.mcl.attributes = {"attrTypeObj" : attrValue}
        objAttr = self.mcl.getAttribute("attrTypeObj")
        eq_(objAttr.type, attrType)
        cl = CClass(self.mcl, "C")
        eq_(cl.getValue("attrTypeObj"), attrValue)

        nonAttrValue = CObject(CClass(self.mcl), "nonAttrValue")
        try:
            cl.setValue("attrTypeObj", nonAttrValue)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "type of object 'nonAttrValue' is not matching type of attribute 'attrTypeObj'")

    def testAddObjectAttributeGetSetValue(self):
        attrType = CClass(self.mcl, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        cl = CClass(self.mcl)
        self.mcl.attributes = {
            "attrTypeObj1" : attrType, "attrTypeObj2" : attrValue
        }
        eq_(cl.getValue("attrTypeObj1"), None)
        eq_(cl.getValue("attrTypeObj2"), attrValue)

    def testObjectAttributeOfSuperclassType(self):
        attrSuperType = CClass(self.mcl, "AttrSuperType") 
        attrType = CClass(self.mcl, "AttrType", superclasses = attrSuperType)
        attrValue = CObject(attrType, "attrValue")
        cl = CClass(self.mcl)
        self.mcl.attributes = {
            "attrTypeObj1" : attrSuperType, "attrTypeObj2" : attrValue
        }
        cl.setValue("attrTypeObj1", attrValue)
        cl.setValue("attrTypeObj2", attrValue)
        eq_(cl.getValue("attrTypeObj1"), attrValue)
        eq_(cl.getValue("attrTypeObj2"), attrValue)

    def testValuesOnAttributesWithNoDefaultValues(self):
        attrType = CClass(self.mcl, "AttrType")
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        mcl = CMetaclass("M", attributes = {
                "b": bool, 
                "i": int,
                "f": float,
                "s": str,
                "C": attrType,
                "e": enumType})
        cl = CClass(mcl, "C")
        for n in ["b", "i", "f", "s", "C", "e"]:
            eq_(cl.getValue(n), None)

    def testEnumTypeAttributeValues(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        mcl = CMetaclass(attributes = {
                "e1": enumType,
                "e2": enumType})
        e2 = mcl.getAttribute("e2")
        e2.default = "A"
        cl = CClass(mcl, "C")
        eq_(cl.getValue("e1"), None)
        eq_(cl.getValue("e2"), "A")
        cl.setValue("e1", "B")
        cl.setValue("e2", "C")
        eq_(cl.getValue("e1"), "B")
        eq_(cl.getValue("e2"), "C")
        try:
            cl.setValue("e1", "X")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "value 'X' is not element of enumeration")

    def testDefaultInitAfterInstanceCreation(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        mcl = CMetaclass(attributes = {
                "e1": enumType,
                "e2": enumType})
        cl = CClass(mcl, "C")
        e2 = mcl.getAttribute("e2")
        e2.default = "A"
        eq_(cl.getValue("e1"), None)
        eq_(cl.getValue("e2"), "A")

    def testAttributeValueTypeCheckBool1(self):
        self.mcl.attributes = {"t": bool}
        cl = CClass(self.mcl, "C")
        try:
            cl.setValue("t", self.mcl)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value for attribute 't' is not a known attribute type", e.value)

    def testAttributeValueTypeCheckBool2(self):
        self.mcl.attributes = {"t": bool}
        cl = CClass(self.mcl, "C")
        try:
            cl.setValue("t", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckInt(self):
        self.mcl.attributes = {"t": int}
        cl = CClass(self.mcl, "C")
        try:
            cl.setValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckFloat(self):
        self.mcl.attributes = {"t": float}
        cl = CClass(self.mcl, "C")
        try:
            cl.setValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckStr(self):
        self.mcl.attributes = {"t": str}
        cl = CClass(self.mcl, "C")
        try:
            cl.setValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckObject(self):
        attrType = CMetaclass("AttrType")
        self.mcl.attributes = {"t": attrType}
        cl = CClass(self.mcl, "C")
        try:
            cl.setValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckEnum(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        self.mcl.attributes = {"t": enumType}
        cl = CClass(self.mcl, "C")
        try:
            cl.setValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeDeleted(self):
        mcl = CMetaclass(attributes = {
                "isBoolean": True, 
                "intVal": 15})
        cl = CClass(mcl, "C")
        eq_(cl.getValue("intVal"), 15)
        mcl.attributes = {
                "isBoolean": False}
        eq_(cl.getValue("isBoolean"), True)
        try:
            cl.getValue("intVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for object 'C'") 
        try:
            cl.setValue("intVal", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for object 'C'") 

    def testAttributeDeletedNoDefault(self):
        mcl = CMetaclass( attributes = {
                "isBoolean": bool, 
                "intVal": int})
        mcl.attributes = {"isBoolean": bool}
        cl = CClass(mcl, "C")
        eq_(cl.getValue("isBoolean"), None)
        try:
            cl.getValue("intVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for object 'C'")    
        try:
            cl.setValue("intVal", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'intVal' unknown for object 'C'") 

    def testAttributesOverwrite(self):
        mcl = CMetaclass(attributes = {
                "isBoolean": True, 
                "intVal": 15})
        cl = CClass(mcl, "C")
        eq_(cl.getValue("intVal"), 15)
        try:
            cl.getValue("floatVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'floatVal' unknown for object 'C'")        
        cl.setValue("intVal", 18)
        mcl.attributes = {
                "isBoolean": False, 
                "intVal": 19, 
                "floatVal": 25.1}
        eq_(cl.getValue("isBoolean"), True)
        eq_(cl.getValue("floatVal"), 25.1)
        eq_(cl.getValue("intVal"), 18)
        cl.setValue("floatVal", 1.2)
        eq_(cl.getValue("floatVal"), 1.2)

    def testAttributesOverwriteNoDefaults(self):
        mcl = CMetaclass(attributes = {
                "isBoolean": bool, 
                "intVal": int})
        cl = CClass(mcl, "C")
        eq_(cl.getValue("isBoolean"), None)   
        cl.setValue("isBoolean", False)
        mcl.attributes = {
                "isBoolean": bool, 
                "intVal": int, 
                "floatVal": float}
        eq_(cl.getValue("isBoolean"), False)
        eq_(cl.getValue("floatVal"), None)
        eq_(cl.getValue("intVal"), None)
        cl.setValue("floatVal", 1.2)
        eq_(cl.getValue("floatVal"), 1.2)

    def testAttributesDeletedOnSubclass(self):
        mcl = CMetaclass("M", attributes = {
                "isBoolean": True, 
                "intVal": 1})
        mcl2 = CMetaclass("M2", attributes = {
                "isBoolean": False}, superclasses = mcl)

        cl = CClass(mcl2, "C")

        eq_(cl.getValue("isBoolean"), False)
        eq_(cl.getValue("isBoolean", mcl), True)   
        eq_(cl.getValue("isBoolean", mcl2), False)   

        mcl2.attributes = {}

        eq_(cl.getValue("isBoolean"), True)
        eq_(cl.getValue("intVal"), 1)
        eq_(cl.getValue("isBoolean", mcl), True)
        try:
            cl.getValue("isBoolean", mcl2) 
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

        eq_(cl.getValue("isBoolean"), None)
        eq_(cl.getValue("isBoolean", mcl), None)   
        eq_(cl.getValue("isBoolean", mcl2), None)   

        mcl2.attributes = {}

        eq_(cl.getValue("isBoolean"), None)
        eq_(cl.getValue("intVal"), None)
        eq_(cl.getValue("isBoolean", mcl), None)
        try:
            cl.getValue("isBoolean", mcl2) 
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
            eq_(cl.getValue(name), value)

        eq_(cl.getValue("i0", t1), 0)
        eq_(cl.getValue("i1", t2), 1)
        eq_(cl.getValue("i2", c), 2)
        eq_(cl.getValue("i3", sc), 3)

        for name, value in {"i0" : 10, "i1" : 11, "i2" : 12, "i3" : 13}.items():
            cl.setValue(name, value)

        for name, value in {"i0" : 10, "i1" : 11, "i2" : 12, "i3" : 13}.items():
            eq_(cl.getValue(name), value)

        eq_(cl.getValue("i0", t1), 10)
        eq_(cl.getValue("i1", t2), 11)
        eq_(cl.getValue("i2", c), 12)
        eq_(cl.getValue("i3", sc), 13)

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
            eq_(cl.getValue(name), value)
        try:
            cl.getValue("i1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for object 'C'")

        eq_(cl.getValue("i0", t1), 0)
        try:
            cl.getValue("i1", t2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for ''")
        eq_(cl.getValue("i2", c), 2)
        eq_(cl.getValue("i3", sc), 3)

        for name, value in {"i0" : 10, "i2" : 12, "i3" : 13}.items():
            cl.setValue(name, value)
        try:
            cl.setValue("i1", 11)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for object 'C'")

        for name, value in {"i0" : 10, "i2" : 12, "i3" : 13}.items():
            eq_(cl.getValue(name), value)
        try:
            cl.getValue("i1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for object 'C'")

        eq_(cl.getValue("i0", t1), 10)
        try:
            cl.getValue("i1", t2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "attribute 'i1' unknown for ''")
        eq_(cl.getValue("i2", c), 12)
        eq_(cl.getValue("i3", sc), 13)


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

        eq_(cl1.getValue("i"), 3) 
        eq_(cl2.getValue("i"), 2) 
        eq_(cl3.getValue("i"), 0)

        eq_(cl1.getValue("i", sc), 3) 
        eq_(cl1.getValue("i", c), 2)
        eq_(cl1.getValue("i", t2), 1)
        eq_(cl1.getValue("i", t1), 0)
        eq_(cl2.getValue("i", c), 2)
        eq_(cl2.getValue("i", t2), 1)
        eq_(cl2.getValue("i", t1), 0)
        eq_(cl3.getValue("i", t1), 0)
        
        cl1.setValue("i", 10)
        cl2.setValue("i", 11)
        cl3.setValue("i", 12)

        eq_(cl1.getValue("i"), 10) 
        eq_(cl2.getValue("i"), 11) 
        eq_(cl3.getValue("i"), 12)

        eq_(cl1.getValue("i", sc), 10) 
        eq_(cl1.getValue("i", c), 2)
        eq_(cl1.getValue("i", t2), 1)
        eq_(cl1.getValue("i", t1), 0)
        eq_(cl2.getValue("i", c), 11)
        eq_(cl2.getValue("i", t2), 1)
        eq_(cl2.getValue("i", t1), 0)
        eq_(cl3.getValue("i", t1), 12)

        cl1.setValue("i", 130, sc)
        cl1.setValue("i", 100, t1)
        cl1.setValue("i", 110, t2)
        cl1.setValue("i", 120, c)   

        eq_(cl1.getValue("i"), 130) 

        eq_(cl1.getValue("i", sc), 130) 
        eq_(cl1.getValue("i", c), 120)
        eq_(cl1.getValue("i", t2), 110)
        eq_(cl1.getValue("i", t1), 100)


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

        eq_(cl.getValue("i0"), 0)
        eq_(cl.getValue("i1"), 1)
        eq_(cl.getValue("i2"), 2)
        eq_(cl.getValue("i3"), 3)
        eq_(cl.getValue("i4"), 4)
        eq_(cl.getValue("i5"), 5)
        eq_(cl.getValue("i6"), 6)
        eq_(cl.getValue("i7"), 7)

        eq_(cl.getValue("i0", t1), 0)
        eq_(cl.getValue("i1", t2), 1)
        eq_(cl.getValue("i2", sta), 2)
        eq_(cl.getValue("i3", suba), 3)
        eq_(cl.getValue("i4", stb), 4)
        eq_(cl.getValue("i5", subb), 5)
        eq_(cl.getValue("i6", stc), 6)
        eq_(cl.getValue("i7", subc), 7)

        cl.setValue("i0", 10)
        cl.setValue("i1", 11)
        cl.setValue("i2", 12)
        cl.setValue("i3", 13)
        cl.setValue("i4", 14)
        cl.setValue("i5", 15)
        cl.setValue("i6", 16)
        cl.setValue("i7", 17)

        eq_(cl.getValue("i0"), 10)
        eq_(cl.getValue("i1"), 11)
        eq_(cl.getValue("i2"), 12)
        eq_(cl.getValue("i3"), 13)
        eq_(cl.getValue("i4"), 14)
        eq_(cl.getValue("i5"), 15)
        eq_(cl.getValue("i6"), 16)
        eq_(cl.getValue("i7"), 17)

if __name__ == "__main__":
    nose.main()