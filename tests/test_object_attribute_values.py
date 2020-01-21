import nose
from nose.tools import eq_

from codeable_models import CMetaclass, CClass, CObject, CException, CEnum
from tests.testing_commons import exception_expected_


class TestObjectAttributeValues:
    def setup(self):
        self.mcl = CMetaclass("MCL")
        self.cl = CClass(self.mcl, "CL")

    def test_values_on_primitive_type_attributes(self):
        cl = CClass(self.mcl, "C", attributes={
            "isBoolean": True,
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc",
            "list": ["a", "b"]})
        o = CObject(cl, "o")

        eq_(o.get_value("isBoolean"), True)
        eq_(o.get_value("intVal"), 1)
        eq_(o.get_value("floatVal"), 1.1)
        eq_(o.get_value("string"), "abc")
        eq_(o.get_value("list"), ["a", "b"])

        o.set_value("isBoolean", False)
        o.set_value("intVal", 2)
        o.set_value("floatVal", 2.1)
        o.set_value("string", "y")

        eq_(o.get_value("isBoolean"), False)
        eq_(o.get_value("intVal"), 2)
        eq_(o.get_value("floatVal"), 2.1)
        eq_(o.get_value("string"), "y")

        o.set_value("list", [])
        eq_(o.get_value("list"), [])
        o.set_value("list", [1, 2, 3])
        eq_(o.get_value("list"), [1, 2, 3])

    def test_attribute_of_value_unknown(self):
        o = CObject(self.cl, "o")
        try:
            o.get_value("x")
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'x' unknown for 'o'")

        self.cl.attributes = {"isBoolean": True, "intVal": 1}
        try:
            o.set_value("x", 1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'x' unknown for 'o'")

    def test_integers_as_floats(self):
        cl = CClass(self.mcl, "C", attributes={
            "floatVal": float})
        o = CObject(cl, "o")
        o.set_value("floatVal", 15)
        eq_(o.get_value("floatVal"), 15)

    def test_attribute_defined_after_instance(self):
        cl = CClass(self.mcl, "C")
        o = CObject(cl, "o")
        cl.attributes = {"floatVal": float}
        o.set_value("floatVal", 15)
        eq_(o.get_value("floatVal"), 15)

    def test_object_type_attribute_values(self):
        attribute_type = CClass(self.mcl, "AttrType")
        attribute_value = CObject(attribute_type, "attribute_value")
        self.cl.attributes = {"attrTypeObj": attribute_value}
        object_attribute = self.cl.get_attribute("attrTypeObj")
        eq_(object_attribute.type, attribute_type)
        o = CObject(self.cl, "o")
        eq_(o.get_value("attrTypeObj"), attribute_value)

        non_attribute_value = CObject(self.cl, "non_attribute_value")
        try:
            o.set_value("attrTypeObj", non_attribute_value)
            exception_expected_()
        except CException as e:
            eq_(e.value, "type of 'non_attribute_value' is not matching type of attribute 'attrTypeObj'")

    def test_class_type_attribute_values(self):
        attribute_type = CMetaclass("AttrType")
        attribute_value = CClass(attribute_type, "attribute_value")
        self.cl.attributes = {"attrTypeCl": attribute_type}
        class_attribute = self.cl.get_attribute("attrTypeCl")
        class_attribute.default = attribute_value
        eq_(class_attribute.type, attribute_type)
        o = CObject(self.cl, "o")
        eq_(o.get_value("attrTypeCl"), attribute_value)

        non_attribute_value = CClass(CMetaclass("MX"), "non_attribute_value")
        try:
            o.set_value("attrTypeCl", non_attribute_value)
            exception_expected_()
        except CException as e:
            eq_(e.value, "type of 'non_attribute_value' is not matching type of attribute 'attrTypeCl'")

    def test_add_object_attribute_get_set_value(self):
        attribute_type = CClass(self.mcl, "AttrType")
        attribute_value = CObject(attribute_type, "attribute_value")
        o1 = CObject(self.cl, "o1")
        self.cl.attributes = {
            "attrTypeObj1": attribute_type, "attrTypeObj2": attribute_value
        }
        eq_(o1.get_value("attrTypeObj1"), None)
        eq_(o1.get_value("attrTypeObj2"), attribute_value)

    def test_object_attribute_of_superclass_type(self):
        attribute_super_type = CClass(self.mcl, "AttrSuperType")
        attribute_type = CClass(self.mcl, "AttrType", superclasses=attribute_super_type)
        attribute_value = CObject(attribute_type, "attribute_value")
        o = CObject(self.cl, "o1")
        self.cl.attributes = {
            "attrTypeObj1": attribute_super_type, "attrTypeObj2": attribute_value
        }
        o.set_value("attrTypeObj1", attribute_value)
        o.set_value("attrTypeObj2", attribute_value)
        eq_(o.get_value("attrTypeObj1"), attribute_value)
        eq_(o.get_value("attrTypeObj2"), attribute_value)

    def test_values_on_attributes_with_no_default_values(self):
        attribute_type = CClass(self.mcl, "AttrType")
        enum_type = CEnum("EnumT", values=["A", "B", "C"])
        cl = CClass(self.mcl, "C", attributes={
            "b": bool,
            "i": int,
            "f": float,
            "s": str,
            "l": list,
            "o": attribute_type,
            "e": enum_type})
        o = CObject(cl, "o")
        for n in ["b", "i", "f", "s", "l", "o", "e"]:
            eq_(o.get_value(n), None)

    def test_values_defined_in_constructor(self):
        object_value_type = CClass(CMetaclass())
        object_value = CObject(object_value_type, "object_value")

        cl = CClass(self.mcl, "C", attributes={
            "isBoolean": True,
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc",
            "list": ["a", "b"],
            "obj": object_value_type})
        o = CObject(cl, "o", values={
            "isBoolean": False, "intVal": 2, "floatVal": 2.1,
            "string": "y", "list": [], "obj": object_value})

        eq_(o.get_value("isBoolean"), False)
        eq_(o.get_value("intVal"), 2)
        eq_(o.get_value("floatVal"), 2.1)
        eq_(o.get_value("string"), "y")
        eq_(o.get_value("list"), [])
        eq_(o.get_value("obj"), object_value)

        eq_(o.values, {"isBoolean": False, "intVal": 2, "floatVal": 2.1,
                       "string": "y", "list": [], "obj": object_value})

    def test_values_setter_overwrite(self):
        cl = CClass(self.mcl, "C", attributes={
            "isBoolean": True,
            "intVal": 1})
        o = CObject(cl, "o", values={
            "isBoolean": False, "intVal": 2})
        o.values = {"isBoolean": True, "intVal": 20}
        eq_(o.get_value("isBoolean"), True)
        eq_(o.get_value("intVal"), 20)
        eq_(o.values, {'isBoolean': True, 'intVal': 20})
        o.values = {}
        # values should not delete existing values
        eq_(o.values, {"isBoolean": True, "intVal": 20})

    def test_values_setter_with_superclass(self):
        scl = CClass(self.mcl, "SCL", attributes={
            "intVal": 20, "intVal2": 30})
        cl = CClass(self.mcl, "C", superclasses=scl, attributes={
            "isBoolean": True,
            "intVal": 1})
        o = CObject(cl, "o", values={
            "isBoolean": False})
        eq_(o.values, {"isBoolean": False, "intVal": 1, "intVal2": 30})
        o.set_value("intVal", 12, scl)
        o.set_value("intVal", 15, cl)
        o.set_value("intVal2", 16, scl)
        eq_(o.values, {"isBoolean": False, "intVal": 15, "intVal2": 16})
        eq_(o.get_value("intVal", scl), 12)
        eq_(o.get_value("intVal", cl), 15)

    def test_values_setter_malformed_description(self):
        cl = CClass(self.mcl, "C", attributes={
            "isBoolean": True,
            "intVal": 1})
        o = CObject(cl, "o")
        try:
            o.values = [1, 2, 3]
            exception_expected_()
        except CException as e:
            eq_(e.value, "malformed attribute values description: '[1, 2, 3]'")

    def test_enum_type_attribute_values(self):
        enum_type = CEnum("EnumT", values=["A", "B", "C"])
        cl = CClass(self.mcl, "C", attributes={
            "e1": enum_type,
            "e2": enum_type})
        e2 = cl.get_attribute("e2")
        e2.default = "A"
        o = CObject(cl, "o")
        eq_(o.get_value("e1"), None)
        eq_(o.get_value("e2"), "A")
        o.set_value("e1", "B")
        o.set_value("e2", "C")
        eq_(o.get_value("e1"), "B")
        eq_(o.get_value("e2"), "C")
        try:
            o.set_value("e1", "X")
            exception_expected_()
        except CException as e:
            eq_(e.value, "value 'X' is not element of enumeration")

    def test_default_init_after_instance_creation(self):
        enum_type = CEnum("EnumT", values=["A", "B", "C"])
        cl = CClass(self.mcl, "C", attributes={
            "e1": enum_type,
            "e2": enum_type})
        o = CObject(cl, "o")
        e2 = cl.get_attribute("e2")
        e2.default = "A"
        eq_(o.get_value("e1"), None)
        eq_(o.get_value("e2"), "A")

    def test_attribute_value_type_check_bool1(self):
        self.cl.attributes = {"t": bool}
        o = CObject(self.cl, "o")
        try:
            o.set_value("t", self.mcl)
            exception_expected_()
        except CException as e:
            eq_(f"value for attribute 't' is not a known attribute type", e.value)

    def test_attribute_value_type_check_bool2(self):
        self.cl.attributes = {"t": bool}
        o = CObject(self.cl, "o")
        try:
            o.set_value("t", 1)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_int(self):
        self.cl.attributes = {"t": int}
        o = CObject(self.cl, "o")
        try:
            o.set_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_float(self):
        self.cl.attributes = {"t": float}
        o = CObject(self.cl, "o")
        try:
            o.set_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_str(self):
        self.cl.attributes = {"t": str}
        o = CObject(self.cl, "o")
        try:
            o.set_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_list(self):
        self.cl.attributes = {"t": list}
        o = CObject(self.cl, "o")
        try:
            o.set_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_object(self):
        attribute_type = CClass(self.mcl, "AttrType")
        self.cl.attributes = {"t": attribute_type}
        o = CObject(self.cl, "o")
        try:
            o.set_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_enum(self):
        enum_type = CEnum("EnumT", values=["A", "B", "C"])
        self.cl.attributes = {"t": enum_type}
        o = CObject(self.cl, "o")
        try:
            o.set_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_deleted(self):
        cl = CClass(self.mcl, "C", attributes={
            "isBoolean": True,
            "intVal": 15})
        o = CObject(cl, "o")
        eq_(o.get_value("intVal"), 15)
        cl.attributes = {
            "isBoolean": False}
        eq_(o.get_value("isBoolean"), True)
        try:
            o.get_value("intVal")
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'intVal' unknown for 'o'")
        try:
            o.set_value("intVal", 1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'intVal' unknown for 'o'")

    def test_attribute_deleted_no_default(self):
        cl = CClass(self.mcl, "C", attributes={
            "isBoolean": bool,
            "intVal": int})
        cl.attributes = {"isBoolean": bool}
        o = CObject(cl, "o")
        eq_(o.get_value("isBoolean"), None)
        try:
            o.get_value("intVal")
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'intVal' unknown for 'o'")
        try:
            o.set_value("intVal", 1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'intVal' unknown for 'o'")

    def test_attributes_overwrite(self):
        cl = CClass(self.mcl, "C", attributes={
            "isBoolean": True,
            "intVal": 15})
        o = CObject(cl, "o")
        eq_(o.get_value("intVal"), 15)
        try:
            o.get_value("floatVal")
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'floatVal' unknown for 'o'")
        o.set_value("intVal", 18)
        cl.attributes = {
            "isBoolean": False,
            "intVal": 19,
            "floatVal": 25.1}
        eq_(o.get_value("isBoolean"), True)
        eq_(o.get_value("floatVal"), 25.1)
        eq_(o.get_value("intVal"), 18)
        o.set_value("floatVal", 1.2)
        eq_(o.get_value("floatVal"), 1.2)

    def test_attributes_overwrite_no_defaults(self):
        cl = CClass(self.mcl, "C", attributes={
            "isBoolean": bool,
            "intVal": int})
        o = CObject(cl, "o")
        eq_(o.get_value("isBoolean"), None)
        o.set_value("isBoolean", False)
        cl.attributes = {
            "isBoolean": bool,
            "intVal": int,
            "floatVal": float}
        eq_(o.get_value("isBoolean"), False)
        eq_(o.get_value("floatVal"), None)
        eq_(o.get_value("intVal"), None)
        o.set_value("floatVal", 1.2)
        eq_(o.get_value("floatVal"), 1.2)

    def test_attributes_deleted_on_subclass(self):
        cl = CClass(self.mcl, "C", attributes={
            "isBoolean": True,
            "intVal": 1})
        cl2 = CClass(self.mcl, "C2", attributes={
            "isBoolean": False}, superclasses=cl)

        o = CObject(cl2, "o")

        eq_(o.get_value("isBoolean"), False)
        eq_(o.get_value("isBoolean", cl), True)
        eq_(o.get_value("isBoolean", cl2), False)

        cl2.attributes = {}

        eq_(o.get_value("isBoolean"), True)
        eq_(o.get_value("intVal"), 1)
        eq_(o.get_value("isBoolean", cl), True)
        try:
            o.get_value("isBoolean", cl2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'isBoolean' unknown for 'C2'")

    def test_attributes_deleted_on_subclass_no_defaults(self):
        cl = CClass(self.mcl, "C", attributes={
            "isBoolean": bool,
            "intVal": int})
        cl2 = CClass(self.mcl, "C2", attributes={
            "isBoolean": bool}, superclasses=cl)

        o = CObject(cl2, "o")

        eq_(o.get_value("isBoolean"), None)
        eq_(o.get_value("isBoolean", cl), None)
        eq_(o.get_value("isBoolean", cl2), None)

        cl2.attributes = {}

        eq_(o.get_value("isBoolean"), None)
        eq_(o.get_value("intVal"), None)
        eq_(o.get_value("isBoolean", cl), None)
        try:
            o.get_value("isBoolean", cl2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'isBoolean' unknown for 'C2'")

    def test_attribute_values_inheritance(self):
        t1 = CClass(self.mcl, "T1")
        t2 = CClass(self.mcl, "T2")
        c = CClass(self.mcl, "C", superclasses=[t1, t2])
        sc = CClass(self.mcl, "C", superclasses=c)

        t1.attributes = {"i0": 0}
        t2.attributes = {"i1": 1}
        c.attributes = {"i2": 2}
        sc.attributes = {"i3": 3}

        o = CObject(sc, "o")

        for name, value in {"i0": 0, "i1": 1, "i2": 2, "i3": 3}.items():
            eq_(o.get_value(name), value)

        eq_(o.get_value("i0", t1), 0)
        eq_(o.get_value("i1", t2), 1)
        eq_(o.get_value("i2", c), 2)
        eq_(o.get_value("i3", sc), 3)

        for name, value in {"i0": 10, "i1": 11, "i2": 12, "i3": 13}.items():
            o.set_value(name, value)

        for name, value in {"i0": 10, "i1": 11, "i2": 12, "i3": 13}.items():
            eq_(o.get_value(name), value)

        eq_(o.get_value("i0", t1), 10)
        eq_(o.get_value("i1", t2), 11)
        eq_(o.get_value("i2", c), 12)
        eq_(o.get_value("i3", sc), 13)

    def test_attribute_values_inheritance_after_delete_superclass(self):
        t1 = CClass(self.mcl, "T1")
        t2 = CClass(self.mcl, "T2")
        c = CClass(self.mcl, "C", superclasses=[t1, t2])
        sc = CClass(self.mcl, "C", superclasses=c)

        t1.attributes = {"i0": 0}
        t2.attributes = {"i1": 1}
        c.attributes = {"i2": 2}
        sc.attributes = {"i3": 3}

        o = CObject(sc, "o")

        t2.delete()

        for name, value in {"i0": 0, "i2": 2, "i3": 3}.items():
            eq_(o.get_value(name), value)
        try:
            o.get_value("i1")
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'i1' unknown for 'o'")

        eq_(o.get_value("i0", t1), 0)
        try:
            o.get_value("i1", t2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'i1' unknown for ''")
        eq_(o.get_value("i2", c), 2)
        eq_(o.get_value("i3", sc), 3)

        for name, value in {"i0": 10, "i2": 12, "i3": 13}.items():
            o.set_value(name, value)
        try:
            o.set_value("i1", 11)
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'i1' unknown for 'o'")

        for name, value in {"i0": 10, "i2": 12, "i3": 13}.items():
            eq_(o.get_value(name), value)
        try:
            o.get_value("i1")
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'i1' unknown for 'o'")

        eq_(o.get_value("i0", t1), 10)
        try:
            o.get_value("i1", t2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'i1' unknown for ''")
        eq_(o.get_value("i2", c), 12)
        eq_(o.get_value("i3", sc), 13)

    def test_attribute_values_same_name_inheritance(self):
        t1 = CClass(self.mcl, "T1")
        t2 = CClass(self.mcl, "T2")
        c = CClass(self.mcl, "C", superclasses=[t1, t2])
        sc = CClass(self.mcl, "C", superclasses=c)

        t1.attributes = {"i": 0}
        t2.attributes = {"i": 1}
        c.attributes = {"i": 2}
        sc.attributes = {"i": 3}

        o1 = CObject(sc)
        o2 = CObject(c)
        o3 = CObject(t1)

        eq_(o1.get_value("i"), 3)
        eq_(o2.get_value("i"), 2)
        eq_(o3.get_value("i"), 0)

        eq_(o1.get_value("i", sc), 3)
        eq_(o1.get_value("i", c), 2)
        eq_(o1.get_value("i", t2), 1)
        eq_(o1.get_value("i", t1), 0)
        eq_(o2.get_value("i", c), 2)
        eq_(o2.get_value("i", t2), 1)
        eq_(o2.get_value("i", t1), 0)
        eq_(o3.get_value("i", t1), 0)

        o1.set_value("i", 10)
        o2.set_value("i", 11)
        o3.set_value("i", 12)

        eq_(o1.get_value("i"), 10)
        eq_(o2.get_value("i"), 11)
        eq_(o3.get_value("i"), 12)

        eq_(o1.get_value("i", sc), 10)
        eq_(o1.get_value("i", c), 2)
        eq_(o1.get_value("i", t2), 1)
        eq_(o1.get_value("i", t1), 0)
        eq_(o2.get_value("i", c), 11)
        eq_(o2.get_value("i", t2), 1)
        eq_(o2.get_value("i", t1), 0)
        eq_(o3.get_value("i", t1), 12)

        o1.set_value("i", 130, sc)
        o1.set_value("i", 100, t1)
        o1.set_value("i", 110, t2)
        o1.set_value("i", 120, c)

        eq_(o1.get_value("i"), 130)

        eq_(o1.get_value("i", sc), 130)
        eq_(o1.get_value("i", c), 120)
        eq_(o1.get_value("i", t2), 110)
        eq_(o1.get_value("i", t1), 100)

    def test_values_multiple_inheritance(self):
        t1 = CClass(self.mcl, "T1")
        t2 = CClass(self.mcl, "T2")
        st_a = CClass(self.mcl, "STA", superclasses=[t1, t2])
        sub_a = CClass(self.mcl, "SubA", superclasses=[st_a])
        st_b = CClass(self.mcl, "STB", superclasses=[t1, t2])
        sub_b = CClass(self.mcl, "SubB", superclasses=[st_b])
        st_c = CClass(self.mcl, "STC")
        sub_c = CClass(self.mcl, "SubC", superclasses=[st_c])

        cl = CClass(self.mcl, "M", superclasses=[sub_a, sub_b, sub_c])
        o = CObject(cl)

        t1.attributes = {"i0": 0}
        t2.attributes = {"i1": 1}
        st_a.attributes = {"i2": 2}
        sub_a.attributes = {"i3": 3}
        st_b.attributes = {"i4": 4}
        sub_b.attributes = {"i5": 5}
        st_c.attributes = {"i6": 6}
        sub_c.attributes = {"i7": 7}

        eq_(o.get_value("i0"), 0)
        eq_(o.get_value("i1"), 1)
        eq_(o.get_value("i2"), 2)
        eq_(o.get_value("i3"), 3)
        eq_(o.get_value("i4"), 4)
        eq_(o.get_value("i5"), 5)
        eq_(o.get_value("i6"), 6)
        eq_(o.get_value("i7"), 7)

        eq_(o.get_value("i0", t1), 0)
        eq_(o.get_value("i1", t2), 1)
        eq_(o.get_value("i2", st_a), 2)
        eq_(o.get_value("i3", sub_a), 3)
        eq_(o.get_value("i4", st_b), 4)
        eq_(o.get_value("i5", sub_b), 5)
        eq_(o.get_value("i6", st_c), 6)
        eq_(o.get_value("i7", sub_c), 7)

        o.set_value("i0", 10)
        o.set_value("i1", 11)
        o.set_value("i2", 12)
        o.set_value("i3", 13)
        o.set_value("i4", 14)
        o.set_value("i5", 15)
        o.set_value("i6", 16)
        o.set_value("i7", 17)

        eq_(o.get_value("i0"), 10)
        eq_(o.get_value("i1"), 11)
        eq_(o.get_value("i2"), 12)
        eq_(o.get_value("i3"), 13)
        eq_(o.get_value("i4"), 14)
        eq_(o.get_value("i5"), 15)
        eq_(o.get_value("i6"), 16)
        eq_(o.get_value("i7"), 17)

    def test_delete_attribute_values(self):
        cl = CClass(self.mcl, "C", attributes={
            "isBoolean": True,
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc",
            "list": ["a", "b"]})
        o = CObject(cl, "o")
        o.delete_value("isBoolean")
        o.delete_value("intVal")
        list_value = o.delete_value("list")
        eq_(o.values, {'floatVal': 1.1, 'string': 'abc'})
        eq_(list_value, ['a', 'b'])

    def test_delete_attribute_values_with_superclass(self):
        scl = CClass(self.mcl, "SCL", attributes={
            "intVal": 20, "intVal2": 30})
        cl = CClass(self.mcl, "C", superclasses=scl, attributes={
            "isBoolean": True,
            "intVal": 1})
        o = CObject(cl, "o", values={
            "isBoolean": False})
        o.delete_value("isBoolean")
        o.delete_value("intVal2")
        eq_(o.values, {"intVal": 1})

        o.set_value("intVal", 2, scl)
        o.set_value("intVal", 3, cl)
        eq_(o.values, {"intVal": 3})
        o.delete_value("intVal")
        eq_(o.values, {"intVal": 2})

        o.set_value("intVal", 2, scl)
        o.set_value("intVal", 3, cl)
        o.delete_value("intVal", cl)
        eq_(o.values, {"intVal": 2})

        o.set_value("intVal", 2, scl)
        o.set_value("intVal", 3, cl)
        o.delete_value("intVal", scl)
        eq_(o.values, {"intVal": 3})

    def test_attribute_values_exceptional_cases(self):
        cl = CClass(self.mcl, "C", attributes={"b": True})
        o1 = CObject(cl, "o")
        o1.delete()

        try:
            o1.get_value("b")
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't get value 'b' on deleted object")

        try:
            o1.set_value("b", 1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't set value 'b' on deleted object")

        try:
            o1.delete_value("b")
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't delete value 'b' on deleted object")

        try:
            o1.values = {"b": 1}
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't set values on deleted object")

        try:
            # we just use list here, in order to not get a warning that o1.values has no effect
            list(o1.values)
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't get values on deleted object")

        o = CObject(cl, "o")
        try:
            o.delete_value("x")
            exception_expected_()
        except CException as e:
            eq_(e.value, "attribute 'x' unknown for 'o'")


if __name__ == "__main__":
    nose.main()
