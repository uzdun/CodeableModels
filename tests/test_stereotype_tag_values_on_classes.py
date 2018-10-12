import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CStereotype, CClass, CObject, CAttribute, CException, CEnum

class TestStereotypeTagValuesOnClasses():
    def setUp(self):
        self.mcl = CMetaclass("MCL")
        self.st = CStereotype("ST")
        self.mcl.stereotypes = self.st
        self.cl = CClass(self.mcl, "C", stereotypeInstances = self.st)

    def testTaggedValuesOnPrimitiveTypeAttributes(self):
        s = CStereotype("S", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"]})
        self.mcl.stereotypes = s
        cl = CClass(self.mcl, "C", stereotypeInstances = s)

        eq_(cl.getTaggedValue("isBoolean"), True)
        eq_(cl.getTaggedValue("intVal"), 1)
        eq_(cl.getTaggedValue("floatVal"), 1.1)
        eq_(cl.getTaggedValue("string"), "abc")
        eq_(cl.getTaggedValue("list"), ["a", "b"])

        cl.setTaggedValue("isBoolean", False)
        cl.setTaggedValue("intVal", 2)
        cl.setTaggedValue("floatVal", 2.1)
        cl.setTaggedValue("string", "y")

        eq_(cl.getTaggedValue("isBoolean"), False)
        eq_(cl.getTaggedValue("intVal"), 2)
        eq_(cl.getTaggedValue("floatVal"), 2.1)
        eq_(cl.getTaggedValue("string"), "y")

        cl.setTaggedValue("list", [])
        eq_(cl.getTaggedValue("list"), [])
        cl.setTaggedValue("list", [1, 2, 3])
        eq_(cl.getTaggedValue("list"), [1, 2, 3])

    def testAttributeOfTaggedValueUnknown(self):
        try:
            self.cl.getTaggedValue("x")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'x' unknown")

        self.mcl.attributes =  {"isBoolean": True, "intVal": 1}
        try:
            self.cl.setTaggedValue("x", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'x' unknown")

    def testIntegersAsFloatTaggedValues(self):
        self.st.attributes = {"floatVal": float}
        self.cl.setTaggedValue("floatVal", 15)
        eq_(self.cl.getTaggedValue("floatVal"), 15)

    def testObjectTypeAttributeTaggedValues(self):
        attrType = CClass(self.mcl, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        self.st.attributes = {"attrTypeObj" : attrValue}
        objAttr = self.st.getAttribute("attrTypeObj")
        eq_(objAttr.type, attrType)
        eq_(self.cl.getTaggedValue("attrTypeObj"), attrValue)

        nonAttrValue = CObject(CClass(self.mcl), "nonAttrValue")
        try:
            self.cl.setTaggedValue("attrTypeObj", nonAttrValue)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "type of object 'nonAttrValue' is not matching type of attribute 'attrTypeObj'")

    def testAddObjectAttributeGetSetTaggedValue(self):
        attrType = CClass(self.mcl, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        self.st.attributes = {
            "attrTypeObj1" : attrType, "attrTypeObj2" : attrValue
        }
        eq_(self.cl.getTaggedValue("attrTypeObj1"), None)
        eq_(self.cl.getTaggedValue("attrTypeObj2"), attrValue)

    def testObjectAttributeTaggedValueOfSuperclassType(self):
        attrSuperType = CClass(self.mcl, "AttrSuperType") 
        attrType = CClass(self.mcl, "AttrType", superclasses = attrSuperType)
        attrValue = CObject(attrType, "attrValue")
        self.st.attributes = {
            "attrTypeObj1" : attrSuperType, "attrTypeObj2" : attrValue
        }
        self.cl.setTaggedValue("attrTypeObj1", attrValue)
        self.cl.setTaggedValue("attrTypeObj2", attrValue)
        eq_(self.cl.getTaggedValue("attrTypeObj1"), attrValue)
        eq_(self.cl.getTaggedValue("attrTypeObj2"), attrValue)

    def testTaggedValuesOnAttributesWithNoDefaultValues(self):
        attrType = CClass(self.mcl, "AttrType")
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        st = CStereotype("S", attributes = {
                "b": bool, 
                "i": int,
                "f": float,
                "s": str,
                "l": list,
                "C": attrType,
                "e": enumType})
        mcl = CMetaclass("M", stereotypes = st)
        cl = CClass(mcl, "C", stereotypeInstances = st)
        for n in ["b", "i", "f", "s", "l", "C", "e"]:
            eq_(cl.getTaggedValue(n), None)

    def testTaggedValuesDefinedInConstructor(self):
        objValType = CClass(CMetaclass())
        objVal = CObject(objValType, "objVal")

        st = CStereotype("S", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"],
                "obj": objValType})
        mcl = CMetaclass("M", stereotypes = st)
        cl = CClass(mcl, "C", stereotypeInstances = st, taggedValues = {
            "isBoolean": False, "intVal": 2, "floatVal": 2.1, 
            "string": "y", "list": [], "obj": objVal})

        eq_(cl.getTaggedValue("isBoolean"), False)
        eq_(cl.getTaggedValue("intVal"), 2)
        eq_(cl.getTaggedValue("floatVal"), 2.1)
        eq_(cl.getTaggedValue("string"), "y")
        eq_(cl.getTaggedValue("list"), [])
        eq_(cl.getTaggedValue("obj"), objVal)

        eq_(cl.taggedValues, {"isBoolean": False, "intVal": 2, "floatVal": 2.1, 
            "string": "y", "list": [], "obj": objVal})

    def testTaggedValuesSetterOverwrite(self):
        st = CStereotype("S", attributes = {
                "isBoolean": True, 
                "intVal": 1})
        mcl = CMetaclass("M", stereotypes = st)
        cl = CClass(mcl, "C", stereotypeInstances = st, taggedValues = {
            "isBoolean": False, "intVal": 2})
        cl.taggedValues = {"isBoolean": True, "intVal": 20}
        eq_(cl.getTaggedValue("isBoolean"), True)
        eq_(cl.getTaggedValue("intVal"), 20)
        eq_(cl.taggedValues, {'isBoolean': True, 'intVal': 20})
        cl.taggedValues = {}
        # tagged values should not delete existing values
        eq_(cl.taggedValues, {"isBoolean": True, "intVal": 20})

    def testTaggedValuesSetterWithSuperclass(self):
        sst = CStereotype("SST", attributes = {
                "intVal": 20, "intVal2": 30})
        st = CStereotype("S", superclasses = sst, attributes = {
                "isBoolean": True, 
                "intVal": 1})
        mcl = CMetaclass("M", stereotypes = st)
        cl = CClass(mcl, "C", stereotypeInstances = st, taggedValues = {
            "isBoolean": False})
        eq_(cl.taggedValues, {"isBoolean": False, "intVal": 1, "intVal2": 30})
        cl.setTaggedValue("intVal", 12, sst)
        cl.setTaggedValue("intVal", 15, st)
        cl.setTaggedValue("intVal2", 16, sst)
        eq_(cl.taggedValues, {"isBoolean": False, "intVal": 15, "intVal2": 16})
        eq_(cl.getTaggedValue("intVal", sst), 12)
        eq_(cl.getTaggedValue("intVal", st), 15)

    def testTaggedValuesSetterMalformedDescription(self):
        st = CStereotype("S", attributes = {
                "isBoolean": True, 
                "intVal": 1})
        mcl = CMetaclass("M", stereotypes = st)
        cl = CClass(mcl, "C", stereotypeInstances = st)
        try:
            cl.taggedValues = [1, 2, 3]
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "malformed tagged values description: '[1, 2, 3]'")

    def testEnumTypeAttributeValues(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        self.st.attributes = {
                "e1": enumType,
                "e2": enumType}
        e2 = self.st.getAttribute("e2")
        e2.default = "A"
        eq_(self.cl.getTaggedValue("e1"), None)
        eq_(self.cl.getTaggedValue("e2"), "A")
        self.cl.setTaggedValue("e1", "B")
        self.cl.setTaggedValue("e2", "C")
        eq_(self.cl.getTaggedValue("e1"), "B")
        eq_(self.cl.getTaggedValue("e2"), "C")
        try:
            self.cl.setTaggedValue("e1", "X")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "value 'X' is not element of enumeration")

    def testDefaultInitAfterInstanceCreation(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        self.st.attributes = {
                "e1": enumType,
                "e2": enumType}
        e2 = self.st.getAttribute("e2")
        e2.default = "A"
        eq_(self.cl.getTaggedValue("e1"), None)
        eq_(self.cl.getTaggedValue("e2"), "A")

    def testAttributeValueTypeCheckBool1(self):
        self.st.attributes = {"t": bool}
        cl = CClass(self.mcl, "C", stereotypeInstances = self.st)
        try:
            cl.setTaggedValue("t", self.mcl)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value for attribute 't' is not a known attribute type", e.value)

    def testAttributeValueTypeCheckBool2(self):
        self.st.attributes = {"t": bool}
        cl = CClass(self.mcl, "C", stereotypeInstances = self.st)
        try:
            cl.setTaggedValue("t", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckInt(self):
        self.st.attributes = {"t": int}
        cl = CClass(self.mcl, "C", stereotypeInstances = self.st)
        try:
            cl.setTaggedValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckFloat(self):
        self.st.attributes = {"t": float}
        cl = CClass(self.mcl, "C", stereotypeInstances = self.st)
        try:
            cl.setTaggedValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckStr(self):
        self.st.attributes = {"t": str}
        cl = CClass(self.mcl, "C", stereotypeInstances = self.st)
        try:
            cl.setTaggedValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckList(self):
        self.st.attributes = {"t": list}
        cl = CClass(self.mcl, "C", stereotypeInstances = self.st)
        try:
            cl.setTaggedValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckObject(self):
        attrType = CMetaclass("AttrType")
        self.st.attributes = {"t": attrType}
        cl = CClass(self.mcl, "C", stereotypeInstances = self.st)
        try:
            cl.setTaggedValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeValueTypeCheckEnum(self):
        enumType = CEnum("EnumT", values = ["A", "B", "C"]) 
        self.st.attributes = {"t": enumType}
        cl = CClass(self.mcl, "C", stereotypeInstances = self.st)
        try:
            cl.setTaggedValue("t", True)
            exceptionExpected_()
        except CException as e: 
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def testAttributeDeleted(self):
        self.st.attributes = {
                "isBoolean": True, 
                "intVal": 15}
        cl = CClass(self.mcl, "C", stereotypeInstances = self.st)
        eq_(cl.getTaggedValue("intVal"), 15)
        self.st.attributes = {
                "isBoolean": False}
        eq_(cl.getTaggedValue("isBoolean"), True)
        try:
            cl.getTaggedValue("intVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'intVal' unknown") 
        try:
            cl.setTaggedValue("intVal", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'intVal' unknown") 

    def testAttributeDeletedNoDefault(self):
        self.st.attributes = {
                "isBoolean": bool, 
                "intVal": int}
        self.st.attributes = {"isBoolean": bool}
        eq_(self.cl.getTaggedValue("isBoolean"), None)
        try:
            self.cl.getTaggedValue("intVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'intVal' unknown")    
        try:
            self.cl.setTaggedValue("intVal", 1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'intVal' unknown") 

    def testAttributesOverwrite(self):
        self.st.attributes = {
                "isBoolean": True, 
                "intVal": 15}
        cl = CClass(self.mcl, "C", stereotypeInstances = self.st)
        eq_(cl.getTaggedValue("intVal"), 15)
        try:
            cl.getTaggedValue("floatVal")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'floatVal' unknown")        
        cl.setTaggedValue("intVal", 18)
        self.st.attributes = {
                "isBoolean": False, 
                "intVal": 19, 
                "floatVal": 25.1}
        eq_(cl.getTaggedValue("isBoolean"), True)
        eq_(cl.getTaggedValue("floatVal"), 25.1)
        eq_(cl.getTaggedValue("intVal"), 18)
        cl.setTaggedValue("floatVal", 1.2)
        eq_(cl.getTaggedValue("floatVal"), 1.2)

    def testAttributesOverwriteNoDefaults(self):
        self.st.attributes = {
                "isBoolean": bool, 
                "intVal": int}
        eq_(self.cl.getTaggedValue("isBoolean"), None)   
        self.cl.setTaggedValue("isBoolean", False)
        self.st.attributes = {
                "isBoolean": bool, 
                "intVal": int, 
                "floatVal": float}
        eq_(self.cl.getTaggedValue("isBoolean"), False)
        eq_(self.cl.getTaggedValue("floatVal"), None)
        eq_(self.cl.getTaggedValue("intVal"), None)
        self.cl.setTaggedValue("floatVal", 1.2)
        eq_(self.cl.getTaggedValue("floatVal"), 1.2)

    def testAttributesDeletedOnSubclass(self):
        self.st.attributes = {
                "isBoolean": True, 
                "intVal": 1}
        st2 = CStereotype("S2", attributes = {
                "isBoolean": False}, superclasses = self.st)
        mcl = CMetaclass("M", stereotypes = st2)
        cl = CClass(mcl, "C", stereotypeInstances = st2)

        eq_(cl.getTaggedValue("isBoolean"), False)
        eq_(cl.getTaggedValue("isBoolean", self.st), True)   
        eq_(cl.getTaggedValue("isBoolean", st2), False)   

        st2.attributes = {}

        eq_(cl.getTaggedValue("isBoolean"), True)
        eq_(cl.getTaggedValue("intVal"), 1)
        eq_(cl.getTaggedValue("isBoolean", self.st), True)
        try:
            cl.getTaggedValue("isBoolean", st2) 
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'isBoolean' unknown for stereotype 'S2'")

    def testAttributesDeletedOnSubclassNoDefaults(self):
        self.st.attributes = {
                "isBoolean": bool, 
                "intVal": int}
        st2 = CStereotype("S2", attributes = {
                "isBoolean": bool}, superclasses = self.st)
        mcl = CMetaclass("M", stereotypes = st2)
        cl = CClass(mcl, "C", stereotypeInstances = st2)

        eq_(cl.getTaggedValue("isBoolean"), None)
        eq_(cl.getTaggedValue("isBoolean", self.st), None)   
        eq_(cl.getTaggedValue("isBoolean", st2), None)   

        st2.attributes = {}

        eq_(cl.getTaggedValue("isBoolean"), None)
        eq_(cl.getTaggedValue("intVal"), None)
        eq_(cl.getTaggedValue("isBoolean", self.st), None)
        try:
            cl.getTaggedValue("isBoolean", st2) 
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'isBoolean' unknown for stereotype 'S2'")


    def testWrongStereotypeInTaggedValue(self):
        self.st.attributes = {
                "isBoolean": True}
        st2 = CStereotype("S2", attributes = {
                "isBoolean": True})
        mcl = CMetaclass("M", stereotypes = self.st)
        cl = CClass(mcl, "C", stereotypeInstances = self.st)

        cl.setTaggedValue("isBoolean", False)

        try:
            cl.setTaggedValue("isBoolean", False, st2)
        except CException as e: 
            eq_(e.value, "stereotype 'S2' is not a stereotype of element")

        eq_(cl.getTaggedValue("isBoolean"), False)

        try:
            cl.getTaggedValue("isBoolean", st2)
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

        mcl = CMetaclass("M", stereotypes = sc)
        cl = CClass(mcl, "C", stereotypeInstances = sc)

        for name, value in {"i0" : 0, "i1" : 1, "i2" : 2, "i3" : 3}.items():
            eq_(cl.getTaggedValue(name), value)

        eq_(cl.getTaggedValue("i0", t1), 0)
        eq_(cl.getTaggedValue("i1", t2), 1)
        eq_(cl.getTaggedValue("i2", c), 2)
        eq_(cl.getTaggedValue("i3", sc), 3)

        for name, value in {"i0" : 10, "i1" : 11, "i2" : 12, "i3" : 13}.items():
            cl.setTaggedValue(name, value)

        for name, value in {"i0" : 10, "i1" : 11, "i2" : 12, "i3" : 13}.items():
            eq_(cl.getTaggedValue(name), value)

        eq_(cl.getTaggedValue("i0", t1), 10)
        eq_(cl.getTaggedValue("i1", t2), 11)
        eq_(cl.getTaggedValue("i2", c), 12)
        eq_(cl.getTaggedValue("i3", sc), 13)

    def testAttributeValuesInheritanceAfterDeleteSuperclass(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        c = CStereotype("C", superclasses = [t1, t2])
        sc = CStereotype("C", superclasses = c)

        t1.attributes = {"i0" : 0}
        t2.attributes = {"i1" : 1}
        c.attributes = {"i2" : 2}
        sc.attributes = {"i3" : 3}

        mcl = CMetaclass("M", stereotypes = sc)
        cl = CClass(mcl, "C", stereotypeInstances = sc)

        t2.delete()

        for name, value in {"i0" : 0, "i2" : 2, "i3" : 3}.items():
            eq_(cl.getTaggedValue(name), value)
        try:
            cl.getTaggedValue("i1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'i1' unknown")

        eq_(cl.getTaggedValue("i0", t1), 0)
        try:
            cl.getTaggedValue("i1", t2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype '' is not a stereotype of element")
        eq_(cl.getTaggedValue("i2", c), 2)
        eq_(cl.getTaggedValue("i3", sc), 3)

        for name, value in {"i0" : 10, "i2" : 12, "i3" : 13}.items():
            cl.setTaggedValue(name, value)
        try:
            cl.setTaggedValue("i1", 11)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'i1' unknown")

        for name, value in {"i0" : 10, "i2" : 12, "i3" : 13}.items():
            eq_(cl.getTaggedValue(name), value)
        try:
            cl.getTaggedValue("i1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "tagged value 'i1' unknown")

        eq_(cl.getTaggedValue("i0", t1), 10)
        try:
            cl.getTaggedValue("i1", t2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "stereotype '' is not a stereotype of element")
        eq_(cl.getTaggedValue("i2", c), 12)
        eq_(cl.getTaggedValue("i3", sc), 13)


    def testAttributeValuesSameNameInheritance(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        c = CStereotype("C", superclasses = [t1, t2])
        sc = CStereotype("C", superclasses = c)

        t1.attributes = {"i" : 0}
        t2.attributes = {"i" : 1}
        c.attributes = {"i" : 2}
        sc.attributes = {"i" : 3}

        mcl = CMetaclass("M", stereotypes = t1)
        cl1 = CClass(mcl, "C", stereotypeInstances = sc)
        cl2 = CClass(mcl, "C", stereotypeInstances = c)
        cl3 = CClass(mcl, "C", stereotypeInstances = t1)

        eq_(cl1.getTaggedValue("i"), 3) 
        eq_(cl2.getTaggedValue("i"), 2) 
        eq_(cl3.getTaggedValue("i"), 0)

        eq_(cl1.getTaggedValue("i", sc), 3) 
        eq_(cl1.getTaggedValue("i", c), 2)
        eq_(cl1.getTaggedValue("i", t2), 1)
        eq_(cl1.getTaggedValue("i", t1), 0)
        eq_(cl2.getTaggedValue("i", c), 2)
        eq_(cl2.getTaggedValue("i", t2), 1)
        eq_(cl2.getTaggedValue("i", t1), 0)
        eq_(cl3.getTaggedValue("i", t1), 0)
        
        cl1.setTaggedValue("i", 10)
        cl2.setTaggedValue("i", 11)
        cl3.setTaggedValue("i", 12)

        eq_(cl1.getTaggedValue("i"), 10) 
        eq_(cl2.getTaggedValue("i"), 11) 
        eq_(cl3.getTaggedValue("i"), 12)

        eq_(cl1.getTaggedValue("i", sc), 10) 
        eq_(cl1.getTaggedValue("i", c), 2)
        eq_(cl1.getTaggedValue("i", t2), 1)
        eq_(cl1.getTaggedValue("i", t1), 0)
        eq_(cl2.getTaggedValue("i", c), 11)
        eq_(cl2.getTaggedValue("i", t2), 1)
        eq_(cl2.getTaggedValue("i", t1), 0)
        eq_(cl3.getTaggedValue("i", t1), 12)

        cl1.setTaggedValue("i", 130, sc)
        cl1.setTaggedValue("i", 100, t1)
        cl1.setTaggedValue("i", 110, t2)
        cl1.setTaggedValue("i", 120, c)   

        eq_(cl1.getTaggedValue("i"), 130) 

        eq_(cl1.getTaggedValue("i", sc), 130) 
        eq_(cl1.getTaggedValue("i", c), 120)
        eq_(cl1.getTaggedValue("i", t2), 110)
        eq_(cl1.getTaggedValue("i", t1), 100)


    def testTaggedValuesInheritanceMultipleStereotypes(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        sta = CStereotype("STA", superclasses = [t1, t2])
        suba = CStereotype("SubA", superclasses = [sta])
        stb = CStereotype("STB", superclasses = [t1, t2])
        subb = CStereotype("SubB", superclasses = [stb])
        stc = CStereotype("STC")
        subc = CStereotype("SubC", superclasses = [stc])

        mcl = CMetaclass("M", stereotypes = [t1, stc])
        cl = CClass(mcl, "C", stereotypeInstances = [suba, subb, subc])

        t1.attributes = {"i0" : 0} 
        t2.attributes = {"i1" : 1}
        sta.attributes = {"i2" : 2}
        suba.attributes = {"i3" : 3}
        stb.attributes = {"i4" : 4}
        subb.attributes = {"i5" : 5}
        stc.attributes = {"i6" : 6}
        subc.attributes = {"i7" : 7}

        eq_(cl.getTaggedValue("i0"), 0)
        eq_(cl.getTaggedValue("i1"), 1)
        eq_(cl.getTaggedValue("i2"), 2)
        eq_(cl.getTaggedValue("i3"), 3)
        eq_(cl.getTaggedValue("i4"), 4)
        eq_(cl.getTaggedValue("i5"), 5)
        eq_(cl.getTaggedValue("i6"), 6)
        eq_(cl.getTaggedValue("i7"), 7)

        eq_(cl.getTaggedValue("i0", t1), 0)
        eq_(cl.getTaggedValue("i1", t2), 1)
        eq_(cl.getTaggedValue("i2", sta), 2)
        eq_(cl.getTaggedValue("i3", suba), 3)
        eq_(cl.getTaggedValue("i4", stb), 4)
        eq_(cl.getTaggedValue("i5", subb), 5)
        eq_(cl.getTaggedValue("i6", stc), 6)
        eq_(cl.getTaggedValue("i7", subc), 7)

        cl.setTaggedValue("i0", 10)
        cl.setTaggedValue("i1", 11)
        cl.setTaggedValue("i2", 12)
        cl.setTaggedValue("i3", 13)
        cl.setTaggedValue("i4", 14)
        cl.setTaggedValue("i5", 15)
        cl.setTaggedValue("i6", 16)
        cl.setTaggedValue("i7", 17)

        eq_(cl.getTaggedValue("i0"), 10)
        eq_(cl.getTaggedValue("i1"), 11)
        eq_(cl.getTaggedValue("i2"), 12)
        eq_(cl.getTaggedValue("i3"), 13)
        eq_(cl.getTaggedValue("i4"), 14)
        eq_(cl.getTaggedValue("i5"), 15)
        eq_(cl.getTaggedValue("i6"), 16)
        eq_(cl.getTaggedValue("i7"), 17)

        cl.setTaggedValue("i0", 210, t1)
        cl.setTaggedValue("i1", 211, t2)
        cl.setTaggedValue("i2", 212, sta)
        cl.setTaggedValue("i3", 213, suba)
        cl.setTaggedValue("i4", 214, stb)
        cl.setTaggedValue("i5", 215, subb)
        cl.setTaggedValue("i6", 216, stc)
        cl.setTaggedValue("i7", 217, subc)

        eq_(cl.getTaggedValue("i0"), 210)
        eq_(cl.getTaggedValue("i1"), 211)
        eq_(cl.getTaggedValue("i2"), 212)
        eq_(cl.getTaggedValue("i3"), 213)
        eq_(cl.getTaggedValue("i4"), 214)
        eq_(cl.getTaggedValue("i5"), 215)
        eq_(cl.getTaggedValue("i6"), 216)
        eq_(cl.getTaggedValue("i7"), 217)

if __name__ == "__main__":
    nose.main()