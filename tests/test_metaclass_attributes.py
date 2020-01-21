import re

import nose
from nose.tools import ok_, eq_
from parameterized import parameterized

from codeable_models import CMetaclass, CClass, CObject, CAttribute, CException, CEnum
from tests.testing_commons import neq_, exception_expected_


class TestMetaClassAttributes:
    def setup(self):
        self.mcl = CMetaclass("MCL")

    def test_primitive_empty_input(self):
        cl = CMetaclass("MCL", attributes={})
        eq_(len(cl.attributes), 0)
        eq_(len(cl.attribute_names), 0)

    def test_primitive_none_input(self):
        cl = CMetaclass("MCL", attributes=None)
        eq_(len(cl.attributes), 0)
        eq_(len(cl.attribute_names), 0)

    def test_primitive_type_attributes(self):
        cl = CMetaclass("MCL", attributes={
            "isBoolean": True,
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc",
            "list": ["a", "b"]})
        eq_(len(cl.attributes), 5)
        eq_(len(cl.attribute_names), 5)

        ok_({"isBoolean", "intVal", "floatVal", "string", "list"}.issubset(cl.attribute_names))

        a1 = cl.get_attribute("isBoolean")
        a2 = cl.get_attribute("intVal")
        a3 = cl.get_attribute("floatVal")
        a4 = cl.get_attribute("string")
        a5 = cl.get_attribute("list")
        ok_({a1, a2, a3, a4}.issubset(cl.attributes))
        eq_(None, cl.get_attribute("X"))

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

    def test_attribute_get_name_and_classifier(self):
        m = CMetaclass("M", attributes={"isBoolean": True})
        a = m.get_attribute("isBoolean")
        eq_(a.name, "isBoolean")
        eq_(a.classifier, m)
        m.delete()
        eq_(a.name, None)
        eq_(a.classifier, None)

    def test_primitive_attributes_no_default(self):
        self.mcl.attributes = {"a": bool, "b": int, "c": str, "d": float, "e": list}
        a1 = self.mcl.get_attribute("a")
        a2 = self.mcl.get_attribute("b")
        a3 = self.mcl.get_attribute("c")
        a4 = self.mcl.get_attribute("d")
        a5 = self.mcl.get_attribute("e")
        ok_({a1, a2, a3, a4, a5}.issubset(self.mcl.attributes))
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

    def test_get_attribute_not_found(self):
        eq_(self.mcl.get_attribute("x"), None)
        self.mcl.attributes = {"a": bool, "b": int, "c": str, "d": float}
        eq_(self.mcl.get_attribute("x"), None)

    def test_same_named_arguments_c_attributes(self):
        a1 = CAttribute(default="")
        a2 = CAttribute(type=str)
        n1 = "a"
        self.mcl.attributes = {n1: a1, "a": a2}
        eq_(set(self.mcl.attributes), {a2})
        eq_(self.mcl.attribute_names, ["a"])

    def test_same_named_arguments_defaults(self):
        n1 = "a"
        self.mcl.attributes = {n1: "", "a": 1}
        ok_(len(self.mcl.attributes), 1)
        eq_(self.mcl.get_attribute("a").default, 1)
        eq_(self.mcl.attribute_names, ["a"])

    def test_object_type_attribute(self):
        attribute_type = CClass(self.mcl, "AttrType")
        attribute_value = CObject(attribute_type, "attribute_value")
        self.mcl.attributes = {"attrTypeObj": attribute_value}
        object_attribute = self.mcl.get_attribute("attrTypeObj")
        attributes = self.mcl.attributes
        eq_(set(attributes), {object_attribute})

        bool_attr = CAttribute(default=True)
        self.mcl.attributes = {"attrTypeObj": object_attribute, "isBoolean": bool_attr}
        attributes = self.mcl.attributes
        eq_(set(attributes), {object_attribute, bool_attr})
        eq_(self.mcl.attribute_names, ["attrTypeObj", "isBoolean"])
        object_attribute = self.mcl.get_attribute("attrTypeObj")
        eq_(object_attribute.type, attribute_type)
        default = object_attribute.default
        ok_(isinstance(default, CObject))
        eq_(default, attribute_value)

        self.mcl.attributes = {"attrTypeObj": attribute_value, "isBoolean": bool_attr}
        eq_(self.mcl.attribute_names, ["attrTypeObj", "isBoolean"])
        # using the CObject in attributes causes a new CAttribute to be created != object_attribute
        neq_(self.mcl.get_attribute("attrTypeObj"), object_attribute)

    def test_class_type_attribute(self):
        attribute_type = CMetaclass("AttrType")
        attribute_value = CClass(attribute_type, "attribute_value")
        self.mcl.attributes = {"attrTypeCl": attribute_type}
        class_attribute = self.mcl.get_attribute("attrTypeCl")
        class_attribute.default = attribute_value
        attributes = self.mcl.attributes
        eq_(set(attributes), {class_attribute})

        bool_attr = CAttribute(default=True)
        self.mcl.attributes = {"attrTypeCl": class_attribute, "isBoolean": bool_attr}
        attributes = self.mcl.attributes
        eq_(set(attributes), {class_attribute, bool_attr})
        eq_(self.mcl.attribute_names, ["attrTypeCl", "isBoolean"])
        class_attribute = self.mcl.get_attribute("attrTypeCl")
        eq_(class_attribute.type, attribute_type)
        default = class_attribute.default
        ok_(isinstance(default, CClass))
        eq_(default, attribute_value)

        self.mcl.attributes = {"attrTypeCl": attribute_value, "isBoolean": bool_attr}
        eq_(self.mcl.attribute_names, ["attrTypeCl", "isBoolean"])
        # using the CClass in attributes causes a new CAttribute to be created != class_attribute
        neq_(self.mcl.get_attribute("attrTypeCl"), class_attribute)

    def test_use_enum_type_attribute(self):
        enum_values = ["A", "B", "C"]
        enum_obj = CEnum("ABCEnum", values=enum_values)
        ea1 = CAttribute(type=enum_obj, default="A")
        ea2 = CAttribute(type=enum_obj)
        self.mcl.attributes = {"letters1": ea1, "letters2": ea2}
        eq_(set(self.mcl.attributes), {ea1, ea2})
        ok_(isinstance(ea1.type, CEnum))

        self.mcl.attributes = {"letters1": ea1, "isBool": True, "letters2": ea2}
        bool_attr = self.mcl.get_attribute("isBool")
        l1 = self.mcl.get_attribute("letters1")
        eq_(set(self.mcl.attributes), {l1, ea2, bool_attr})
        eq_(l1.default, "A")
        eq_(ea2.default, None)

    def test_unknown_attribute_type(self):
        try:
            self.mcl.attributes = {"x": CEnum, "b": bool}
            exception_expected_()
        except CException as e:
            ok_(re.match("^(unknown attribute type: '<class ).*(CEnum'>')$", e.value))

    def test_set_attribute_default_value(self):
        enum_obj = CEnum("ABCEnum", values=["A", "B", "C"])
        self.mcl.attributes = {"letters": enum_obj, "b": bool}
        letters = self.mcl.get_attribute("letters")
        b = self.mcl.get_attribute("b")
        eq_(letters.default, None)
        eq_(b.default, None)
        letters.default = "B"
        b.default = False
        eq_(letters.default, "B")
        eq_(b.default, False)
        eq_(letters.type, enum_obj)
        eq_(b.type, bool)

    def test_cclass_vs_cobject(self):
        cl_a = CClass(self.mcl, "A")
        cl_b = CClass(self.mcl, "B")
        obj_b = CObject(cl_b, "obj_b")

        self.mcl.attributes = {"a": cl_a, "b": obj_b}
        a = self.mcl.get_attribute("a")
        b = self.mcl.get_attribute("b")
        eq_(a.type, cl_a)
        eq_(a.default, None)
        eq_(b.type, cl_b)
        eq_(b.default, obj_b)

    testMetaclass = CMetaclass("A")
    testEnum = CEnum("AEnum", values=[1, 2])
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
    def test_attribute_type_check(self, type_to_check, wrong_default):
        self.mcl.attributes = {"a": type_to_check}
        attr = self.mcl.get_attribute("a")
        try:
            attr.default = wrong_default
            exception_expected_()
        except CException as e:
            eq_(f"default value '{wrong_default!s}' incompatible with attribute's type '{type_to_check!s}'", e.value)

    def test_delete_attributes(self):
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

    def test_type_object_attribute_class_is_deleted_in_constructor(self):
        attribute_class = CClass(self.mcl, "AC")
        attribute_class.delete()
        try:
            CMetaclass("M", attributes={"ac": attribute_class})
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_type_object_attribute_class_is_none(self):
        m = CMetaclass("M", attributes={"ac": None})
        ac = m.get_attribute("ac")
        eq_(ac.default, None)
        eq_(ac.type, None)

    def test_default_object_attribute_is_deleted_in_constructor(self):
        attribute_class = CClass(self.mcl, "AC")
        default_object = CObject(attribute_class)
        default_object.delete()
        try:
            CMetaclass("M", attributes={"ac": default_object})
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")


if __name__ == "__main__":
    nose.main()
