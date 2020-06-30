import nose
from nose.tools import eq_

from codeable_models import CMetaclass, CClass, CObject, CException, set_links, add_links, CStereotype, CBundle
from codeable_models.internal.commons import get_links
from tests.testing_commons import exception_expected_


class TestLinkObjectsForClasses:
    def setup(self):
        self.mcl = CMetaclass("MCL")
        self.cl = CClass(self.mcl, "CL")

    def test_reference_to_link(self):
        code = CClass(self.mcl, "Code")
        source = CClass(self.mcl, "Source")
        code_association = code.association(source, "[contained_code] * -> [source] *")
        code_a = CClass(self.mcl, "Code A", superclasses=code)
        code_b = CClass(self.mcl, "Code B", superclasses=code)
        a_b_association = code_a.association(code_b, "a_b: [code_a] * -> [code_b] *", superclasses=code)

        source_1 = CObject(source, "source_1")

        code_a1 = CObject(code_a, "code_a1")
        code_b1 = CObject(code_b, "code_b1")
        code_b2 = CObject(code_b, "code_b2")
        code_b3 = CObject(code_b, "code_b3")
        a_b_links = add_links({code_a1: [code_b1, code_b2]}, association=a_b_association)

        code_links = add_links({source_1: [code_a1, code_b2, code_b1, a_b_links[0], a_b_links[1]]},
                               role_name="contained_code")
        eq_(len(code_links), 5)

        # test getter methods on object
        eq_(set(source_1.get_linked(role_name="contained_code")),
            {code_a1, code_b2, code_b1, a_b_links[0], a_b_links[1]})
        eq_(set(source_1.linked), {code_a1, code_b2, code_b1, a_b_links[0], a_b_links[1]})
        eq_(set(source_1.links), set(code_links))
        eq_(set(source_1.get_links_for_association(code_association)), set(code_links))
        eq_(set(get_links([source_1])), set(code_links))

        # test getter methods on link
        eq_(a_b_links[0].get_linked(role_name="source"), [source_1])
        eq_(a_b_links[0].linked, [source_1])
        eq_(a_b_links[0].links, [code_links[3]])
        eq_(a_b_links[0].get_links_for_association(code_association), [code_links[3]])
        eq_(set(get_links([a_b_links[0]])), {code_links[3]})
        eq_(set(get_links([code_a1, a_b_links[0], a_b_links[1]])),
            {code_links[0], a_b_links[0], a_b_links[1], code_links[3], code_links[4]})

        # test add/delete links
        code_b3_link = code_a1.add_links(code_b3)[0]
        source_1.add_links(code_b3_link)
        eq_(set(code_a1.linked), {code_b1, code_b2, source_1, code_b3})
        eq_(set(source_1.linked), {code_a1, code_b2, code_b1, a_b_links[0], a_b_links[1], code_b3_link})
        eq_(code_b3_link.linked, [source_1])
        a_b_links[1].delete_links([source_1])
        eq_(set(source_1.linked), {code_a1, code_b2, code_b1, a_b_links[0], code_b3_link})
        source_1.delete_links([code_a1, a_b_links[0]])
        eq_(set(source_1.linked), {code_b2, code_b1, code_b3_link})

        # test whether metaclass links fail on class
        mcl_a = CMetaclass("M")
        mcl_b = CMetaclass("Source")
        mcl_association = mcl_a.association(mcl_b, "[a] * -> [b] *")

        cl_a = CClass(mcl_a, "cla")
        cl_b = CClass(mcl_a, "clb")
        class_link = add_links({cl_a: [cl_b]}, association=mcl_association)[0]

        try:
            add_links({source_1: [code_a1, code_b2, code_b1, class_link]}, role_name="contained_code")
            exception_expected_()
        except CException as e:
            eq_("link target is a class link, but source is an object", e.value)

    def test_link_association_has_a_compatible_superclass(self):
        code = CClass(self.mcl, "Code")
        source = CClass(self.mcl, "Source")
        code.association(source, "[contained_code] * -> [source] *")
        code_a = CClass(self.mcl, "Code A", superclasses=code)
        code_b = CClass(self.mcl, "Code B", superclasses=code)
        a_b_association = code_a.association(code_b, "a_b: [code_a] * -> [code_b] *")

        source_1 = CObject(source, "source_1")

        code_a1 = CObject(code_a, "code_a1")
        code_b1 = CObject(code_b, "code_b1")
        code_b2 = CObject(code_b, "code_b2")
        links = add_links({code_a1: [code_b1, code_b2]}, association=a_b_association)

        try:
            add_links({source_1: [code_a1, code_b2, code_b1, links[0], links[1]]},
                      role_name="contained_code")
            exception_expected_()
        except CException as e:
            eq_("the link's association is missing a compatible classifier", e.value)

        a_b_association.superclasses = self.cl
        try:
            add_links({source_1: [code_a1, code_b2, code_b1, links[0], links[1]]},
                      role_name="contained_code")
            exception_expected_()
        except CException as e:
            eq_("the link's association is missing a compatible classifier", e.value)

        a_b_association.superclasses = code_b
        add_links({source_1: [code_a1, code_b2, code_b1, links[0], links[1]]},
                  role_name="contained_code")

    def test_association_to_association_not_possible(self):
        clx = CClass(self.mcl, "X")
        cla = CClass(self.mcl, "A")
        clb = CClass(self.mcl, "B")
        a_b_association = cla.association(clb, "a_b: [a] * -> [b] *")
        try:
            clx.association(a_b_association, "[x] * -> [a_b_association] *")
            exception_expected_()
        except CException as e:
            eq_("class 'X' is not compatible with association target 'a_b'", e.value)

    def test_link_to_link(self):
        collection1 = CClass(self.mcl, "Collection1")
        collection2 = CClass(self.mcl, "Collection2")
        collections_association = collection1.association(collection2,
                                                          "element references: [references] * -> [referenced] *")
        type_a = CClass(self.mcl, "Type A", superclasses=collection1)
        type_b = CClass(self.mcl, "Type B", superclasses=collection1)
        a_b_association = type_a.association(type_b, "a_b: [type_a] * -> [type_b] *", superclasses=collection1)
        type_c = CClass(self.mcl, "Type C", superclasses=collection2)
        type_d = CClass(self.mcl, "Type D", superclasses=[collection1, collection2])
        c_d_association = type_c.association(type_d, "c_d: [type_c] * -> [type_d] *", superclasses=collection2)
        a_d_association = type_a.association(type_d, "a_d: [type_a] * -> [type_d] *",
                                             superclasses=[collection1, collection2])

        a1 = CObject(type_a, "a1")
        b1 = CObject(type_b, "b1")
        b2 = CObject(type_b, "b2")
        c1 = CObject(type_c, "c1")
        c2 = CObject(type_c, "c2")
        d1 = CObject(type_d, "d1")

        a_b_links = add_links({a1: [b1, b2]}, association=a_b_association)
        c_d_links = add_links({d1: [c1, c2]}, association=c_d_association)
        a_d_links = add_links({a1: [d1]}, association=a_d_association)

        references_links = add_links({a_b_links[0]: c_d_links[0],
                                      a_b_links[1]: [c1, c2, d1, c_d_links[1], c_d_links[0]],
                                      a_d_links[0]: [a_d_links[0], c_d_links[1], c1, d1]}, role_name="referenced")

        eq_(set(a_b_links[0].get_linked(role_name="referenced")),
            {c_d_links[0]})
        eq_(set(a_b_links[0].linked), {c_d_links[0]})
        eq_(set(a_b_links[0].links), {references_links[0]})
        eq_(set(a_b_links[0].get_links_for_association(collections_association)), {references_links[0]})
        eq_(set(get_links([a_b_links[0]])), {references_links[0]})

        eq_(set(a_b_links[1].get_linked(role_name="referenced")),
            {c1, c2, d1, c_d_links[1], c_d_links[0]})
        eq_(set(a_b_links[1].linked), {c1, c2, d1, c_d_links[1], c_d_links[0]})
        correct_links_set = {references_links[1], references_links[2], references_links[3], references_links[4],
                             references_links[5]}
        eq_(set(a_b_links[1].links), correct_links_set)
        eq_(set(a_b_links[1].get_links_for_association(collections_association)), correct_links_set)
        eq_(set(get_links([a_b_links[1]])), correct_links_set)

        eq_(set(a_d_links[0].get_linked(role_name="referenced")),
            {a_d_links[0], c_d_links[1], c1, d1})
        eq_(set(a_d_links[0].linked), {a_d_links[0], c_d_links[1], c1, d1})
        correct_links_set = {references_links[6], references_links[7], references_links[8], references_links[9]}
        eq_(set(a_d_links[0].links), correct_links_set)
        eq_(set(a_d_links[0].get_links_for_association(collections_association)), correct_links_set)
        eq_(set(get_links([a_d_links[0]])), correct_links_set)

    def test_links_as_attribute_values(self):
        code = CClass(self.mcl, "Code")
        source = CClass(self.mcl, "Source")
        code.association(source, "[contained_code] * -> [source] *")
        code_a = CClass(self.mcl, "Code A", superclasses=code)
        code_b = CClass(self.mcl, "Code B", superclasses=code)
        a_b_association = code_a.association(code_b, "a_b: [code_a] * -> [code_b] *", superclasses=code)
        code_a1 = CObject(code_a, "code_a1")
        code_b1 = CObject(code_b, "code_b1")
        code_b2 = CObject(code_b, "code_b2")
        a_b_links = add_links({code_a1: [code_b1, code_b2]}, association=a_b_association)

        links_list = [code_a1, code_b2, code_b1, a_b_links[0], a_b_links[1]]

        collection_type = CClass(self.mcl, "Collection Type", attributes={
            "primary_code": code,
            "default_value_code": a_b_links[0],
            "codes": list,
            "default_values_list": links_list
        })
        collection = CObject(collection_type)

        eq_(collection.get_value("primary_code"), None)
        eq_(collection.get_value("default_value_code"), a_b_links[0])
        eq_(collection.get_value("codes"), None)
        eq_(collection.get_value("default_values_list"), links_list)

        collection.set_value("primary_code", a_b_links[1])
        collection.set_value("default_value_code", a_b_links[1])
        collection.set_value("codes", [code_a1, a_b_links[0]])
        collection.set_value("default_values_list", [a_b_links[0], a_b_links[1]])

        eq_(collection.get_value("primary_code"), a_b_links[1])
        eq_(collection.get_value("default_value_code"), a_b_links[1])
        eq_(collection.get_value("codes"), [code_a1, a_b_links[0]])
        eq_(collection.get_value("default_values_list"), [a_b_links[0], a_b_links[1]])

        collection.values = {'default_values_list': [a_b_links[0]], "codes": []}

        eq_(collection.values, {'default_value_code': a_b_links[1],
                                'default_values_list': [a_b_links[0]],
                                'codes': [],
                                'primary_code': a_b_links[1]})

        collection.delete_value("primary_code")
        collection.delete_value("default_value_code")
        collection.delete_value("codes")
        collection.delete_value("default_values_list")

        eq_(collection.get_value("primary_code"), None)
        eq_(collection.get_value("default_value_code"), None)
        eq_(collection.get_value("codes"), None)
        eq_(collection.get_value("default_values_list"), None)

    def create_simple_link_object_test_setup(self):
        self.a = CClass(self.mcl, "A")
        self.a1 = CClass(self.mcl, "A1", superclasses=self.a)
        self.a2 = CClass(self.mcl, "A2", superclasses=self.a)
        self.a_association = self.a1.association(self.a2, "[a1] * -> [a2] *", superclasses=self.a)
        self.b = CClass(self.mcl, "B")
        self.b_a_association = self.b.association(self.a, "[b] * -> [a] *")

        self.a1_1 = CObject(self.a1, "a1_1")
        self.a1_2 = CObject(self.a1, "a1_2")
        self.a2_1 = CObject(self.a2, "a2_1")
        self.b_1 = CObject(self.b, "b_1")
        self.a_links = add_links({self.a2_1: [self.a1_1, self.a1_2]}, association=self.a_association)

        self.b_a_links = add_links({self.b_1: [self.a_links[0], self.a_links[1]]}, association=self.b_a_association)

    def test_attributes_on_association_classifier(self):
        self.create_simple_link_object_test_setup()
        eq_(self.b_a_association.attributes, [])
        eq_(self.b_a_association.attribute_names, [])
        try:
            self.b_a_association.attributes = {
                "i1": int,
                "i2": 15,
                "s1": str,
                "s2": "abc"
            }
            exception_expected_()
        except CException as e:
            eq_("setting of attributes not supported for associations", e.value)

        eq_(self.b_a_association.get_attribute("i1"), None)

    def test_superclass_sub_class_method_on_association_classifier(self):
        self.create_simple_link_object_test_setup()
        eq_(self.a_association.superclasses, [self.a])
        eq_(self.a_association.subclasses, [])
        eq_(self.b_a_association.superclasses, [])
        eq_(self.b_a_association.subclasses, [])
        eq_(self.a.subclasses, [self.a1, self.a2, self.a_association])

        try:
            another_sc = CMetaclass("ASC")
            self.a_association.superclasses = [self.a, another_sc]
            exception_expected_()
        except CException as e:
            eq_("cannot add superclass 'ASC': not a class or class association", e.value)

        try:
            another_sc = CStereotype("ASC")
            self.a_association.superclasses = [self.a, another_sc]
            exception_expected_()
        except CException as e:
            eq_("cannot add superclass 'ASC': not a class or class association", e.value)

        another_sc = CClass(self.mcl, "ASC")
        self.a_association.superclasses = [self.a, another_sc]
        eq_(self.a_association.superclasses, [self.a, another_sc])
        eq_(set(self.a_association.all_superclasses), {self.a, another_sc})

        a2_association = self.a1.association(self.a2, "[a1] * -> [a2] *", superclasses=self.a)
        self.a_association.superclasses = [a2_association]
        eq_(self.a_association.superclasses, [a2_association])
        eq_(self.a_association.all_subclasses, set())
        eq_(self.a_association.all_superclasses, {a2_association, self.a})
        eq_(a2_association.superclasses, [self.a])
        eq_(a2_association.subclasses, [self.a_association])
        eq_(a2_association.all_subclasses, {self.a_association})

        eq_(a2_association.has_subclass(self.a_association), True)
        eq_(a2_association.has_subclass(self.a1), False)
        eq_(a2_association.has_superclass(self.a_association), False)
        eq_(a2_association.has_superclass(self.a), True)

        eq_(self.a_association.is_classifier_of_type(self.a_association), True)
        eq_(self.a_association.is_classifier_of_type(a2_association), True)
        eq_(self.a_association.is_classifier_of_type(self.a), True)
        eq_(self.a_association.is_classifier_of_type(self.a1), False)

        # test linking still works after superclass changes
        self.b_1.delete_links([self.a_links[0], self.a_links[1]])
        eq_(self.b_1.get_linked(), [])
        self.b_a_links = set_links({self.b_1: [self.a_links[1], self.a_links[0]]}, association=self.b_a_association)
        eq_(self.b_1.get_linked(), [self.a_links[1], self.a_links[0]])

    def test_delete_linked_association(self):
        self.create_simple_link_object_test_setup()
        self.a_association.delete()
        eq_(self.a.subclasses, [self.a1, self.a2])
        eq_(self.a2_1.get_linked(), [])
        eq_(self.b_1.get_linked(), [])

    def test_delete_linking_association(self):
        self.create_simple_link_object_test_setup()
        self.b_a_association.delete()
        eq_(self.a2_1.get_linked(), [self.a1_1, self.a1_2])
        eq_(self.b_1.get_linked(), [])

    def test_link_object_classifier(self):
        self.create_simple_link_object_test_setup()
        eq_(self.a_links[0].classifier, self.a_association)
        eq_(self.b_a_links[0].classifier, self.b_a_association)

        try:
            self.a_links[0].classifier = self.b_a_association
            exception_expected_()
        except CException as e:
            eq_("Changes to the classifier (i.e., the association) of a link" +
                " should not be performed with CObject methods", e.value)

    def test_link_object_class_object_class(self):
        self.create_simple_link_object_test_setup()
        eq_(self.a_links[0].class_object_class, None)
        eq_(self.b_a_links[0].class_object_class, None)

    def test_link_object_instance_of(self):
        self.create_simple_link_object_test_setup()
        eq_(self.a_links[0].instance_of(self.a_association), True)
        eq_(self.a_links[0].instance_of(self.b_a_association), False)
        eq_(self.a_links[0].instance_of(self.a), True)
        eq_(self.a_links[0].instance_of(self.a1), False)
        try:
            eq_(self.a_links[0].instance_of(self.mcl), False)
            exception_expected_()
        except CException as e:
            eq_("'MCL' is not an association or a class", e.value)

        eq_(self.b_a_links[0].instance_of(self.a_association), False)
        eq_(self.b_a_links[0].instance_of(self.b_a_association), True)
        eq_(self.b_a_links[0].instance_of(self.a), False)

    def test_link_object_delete(self):
        self.create_simple_link_object_test_setup()
        self.a_links[0].delete()
        self.b_a_links[0].delete()
        eq_(self.b_1.get_linked(), [self.a_links[1]])
        eq_(self.a2_1.get_linked(), [self.a1_2])
        eq_(self.a_links[1].get_linked(), [self.b_1])

        try:
            self.a_links[0].get_value("a")
            exception_expected_()
        except CException as e:
            eq_("can't get value 'a' on deleted link", e.value)

        try:
            self.a_links[0].delete_value("a")
            exception_expected_()
        except CException as e:
            eq_("can't delete value 'a' on deleted link", e.value)

        try:
            self.a_links[0].set_value("a", 1)
            exception_expected_()
        except CException as e:
            eq_("can't set value 'a' on deleted link", e.value)

        try:
            self.a_links[0].values = {"a": 1}
            exception_expected_()
        except CException as e:
            eq_("can't set values on deleted link", e.value)

    def test_object_link_classifier_bundable(self):
        self.create_simple_link_object_test_setup()

        bundle = CBundle("Bundle", elements=self.a.get_connected_elements())
        eq_(set(bundle.elements), {self.a, self.a1, self.a2, self.b})

        try:
            bundle.elements = self.a.get_connected_elements(add_links=True)
            exception_expected_()
        except CException as e:
            eq_("unknown keyword argument 'add_links', should be one of:" +
                " ['add_associations', 'add_bundles', 'process_bundles', 'stop_elements_inclusive', " +
                "'stop_elements_exclusive']", e.value)

        eq_(self.a_association.bundles, [])

        bundle.elements = self.a.get_connected_elements(add_associations=True)
        eq_(set(bundle.elements), {self.a, self.a1, self.a2, self.b, self.a_association})

        eq_(self.a_association.bundles, [bundle])

        bundle2 = CBundle("Bundle2", elements=self.a_association.get_connected_elements(add_associations=True))
        eq_(set(bundle2.elements), {self.a, self.a1, self.a2, self.b, self.a_association})
        eq_(set(self.a_association.bundles), {bundle, bundle2})

        bundle2.delete()
        eq_(set(self.a_association.bundles), {bundle})

        self.a_association.delete()
        eq_(set(bundle.elements), {self.a, self.a1, self.a2, self.b})

    def test_object_link_bundable(self):
        self.create_simple_link_object_test_setup()

        bundle = CBundle("Bundle", elements=self.a1_1.get_connected_elements())
        eq_(set(bundle.elements), {self.a1_1, self.a1_2, self.a2_1})

        try:
            bundle.elements = self.a1_1.get_connected_elements(add_associations=True)
            exception_expected_()
        except CException as e:
            eq_("unknown keyword argument 'add_associations', should be one of:" +
                " ['add_links', 'add_bundles', 'process_bundles', 'stop_elements_inclusive'," +
                " 'stop_elements_exclusive']", e.value)

        bundle.elements = self.b_1.get_connected_elements()
        eq_(set(bundle.elements), {self.b_1})

        eq_(self.a_links[0].bundles, [])

        bundle.elements = self.b_1.get_connected_elements(add_links=True)
        eq_(set(bundle.elements), {self.b_1, self.a_links[0], self.a_links[1]})

        eq_(self.a_links[0].bundles, [bundle])

        bundle2 = CBundle("Bundle2", elements=self.a_links[0].get_connected_elements(add_links=True))
        eq_(set(bundle2.elements), {self.b_1, self.a_links[0], self.a_links[1]})
        eq_(set(self.a_links[0].bundles), {bundle, bundle2})

        bundle2.delete()
        eq_(set(self.a_links[0].bundles), {bundle})

        self.a_links[0].delete()
        eq_(set(bundle.elements), {self.b_1, self.a_links[1]})


if __name__ == "__main__":
    nose.main()
