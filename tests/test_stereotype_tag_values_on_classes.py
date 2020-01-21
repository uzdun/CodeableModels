import nose
from nose.tools import eq_

from codeable_models import CMetaclass, CStereotype, CClass, CObject, CException, CEnum
from tests.testing_commons import exception_expected_


class TestStereotypeTagValuesOnClasses:
    def setup(self):
        self.mcl = CMetaclass("MCL")
        self.st = CStereotype("ST")
        self.mcl.stereotypes = self.st
        self.cl = CClass(self.mcl, "C", stereotype_instances=self.st)

    def test_tagged_values_on_primitive_type_attributes(self):
        s = CStereotype("S", attributes={
            "isBoolean": True,
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc",
            "list": ["a", "b"]})
        self.mcl.stereotypes = s
        cl = CClass(self.mcl, "C", stereotype_instances=s)

        eq_(cl.get_tagged_value("isBoolean"), True)
        eq_(cl.get_tagged_value("intVal"), 1)
        eq_(cl.get_tagged_value("floatVal"), 1.1)
        eq_(cl.get_tagged_value("string"), "abc")
        eq_(cl.get_tagged_value("list"), ["a", "b"])

        cl.set_tagged_value("isBoolean", False)
        cl.set_tagged_value("intVal", 2)
        cl.set_tagged_value("floatVal", 2.1)
        cl.set_tagged_value("string", "y")

        eq_(cl.get_tagged_value("isBoolean"), False)
        eq_(cl.get_tagged_value("intVal"), 2)
        eq_(cl.get_tagged_value("floatVal"), 2.1)
        eq_(cl.get_tagged_value("string"), "y")

        cl.set_tagged_value("list", [])
        eq_(cl.get_tagged_value("list"), [])
        cl.set_tagged_value("list", [1, 2, 3])
        eq_(cl.get_tagged_value("list"), [1, 2, 3])

    def test_attribute_of_tagged_value_unknown(self):
        try:
            self.cl.get_tagged_value("x")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'x' unknown for 'C'")

        self.mcl.attributes = {"isBoolean": True, "intVal": 1}
        try:
            self.cl.set_tagged_value("x", 1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'x' unknown for 'C'")

    def test_integers_as_float_tagged_values(self):
        self.st.attributes = {"floatVal": float}
        self.cl.set_tagged_value("floatVal", 15)
        eq_(self.cl.get_tagged_value("floatVal"), 15)

    def test_object_type_attribute_tagged_values(self):
        attribute_type = CClass(self.mcl, "AttrType")
        attribute_value = CObject(attribute_type, "attribute_value")
        self.st.attributes = {"attrTypeObj": attribute_value}
        object_attribute = self.st.get_attribute("attrTypeObj")
        eq_(object_attribute.type, attribute_type)
        eq_(self.cl.get_tagged_value("attrTypeObj"), attribute_value)

        non_attribute_value = CObject(CClass(self.mcl), "non_attribute_value")
        try:
            self.cl.set_tagged_value("attrTypeObj", non_attribute_value)
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
        eq_(self.cl.get_tagged_value("attrTypeCl"), attribute_value)

        non_attribute_value = CClass(CMetaclass("MX"), "non_attribute_value")
        try:
            self.cl.set_tagged_value("attrTypeCl", non_attribute_value)
            exception_expected_()
        except CException as e:
            eq_(e.value, "type of 'non_attribute_value' is not matching type of attribute 'attrTypeCl'")

    def test_add_object_attribute_get_set_tagged_value(self):
        attribute_type = CClass(self.mcl, "AttrType")
        attribute_value = CObject(attribute_type, "attribute_value")
        self.st.attributes = {
            "attrTypeObj1": attribute_type, "attrTypeObj2": attribute_value
        }
        eq_(self.cl.get_tagged_value("attrTypeObj1"), None)
        eq_(self.cl.get_tagged_value("attrTypeObj2"), attribute_value)

    def test_object_attribute_tagged_value_of_superclass_type(self):
        attribute_super_type = CClass(self.mcl, "AttrSuperType")
        attribute_type = CClass(self.mcl, "AttrType", superclasses=attribute_super_type)
        attribute_value = CObject(attribute_type, "attribute_value")
        self.st.attributes = {
            "attrTypeObj1": attribute_super_type, "attrTypeObj2": attribute_value
        }
        self.cl.set_tagged_value("attrTypeObj1", attribute_value)
        self.cl.set_tagged_value("attrTypeObj2", attribute_value)
        eq_(self.cl.get_tagged_value("attrTypeObj1"), attribute_value)
        eq_(self.cl.get_tagged_value("attrTypeObj2"), attribute_value)

    def test_tagged_values_on_attributes_with_no_default_values(self):
        attribute_type = CClass(self.mcl, "AttrType")
        enum_type = CEnum("EnumT", values=["A", "B", "C"])
        st = CStereotype("S", attributes={
            "b": bool,
            "i": int,
            "f": float,
            "s": str,
            "l": list,
            "C": attribute_type,
            "e": enum_type})
        mcl = CMetaclass("M", stereotypes=st)
        cl = CClass(mcl, "C", stereotype_instances=st)
        for n in ["b", "i", "f", "s", "l", "C", "e"]:
            eq_(cl.get_tagged_value(n), None)

    def test_tagged_values_defined_in_constructor(self):
        object_value_type = CClass(CMetaclass())
        object_value = CObject(object_value_type, "object_value")

        st = CStereotype("S", attributes={
            "isBoolean": True,
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc",
            "list": ["a", "b"],
            "obj": object_value_type})
        mcl = CMetaclass("M", stereotypes=st)
        cl = CClass(mcl, "C", stereotype_instances=st, tagged_values={
            "isBoolean": False, "intVal": 2, "floatVal": 2.1,
            "string": "y", "list": [], "obj": object_value})

        eq_(cl.get_tagged_value("isBoolean"), False)
        eq_(cl.get_tagged_value("intVal"), 2)
        eq_(cl.get_tagged_value("floatVal"), 2.1)
        eq_(cl.get_tagged_value("string"), "y")
        eq_(cl.get_tagged_value("list"), [])
        eq_(cl.get_tagged_value("obj"), object_value)

        eq_(cl.tagged_values, {"isBoolean": False, "intVal": 2, "floatVal": 2.1,
                               "string": "y", "list": [], "obj": object_value})

    def test_tagged_values_setter_overwrite(self):
        st = CStereotype("S", attributes={
            "isBoolean": True,
            "intVal": 1})
        mcl = CMetaclass("M", stereotypes=st)
        cl = CClass(mcl, "C", stereotype_instances=st, tagged_values={
            "isBoolean": False, "intVal": 2})
        cl.tagged_values = {"isBoolean": True, "intVal": 20}
        eq_(cl.get_tagged_value("isBoolean"), True)
        eq_(cl.get_tagged_value("intVal"), 20)
        eq_(cl.tagged_values, {'isBoolean': True, 'intVal': 20})
        cl.tagged_values = {}
        # tagged values should not delete existing values
        eq_(cl.tagged_values, {"isBoolean": True, "intVal": 20})

    def test_tagged_values_setter_with_superclass(self):
        sst = CStereotype("SST", attributes={
            "intVal": 20, "intVal2": 30})
        st = CStereotype("S", superclasses=sst, attributes={
            "isBoolean": True,
            "intVal": 1})
        mcl = CMetaclass("M", stereotypes=st)
        cl = CClass(mcl, "C", stereotype_instances=st, tagged_values={
            "isBoolean": False})
        eq_(cl.tagged_values, {"isBoolean": False, "intVal": 1, "intVal2": 30})
        cl.set_tagged_value("intVal", 12, sst)
        cl.set_tagged_value("intVal", 15, st)
        cl.set_tagged_value("intVal2", 16, sst)
        eq_(cl.tagged_values, {"isBoolean": False, "intVal": 15, "intVal2": 16})
        eq_(cl.get_tagged_value("intVal", sst), 12)
        eq_(cl.get_tagged_value("intVal", st), 15)

    def test_tagged_values_setter_malformed_description(self):
        st = CStereotype("S", attributes={
            "isBoolean": True,
            "intVal": 1})
        mcl = CMetaclass("M", stereotypes=st)
        cl = CClass(mcl, "C", stereotype_instances=st)
        try:
            cl.tagged_values = [1, 2, 3]
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
        eq_(self.cl.get_tagged_value("e1"), None)
        eq_(self.cl.get_tagged_value("e2"), "A")
        self.cl.set_tagged_value("e1", "B")
        self.cl.set_tagged_value("e2", "C")
        eq_(self.cl.get_tagged_value("e1"), "B")
        eq_(self.cl.get_tagged_value("e2"), "C")
        try:
            self.cl.set_tagged_value("e1", "X")
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
        eq_(self.cl.get_tagged_value("e1"), None)
        eq_(self.cl.get_tagged_value("e2"), "A")

    def test_attribute_value_type_check_bool1(self):
        self.st.attributes = {"t": bool}
        cl = CClass(self.mcl, "C", stereotype_instances=self.st)
        try:
            cl.set_tagged_value("t", self.mcl)
            exception_expected_()
        except CException as e:
            eq_(f"value for attribute 't' is not a known attribute type", e.value)

    def test_attribute_value_type_check_bool2(self):
        self.st.attributes = {"t": bool}
        cl = CClass(self.mcl, "C", stereotype_instances=self.st)
        try:
            cl.set_tagged_value("t", 1)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_int(self):
        self.st.attributes = {"t": int}
        cl = CClass(self.mcl, "C", stereotype_instances=self.st)
        try:
            cl.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_float(self):
        self.st.attributes = {"t": float}
        cl = CClass(self.mcl, "C", stereotype_instances=self.st)
        try:
            cl.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_str(self):
        self.st.attributes = {"t": str}
        cl = CClass(self.mcl, "C", stereotype_instances=self.st)
        try:
            cl.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_list(self):
        self.st.attributes = {"t": list}
        cl = CClass(self.mcl, "C", stereotype_instances=self.st)
        try:
            cl.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_object(self):
        attribute_type = CClass(CMetaclass(), "AttrType")
        self.st.attributes = {"t": attribute_type}
        cl = CClass(self.mcl, "C", stereotype_instances=self.st)
        try:
            cl.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_value_type_check_enum(self):
        enum_type = CEnum("EnumT", values=["A", "B", "C"])
        self.st.attributes = {"t": enum_type}
        cl = CClass(self.mcl, "C", stereotype_instances=self.st)
        try:
            cl.set_tagged_value("t", True)
            exception_expected_()
        except CException as e:
            eq_(f"value type for attribute 't' does not match attribute type", e.value)

    def test_attribute_deleted(self):
        self.st.attributes = {
            "isBoolean": True,
            "intVal": 15}
        cl = CClass(self.mcl, "C", stereotype_instances=self.st)
        eq_(cl.get_tagged_value("intVal"), 15)
        self.st.attributes = {
            "isBoolean": False}
        eq_(cl.get_tagged_value("isBoolean"), True)
        try:
            cl.get_tagged_value("intVal")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'intVal' unknown for 'C'")
        try:
            cl.set_tagged_value("intVal", 1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'intVal' unknown for 'C'")

    def test_attribute_deleted_no_default(self):
        self.st.attributes = {
            "isBoolean": bool,
            "intVal": int}
        self.st.attributes = {"isBoolean": bool}
        eq_(self.cl.get_tagged_value("isBoolean"), None)
        try:
            self.cl.get_tagged_value("intVal")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'intVal' unknown for 'C'")
        try:
            self.cl.set_tagged_value("intVal", 1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'intVal' unknown for 'C'")

    def test_attributes_overwrite(self):
        self.st.attributes = {
            "isBoolean": True,
            "intVal": 15}
        cl = CClass(self.mcl, "C", stereotype_instances=self.st)
        eq_(cl.get_tagged_value("intVal"), 15)
        try:
            cl.get_tagged_value("floatVal")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'floatVal' unknown for 'C'")
        cl.set_tagged_value("intVal", 18)
        self.st.attributes = {
            "isBoolean": False,
            "intVal": 19,
            "floatVal": 25.1}
        eq_(cl.get_tagged_value("isBoolean"), True)
        eq_(cl.get_tagged_value("floatVal"), 25.1)
        eq_(cl.get_tagged_value("intVal"), 18)
        cl.set_tagged_value("floatVal", 1.2)
        eq_(cl.get_tagged_value("floatVal"), 1.2)

    def test_attributes_overwrite_no_defaults(self):
        self.st.attributes = {
            "isBoolean": bool,
            "intVal": int}
        eq_(self.cl.get_tagged_value("isBoolean"), None)
        self.cl.set_tagged_value("isBoolean", False)
        self.st.attributes = {
            "isBoolean": bool,
            "intVal": int,
            "floatVal": float}
        eq_(self.cl.get_tagged_value("isBoolean"), False)
        eq_(self.cl.get_tagged_value("floatVal"), None)
        eq_(self.cl.get_tagged_value("intVal"), None)
        self.cl.set_tagged_value("floatVal", 1.2)
        eq_(self.cl.get_tagged_value("floatVal"), 1.2)

    def test_attributes_deleted_on_subclass(self):
        self.st.attributes = {
            "isBoolean": True,
            "intVal": 1}
        st2 = CStereotype("S2", attributes={
            "isBoolean": False}, superclasses=self.st)
        mcl = CMetaclass("M", stereotypes=st2)
        cl = CClass(mcl, "C", stereotype_instances=st2)

        eq_(cl.get_tagged_value("isBoolean"), False)
        eq_(cl.get_tagged_value("isBoolean", self.st), True)
        eq_(cl.get_tagged_value("isBoolean", st2), False)

        st2.attributes = {}

        eq_(cl.get_tagged_value("isBoolean"), True)
        eq_(cl.get_tagged_value("intVal"), 1)
        eq_(cl.get_tagged_value("isBoolean", self.st), True)
        try:
            cl.get_tagged_value("isBoolean", st2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'isBoolean' unknown for 'S2'")

    def test_attributes_deleted_on_subclass_no_defaults(self):
        self.st.attributes = {
            "isBoolean": bool,
            "intVal": int}
        st2 = CStereotype("S2", attributes={
            "isBoolean": bool}, superclasses=self.st)
        mcl = CMetaclass("M", stereotypes=st2)
        cl = CClass(mcl, "C", stereotype_instances=st2)

        eq_(cl.get_tagged_value("isBoolean"), None)
        eq_(cl.get_tagged_value("isBoolean", self.st), None)
        eq_(cl.get_tagged_value("isBoolean", st2), None)

        st2.attributes = {}

        eq_(cl.get_tagged_value("isBoolean"), None)
        eq_(cl.get_tagged_value("intVal"), None)
        eq_(cl.get_tagged_value("isBoolean", self.st), None)
        try:
            cl.get_tagged_value("isBoolean", st2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'isBoolean' unknown for 'S2'")

    def test_wrong_stereotype_in_tagged_value(self):
        self.st.attributes = {
            "isBoolean": True}
        st2 = CStereotype("S2", attributes={
            "isBoolean": True})
        mcl = CMetaclass("M", stereotypes=self.st)
        cl = CClass(mcl, "C", stereotype_instances=self.st)

        cl.set_tagged_value("isBoolean", False)

        try:
            cl.set_tagged_value("isBoolean", False, st2)
        except CException as e:
            eq_(e.value, "stereotype 'S2' is not a stereotype of element")

        eq_(cl.get_tagged_value("isBoolean"), False)

        try:
            cl.get_tagged_value("isBoolean", st2)
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

        mcl = CMetaclass("M", stereotypes=sc)
        cl = CClass(mcl, "C", stereotype_instances=sc)

        for name, value in {"i0": 0, "i1": 1, "i2": 2, "i3": 3}.items():
            eq_(cl.get_tagged_value(name), value)

        eq_(cl.get_tagged_value("i0", t1), 0)
        eq_(cl.get_tagged_value("i1", t2), 1)
        eq_(cl.get_tagged_value("i2", c), 2)
        eq_(cl.get_tagged_value("i3", sc), 3)

        for name, value in {"i0": 10, "i1": 11, "i2": 12, "i3": 13}.items():
            cl.set_tagged_value(name, value)

        for name, value in {"i0": 10, "i1": 11, "i2": 12, "i3": 13}.items():
            eq_(cl.get_tagged_value(name), value)

        eq_(cl.get_tagged_value("i0", t1), 10)
        eq_(cl.get_tagged_value("i1", t2), 11)
        eq_(cl.get_tagged_value("i2", c), 12)
        eq_(cl.get_tagged_value("i3", sc), 13)

    def test_attribute_values_inheritance_after_delete_superclass(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        c = CStereotype("C", superclasses=[t1, t2])
        sc = CStereotype("C", superclasses=c)

        t1.attributes = {"i0": 0}
        t2.attributes = {"i1": 1}
        c.attributes = {"i2": 2}
        sc.attributes = {"i3": 3}

        mcl = CMetaclass("M", stereotypes=sc)
        cl = CClass(mcl, "C", stereotype_instances=sc)

        t2.delete()

        for name, value in {"i0": 0, "i2": 2, "i3": 3}.items():
            eq_(cl.get_tagged_value(name), value)
        try:
            cl.get_tagged_value("i1")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'i1' unknown for 'C'")

        eq_(cl.get_tagged_value("i0", t1), 0)
        try:
            cl.get_tagged_value("i1", t2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'i1' unknown for ''")
        eq_(cl.get_tagged_value("i2", c), 2)
        eq_(cl.get_tagged_value("i3", sc), 3)

        for name, value in {"i0": 10, "i2": 12, "i3": 13}.items():
            cl.set_tagged_value(name, value)
        try:
            cl.set_tagged_value("i1", 11)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'i1' unknown for 'C'")

        for name, value in {"i0": 10, "i2": 12, "i3": 13}.items():
            eq_(cl.get_tagged_value(name), value)
        try:
            cl.get_tagged_value("i1")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'i1' unknown for 'C'")

        eq_(cl.get_tagged_value("i0", t1), 10)
        try:
            cl.get_tagged_value("i1", t2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'i1' unknown for ''")
        eq_(cl.get_tagged_value("i2", c), 12)
        eq_(cl.get_tagged_value("i3", sc), 13)

    def test_attribute_values_same_name_inheritance(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        c = CStereotype("C", superclasses=[t1, t2])
        sc = CStereotype("C", superclasses=c)

        t1.attributes = {"i": 0}
        t2.attributes = {"i": 1}
        c.attributes = {"i": 2}
        sc.attributes = {"i": 3}

        mcl = CMetaclass("M", stereotypes=t1)
        cl1 = CClass(mcl, "C", stereotype_instances=sc)
        cl2 = CClass(mcl, "C", stereotype_instances=c)
        cl3 = CClass(mcl, "C", stereotype_instances=t1)

        eq_(cl1.get_tagged_value("i"), 3)
        eq_(cl2.get_tagged_value("i"), 2)
        eq_(cl3.get_tagged_value("i"), 0)

        eq_(cl1.get_tagged_value("i", sc), 3)
        eq_(cl1.get_tagged_value("i", c), 2)
        eq_(cl1.get_tagged_value("i", t2), 1)
        eq_(cl1.get_tagged_value("i", t1), 0)
        eq_(cl2.get_tagged_value("i", c), 2)
        eq_(cl2.get_tagged_value("i", t2), 1)
        eq_(cl2.get_tagged_value("i", t1), 0)
        eq_(cl3.get_tagged_value("i", t1), 0)

        cl1.set_tagged_value("i", 10)
        cl2.set_tagged_value("i", 11)
        cl3.set_tagged_value("i", 12)

        eq_(cl1.get_tagged_value("i"), 10)
        eq_(cl2.get_tagged_value("i"), 11)
        eq_(cl3.get_tagged_value("i"), 12)

        eq_(cl1.get_tagged_value("i", sc), 10)
        eq_(cl1.get_tagged_value("i", c), 2)
        eq_(cl1.get_tagged_value("i", t2), 1)
        eq_(cl1.get_tagged_value("i", t1), 0)
        eq_(cl2.get_tagged_value("i", c), 11)
        eq_(cl2.get_tagged_value("i", t2), 1)
        eq_(cl2.get_tagged_value("i", t1), 0)
        eq_(cl3.get_tagged_value("i", t1), 12)

        cl1.set_tagged_value("i", 130, sc)
        cl1.set_tagged_value("i", 100, t1)
        cl1.set_tagged_value("i", 110, t2)
        cl1.set_tagged_value("i", 120, c)

        eq_(cl1.get_tagged_value("i"), 130)

        eq_(cl1.get_tagged_value("i", sc), 130)
        eq_(cl1.get_tagged_value("i", c), 120)
        eq_(cl1.get_tagged_value("i", t2), 110)
        eq_(cl1.get_tagged_value("i", t1), 100)

    def test_tagged_values_inheritance_multiple_stereotypes(self):
        t1 = CStereotype("T1")
        t2 = CStereotype("T2")
        st_a = CStereotype("STA", superclasses=[t1, t2])
        sub_a = CStereotype("SubA", superclasses=[st_a])
        st_b = CStereotype("STB", superclasses=[t1, t2])
        sub_b = CStereotype("SubB", superclasses=[st_b])
        st_c = CStereotype("STC")
        sub_c = CStereotype("SubC", superclasses=[st_c])

        mcl = CMetaclass("M", stereotypes=[t1, st_c])
        cl = CClass(mcl, "C", stereotype_instances=[sub_a, sub_b, sub_c])

        t1.attributes = {"i0": 0}
        t2.attributes = {"i1": 1}
        st_a.attributes = {"i2": 2}
        sub_a.attributes = {"i3": 3}
        st_b.attributes = {"i4": 4}
        sub_b.attributes = {"i5": 5}
        st_c.attributes = {"i6": 6}
        sub_c.attributes = {"i7": 7}

        eq_(cl.get_tagged_value("i0"), 0)
        eq_(cl.get_tagged_value("i1"), 1)
        eq_(cl.get_tagged_value("i2"), 2)
        eq_(cl.get_tagged_value("i3"), 3)
        eq_(cl.get_tagged_value("i4"), 4)
        eq_(cl.get_tagged_value("i5"), 5)
        eq_(cl.get_tagged_value("i6"), 6)
        eq_(cl.get_tagged_value("i7"), 7)

        eq_(cl.get_tagged_value("i0", t1), 0)
        eq_(cl.get_tagged_value("i1", t2), 1)
        eq_(cl.get_tagged_value("i2", st_a), 2)
        eq_(cl.get_tagged_value("i3", sub_a), 3)
        eq_(cl.get_tagged_value("i4", st_b), 4)
        eq_(cl.get_tagged_value("i5", sub_b), 5)
        eq_(cl.get_tagged_value("i6", st_c), 6)
        eq_(cl.get_tagged_value("i7", sub_c), 7)

        cl.set_tagged_value("i0", 10)
        cl.set_tagged_value("i1", 11)
        cl.set_tagged_value("i2", 12)
        cl.set_tagged_value("i3", 13)
        cl.set_tagged_value("i4", 14)
        cl.set_tagged_value("i5", 15)
        cl.set_tagged_value("i6", 16)
        cl.set_tagged_value("i7", 17)

        eq_(cl.get_tagged_value("i0"), 10)
        eq_(cl.get_tagged_value("i1"), 11)
        eq_(cl.get_tagged_value("i2"), 12)
        eq_(cl.get_tagged_value("i3"), 13)
        eq_(cl.get_tagged_value("i4"), 14)
        eq_(cl.get_tagged_value("i5"), 15)
        eq_(cl.get_tagged_value("i6"), 16)
        eq_(cl.get_tagged_value("i7"), 17)

        cl.set_tagged_value("i0", 210, t1)
        cl.set_tagged_value("i1", 211, t2)
        cl.set_tagged_value("i2", 212, st_a)
        cl.set_tagged_value("i3", 213, sub_a)
        cl.set_tagged_value("i4", 214, st_b)
        cl.set_tagged_value("i5", 215, sub_b)
        cl.set_tagged_value("i6", 216, st_c)
        cl.set_tagged_value("i7", 217, sub_c)

        eq_(cl.get_tagged_value("i0"), 210)
        eq_(cl.get_tagged_value("i1"), 211)
        eq_(cl.get_tagged_value("i2"), 212)
        eq_(cl.get_tagged_value("i3"), 213)
        eq_(cl.get_tagged_value("i4"), 214)
        eq_(cl.get_tagged_value("i5"), 215)
        eq_(cl.get_tagged_value("i6"), 216)
        eq_(cl.get_tagged_value("i7"), 217)

    def test_delete_tagged_values(self):
        s = CStereotype("S", attributes={
            "isBoolean": True,
            "intVal": 1,
            "floatVal": 1.1,
            "string": "abc",
            "list": ["a", "b"]})
        self.mcl.stereotypes = s
        cl = CClass(self.mcl, "C", stereotype_instances=s)
        cl.delete_tagged_value("isBoolean")
        cl.delete_tagged_value("intVal")
        list_value = cl.delete_tagged_value("list")
        eq_(cl.tagged_values, {'floatVal': 1.1, 'string': 'abc'})
        eq_(list_value, ['a', 'b'])

    def test_delete_tagged_values_with_superclass(self):
        sst = CStereotype("SST", attributes={
            "intVal": 20, "intVal2": 30})
        st = CStereotype("ST", superclasses=sst, attributes={
            "isBoolean": True,
            "intVal": 1})
        self.mcl.stereotypes = st

        cl = CClass(self.mcl, "C", stereotype_instances=st, tagged_values={
            "isBoolean": False})
        cl.delete_tagged_value("isBoolean")
        cl.delete_tagged_value("intVal2")
        eq_(cl.tagged_values, {"intVal": 1})

        cl.set_tagged_value("intVal", 2, sst)
        cl.set_tagged_value("intVal", 3, st)
        eq_(cl.tagged_values, {"intVal": 3})
        cl.delete_tagged_value("intVal")
        eq_(cl.tagged_values, {"intVal": 2})

        cl.set_tagged_value("intVal", 2, sst)
        cl.set_tagged_value("intVal", 3, st)
        cl.delete_tagged_value("intVal", st)
        eq_(cl.tagged_values, {"intVal": 2})

        cl.set_tagged_value("intVal", 2, sst)
        cl.set_tagged_value("intVal", 3, st)
        cl.delete_tagged_value("intVal", sst)
        eq_(cl.tagged_values, {"intVal": 3})

    def test_tagged_values_exceptional_cases(self):
        s = CStereotype("S", attributes={"b": True})
        self.mcl.stereotypes = s
        cl1 = CClass(self.mcl, "C", stereotype_instances=s)
        cl1.delete()

        try:
            cl1.get_tagged_value("b")
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't get tagged value 'b' on deleted class")

        try:
            cl1.set_tagged_value("b", 1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't set tagged value 'b' on deleted class")

        try:
            cl1.delete_tagged_value("b")
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't delete tagged value 'b' on deleted class")

        try:
            cl1.tagged_values = {"b": 1}
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't set tagged values on deleted class")

        try:
            # we just use list here, in order to not get a warning that cl1.tagged_values has no effect
            list(cl1.tagged_values)
            exception_expected_()
        except CException as e:
            eq_(e.value, "can't get tagged values on deleted class")

        cl = CClass(self.mcl, "C", stereotype_instances=s)
        try:
            cl.delete_tagged_value("x")
            exception_expected_()
        except CException as e:
            eq_(e.value, "tagged value 'x' unknown for 'C'")


if __name__ == "__main__":
    nose.main()
