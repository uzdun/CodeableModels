import sys
sys.path.append("..")

import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

import re

from codeableModels import CMetaclass, CClass, CObject, CAttribute, CException, CEnum


class TestMetaClassAttributes():
    def setUp(self):
        self.mcl = CMetaclass("MCL")

    def testPrimitiveEmptyInput(self):
        cl = CMetaclass("MCL", attributes = {})
        eq_(len(cl.attributes), 0)
        eq_(len(cl.attributeNames), 0)

    def testPrimitiveNoneInput(self):
        cl = CMetaclass("MCL", attributes = None)
        eq_(len(cl.attributes), 0)
        eq_(len(cl.attributeNames), 0)

    def testPrimitiveTypeAttributes(self):
        cl = CMetaclass("MCL", attributes = {
                "isBoolean": True, 
                "intVal": 1,
                "floatVal": 1.1,
                "string": "abc"})
        eq_(len(cl.attributes), 4)
        eq_(len(cl.attributeNames), 4)

        ok_(set(["isBoolean", "intVal", "floatVal", "string"]).issubset(cl.attributeNames))

        a1 = cl.getAttribute("isBoolean")
        a2 = cl.getAttribute("intVal") 
        a3 = cl.getAttribute("floatVal")
        a4 = cl.getAttribute("string")
        ok_(set([a1, a2, a3, a4]).issubset(cl.attributes))
        eq_(None, cl.getAttribute("X"))

        eq_(a1.type, bool)
        eq_(a2.type, int)
        eq_(a3.type, float)
        eq_(a4.type, str)

        d1 = a1.default
        d2 = a2.default
        d3 = a3.default
        d4 = a4.default

        ok_(isinstance(d1, bool))
        ok_(isinstance(d2, int))
        ok_(isinstance(d3, float))
        ok_(isinstance(d4, str))

        eq_(d1, True)
        eq_(d2, 1)
        eq_(d3, 1.1)
        eq_(d4, "abc")

    def testAttributeGetNameAndClassifier(self):
        m = CMetaclass("M", attributes = {"isBoolean": True})
        a = m.getAttribute("isBoolean")
        eq_(a.name, "isBoolean")
        eq_(a.classifier, m)
        m.delete()
        eq_(a.name, None)
        eq_(a.classifier, None)

    def testPrimitiveAttributesNoDefault(self):
        self.mcl.attributes = {"a": bool, "b": int, "c": str, "d": float}
        a1 = self.mcl.getAttribute("a")
        a2 = self.mcl.getAttribute("b") 
        a3 = self.mcl.getAttribute("c")
        a4 = self.mcl.getAttribute("d")
        ok_(set([a1, a2, a3, a4]).issubset(self.mcl.attributes))
        eq_(a1.default, None)
        eq_(a1.type, bool)
        eq_(a2.default, None)
        eq_(a2.type, int)
        eq_(a3.default, None)
        eq_(a3.type, str)
        eq_(a4.default, None)
        eq_(a4.type, float)

    def testGetAttributeNotFound(self):
        eq_(self.mcl.getAttribute("x"), None)
        self.mcl.attributes = {"a": bool, "b": int, "c": str, "d": float}
        eq_(self.mcl.getAttribute("x"), None)

    def testSameNamedArgumentsCAttributes(self):
        a1 = CAttribute(default = "")
        a2 = CAttribute(type = str)
        n1 = "a"
        self.mcl.attributes = {n1: a1, "a": a2}
        eq_(set(self.mcl.attributes), {a2})
        eq_(self.mcl.attributeNames, ["a"])
        
    def testSameNamedArgumentsDefaults(self):
        n1 = "a"
        self.mcl.attributes = {n1: "", "a": 1}
        ok_(len(self.mcl.attributes), 1)
        eq_(self.mcl.getAttribute("a").default, 1)
        eq_(self.mcl.attributeNames, ["a"])

    def testObjectTypeAttribute(self):
        attrType = CClass(self.mcl, "AttrType")
        attrValue = CObject(attrType, "attrValue")
        self.mcl.attributes = {"attrTypeObj" : attrValue}
        objAttr = self.mcl.getAttribute("attrTypeObj")
        attributes = self.mcl.attributes
        eq_(set(attributes), {objAttr})

        boolAttr = CAttribute(default = True)
        self.mcl.attributes = {"attrTypeObj" : objAttr, "isBoolean" : boolAttr}
        attributes = self.mcl.attributes
        eq_(set(attributes), {objAttr, boolAttr})
        eq_(self.mcl.attributeNames, ["attrTypeObj", "isBoolean"])
        objAttr = self.mcl.getAttribute("attrTypeObj")
        eq_(objAttr.type, attrType)
        default = objAttr.default
        ok_(isinstance(default, CObject))
        eq_(default, attrValue)

        self.mcl.attributes = {"attrTypeObj" : attrValue, "isBoolean" : boolAttr}
        eq_(self.mcl.attributeNames, ["attrTypeObj", "isBoolean"])
        # using the CObject in attributes causes a new CAttribute to be created != objAttr
        neq_(self.mcl.getAttribute("attrTypeObj"), objAttr)
    
    def testUseEnumTypeAttribute(self):
        enumValues = ["A", "B", "C"]
        enumObj = CEnum("ABCEnum", values = enumValues)
        ea1 = CAttribute(type = enumObj, default = "A")
        ea2 = CAttribute(type = enumObj)
        self.mcl.attributes = {"letters1": ea1, "letters2": ea2}
        eq_(set(self.mcl.attributes), {ea1, ea2})
        ok_(isinstance(ea1.type, CEnum))

        self.mcl.attributes = {"letters1": ea1, "isBool": True, "letters2": ea2}
        boolAttr = self.mcl.getAttribute("isBool")
        l1 = self.mcl.getAttribute("letters1")
        eq_(set(self.mcl.attributes), {l1, ea2, boolAttr})
        eq_(l1.default, "A")
        eq_(ea2.default, None)

    def testUnknownAttributeType(self):
        try:
            self.mcl.attributes = {"x": CEnum, "b" : bool}
            exceptionExpected_()
        except CException as e: 
            ok_(re.match("^(unknown attribute type: '<class ).*(CEnum'>')$", e.value))


    def testSetAttributeDefaultValue(self):
        enumObj = CEnum("ABCEnum", values = ["A", "B", "C"])
        self.mcl.attributes = {"letters": enumObj, "b" : bool}
        l = self.mcl.getAttribute("letters")
        b = self.mcl.getAttribute("b")
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

        self.mcl.attributes = {"a": cl_a, "b": obj_b}
        a = self.mcl.getAttribute("a")
        b = self.mcl.getAttribute("b")
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
        self.mcl.attributes = {"a": type}
        attr = self.mcl.getAttribute("a")
        try:
            attr.default = wrongDefault
            exceptionExpected_()
        except CException as e: 
            eq_(f"default value '{wrongDefault!s}' incompatible with attribute's type '{type!s}'", e.value)

    def test_DeleteAttributes(self):
        self.mcl.attributes = {
            "isBoolean": True, 
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc"}
        eq_(len(set(self.mcl.attributes)), 4)
        self.mcl.attributes = {}
        eq_(set(self.mcl.attributes), set())
        self.mcl.attributes = {
            "isBoolean": True, 
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc"}
        eq_(len(set(self.mcl.attributes)), 4)
        self.mcl.attributes = {}
        eq_(set(self.mcl.attributes), set())

    def testTypeObjectAttributeClassIsDeletedInConstructor(self):
        attrCl = CClass(self.mcl, "AC")
        attrCl.delete()
        try:
            CMetaclass("M", attributes = {"ac": attrCl})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testTypeObjectAttributeClassIsNone(self):
        m = CMetaclass("M", attributes = {"ac": None})
        ac = m.getAttribute("ac")
        eq_(ac.default, None)
        eq_(ac.type, None)

    def testDefaultObjectAttributeIsDeletedInConstructor(self):
        attrCl = CClass(self.mcl, "AC")
        defaultObj = CObject(attrCl)
        defaultObj.delete()
        try:
            CMetaclass("M", attributes = {"ac": defaultObj})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

if __name__ == "__main__":
    nose.main()


