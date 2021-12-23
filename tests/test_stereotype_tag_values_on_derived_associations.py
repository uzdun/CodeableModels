import nose
from nose.tools import eq_

from codeable_models import *
from tests.testing_commons import exception_expected_


class TestStereotypeTagValuesOnDerivedAssociations:
    def setup(self):
        self.st = CStereotype("ST")
        self.m1 = CMetaclass("M1")
        self.m2 = CMetaclass("M2")
        self.a = self.m1.association(self.m2, name="a", multiplicity="*", role_name="m1",
                                     source_multiplicity="1..*", source_role_name="m2")
        self.a.stereotypes = self.st
        self.c1 = CClass(self.m1, "C1")
        self.c2 = CClass(self.m2, "C2")
        self.c3 = CClass(self.m2, "C3")
        self.c4 = CClass(self.m2, "C4")

        self.a1 = self.c1.association(self.c2, name="a1", multiplicity="*", role_name="c2",
                                      source_multiplicity="1", source_role_name="c1", derived_from=self.a)
        self.a2 = self.c1.association(self.c2, name="a2", multiplicity="*", role_name="c3",
                                      source_multiplicity="1", source_role_name="c1", derived_from=self.a)
        self.a3 = self.c1.association(self.c4, name="a3", multiplicity="*", role_name="c4",
                                      source_multiplicity="1", source_role_name="c1", derived_from=self.a)
        self.a1.stereotype_instances = self.st

    def test_tagged_values_on_primitive_type_attributes(self):
        s = CStereotype("S", attributes={
            "isBoolean": True,
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc",
            "list": ["a", "b"]})
        self.a.stereotypes = s
        self.a1.stereotype_instances = s

        eq_(self.a1.get_tagged_value("isBoolean"), True)
        eq_(self.a1.get_tagged_value("intVal"), 1)
        eq_(self.a1.get_tagged_value("floatVal"), 1.1)
        eq_(self.a1.get_tagged_value("string"), "abc")
        eq_(self.a1.get_tagged_value("list"), ["a", "b"])

        self.a1.set_tagged_value("isBoolean", False)
        self.a1.set_tagged_value("intVal", 2)
        self.a1.set_tagged_value("floatVal", 2.1)
        self.a1.set_tagged_value("string", "y")

        eq_(self.a1.get_tagged_value("isBoolean"), False)
        eq_(self.a1.get_tagged_value("intVal"), 2)
        eq_(self.a1.get_tagged_value("floatVal"), 2.1)
        eq_(self.a1.get_tagged_value("string"), "y")

        self.a1.set_tagged_value("list", [])
        eq_(self.a1.get_tagged_value("list"), [])
        self.a1.set_tagged_value("list", [1, 2, 3])
        eq_(self.a1.get_tagged_value("list"), [1, 2, 3])

    def test_attribute_of_tagged_value_unknown(self):
        try:
            self.a1.get_tagged_value("x")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'x' unknown for 'a1'")

    def test_integers_as_float_tagged_values(self):
        self.st.attributes = {"floatVal": float}
        self.a1.set_tagged_value("floatVal", 15)
        eq_(self.a1.get_tagged_value("floatVal"), 15)

    def test_object_type_attribute_tagged_values(self):
        attribute_type = CClass(self.m1, "AttrType")
        attribute_value = CObject(attribute_type, "attribute_value")
        self.st.attributes = {"attrTypeObj": attribute_value}
        object_attribute = self.st.get_attribute("attrTypeObj")
        eq_(object_attribute.type, attribute_type)
        eq_(self.a1.get_tagged_value("attrTypeObj"), attribute_value)

        non_attribute_value = CObject(CClass(self.m1), "non_attribute_value")
        try:
            self.a1.set_tagged_value("attrTypeObj", non_attribute_value)
            exception_expected_()
        except CException as e:
            eq_(e.value, "type of 'non_attribute_value' is not matching type of attribute 'attrTypeObj'")

    def test_class_type_attribute_tagged_values(self):
        attribute_type = CMetaclass("AttrType")
        attribute_value = CClass(attribute_type, "attribute_value")
        self.st.attributes = {"attrTypeCl": attribute_type}
        class_attribute = self.st.get_attribute("attrTypeCl")
        class_attribute.default = attribute_value
        eq_(class_attribute.type, attribute_type)
        eq_(self.a1.get_tagged_value("attrTypeCl"), attribute_value)

        non_attribute_value = CClass(CMetaclass("MX"), "non_attribute_value")
        try:
            self.a1.set_tagged_value("attrTypeCl", non_attribute_value)
            exception_expected_()
        except CException as e:
            eq_(e.value, "type of 'non_attribute_value' is not matching type of attribute 'attrTypeCl'")

    def test_add_object_attribute_get_set_tagged_value(self):
        attribute_type = CClass(self.m1, "AttrType")
        attribute_value = CObject(attribute_type, "attribute_value")
        self.st.attributes = {
            "attrTypeObj1": attribute_type, "attrTypeObj2": attribute_value
        }
        eq_(self.a1.get_tagged_value("attrTypeObj1"), None)
        eq_(self.a1.get_tagged_value("attrTypeObj2"), attribute_value)

    def test_object_attribute_tagged_value_of_superclass_type(self):
        attribute_super_type = CClass(self.m1, "AttrSuperType")
        attribute_type = CClass(self.m1, "AttrType", superclasses=attribute_super_type)
        attribute_value = CObject(attribute_type, "attribute_value")
        self.st.attributes = {
            "attrTypeObj1": attribute_super_type, "attrTypeObj2": attribute_value
        }
        self.a1.set_tagged_value("attrTypeObj1", attribute_value)
        self.a1.set_tagged_value("attrTypeObj2", attribute_value)
        eq_(self.a1.get_tagged_value("attrTypeObj1"), attribute_value)
        eq_(self.a1.get_tagged_value("attrTypeObj2"), attribute_value)

    def test_tagged_values_on_attributes_with_no_default_values(self):
        attribute_type = CClass(self.m1, "AttrType")
        enum_type = CEnum("EnumT", values=["A", "B", "C"])
        st = CStereotype("S", attributes={
            "b": bool,
            "i": int,
            "f": float,
            "s": str,
            "l": list,
            "C": attribute_type,
            "e": enum_type})
        self.a.stereotypes = st
        self.a1.stereotype_instances = st
        for n in ["b", "i", "f", "s", "l", "C", "e"]:
            eq_(self.a1.get_tagged_value(n), None)

    def test_tagged_values_setter(self):
        object_value_type = CClass(CMetaclass())
        object_value = CObject(object_value_type, "object_value")

        st = CStereotype("S", attributes={
            "isBoolean": True,
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc",
            "list": ["a", "b"],
            "obj": object_value_type})
        self.a.stereotypes = st
        self.a1.stereotype_instances = st
        self.a1.tagged_values = {
            "isBoolean": False, "intVal": 2, "floatVal": 2.1,
            "string": "y", "list": [], "obj": object_value}

        eq_(self.a1.get_tagged_value("isBoolean"), False)
        eq_(self.a1.get_tagged_value("intVal"), 2)
        eq_(self.a1.get_tagged_value("floatVal"), 2.1)
        eq_(self.a1.get_tagged_value("string"), "y")
        eq_(self.a1.get_tagged_value("list"), [])
        eq_(self.a1.get_tagged_value("obj"), object_value)

        eq_(self.a1.tagged_values, {"isBoolean": False, "intVal": 2, "floatVal": 2.1,
                                    "string": "y", "list": [], "obj": object_value})

    def test_tagged_values_setter_overwrite(self):
        st = CStereotype("S", attributes={
            "isBoolean": True,
            "intVal": 1})
        self.a.stereotypes = st
        self.a1.stereotype_instances = st
        self.a1.tagged_values = {"isBoolean": False, "intVal": 2}
        self.a1.tagged_values = {"isBoolean": True, "intVal": 20}
        eq_(self.a1.get_tagged_value("isBoolean"), True)
        eq_(self.a1.get_tagged_value("intVal"), 20)
        eq_(self.a1.tagged_values, {'isBoolean': True, 'intVal': 20})
        self.a1.tagged_values = {}
        # tagged values should not delete existing values
        eq_(self.a1.tagged_values, {"isBoolean": True, "intVal": 20})

    def test_tagged_values_setter_with_superclass(self):
        sst = CStereotype("SST", attributes={
            "intVal": 20, "intVal2": 30})
        st = CStereotype("S", superclasses=sst, attributes={
            "isBoolean": True,
            "intVal": 1})
        self.a.stereotypes = st
        self.a1.stereotype_instances = st
        self.a1.tagged_values = {"isBoolean": False}
        eq_(self.a1.tagged_values, {"isBoolean": False, "intVal": 1, "intVal2": 30})
        self.a1.set_tagged_value("intVal", 12, sst)
        self.a1.set_tagged_value("intVal", 15, st)
        self.a1.set_tagged_value("intVal2", 16, sst)
        eq_(self.a1.tagged_values, {"isBoolean": False, "intVal": 15, "intVal2": 16})
        eq_(self.a1.get_tagged_value("intVal", sst), 12)
        eq_(self.a1.get_tagged_value("intVal", st), 15)

    def test_tagged_values_setter_malformed_description(self):
        try:
            self.a1.tagged_values = [1, 2, 3]
            exception_expected_()
        except CException as e:
            eq_(e.value, "malformed tagged values description: '[1, 2, 3]'")

    def test_enum_type_attribute_values(self):
        enum_type = CEnum("EnumT", values=["A", "B", "C"])
        self.st.attributes = {
            "e1": enum_type,
            "e2": enum_type}
        e2 = self.st.get_attribute("e2")
        e2.default = "A"
        eq_(self.a1.get_tagged_value("e1"), None)
        eq_(self.a1.get_tagged_value("e2"), "A")
        self.a1.set_tagged_value("e1", "B")
        self.a1.set_tagged_value("e2", "C")
        eq_(self.a1.get_tagged_value("e1"), "B")
        eq_(self.a1.get_tagged_value("e2"), "C")
        try:
            self.a1.set_tagged_value("e1", "X")
            exception_expected_()
        except CException as e:
            eq_(e.value, "value 'X' is not element of enumeration")

    def test_default_init_after_instance_creation(self):
        enum_type = CEnum("EnumT", values=["A", "B", "C"])
        self.st.attributes = {
            "e1": enum_type,
            "e2": enum_type}
        e2 = self.st.get_attribute("e2")
        e2.default = "A"
        eq_(self.a1.get_tagged_value("e1"), None)
        eq_(self.a1.get_tagged_value("e2"), "A")

    def test_attribute_value_type_check_bool1(self):
        self.st.attributes = {"t": bool}
        self.stereotype_instances = self.st
        try:
            self.a1.set_tagged_value("t", self.m1)
            exception_expected_()
        except CException as e:
            eq_(f"value for attribute 't' is not a known attribute type", e.value)

    def test_attribute_value_type_check_bool2(self):
        self.st.attributes = {"t": bool}
        self.a1.stereotype_instances = self.st
        try:
            self.a1.set_tagged_value("t", 1)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_int(self):
        self.st.attributes = {"t": int}
        self.a1.stereotype_instances = self.st
        try:
            self.a1.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_float(self):
        self.st.attributes = {"t": float}
        self.a1.stereotype_instances = self.st
        try:
            self.a1.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_str(self):
        self.st.attributes = {"t": str}
        self.a1.stereotype_instances = self.st
        try:
            self.a1.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_list(self):
        self.st.attributes = {"t": list}
        self.a1.stereotype_instances = self.st
        try:
            self.a1.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_object(self):
        attribute_type = CClass(CMetaclass(), "AttrType")
        self.st.attributes = {"t": attribute_type}
        self.a1.stereotype_instances = self.st
        try:
            self.a1.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_enum(self):
        enum_type = CEnum("EnumT", values=["A", "B", "C"])
        self.st.attributes = {"t": enum_type}
        self.a1.stereotype_instances = self.st
        try:
            self.a1.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_deleted(self):
        self.st.attributes = {
            "isBoolean": True,
            "intVal": 15}
        self.a1.stereotype_instances = self.st
        eq_(self.a1.get_tagged_value("intVal"), 15)
        self.st.attributes = {
            "isBoolean": False}
        eq_(self.a1.get_tagged_value("isBoolean"), True)
        try:
            self.a1.get_tagged_value("intVal")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'intVal' unknown for 'a1'")
        try:
            self.a1.set_tagged_value("intVal", 1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'intVal' unknown for 'a1'")

    def test_attribute_deleted_no_default(self):
        self.st.attributes = {
            "isBoolean": bool,
            "intVal": int}
        self.st.attributes = {"isBoolean": bool}
        eq_(self.a1.get_tagged_value("isBoolean"), None)
        try:
            self.a1.get_tagged_value("intVal")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'intVal' unknown for 'a1'")
        try:
            self.a1.set_tagged_value("intVal", 1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'intVal' unknown for 'a1'")

    def test_attributes_overwrite(self):
        self.st.attributes = {
            "isBoolean": True,
            "intVal": 15}
        self.a1.stereotype_instances = self.st
        eq_(self.a1.get_tagged_value("intVal"), 15)
        try:
            self.a1.get_tagged_value("floatVal")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'floatVal' unknown for 'a1'")
        self.a1.set_tagged_value("intVal", 18)
        self.st.attributes = {
            "isBoolean": False,
            "intVal": 19,
            "floatVal": 25.1}
        eq_(self.a1.get_tagged_value("isBoolean"), True)
        eq_(self.a1.get_tagged_value("floatVal"), 25.1)
        eq_(self.a1.get_tagged_value("intVal"), 18)
        self.a1.set_tagged_value("floatVal", 1.2)
        eq_(self.a1.get_tagged_value("floatVal"), 1.2)

    def test_attributes_overwrite_no_defaults(self):
        self.st.attributes = {
            "isBoolean": bool,
            "intVal": int}
        eq_(self.a1.get_tagged_value("isBoolean"), None)
        self.a1.set_tagged_value("isBoolean", False)
        self.st.attributes = {
            "isBoolean": bool,
            "intVal": int,
            "floatVal": float}
        eq_(self.a1.get_tagged_value("isBoolean"), False)
        eq_(self.a1.get_tagged_value("floatVal"), None)
        eq_(self.a1.get_tagged_value("intVal"), None)
        self.a1.set_tagged_value("floatVal", 1.2)
        eq_(self.a1.get_tagged_value("floatVal"), 1.2)

    def test_attributes_deleted_on_subclass(self):
        self.st.attributes = {
            "isBoolean": True,
            "intVal": 1}
        st2 = CStereotype("S2", attributes={
            "isBoolean": False}, superclasses=self.st)
        self.a.stereotypes = st2
        self.a1.stereotype_instances = st2

        eq_(self.a1.get_tagged_value("isBoolean"), False)
        eq_(self.a1.get_tagged_value("isBoolean", self.st), True)
        eq_(self.a1.get_tagged_value("isBoolean", st2), False)

        st2.attributes = {}

        eq_(self.a1.get_tagged_value("isBoolean"), True)
        eq_(self.a1.get_tagged_value("intVal"), 1)
        eq_(self.a1.get_tagged_value("isBoolean", self.st), True)
        try:
            self.a1.get_tagged_value("isBoolean", st2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'isBoolean' unknown for 'S2'")

    def test_attributes_deleted_on_subclass_no_defaults(self):
        self.st.attributes = {
            "isBoolean": bool,
            "intVal": int}
        st2 = CStereotype("S2", attributes={
            "isBoolean": bool}, superclasses=self.st)
        self.a.stereotypes = st2
        self.a1.stereotype_instances = st2

        eq_(self.a1.get_tagged_value("isBoolean"), None)
        eq_(self.a1.get_tagged_value("isBoolean", self.st), None)
        eq_(self.a1.get_tagged_value("isBoolean", st2), None)

        st2.attributes = {}

        eq_(self.a1.get_tagged_value("isBoolean"), None)
        eq_(self.a1.get_tagged_value("intVal"), None)
        eq_(self.a1.get_tagged_value("isBoolean", self.st), None)
        try:
            self.a1.get_tagged_value("isBoolean", st2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'isBoolean' unknown for 'S2'")

    def test_wrong_stereotype_in_tagged_value(self):
        self.st.attributes = {
            "isBoolean": True}
        st2 = CStereotype("S2", attributes={
            "isBoolean": True})
        self.a.stereotypes = st2
        self.a1.stereotype_instances = st2

        self.a1.set_tagged_value("isBoolean", False)

        try:
            self.a1.set_tagged_value("isBoolean", False, st2)
        except CException as e:
            eq_(e.value, "stereotype 'S2' is not a stereotype of element")

        eq_(self.a1.get_tagged_value("isBoolean"), False)

        try:
            self.a1.get_tagged_value("isBoolean", st2)
        except CException as e:
            eq_(e.value, "stereotype 'S2' is not a stereotype of element")

    def test_attribute_values_inheritance(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        c = CStereotype("C", superclasses=[t1, t2])
        sc = CStereotype("C", superclasses=c)

        t1.attributes = {"i0": 0}
        t2.attributes = {"i1": 1}
        c.attributes = {"i2": 2}
        sc.attributes = {"i3": 3}

        self.a.stereotypes = sc
        self.a1.stereotype_instances = sc

        for name, value in {"i0": 0, "i1": 1, "i2": 2, "i3": 3}.items():
            eq_(self.a1.get_tagged_value(name), value)

        eq_(self.a1.get_tagged_value("i0", t1), 0)
        eq_(self.a1.get_tagged_value("i1", t2), 1)
        eq_(self.a1.get_tagged_value("i2", c), 2)
        eq_(self.a1.get_tagged_value("i3", sc), 3)

        for name, value in {"i0": 10, "i1": 11, "i2": 12, "i3": 13}.items():
            self.a1.set_tagged_value(name, value)

        for name, value in {"i0": 10, "i1": 11, "i2": 12, "i3": 13}.items():
            eq_(self.a1.get_tagged_value(name), value)

        eq_(self.a1.get_tagged_value("i0", t1), 10)
        eq_(self.a1.get_tagged_value("i1", t2), 11)
        eq_(self.a1.get_tagged_value("i2", c), 12)
        eq_(self.a1.get_tagged_value("i3", sc), 13)

    def test_attribute_values_inheritance_after_delete_superclass(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        c = CStereotype("C", superclasses=[t1, t2])
        sc = CStereotype("C", superclasses=c)

        t1.attributes = {"i0": 0}
        t2.attributes = {"i1": 1}
        c.attributes = {"i2": 2}
        sc.attributes = {"i3": 3}

        self.a.stereotypes = sc
        self.a1.stereotype_instances = sc

        t2.delete()

        for name, value in {"i0": 0, "i2": 2, "i3": 3}.items():
            eq_(self.a1.get_tagged_value(name), value)
        try:
            self.a1.get_tagged_value("i1")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'i1' unknown for 'a1'")

        eq_(self.a1.get_tagged_value("i0", t1), 0)
        try:
            self.a1.get_tagged_value("i1", t2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'i1' unknown for ''")
        eq_(self.a1.get_tagged_value("i2", c), 2)
        eq_(self.a1.get_tagged_value("i3", sc), 3)

        for name, value in {"i0": 10, "i2": 12, "i3": 13}.items():
            self.a1.set_tagged_value(name, value)
        try:
            self.a1.set_tagged_value("i1", 11)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'i1' unknown for 'a1'")

        for name, value in {"i0": 10, "i2": 12, "i3": 13}.items():
            eq_(self.a1.get_tagged_value(name), value)
        try:
            self.a1.get_tagged_value("i1")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'i1' unknown for 'a1'")

        eq_(self.a1.get_tagged_value("i0", t1), 10)
        try:
            self.a1.get_tagged_value("i1", t2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'i1' unknown for ''")
        eq_(self.a1.get_tagged_value("i2", c), 12)
        eq_(self.a1.get_tagged_value("i3", sc), 13)

    def test_attribute_values_same_name_inheritance(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        c = CStereotype("C", superclasses=[t1, t2])
        sc = CStereotype("C", superclasses=c)

        t1.attributes = {"i": 0}
        t2.attributes = {"i": 1}
        c.attributes = {"i": 2}
        sc.attributes = {"i": 3}

        self.a.stereotypes = t1
        self.a1.stereotype_instances = sc
        self.a2.stereotype_instances = c
        self.a3.stereotype_instances = t1

        eq_(self.a1.get_tagged_value("i"), 3)
        eq_(self.a2.get_tagged_value("i"), 2)
        eq_(self.a3.get_tagged_value("i"), 0)

        eq_(self.a1.get_tagged_value("i", sc), 3)
        eq_(self.a1.get_tagged_value("i", c), 2)
        eq_(self.a1.get_tagged_value("i", t2), 1)
        eq_(self.a1.get_tagged_value("i", t1), 0)
        eq_(self.a2.get_tagged_value("i", c), 2)
        eq_(self.a2.get_tagged_value("i", t2), 1)
        eq_(self.a2.get_tagged_value("i", t1), 0)
        eq_(self.a3.get_tagged_value("i", t1), 0)

        self.a1.set_tagged_value("i", 10)
        self.a2.set_tagged_value("i", 11)
        self.a3.set_tagged_value("i", 12)

        eq_(self.a1.get_tagged_value("i"), 10)
        eq_(self.a2.get_tagged_value("i"), 11)
        eq_(self.a3.get_tagged_value("i"), 12)

        eq_(self.a1.get_tagged_value("i", sc), 10)
        eq_(self.a1.get_tagged_value("i", c), 2)
        eq_(self.a1.get_tagged_value("i", t2), 1)
        eq_(self.a1.get_tagged_value("i", t1), 0)
        eq_(self.a2.get_tagged_value("i", c), 11)
        eq_(self.a2.get_tagged_value("i", t2), 1)
        eq_(self.a2.get_tagged_value("i", t1), 0)
        eq_(self.a3.get_tagged_value("i", t1), 12)

        self.a1.set_tagged_value("i", 130, sc)
        self.a1.set_tagged_value("i", 100, t1)
        self.a1.set_tagged_value("i", 110, t2)
        self.a1.set_tagged_value("i", 120, c)

        eq_(self.a1.get_tagged_value("i"), 130)

        eq_(self.a1.get_tagged_value("i", sc), 130)
        eq_(self.a1.get_tagged_value("i", c), 120)
        eq_(self.a1.get_tagged_value("i", t2), 110)
        eq_(self.a1.get_tagged_value("i", t1), 100)

    def test_tagged_values_inheritance_multiple_stereotypes(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        st_a = CStereotype("STA", superclasses=[t1, t2])
        sub_a = CStereotype("SubA", superclasses=[st_a])
        st_b = CStereotype("STB", superclasses=[t1, t2])
        sub_b = CStereotype("SubB", superclasses=[st_b])
        st_c = CStereotype("STC")
        sub_c = CStereotype("SubC", superclasses=[st_c])

        self.a.stereotypes = [t1, st_c]
        self.a1.stereotype_instances = [sub_a, sub_b, sub_c]

        t1.attributes = {"i0": 0}
        t2.attributes = {"i1": 1}
        st_a.attributes = {"i2": 2}
        sub_a.attributes = {"i3": 3}
        st_b.attributes = {"i4": 4}
        sub_b.attributes = {"i5": 5}
        st_c.attributes = {"i6": 6}
        sub_c.attributes = {"i7": 7}

        eq_(self.a1.get_tagged_value("i0"), 0)
        eq_(self.a1.get_tagged_value("i1"), 1)
        eq_(self.a1.get_tagged_value("i2"), 2)
        eq_(self.a1.get_tagged_value("i3"), 3)
        eq_(self.a1.get_tagged_value("i4"), 4)
        eq_(self.a1.get_tagged_value("i5"), 5)
        eq_(self.a1.get_tagged_value("i6"), 6)
        eq_(self.a1.get_tagged_value("i7"), 7)

        eq_(self.a1.get_tagged_value("i0", t1), 0)
        eq_(self.a1.get_tagged_value("i1", t2), 1)
        eq_(self.a1.get_tagged_value("i2", st_a), 2)
        eq_(self.a1.get_tagged_value("i3", sub_a), 3)
        eq_(self.a1.get_tagged_value("i4", st_b), 4)
        eq_(self.a1.get_tagged_value("i5", sub_b), 5)
        eq_(self.a1.get_tagged_value("i6", st_c), 6)
        eq_(self.a1.get_tagged_value("i7", sub_c), 7)

        self.a1.set_tagged_value("i0", 10)
        self.a1.set_tagged_value("i1", 11)
        self.a1.set_tagged_value("i2", 12)
        self.a1.set_tagged_value("i3", 13)
        self.a1.set_tagged_value("i4", 14)
        self.a1.set_tagged_value("i5", 15)
        self.a1.set_tagged_value("i6", 16)
        self.a1.set_tagged_value("i7", 17)

        eq_(self.a1.get_tagged_value("i0"), 10)
        eq_(self.a1.get_tagged_value("i1"), 11)
        eq_(self.a1.get_tagged_value("i2"), 12)
        eq_(self.a1.get_tagged_value("i3"), 13)
        eq_(self.a1.get_tagged_value("i4"), 14)
        eq_(self.a1.get_tagged_value("i5"), 15)
        eq_(self.a1.get_tagged_value("i6"), 16)
        eq_(self.a1.get_tagged_value("i7"), 17)

        self.a1.set_tagged_value("i0", 210, t1)
        self.a1.set_tagged_value("i1", 211, t2)
        self.a1.set_tagged_value("i2", 212, st_a)
        self.a1.set_tagged_value("i3", 213, sub_a)
        self.a1.set_tagged_value("i4", 214, st_b)
        self.a1.set_tagged_value("i5", 215, sub_b)
        self.a1.set_tagged_value("i6", 216, st_c)
        self.a1.set_tagged_value("i7", 217, sub_c)

        eq_(self.a1.get_tagged_value("i0"), 210)
        eq_(self.a1.get_tagged_value("i1"), 211)
        eq_(self.a1.get_tagged_value("i2"), 212)
        eq_(self.a1.get_tagged_value("i3"), 213)
        eq_(self.a1.get_tagged_value("i4"), 214)
        eq_(self.a1.get_tagged_value("i5"), 215)
        eq_(self.a1.get_tagged_value("i6"), 216)
        eq_(self.a1.get_tagged_value("i7"), 217)

    def test_tagged_values_non_pos_argument_in_association(self):
        s = CStereotype("S", attributes={
            "isBoolean": True,
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc",
            "list": ["a", "b"]})
        self.a.stereotypes = s

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")

        a1 = c1.association(c2, name="a1", multiplicity="*", role_name="c2",
                            source_multiplicity="1", source_role_name="c1",
                            derived_from=self.a,
                            stereotype_instances=s, tagged_values={"isBoolean": True, "intVal": 1, "floatVal": 1.1,
                                                                   "string": "abc", "list": ["a", "b"]})

        eq_(a1.stereotype_instances, [s])
        eq_(a1.get_tagged_value("isBoolean"), True)
        eq_(a1.get_tagged_value("intVal"), 1)
        eq_(a1.get_tagged_value("floatVal"), 1.1)
        eq_(a1.get_tagged_value("string"), "abc")
        eq_(a1.get_tagged_value("list"), ["a", "b"])

    def test_delete_tagged_values(self):
        s = CStereotype("S", attributes={
            "isBoolean": True,
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc",
            "list": ["a", "b"]})
        self.a.stereotypes = s
        self.a1.stereotype_instances = s
        self.a1.delete_tagged_value("isBoolean")
        self.a1.delete_tagged_value("intVal")
        list_value = self.a1.delete_tagged_value("list")
        eq_(self.a1.tagged_values, {'floatVal': 1.1, 'string': 'abc'})
        eq_(list_value, ['a', 'b'])

    def test_delete_tagged_values_with_superclass(self):
        sst = CStereotype("SST", attributes={
            "intVal": 20, "intVal2": 30})
        st = CStereotype("ST", superclasses=sst, attributes={
            "isBoolean": True,
            "intVal": 1})
        self.a.stereotypes = st
        self.a1.stereotype_instances = st

        self.a1.delete_tagged_value("isBoolean")
        self.a1.delete_tagged_value("intVal2")
        eq_(self.a1.tagged_values, {"intVal": 1})

        self.a1.set_tagged_value("intVal", 2, sst)
        self.a1.set_tagged_value("intVal", 3, st)
        eq_(self.a1.tagged_values, {"intVal": 3})
        self.a1.delete_tagged_value("intVal")
        eq_(self.a1.tagged_values, {"intVal": 2})

        self.a1.set_tagged_value("intVal", 2, sst)
        self.a1.set_tagged_value("intVal", 3, st)
        self.a1.delete_tagged_value("intVal", st)
        eq_(self.a1.tagged_values, {"intVal": 2})

        self.a1.set_tagged_value("intVal", 2, sst)
        self.a1.set_tagged_value("intVal", 3, st)
        self.a1.delete_tagged_value("intVal", sst)
        eq_(self.a1.tagged_values, {"intVal": 3})

    def test_delete_tagged_values_exceptional_cases(self):
        s = CStereotype("S", attributes={"b": True})
        self.a.stereotypes = s
        self.a1.stereotype_instances = s
        self.a2.delete()

        try:
            self.a2.get_tagged_value("b")
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't get tagged value 'b' on deleted link")

        try:
            self.a2.set_tagged_value("b", 1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't set tagged value 'b' on deleted link")

        try:
            self.a2.delete_tagged_value("b")
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't delete tagged value 'b' on deleted link")

        try:
            self.a2.tagged_values = {"b": 1}
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't set tagged values on deleted link")

        try:
            # we just use list here, in order to not get a warning that self.l2.tagged_values has no effect
            list(self.a2.tagged_values)
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't get tagged values on deleted link")

        self.a1.stereotype_instances = s
        try:
            self.a1.delete_tagged_value("x")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'x' unknown for 'a1'")


if __name__ == "__main__":
    nose.main()
