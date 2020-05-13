import nose
from nose.tools import eq_

from codeable_models import CMetaclass, CStereotype, CClass, CException, set_links, add_links
from tests.testing_commons import exception_expected_


class TestStereotypeInstancesOnAssociations:
    def setup(self):
        self.m1 = CMetaclass("M1")
        self.m2 = CMetaclass("M2")
        self.a = self.m1.association(self.m2, name="a", multiplicity="*", role_name="m1",
                                     source_multiplicity="1", source_role_name="m2")

    def test_stereotype_instances_on_association(self):
        s1 = CStereotype("S1", extended=self.a)
        s2 = CStereotype("S2", extended=self.a)
        s3 = CStereotype("S3", extended=self.a)

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        link_objects = set_links({c1: [c2, c3]})
        l1 = link_objects[0]

        eq_(l1.stereotype_instances, [])
        eq_(s1.extended_instances, [])
        l1.stereotype_instances = [s1]
        eq_(s1.extended_instances, [l1])
        eq_(l1.stereotype_instances, [s1])
        l1.stereotype_instances = [s1, s2, s3]
        eq_(s1.extended_instances, [l1])
        eq_(s2.extended_instances, [l1])
        eq_(s3.extended_instances, [l1])
        eq_(set(l1.stereotype_instances), {s1, s2, s3})
        l1.stereotype_instances = s2
        eq_(l1.stereotype_instances, [s2])
        eq_(s1.extended_instances, [])
        eq_(s2.extended_instances, [l1])
        eq_(s3.extended_instances, [])

        eq_(c1.get_link_objects_for_association(self.a), link_objects)
        eq_(c1.get_link_stereotype_instances_for_association(self.a), [(c1, c2, s2)])
        eq_(c2.get_link_objects_for_association(self.a), [l1])
        eq_(c2.get_link_stereotype_instances_for_association(self.a), [(c1, c2, s2)])
        eq_(c3.get_link_objects_for_association(self.a), [link_objects[1]])
        eq_(c3.get_link_stereotype_instances_for_association(self.a), [])

    def test_stereotype_instances_double_assignment(self):
        s1 = CStereotype("S1", extended=self.a)

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        links = set_links({c1: c2})[0]

        try:
            links.stereotype_instances = [s1, s1]
            exception_expected_()
        except CException as e:
            eq_(e.value, "'S1' is already a stereotype instance on link from 'C1' to 'C2'")
        eq_(links.stereotype_instances, [s1])

    def test_stereotype_instances_none_assignment(self):
        CStereotype("S1", extended=self.a)

        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        links = set_links({c1: [c2]})[0]

        try:
            links.stereotype_instances = [None]
            exception_expected_()
        except CException as e:
            eq_(e.value, "'None' is not a stereotype")
        eq_(links.stereotype_instances, [])

    def test_stereotype_instances_wrong_type_in_assignment(self):
        CStereotype("S1", extended=self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        links = c1.add_links(c2)[0]
        try:
            links.stereotype_instances = self.a
            exception_expected_()
        except CException as e:
            eq_(e.value, "a list or a stereotype is required as input")
        eq_(links.stereotype_instances, [])

    def test_multiple_extended_instances(self):
        s1 = CStereotype("S1", extended=self.a)
        s2 = CStereotype("S2", extended=self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        c4 = CClass(self.m2, "C4")
        link_objects = set_links({c1: [c2, c3, c4]})
        link_objects[0].stereotype_instances = [s1]
        eq_(s1.extended_instances, [link_objects[0]])
        link_objects[1].stereotype_instances = [s1]
        eq_(set(s1.extended_instances), {link_objects[0], link_objects[1]})
        link_objects[2].stereotype_instances = [s1, s2]
        eq_(set(s1.extended_instances), {link_objects[0], link_objects[1], link_objects[2]})
        eq_(set(s2.extended_instances), {link_objects[2]})

        eq_(c1.get_link_objects_for_association(self.a), link_objects)
        eq_(c1.get_link_stereotype_instances_for_association(self.a),
            [(c1, c2, s1), (c1, c3, s1), (c1, c4, s1), (c1, c4, s2)])

    def test_delete_stereotype_of_extended_instances(self):
        s1 = CStereotype("S1", extended=self.a)
        s1.delete()
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        links = set_links({c1: c2})[0]
        try:
            links.stereotype_instances = [s1]
            exception_expected_()
        except CException as e:
            eq_(e.value, "cannot access named element that has been deleted")

    def test_delete_stereotyped_element_instance(self):
        s1 = CStereotype("S1", extended=self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        links = set_links({c1: c2}, stereotype_instances=[s1])[0]
        eq_(s1.extended_instances, [links])
        eq_(links.stereotype_instances, [s1])
        links.delete()
        eq_(s1.extended_instances, [])
        eq_(links.stereotype_instances, [])

    def test_add_stereotype_instance_wrong_association(self):
        other_association = self.m1.association(self.m2, name="b", multiplicity="*", role_name="m1",
                                                source_multiplicity="1", source_role_name="m2")
        s1 = CStereotype("S1", extended=self.a)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        links = set_links({c1: c2}, association=other_association)[0]
        try:
            links.stereotype_instances = [s1]
            exception_expected_()
        except CException as e:
            eq_(e.value,
                "stereotype 'S1' cannot be added to link from 'C1' to 'C2': no extension by this stereotype found")

    def test_add_stereotype_of_inherited_metaclass(self):
        sub1 = CMetaclass("Sub1", superclasses=self.m1)
        sub2 = CMetaclass("Sub2", superclasses=self.m2)
        s = CStereotype("S1", extended=self.a)
        c1 = CClass(sub1, "C1")
        c2 = CClass(sub2, "C2")
        links = add_links({c1: c2}, stereotype_instances=s)[0]
        eq_(s.extended_instances, [links])
        eq_(links.stereotype_instances, [s])

    def test_add_stereotype_instance_correct_by_inheritance_of_stereotype(self):
        s1 = CStereotype("S1", extended=self.a)
        s2 = CStereotype("S2", superclasses=s1)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        links = c1.add_links(c2, stereotype_instances=[s2])[0]
        eq_(s2.extended_instances, [links])
        eq_(links.stereotype_instances, [s2])

    def test_all_extended_instances(self):
        s1 = CStereotype("S1", extended=self.a)
        s2 = CStereotype("S2", superclasses=s1)
        c1 = CClass(self.m1, "C1")
        c2 = CClass(self.m2, "C2")
        c3 = CClass(self.m2, "C3")
        link_objects = set_links({c1: [c2, c3]})
        link_objects[0].stereotype_instances = s1
        link_objects[1].stereotype_instances = s2
        eq_(s1.extended_instances, [link_objects[0]])
        eq_(s2.extended_instances, [link_objects[1]])
        eq_(s1.all_extended_instances, [link_objects[0], link_objects[1]])
        eq_(s2.all_extended_instances, [link_objects[1]])


if __name__ == "__main__":
    nose.main()
