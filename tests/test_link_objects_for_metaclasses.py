import nose
from nose.tools import eq_

from codeable_models import CMetaclass, CClass, CObject, CException, set_links, add_links, delete_links, CAssociation
from tests.testing_commons import exception_expected_


class TestLinkObjects:
    def setup(self):
        self.mcl = CMetaclass("MCL")

    def test_reference_to_link_object(self):
        code = CClass(self.mcl, "Code")

        source = CClass(self.mcl, "Source")
        code.association(source, "[contained_code] * -> [source] *")

        code_a = CClass(self.mcl, "Code A", superclasses=code)
        code_b = CClass(self.mcl, "Code B", superclasses=code)
        a_b_association = code_a.association(code_b, "a_b: [code_a] * -> [code_b] *", superclasses=code)



        source_1 = CObject(source, "source_1")

        # link_collection = CClass(self.mcl, attributes={
        #     links_objects:
        # })

        code_a1 = CObject(code_a, "code_a1")
        code_b1 = CObject(code_b, "code_b1")
        code_b2 = CObject(code_b, "code_b2")
        link_objects = add_links({code_a1: [code_b1, code_b2]}, association=a_b_association)

        add_links({source_1: [code_a1, code_b2, code_b1, link_objects[0], link_objects[1]]}, role_name="contained_code")


    def test_reference_to_link_class(self):
        code = CMetaclass(self.mcl, "Code")

        source = CMetaclass(self.mcl, "Source")
        code.association(source, "[contained_code] * -> [source] *")

        code_a = CMetaclass(self.mcl, "Code A", superclasses=code)
        code_b = CMetaclass(self.mcl, "Code B", superclasses=code)
        a_b_association = code_a.association(code_b, "a_b: [code_a] * -> [code_b] *", superclasses=code)



        source_1 = CObject(source, "source_1")

        # link_collection = CClass(self.mcl, attributes={
        #     links_objects:
        # })

        code_a1 = CObject(code_a, "code_a1")
        code_b1 = CObject(code_b, "code_b1")
        code_b2 = CObject(code_b, "code_b2")
        link_objects = add_links({code_a1: [code_b1, code_b2]}, association=a_b_association)

        add_links({source_1: [code_a1, code_b2, code_b1, link_objects[0], link_objects[1]]}, role_name="contained_code")


if __name__ == "__main__":
    nose.main()
