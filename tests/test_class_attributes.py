import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized
import re

from codeableModels import CMetaclass, CClass, CObject, CAttribute, CException, CEnum

class TestClassAttributes():    
    def setUp(self):
        self.mcl = CMetaclass("MCL")
        self.cl = CClass(self.mcl, "CL")

    def testPrimitiveEmptyInput(self):
        cl = CClass(self.mcl, "C", attributes = {})
        eq_(len(cl.attributes), 0)
        eq_(len(cl.attributeNames), 0)

    def testPrimitiveNoneInput(self):
        cl = CClass(self.mcl, "C", attributes = None)
        eq_(len(cl.attributes), 0)
        eq_(len(cl.attributeNames), 0)

    def testPrimitiveTypeAttributes(self):
        cl = CClass(self.mcl, "C", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc",
                "list": ["a", "b"]})
        eq_(len(cl.attributes), 5)
        eq_(len(cl.attributeNames), 5)

        ok_(set(["isBoolean", "intVal", "floatVal", "string", "list"]).issubset(cl.attributeNames))

        a1 = cl.getAttribute("isBoolean")
        a2 = cl.getAttribute("intVal") 
        a3 = cl.getAttribute("floatVal")
        a4 = cl.getAttribute("string")
        a5 = cl.getAttribute("list")
        ok_(set([a1, a2, a3, a4, a5]).issubset(cl.attributes))
        eq_(None, cl.getAttribute("X"))

        eq_(a1.type, bool)
        eq_(a2.type, int)
        eq_(a3.type, float)
        eq_(a4.type, str)
        eq_(a5.type, list)

        d1 = a1.default
        d2 = a2.default
        d3 = a3.default
        d4 = a4.default
        d5 = a5.default

        ok_(isinstance(d1, bool))
        ok_(isinstance(d2, int))
        ok_(isinstance(d3, float))
        ok_(isinstance(d4, str))
        ok_(isinstance(d5, list))

        eq_(d1, True)
        eq_(d2, 1)
        eq_(d3, 1.1)
        eq_(d4, "abc")
        eq_(d5, ["a", "b"])

    def testAttributeGetNameAndClassifier(self):
        cl = CClass(self.mcl, "C", attributes = {"isBoolean": True})
        a = cl.getAttribute("isBoolean")
        eq_(a.name, "isBoolean")
        eq_(a.classifier, cl)
        cl.delete()
        eq_(a.name, None)
        eq_(a.classifier, None)

    def testPrimitiveAttributesNoDefault(self):
        self.cl.attributes = {"a": bool, "b": int, "c": str, "d": float, "e": list}
        a1 = self.cl.getAttribute("a")
        a2 = self.cl.getAttribute("b") 
        a3 = self.cl.getAttribute("c")
        a4 = self.cl.getAttribute("d")
        a5 = self.cl.getAttribute("e")
        ok_(set([a1, a2, a3, a4, a5]).issubset(self.cl.attributes))
        eq_(a1.default, None)
        eq_(a1.type, bool)
        eq_(a2.default, None)
        eq_(a2.type, int)
        eq_(a3.default, None)
        eq_(a3.type, str)
        eq_(a4.default, None)
        eq_(a4.type, float)
        eq_(a5.default, None)
        eq_(a5.type, list)

    def testGetAttributeNotFound(self):
        eq_(self.cl.getAttribute("x"), None)
        self.cl.attributes = {"a": bool, "b": int, "c": str, "d": float}
        eq_(self.cl.getAttribute("x"), None)

    def testTypeAndDefaultOnAttribute(self):
        CAttribute(default = "", type = str)
        CAttribute(type = str, default = "")
        try:
            CAttribute(default = 1, type = str)
            exceptionExpected_()
        except CException as e: 
            eq_("default value '1' incompatible with attribute's type '<class 'str'>'", e.value)
        try:
            CAttribute(type = str, default = 1)
            exceptionExpected_()
        except CException as e: 
            eq_("default value '1' incompatible with attribute's type '<class 'str'>'", e.value)
        a5 = CAttribute(type = int)
        eq_(a5.default, None)

    def testSameNamedArgumentsCAttributes(self):
        a1 = CAttribute(default = "")
        a2 = CAttribute(type = str)
        n1 = "a"
        self.cl.attributes = {n1: a1, "a": a2}
        eq_(set(self.cl.attributes), {a2})
        eq_(self.cl.attributeNames, ["a"])
        
    def testSameNamedArgumentsDefaults(self):
        n1 = "a"
        self.cl.attributes = {n1: "", "a": 1}
        ok_(len(self.cl.attributes), 1)
        eq_(self.cl.getAttribute("a").default, 1)
        eq_(self.cl.attributeNames, ["a"])

    def testObjectTypeAttribute(self):
        attrType = CClass(self.mcl, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        self.cl.attributes = {"attrTypeObj" : attrValue}
        objAttr = self.cl.getAttribute("attrTypeObj")
        attributes = self.cl.attributes
        eq_(set(attributes), {objAttr})

        boolAttr = CAttribute(default = True)
        self.cl.attributes = {"attrTypeObj" : objAttr, "isBoolean" : boolAttr}
        attributes = self.cl.attributes
        eq_(set(attributes), {objAttr, boolAttr})
        eq_(self.cl.attributeNames, ["attrTypeObj", "isBoolean"])
        objAttr = self.cl.getAttribute("attrTypeObj")
        eq_(objAttr.type, attrType)
        default = objAttr.default
        ok_(isinstance(default, CObject))
        eq_(default, attrValue)

        self.cl.attributes = {"attrTypeObj" : attrValue, "isBoolean" : boolAttr}
        eq_(self.cl.attributeNames, ["attrTypeObj", "isBoolean"])
        # using the CObject in attributes causes a new CAttribute to be created != objAttr
        neq_(self.cl.getAttribute("attrTypeObj"), objAttr)
    
    def testClassTypeAttribute(self):
        attrType = CMetaclass("AttrType")
        attrValue = CClass(attrType, "attrValue")
        self.cl.attributes = {"attrTypeCl" : attrType}
        clAttr = self.cl.getAttribute("attrTypeCl")
        clAttr.default = attrValue
        attributes = self.cl.attributes
        eq_(set(attributes), {clAttr})

        boolAttr = CAttribute(default = True)
        self.cl.attributes = {"attrTypeCl" : clAttr, "isBoolean" : boolAttr}
        attributes = self.cl.attributes
        eq_(set(attributes), {clAttr, boolAttr})
        eq_(self.cl.attributeNames, ["attrTypeCl", "isBoolean"])
        clAttr = self.cl.getAttribute("attrTypeCl")
        eq_(clAttr.type, attrType)
        default = clAttr.default
        ok_(isinstance(default, CClass))
        eq_(default, attrValue)

        self.cl.attributes = {"attrTypeCl" : attrValue, "isBoolean" : boolAttr}
        eq_(self.cl.attributeNames, ["attrTypeCl", "isBoolean"])
        # using the CClass in attributes causes a new CAttribute to be created != clAttr
        neq_(self.cl.getAttribute("attrTypeCl"), clAttr)

    def testEnumGetValues(self):
        enumValues = ["A", "B", "C"]
        enumObj = CEnum("ABCEnum", values = enumValues)
        eq_(["A", "B", "C"], enumObj.values)
        ok_("A" in enumObj.values)
        ok_(not("X" in enumObj.values))
        enumValues = [1, 2, 3]
        enumObj = CEnum("123Enum", values = enumValues)
        eq_([1,2,3], enumObj.values)

    def testEnumEmpty(self):
        enumObj = CEnum("ABCEnum", values = [])
        eq_(enumObj.values, [])
        enumObj = CEnum("ABCEnum", values = None)
        eq_(enumObj.values, [])

    def testEnumNoList(self):
        enumValues = {"A", "B", "C"}
        try:
            CEnum("ABCEnum", values = enumValues)
            exceptionExpected_()
        except CException as e:
            ok_(re.match("^an enum needs to be initialized with a list of values, but got:([ {}'CAB,]+)$", e.value))

    def testEnumName(self):
        enumValues = ["A", "B", "C"]
        enumObj = CEnum("ABCEnum", values = enumValues)
        eq_("ABCEnum", enumObj.name)

    def testDefineEnumTypeAttribute(self):
        enumValues = ["A", "B", "C"]
        enumObj = CEnum("ABCEnum", values = enumValues)
        CAttribute(type = enumObj, default = "A")
        CAttribute(default = "A", type = enumObj)
        try:
            CAttribute(type = enumObj, default = "X")
            exceptionExpected_()
        except CException as e: 
            eq_("default value 'X' incompatible with attribute's type 'ABCEnum'", e.value)
        try:
            CAttribute(default = "X", type = enumObj)        
            exceptionExpected_()
        except CException as e: 
            eq_("default value 'X' incompatible with attribute's type 'ABCEnum'", e.value)

    def testUseEnumTypeAttribute(self):
        enumValues = ["A", "B", "C"]
        enumObj = CEnum("ABCEnum", values = enumValues)
        ea1 = CAttribute(type = enumObj, default = "A")
        ea2 = CAttribute(type = enumObj)
        self.cl.attributes = {"letters1": ea1, "letters2": ea2}
        eq_(set(self.cl.attributes), {ea1, ea2})
        ok_(isinstance(ea1.type, CEnum))

        self.cl.attributes = {"letters1": ea1, "isBool": True, "letters2": ea2}
        boolAttr = self.cl.getAttribute("isBool")
        l1 = self.cl.getAttribute("letters1")
        eq_(set(self.cl.attributes), {l1, ea2, boolAttr})
        eq_(l1.default, "A")
        eq_(ea2.default, None)

    def testUnknownAttributeType(self):
        try:
            self.cl.attributes = {"x": CEnum, "b" : bool}
            exceptionExpected_()
        except CException as e: 
            ok_(re.match("^(unknown attribute type: '<class ).*(CEnum'>')$", e.value))

    def testSetAttributeDefaultValue(self):
        enumObj = CEnum("ABCEnum", values = ["A", "B", "C"])
        self.cl.attributes = {"letters": enumObj, "b" : bool}
        l = self.cl.getAttribute("letters")
        b = self.cl.getAttribute("b")
        eq_(l.default, None)
        eq_(b.default, None)
        l.default = "B"
        b.default = False
        eq_(l.default, "B")
        eq_(b.default, False)
        eq_(l.type, enumObj)
        eq_(b.type, bool)
    
    def testCClassVsCObject(self):
        cl_a = CClass(self.mcl, "A")
        cl_b = CClass(self.mcl, "B")
        obj_b = CObject(cl_b, "obj_b")

        self.cl.attributes = {"a": cl_a, "b": obj_b}
        a = self.cl.getAttribute("a")
        b = self.cl.getAttribute("b")
        eq_(a.type, cl_a)
        eq_(a.default, None)
        eq_(b.type, cl_b)
        eq_(b.default, obj_b)

    testMetaclass = CMetaclass("A")
    testEnum = CEnum("AEnum", values = [1,2])
    testClass = CClass(testMetaclass, "CL")

    @parameterized.expand([
        (bool, testMetaclass),
        (bool, 1.1), 
        (int, testMetaclass),
        (int, "abc"),
        (float, "1"),
        (float, testMetaclass),
        (str, 1),
        (str, testMetaclass),
        (testEnum, "1"),
        (testEnum, testMetaclass),
        (testClass, "1"),
        (testClass, testMetaclass)])
    def testAttributeTypeCheck(self, type, wrongDefault):
        self.cl.attributes = {"a": type}
        attr = self.cl.getAttribute("a")
        try:
            attr.default = wrongDefault
            exceptionExpected_()
        except CException as e: 
            eq_(f"default value '{wrongDefault!s}' incompatible with attribute's type '{type!s}'", e.value)

    def test_DeleteAttributes(self):
        self.cl.attributes = {
            "isBoolean": True, 
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc"}
        eq_(len(set(self.cl.attributes)), 4)
        self.cl.attributes = {}
        eq_(set(self.cl.attributes), set())
        self.cl.attributes = {
            "isBoolean": True, 
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc"}
        eq_(len(set(self.cl.attributes)), 4)
        self.cl.attributes = {}
        eq_(set(self.cl.attributes), set())

    def testTypeObjectAttributeClassIsDeletedInConstructor(self):
        attrCl = CClass(self.mcl, "AC")
        attrCl.delete()
        try:
            CClass(self.mcl, "C", attributes = {"ac": attrCl})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testTypeObjectAttributeClassIsDeletedInTypeMethod(self):
        attrCl = CClass(self.mcl, "AC")
        attrCl.delete()
        try:
            a = CAttribute()
            a.type = attrCl
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testSetCAttributeMethodToNone(self):
        # setting the type/default to their default value (None) should work
        a = CAttribute()
        a.type = None
        a.default = None
        eq_(a.type, None)
        eq_(a.default, None)

    def testTypeObjectAttributeClassIsNone(self):
        c = CClass(self.mcl, "C", attributes = {"ac": None})
        ac = c.getAttribute("ac")
        eq_(ac.default, None)
        eq_(ac.type, None)

    def testDefaultObjectAttributeIsDeletedInConstructor(self):
        attrCl = CClass(self.mcl, "AC")
        defaultObj = CObject(attrCl)
        defaultObj.delete()
        try:
            CClass(self.mcl, "C", attributes = {"ac": defaultObj})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testDefaultObjectAttributeIsDeletedInDefaultMethod(self):
        attrCl = CClass(self.mcl, "AC")
        defaultObj = CObject(attrCl)
        defaultObj.delete()
        try:
            a = CAttribute()
            a.default = defaultObj
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")


if __name__ == "__main__":
    nose.main()




