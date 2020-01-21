import re

import nose
from nose.tools import ok_, eq_
from parameterized import parameterized

from codeable_models import CMetaclass, CClass, CObject, CAttribute, CException, CEnum
from tests.testing_commons import neq_, exception_expected_


class TestClassAttributes:
    def setup(self):
        self.mcl = CMetaclass("MCL")
        self.cl = CClass(self.mcl, "CL")

    def test_primitive_empty_input(self):
        cl = CClass(self.mcl, "C", attributes={})
        eq_(len(cl.attributes), 0)
        eq_(len(cl.attribute_names), 0)

    def test_primitive_none_input(self):
        cl = CClass(self.mcl, "C", attributes=None)
        eq_(len(cl.attributes), 0)
        eq_(len(cl.attribute_names), 0)

    def test_primitive_type_attributes(self):
        cl = CClass(self.mcl, "C", attributes={
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
        ok_({a1, a2, a3, a4, a5}.issubset(cl.attributes))
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
        cl = CClass(self.mcl, "C", attributes={"isBoolean": True})
        a = cl.get_attribute("isBoolean")
        eq_(a.name, "isBoolean")
        eq_(a.classifier, cl)
        cl.delete()
        eq_(a.name, None)
        eq_(a.classifier, None)

    def test_primitive_attributes_no_default(self):
        self.cl.attributes = {"a": bool, "b": int, "c": str, "d": float, "e": list}
        a1 = self.cl.get_attribute("a")
        a2 = self.cl.get_attribute("b")
        a3 = self.cl.get_attribute("c")
        a4 = self.cl.get_attribute("d")
        a5 = self.cl.get_attribute("e")
        ok_({a1, a2, a3, a4, a5}.issubset(self.cl.attributes))
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
        eq_(self.cl.get_attribute("x"), None)
        self.cl.attributes = {"a": bool, "b": int, "c": str, "d": float}
        eq_(self.cl.get_attribute("x"), None)

    def test_type_and_default_on_attribute(self):
        CAttribute(default="", type=str)
        CAttribute(type=str, default="")
        try:
            CAttribute(default=1, type=str)
            exception_expected_()
        except CException as e:
            eq_("default value '1' incompatible with attribute's type '<class 'str'>'", e.value)
        try:
            CAttribute(type=str, default=1)
            exception_expected_()
        except CException as e:
            eq_("default value '1' incompatible with attribute's type '<class 'str'>'", e.value)
        a5 = CAttribute(type=int)
        eq_(a5.default, None)

    def test_same_named_attributes(self):
        a1 = CAttribute(default="")
        a2 = CAttribute(type=str)
        n1 = "a"
        self.cl.attributes = {n1: a1, "a": a2}
        eq_(set(self.cl.attributes), {a2})
        eq_(self.cl.attribute_names, ["a"])

    def test_same_named_arguments_defaults(self):
        n1 = "a"
        self.cl.attributes = {n1: "", "a": 1}
        ok_(len(self.cl.attributes), 1)
        eq_(self.cl.get_attribute("a").default, 1)
        eq_(self.cl.attribute_names, ["a"])

    def test_object_type_attribute(self):
        attr_type = CClass(self.mcl, "AttrType")
        attr_value = CObject(attr_type, "attribute_value")
        self.cl.attributes = {"attrTypeObj": attr_value}
        obj_attr = self.cl.get_attribute("attrTypeObj")
        attributes = self.cl.attributes
        eq_(set(attributes), {obj_attr})

        bool_attr = CAttribute(default=True)
        self.cl.attributes = {"attrTypeObj": obj_attr, "isBoolean": bool_attr}
        attributes = self.cl.attributes
        eq_(set(attributes), {obj_attr, bool_attr})
        eq_(self.cl.attribute_names, ["attrTypeObj", "isBoolean"])
        obj_attr = self.cl.get_attribute("attrTypeObj")
        eq_(obj_attr.type, attr_type)
        default = obj_attr.default
        ok_(isinstance(default, CObject))
        eq_(default, attr_value)

        self.cl.attributes = {"attrTypeObj": attr_value, "isBoolean": bool_attr}
        eq_(self.cl.attribute_names, ["attrTypeObj", "isBoolean"])
        # using the CObject in attributes causes a new CAttribute to be created != obj_attr
        neq_(self.cl.get_attribute("attrTypeObj"), obj_attr)

    def test_class_type_attribute(self):
        attr_type = CMetaclass("AttrType")
        attr_value = CClass(attr_type, "attribute_value")
        self.cl.attributes = {"attrTypeCl": attr_type}
        cl_attr = self.cl.get_attribute("attrTypeCl")
        cl_attr.default = attr_value
        attributes = self.cl.attributes
        eq_(set(attributes), {cl_attr})

        bool_attr = CAttribute(default=True)
        self.cl.attributes = {"attrTypeCl": cl_attr, "isBoolean": bool_attr}
        attributes = self.cl.attributes
        eq_(set(attributes), {cl_attr, bool_attr})
        eq_(self.cl.attribute_names, ["attrTypeCl", "isBoolean"])
        cl_attr = self.cl.get_attribute("attrTypeCl")
        eq_(cl_attr.type, attr_type)
        default = cl_attr.default
        ok_(isinstance(default, CClass))
        eq_(default, attr_value)

        self.cl.attributes = {"attrTypeCl": attr_value, "isBoolean": bool_attr}
        eq_(self.cl.attribute_names, ["attrTypeCl", "isBoolean"])
        # using the CClass in attributes causes a new CAttribute to be created != cl_attr
        neq_(self.cl.get_attribute("attrTypeCl"), cl_attr)

    def test_enum_get_values(self):
        enum_values = ["A", "B", "C"]
        enum_obj = CEnum("ABCEnum", values=enum_values)
        eq_(["A", "B", "C"], enum_obj.values)
        ok_("A" in enum_obj.values)
        ok_(not ("X" in enum_obj.values))
        enum_values = [1, 2, 3]
        enum_obj = CEnum("123Enum", values=enum_values)
        eq_([1, 2, 3], enum_obj.values)

    def test_enum_empty(self):
        enum_obj = CEnum("ABCEnum", values=[])
        eq_(enum_obj.values, [])
        enum_obj = CEnum("ABCEnum", values=None)
        eq_(enum_obj.values, [])

    def test_enum_no_list(self):
        enum_values = {"A", "B", "C"}
        try:
            CEnum("ABCEnum", values=enum_values)
            exception_expected_()
        except CException as e:
            ok_(re.match("^an enum needs to be initialized with a list of values, but got:([ {}'CAB,]+)$", e.value))

    def test_enum_name(self):
        enum_values = ["A", "B", "C"]
        enum_obj = CEnum("ABCEnum", values=enum_values)
        eq_("ABCEnum", enum_obj.name)

    def test_define_enum_type_attribute(self):
        enum_values = ["A", "B", "C"]
        enum_obj = CEnum("ABCEnum", values=enum_values)
        CAttribute(type=enum_obj, default="A")
        CAttribute(default="A", type=enum_obj)
        try:
            CAttribute(type=enum_obj, default="X")
            exception_expected_()
        except CException as e:
            eq_("default value 'X' incompatible with attribute's type 'ABCEnum'", e.value)
        try:
            CAttribute(default="X", type=enum_obj)
            exception_expected_()
        except CException as e:
            eq_("default value 'X' incompatible with attribute's type 'ABCEnum'", e.value)

    def test_use_enum_type_attribute(self):
        enum_values = ["A", "B", "C"]
        enum_obj = CEnum("ABCEnum", values=enum_values)
        ea1 = CAttribute(type=enum_obj, default="A")
        ea2 = CAttribute(type=enum_obj)
        self.cl.attributes = {"letters1": ea1, "letters2": ea2}
        eq_(set(self.cl.attributes), {ea1, ea2})
        ok_(isinstance(ea1.type, CEnum))

        self.cl.attributes = {"letters1": ea1, "isBool": True, "letters2": ea2}
        bool_attr = self.cl.get_attribute("isBool")
        l1 = self.cl.get_attribute("letters1")
        eq_(set(self.cl.attributes), {l1, ea2, bool_attr})
        eq_(l1.default, "A")
        eq_(ea2.default, None)

    def test_unknown_attribute_type(self):
        try:
            self.cl.attributes = {"x": CEnum, "b": bool}
            exception_expected_()
        except CException as e:
            ok_(re.match("^(unknown attribute type: '<class ).*(CEnum'>')$", e.value))

    def test_set_attribute_default_value(self):
        enum_obj = CEnum("ABCEnum", values=["A", "B", "C"])
        self.cl.attributes = {"letters": enum_obj, "b": bool}
        letters = self.cl.get_attribute("letters")
        b = self.cl.get_attribute("b")
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

        self.cl.attributes = {"a": cl_a, "b": obj_b}
        a = self.cl.get_attribute("a")
        b = self.cl.get_attribute("b")
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
        self.cl.attributes = {"a": type_to_check}
        attr = self.cl.get_attribute("a")
        try:
            attr.default = wrong_default
            exception_expected_()
        except CException as e:
            eq_(f"default value '{wrong_default!s}' incompatible with attribute's type '{type_to_check!s}'", e.value)

    def test_delete_attributes(self):
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

    def test_type_object_attribute_class_is_deleted_in_constructor(self):
        attr_cl = CClass(self.mcl, "AC")
        attr_cl.delete()
        try:
            CClass(self.mcl, "C", attributes={"ac": attr_cl})
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_type_object_attribute_class_is_deleted_in_type_method(self):
        attr_cl = CClass(self.mcl, "AC")
        attr_cl.delete()
        try:
            a = CAttribute()
            a.type = attr_cl
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_set_cattribute_method_to_none(self):
        # setting the type/default to their default value (None) should work
        a = CAttribute()
        a.type = None
        a.default = None
        eq_(a.type, None)
        eq_(a.default, None)

    def test_type_object_attribute_class_is_none(self):
        c = CClass(self.mcl, "C", attributes={"ac": None})
        ac = c.get_attribute("ac")
        eq_(ac.default, None)
        eq_(ac.type, None)

    def test_default_object_attribute_is_deleted_in_constructor(self):
        attr_cl = CClass(self.mcl, "AC")
        default_obj = CObject(attr_cl)
        default_obj.delete()
        try:
            CClass(self.mcl, "C", attributes={"ac": default_obj})
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_default_object_attribute_is_deleted_in_default_method(self):
        attr_cl = CClass(self.mcl, "AC")
        default_obj = CObject(attr_cl)
        default_obj.delete()
        try:
            a = CAttribute()
            a.default = default_obj
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")


if __name__ == "__main__":
    nose.main()
