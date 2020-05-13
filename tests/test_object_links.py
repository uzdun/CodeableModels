import nose
from nose.tools import eq_

from codeable_models import CMetaclass, CClass, CObject, CException, set_links, add_links, delete_links
from tests.testing_commons import exception_expected_


class TestObjectLinks:
    def setup(self):
        self.mcl = CMetaclass("MCL")
        self.c1 = CClass(self.mcl, "C1")
        self.c2 = CClass(self.mcl, "C2")

    def test_link_methods_wrong_keyword_args(self):
        o1 = CObject(self.c1, "o1")
        try:
            add_links({o1: o1}, associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            o1.add_links(o1, associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            set_links({o1: o1}, associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            delete_links({o1: o1}, associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            o1.delete_links(o1, associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            o1.get_links(associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            delete_links({o1: o1}, stereotype_instances=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            delete_links({o1: o1}, tagged_values=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")

    def test_set_one_to_one_link(self):
        self.c1.association(self.c2, name="l", multiplicity="1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        eq_(o1.links, [])

        set_links({o1: o2})
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])

        set_links({o1: o3})
        eq_(o1.links, [o3])
        eq_(o2.links, [])
        eq_(o3.links, [o1])

    def test_add_one_to_one_link(self):
        self.c1.association(self.c2, "l: 1 -> [target] 0..1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        eq_(o1.links, [])

        add_links({o1: o3})
        eq_(o1.links, [o3])
        eq_(o3.links, [o1])

        set_links({o1: []}, role_name="target")
        eq_(o1.links, [])

        o1.add_links(o2)
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])

        try:
            add_links({o1: o3})
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o1' have wrong multiplicity '2': should be '0..1'")
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])
        eq_(o3.links, [])

    def test_wrong_types_add_links(self):
        self.c1.association(self.c2, name="l", multiplicity="1")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            add_links({o1: self.mcl})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            o1.add_links([o2, self.mcl])
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")

    def test_wrong_types_set_links(self):
        self.c1.association(self.c2, name="l", multiplicity="1")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            set_links({o1: self.mcl})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            set_links({o1: [o2, self.mcl]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            set_links({o1: [o2, None]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'None' is neither an object nor a class")
        try:
            set_links({self.mcl: o2})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link source 'MCL' is neither an object nor a class")
        try:
            set_links({None: o2})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link should not contain an empty source")

    def test_wrong_format_set_links(self):
        self.c1.association(self.c2, name="l", multiplicity="1")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            set_links([o1, o2])
            exception_expected_()
        except CException as e:
            eq_(e.value, "link definitions should be of the form {<link source 1>: " +
                "<link target(s) 1>, ..., <link source n>: <link target(s) n>}")

    def test_remove_one_to_one_link(self):
        a = self.c1.association(self.c2, "l: 1 -> [c2] 0..1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c1, "o3")
        o4 = CObject(self.c2, "o4")

        links = set_links({o1: o2, o3: o4})
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])
        eq_(o3.links, [o4])
        eq_(o4.links, [o3])
        eq_(o1.link_objects, [links[0]])
        eq_(o2.link_objects, [links[0]])
        eq_(o3.link_objects, [links[1]])
        eq_(o4.link_objects, [links[1]])

        try:
            links = set_links({o1: None})
            exception_expected_()
        except CException as e:
            eq_(e.value, "matching association not found for source 'o1' and targets '[]'")

        set_links({o1: None}, association=a)
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [o4])
        eq_(o4.links, [o3])
        eq_(o1.link_objects, [])
        eq_(o2.link_objects, [])
        eq_(o3.link_objects, [links[1]])
        eq_(o4.link_objects, [links[1]])

    def test_set_links_one_to_n_link(self):
        self.c1.association(self.c2, name="l")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        set_links({o1: [o2, o3]})
        eq_(o1.links, [o2, o3])
        eq_(o2.links, [o1])
        eq_(o3.links, [o1])
        set_links({o1: o2})
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])
        eq_(o3.links, [])
        set_links({o3: o1, o2: o1})
        eq_(o1.links, [o3, o2])
        eq_(o2.links, [o1])
        eq_(o3.links, [o1])

    def test_add_links_one_to_n_link(self):
        self.c1.association(self.c2, name="l")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")
        o6 = CObject(self.c2, "o6")

        add_links({o1: [o2, o3]})
        eq_(o1.links, [o2, o3])
        eq_(o2.links, [o1])
        eq_(o3.links, [o1])
        add_links({o1: o4})
        eq_(o1.links, [o2, o3, o4])
        eq_(o2.links, [o1])
        eq_(o3.links, [o1])
        eq_(o4.links, [o1])
        o1.add_links([o5, o6])
        eq_(o1.links, [o2, o3, o4, o5, o6])
        eq_(o2.links, [o1])
        eq_(o3.links, [o1])
        eq_(o4.links, [o1])
        eq_(o5.links, [o1])
        eq_(o6.links, [o1])

    def test_remove_one_to_n_link(self):
        a = self.c1.association(self.c2, name="l", multiplicity="*")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        set_links({o1: [o2, o3]})
        set_links({o1: o2})
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])
        eq_(o3.links, [])
        try:
            set_links({o1: []})
            exception_expected_()
        except CException as e:
            eq_(e.value, "matching association not found for source 'o1' and targets '[]'")
        set_links({o1: []}, association=a)
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [])

    def test_n_to_n_link(self):
        a = self.c1.association(self.c2, name="l", source_multiplicity="*")
        o1a = CObject(self.c1, "o1a")
        o1b = CObject(self.c1, "o1b")
        o1c = CObject(self.c1, "o1c")
        o2a = CObject(self.c2, "o2a")
        o2b = CObject(self.c2, "o2b")

        set_links({o1a: [o2a, o2b], o1b: [o2a], o1c: [o2b]})

        eq_(o1a.links, [o2a, o2b])
        eq_(o1b.links, [o2a])
        eq_(o1c.links, [o2b])
        eq_(o2a.links, [o1a, o1b])
        eq_(o2b.links, [o1a, o1c])

        set_links({o2a: [o1a, o1b]})
        try:
            set_links({o2b: []})
            exception_expected_()
        except CException as e:
            eq_(e.value, "matching association not found for source 'o2b' and targets '[]'")
        set_links({o2b: []}, association=a)

        eq_(o1a.links, [o2a])
        eq_(o1b.links, [o2a])
        eq_(o1c.links, [])
        eq_(o2a.links, [o1a, o1b])
        eq_(o2b.links, [])

    def test_remove_n_to_n_link(self):
        self.c1.association(self.c2, name="l", source_multiplicity="*", multiplicity="*")
        o1 = CObject(self.c1, "o2")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c1, "o4")
        set_links({o1: [o2, o3], o4: o2})
        set_links({o1: o2, o4: [o3, o2]})
        eq_(o1.links, [o2])
        eq_(o2.links, [o1, o4])
        eq_(o3.links, [o4])
        eq_(o4.links, [o3, o2])

    def test_n_to_n_set_self_link(self):
        self.c1.association(self.c1, name="a", source_multiplicity="*", multiplicity="*", source_role_name="super",
                            role_name="sub")

        top = CObject(self.c1, "Top")
        mid1 = CObject(self.c1, "Mid1")
        mid2 = CObject(self.c1, "Mid2")
        mid3 = CObject(self.c1, "Mid3")
        bottom1 = CObject(self.c1, "Bottom1")
        bottom2 = CObject(self.c1, "Bottom2")

        set_links({top: [mid1, mid2, mid3]}, role_name="sub")
        add_links({mid1: [bottom1, bottom2]}, role_name="sub")

        eq_(top.links, [mid1, mid2, mid3])
        eq_(mid1.links, [top, bottom1, bottom2])
        eq_(mid2.links, [top])
        eq_(mid3.links, [top])
        eq_(bottom1.links, [mid1])
        eq_(bottom2.links, [mid1])

        eq_(top.get_links(role_name="sub"), [mid1, mid2, mid3])
        eq_(mid1.get_links(role_name="sub"), [bottom1, bottom2])
        eq_(mid2.get_links(role_name="sub"), [])
        eq_(mid3.get_links(role_name="sub"), [])
        eq_(bottom1.get_links(role_name="sub"), [])
        eq_(bottom2.get_links(role_name="sub"), [])

        eq_(top.get_links(role_name="super"), [])
        eq_(mid1.get_links(role_name="super"), [top])
        eq_(mid2.get_links(role_name="super"), [top])
        eq_(mid3.get_links(role_name="super"), [top])
        eq_(bottom1.get_links(role_name="super"), [mid1])
        eq_(bottom2.get_links(role_name="super"), [mid1])

    def test_n_to_n_set_self_link_delete_links(self):
        self.c1.association(self.c1, name="a", source_multiplicity="*", multiplicity="*", source_role_name="super",
                            role_name="sub")

        top = CObject(self.c1, "Top")
        mid1 = CObject(self.c1, "Mid1")
        mid2 = CObject(self.c1, "Mid2")
        mid3 = CObject(self.c1, "Mid3")
        bottom1 = CObject(self.c1, "Bottom1")
        bottom2 = CObject(self.c1, "Bottom2")

        set_links({top: [mid1, mid2, mid3], mid1: [bottom1, bottom2]}, role_name="sub")
        # delete links
        set_links({top: []}, role_name="sub")
        eq_(top.links, [])
        eq_(mid1.links, [bottom1, bottom2])
        # change links
        set_links({mid1: top, mid3: top, bottom1: mid1, bottom2: mid1}, role_name="super")

        eq_(top.links, [mid1, mid3])
        eq_(mid1.links, [top, bottom1, bottom2])
        eq_(mid2.links, [])
        eq_(mid3.links, [top])
        eq_(bottom1.links, [mid1])
        eq_(bottom2.links, [mid1])

        eq_(top.get_links(role_name="sub"), [mid1, mid3])
        eq_(mid1.get_links(role_name="sub"), [bottom1, bottom2])
        eq_(mid2.get_links(role_name="sub"), [])
        eq_(mid3.get_links(role_name="sub"), [])
        eq_(bottom1.get_links(role_name="sub"), [])
        eq_(bottom2.get_links(role_name="sub"), [])

        eq_(top.get_links(role_name="super"), [])
        eq_(mid1.get_links(role_name="super"), [top])
        eq_(mid2.get_links(role_name="super"), [])
        eq_(mid3.get_links(role_name="super"), [top])
        eq_(bottom1.get_links(role_name="super"), [mid1])
        eq_(bottom2.get_links(role_name="super"), [mid1])

    def test_incompatible_classifier(self):
        self.c1.association(self.c2, name="l", multiplicity="*")
        cl = CClass(self.mcl, "CLX")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(cl, "o3")
        try:
            set_links({o1: [o2, o3]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "object 'o3' has an incompatible classifier")
        try:
            set_links({o1: o3})
            exception_expected_()
        except CException as e:
            eq_(e.value, "matching association not found for source 'o1' and targets '['o3']'")

    def test_duplicate_assignment(self):
        a = self.c1.association(self.c2, "l: *->*")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            set_links({o1: [o2, o2]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "trying to link the same link twice 'o1 -> o2'' twice for the same association")
        eq_(o1.get_links(), [])
        eq_(o2.get_links(), [])
        b = self.c1.association(self.c2, "l: *->*")
        o1.add_links(o2, association=a)
        o1.add_links(o2, association=b)
        eq_(o1.get_links(), [o2, o2])
        eq_(o2.get_links(), [o1, o1])

    def test_non_existing_role_name(self):
        self.c1.association(self.c1, role_name="next", source_role_name="prior",
                            source_multiplicity="1", multiplicity="1")
        o1 = CObject(self.c1, "o1")
        try:
            set_links({o1: o1}, role_name="target")
            exception_expected_()
        except CException as e:
            eq_(e.value, "matching association not found for source 'o1' and targets '['o1']'")

    def test_link_association_ambiguous(self):
        self.c1.association(self.c2, name="a1", role_name="c2", multiplicity="*")
        self.c1.association(self.c2, name="a2", role_name="c2", multiplicity="*")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            set_links({o1: o2})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link specification ambiguous, multiple matching associations " +
                "found for source 'o1' and targets '['o2']'")
        try:
            set_links({o1: o2}, role_name="c2")
            exception_expected_()
        except CException as e:
            eq_(e.value, "link specification ambiguous, multiple matching associations " +
                "found for source 'o1' and targets '['o2']'")

    def test_link_and_get_links_by_association(self):
        a1 = self.c1.association(self.c2, name="a1", multiplicity="*")
        a2 = self.c1.association(self.c2, name="a2", multiplicity="*")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        links_a1 = set_links({o1: o2}, association=a1)
        links_a2 = set_links({o1: [o2, o3]}, association=a2)

        eq_(o1.get_links(), [o2, o2, o3])
        eq_(o1.links, [o2, o2, o3])

        eq_(o1.get_links(association=a1), [o2])
        eq_(o1.get_links(association=a2), [o2, o3])

        eq_(o1.get_link_objects_for_association(a1), links_a1)
        eq_(o1.get_link_objects_for_association(a2), links_a2)

    def test_link_with_inheritance_in_classifier_targets(self):
        sub_class = CClass(self.mcl, superclasses=self.c2)
        a1 = self.c1.association(sub_class, name="a1", multiplicity="*")
        a2 = self.c1.association(self.c2, name="a2", multiplicity="*")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o_sub_1 = CObject(sub_class, "o_sub_1")
        o_sub_2 = CObject(sub_class, "o_sub_2")
        o_super_1 = CObject(self.c2, "o_super_1")
        o_super_2 = CObject(self.c2, "o_super_2")
        try:
            # ambiguous, list works for both associations 
            set_links({o1: [o_sub_1, o_sub_2]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link specification ambiguous, multiple matching associations " +
                "found for source 'o1' and targets '['o_sub_1', 'o_sub_2']'")
        set_links({o1: [o_sub_1, o_sub_2]}, association=a1)
        set_links({o1: [o_sub_1]}, association=a2)
        set_links({o2: [o_super_1, o_super_2]})

        eq_(o1.links, [o_sub_1, o_sub_2, o_sub_1])
        eq_(o1.get_links(), [o_sub_1, o_sub_2, o_sub_1])
        eq_(o2.get_links(), [o_super_1, o_super_2])
        eq_(o1.get_links(association=a1), [o_sub_1, o_sub_2])
        eq_(o1.get_links(association=a2), [o_sub_1])
        eq_(o2.get_links(association=a1), [])
        eq_(o2.get_links(association=a2), [o_super_1, o_super_2])

        # this mixed list is applicable only for a2
        set_links({o2: [o_sub_1, o_super_1]})
        eq_(o2.get_links(association=a1), [])
        eq_(o2.get_links(association=a2), [o_sub_1, o_super_1])

    def test_link_with_inheritance_in_classifier_targets_using_role_names(self):
        sub_class = CClass(self.mcl, superclasses=self.c2)
        a1 = self.c1.association(sub_class, "a1: * -> [sub_class] *")
        a2 = self.c1.association(self.c2, "a2: * -> [c2] *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o_sub_1 = CObject(sub_class, "o_sub_1")
        o_sub_2 = CObject(sub_class, "o_sub_2")
        o_super_1 = CObject(self.c2, "o_super_1")
        o_super_2 = CObject(self.c2, "o_super_2")
        set_links({o1: [o_sub_1, o_sub_2]}, role_name="sub_class")
        set_links({o1: [o_sub_1]}, role_name="c2")
        set_links({o2: [o_super_1, o_super_2]})

        eq_(o1.links, [o_sub_1, o_sub_2, o_sub_1])
        eq_(o1.get_links(), [o_sub_1, o_sub_2, o_sub_1])
        eq_(o2.get_links(), [o_super_1, o_super_2])
        eq_(o1.get_links(association=a1), [o_sub_1, o_sub_2])
        eq_(o1.get_links(association=a2), [o_sub_1])
        eq_(o2.get_links(association=a1), [])
        eq_(o2.get_links(association=a2), [o_super_1, o_super_2])
        eq_(o1.get_links(role_name="sub_class"), [o_sub_1, o_sub_2])
        eq_(o1.get_links(role_name="c2"), [o_sub_1])
        eq_(o2.get_links(role_name="sub_class"), [])
        eq_(o2.get_links(role_name="c2"), [o_super_1, o_super_2])

    def test_link_delete_association(self):
        a = self.c1.association(self.c2, name="l", source_multiplicity="*", multiplicity="*")
        o1 = CObject(self.c1, "o2")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c1, "o4")
        set_links({o1: [o2, o3]})
        set_links({o4: [o2]})
        set_links({o1: [o2]})
        set_links({o4: [o3, o2]})
        a.delete()
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [])
        eq_(o4.links, [])
        try:
            set_links({o1: [o2, o3]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "matching association not found for source 'o2' and targets '['o2', 'o3']'")

    def test_one_to_one_link_multiplicity(self):
        a = self.c1.association(self.c2, name="l", multiplicity="1", source_multiplicity="1..1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c1, "o4")

        try:
            set_links({o1: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o1' have wrong multiplicity '0': should be '1'")
        try:
            set_links({o1: [o2, o3]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o1' have wrong multiplicity '2': should be '1'")

        try:
            set_links({o2: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o2' have wrong multiplicity '0': should be '1..1'")
        try:
            set_links({o2: [o1, o4]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o2' have wrong multiplicity '2': should be '1..1'")

    def test_one_to_n_link_multiplicity(self):
        a = self.c1.association(self.c2, name="l", source_multiplicity="1", multiplicity="1..*")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c1, "o4")

        try:
            set_links({o1: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o1' have wrong multiplicity '0': should be '1..*'")

        set_links({o1: [o2, o3]})
        eq_(o1.get_links(association=a), [o2, o3])

        try:
            set_links({o2: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o2' have wrong multiplicity '0': should be '1'")
        try:
            set_links({o2: [o1, o4]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o2' have wrong multiplicity '2': should be '1'")

    def test_specific_n_to_n_link_multiplicity(self):
        a = self.c1.association(self.c2, name="l", source_multiplicity="1..2", multiplicity="2")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c1, "o4")
        o5 = CObject(self.c1, "o5")
        o6 = CObject(self.c2, "o6")

        try:
            set_links({o1: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o1' have wrong multiplicity '0': should be '2'")
        try:
            set_links({o1: [o2]}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o1' have wrong multiplicity '1': should be '2'")
        try:
            set_links({o1: [o2, o3, o6]}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o1' have wrong multiplicity '3': should be '2'")

        set_links({o1: [o2, o3]})
        eq_(o1.get_links(association=a), [o2, o3])
        set_links({o2: [o1, o4], o1: o3, o4: o3})
        eq_(o2.get_links(association=a), [o1, o4])

        try:
            set_links({o2: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o2' have wrong multiplicity '0': should be '1..2'")
        try:
            set_links({o2: [o1, o4, o5]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o2' have wrong multiplicity '3': should be '1..2'")

    def test_get_link_objects(self):
        c1_sub_class = CClass(self.mcl, "C1Sub", superclasses=self.c1)
        c2_sub_class = CClass(self.mcl, "C2Sub", superclasses=self.c2)
        a1 = self.c1.association(self.c2, role_name="c2", source_role_name="c1",
                                 source_multiplicity="*", multiplicity="*")
        a2 = self.c1.association(self.c1, role_name="next", source_role_name="prior",
                                 source_multiplicity="1", multiplicity="0..1")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o1_sub = CObject(c1_sub_class, "o1_sub")
        o2_sub = CObject(c2_sub_class, "o2_sub")

        link_objects1 = set_links({o1: o2})
        eq_(link_objects1, o1.link_objects)
        link1 = o1.link_objects[0]
        link2 = [o for o in o1.link_objects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, o1)
        eq_(link1.target, o2)

        link_objects2 = set_links({o1: o2_sub})
        eq_(link_objects2, o1.link_objects)
        eq_(len(o1.link_objects), 1)
        link1 = o1.link_objects[0]
        link2 = [o for o in o1.link_objects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, o1)
        eq_(link1.target, o2_sub)

        link_objects3 = set_links({o1: o2})
        eq_(link_objects3, o1.link_objects)
        eq_(len(o1.link_objects), 1)
        link1 = o1.link_objects[0]
        link2 = [o for o in o1.link_objects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, o1)
        eq_(link1.target, o2)

        link_objects4 = set_links({o1: o1}, role_name="next")
        eq_(link_objects3 + link_objects4, o1.link_objects)
        eq_(len(o1.link_objects), 2)
        link1 = o1.link_objects[1]
        link2 = [o for o in o1.link_objects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, o1)
        eq_(link1.target, o1)

        link_objects5 = set_links({o1: o1_sub}, role_name="next")
        eq_(link_objects3 + link_objects5, o1.link_objects)
        eq_(len(o1.link_objects), 2)
        link1 = o1.link_objects[1]
        link2 = [o for o in o1.link_objects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, o1)
        eq_(link1.target, o1_sub)

        set_links({o1: o1}, role_name="next")
        eq_(len(o1.link_objects), 2)
        link1 = o1.link_objects[1]
        link2 = [o for o in o1.link_objects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, o1)
        eq_(link1.target, o1)

        set_links({o1: []}, association=a1)
        set_links({o1: []}, association=a2)
        eq_(len(o1.link_objects), 0)

        set_links({o1_sub: o1}, role_name="next")
        eq_(len(o1_sub.link_objects), 1)
        link1 = o1_sub.link_objects[0]
        link2 = [o for o in o1_sub.link_objects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, o1_sub)
        eq_(link1.target, o1)

    def test_get_link_objects_self_link(self):
        a1 = self.c1.association(self.c1, role_name="to", source_role_name="from",
                                 source_multiplicity="*", multiplicity="*")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c1, "o3")
        o4 = CObject(self.c1, "o4")

        set_links({o1: [o2, o3, o1]})
        o4.add_links([o1, o3])
        link1 = o1.link_objects[0]
        link2 = [o for o in o1.link_objects if o.association == a1][0]
        link3 = [o for o in o1.link_objects if o.role_name == "to"][0]
        link4 = [o for o in o1.link_objects if o.source_role_name == "from"][0]
        eq_(link1, link2)
        eq_(link1, link3)
        eq_(link1, link4)
        eq_(link1.association, a1)
        eq_(link1.source, o1)
        eq_(link1.target, o2)

        eq_(len(o1.link_objects), 4)
        eq_(len(o2.link_objects), 1)
        eq_(len(o3.link_objects), 2)
        eq_(len(o4.link_objects), 2)

    def test_add_links(self):
        self.c1.association(self.c2, "1 -> [role1] *")
        self.c1.association(self.c2, "* -> [role2] *")
        self.c1.association(self.c2, "1 -> [role3] 1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")

        add_links({o1: o2}, role_name="role1")
        eq_(o1.get_links(role_name="role1"), [o2])
        add_links({o1: [o3, o4]}, role_name="role1")
        o1.get_links(role_name="role1")
        eq_(o1.get_links(role_name="role1"), [o2, o3, o4])

        o1.add_links(o2, role_name="role2")
        eq_(o1.get_links(role_name="role2"), [o2])
        o1.add_links([o3, o4], role_name="role2")
        o1.get_links(role_name="role2")
        eq_(o1.get_links(role_name="role2"), [o2, o3, o4])

        add_links({o1: o2}, role_name="role3")
        eq_(o1.get_links(role_name="role3"), [o2])
        try:
            add_links({o1: [o3, o4]}, role_name="role3")
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o1' have wrong multiplicity '3': should be '1'")

        try:
            add_links({o1: [o3]}, role_name="role3")
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o1' have wrong multiplicity '2': should be '1'")
        eq_(o1.get_links(role_name="role3"), [o2])

    def test_link_source_multiplicity(self):
        self.c1.association(self.c2, "[sourceRole1] 1 -> [role1] *")
        self.c1.association(self.c2, "[sourceRole2] 1 -> [role2] 1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        CObject(self.c2, "o4")
        CObject(self.c2, "o5")

        set_links({o1: o3}, role_name="role1")
        set_links({o2: o3}, role_name="role1")

        eq_(o3.get_links(role_name="sourceRole1"), [o2])

    def test_add_links_source_multiplicity(self):
        self.c1.association(self.c2, "[sourceRole1] 1 -> [role1] *")
        self.c1.association(self.c2, "[sourceRole2] 1 -> [role2] 1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")
        o6 = CObject(self.c2, "o6")

        add_links({o2: o3}, role_name="role1")
        add_links({o2: o4}, role_name="role1")

        eq_(o3.get_links(role_name="sourceRole1"), [o2])

        add_links({o2: o5}, role_name="role1")
        eq_(o2.get_links(role_name="role1"), [o3, o4, o5])

        try:
            add_links({o1: [o4]}, role_name="role1")
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o4' have wrong multiplicity '2': should be '1'")

        add_links({o1: o6}, role_name="role2")
        eq_(o1.get_links(role_name="role2"), [o6])
        try:
            add_links({o1: [o3, o4]}, role_name="role2")
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o1' have wrong multiplicity '3': should be '1'")
        eq_(o1.get_links(role_name="role2"), [o6])

    def test_set_links_multiple_links_in_definition(self):
        self.c1.association(self.c2, "[sourceRole1] * -> [role1] *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c1, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")

        set_links({o1: o4, o2: [o4], o5: [o1, o2, o3]})
        eq_(o1.get_links(), [o4, o5])
        eq_(o2.get_links(), [o4, o5])
        eq_(o3.get_links(), [o5])
        eq_(o4.get_links(), [o1, o2])
        eq_(o5.get_links(), [o1, o2, o3])

    def test_add_links_multiple_links_in_definition(self):
        self.c1.association(self.c2, "[sourceRole1] * -> [role1] *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c1, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")

        add_links({o1: o4, o2: [o4], o5: [o1, o2, o3]})
        eq_(o1.get_links(), [o4, o5])
        eq_(o2.get_links(), [o4, o5])
        eq_(o3.get_links(), [o5])
        eq_(o4.get_links(), [o1, o2])
        eq_(o5.get_links(), [o1, o2, o3])

    def test_wrong_types_delete_links(self):
        self.c1.association(self.c2, name="l", multiplicity="1")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            delete_links(o1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "link definitions should be of the form " +
                "{<link source 1>: <link target(s) 1>, ..., <link source n>: <link target(s) n>}")
        try:
            delete_links({o1: self.mcl})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            delete_links({o1: [o2, self.mcl]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            delete_links({o1: [o2, None]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'None' is neither an object nor a class")
        try:
            delete_links({self.mcl: o2})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link source 'MCL' is neither an object nor a class")
        try:
            delete_links({None: o2})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link should not contain an empty source")

    def test_delete_one_to_one_link(self):
        self.c1.association(self.c2, "l: 1 -> [c2] 0..1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c1, "o3")
        o4 = CObject(self.c2, "o4")

        links = add_links({o1: o2, o3: o4})
        o1.delete_links(o2)
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [o4])
        eq_(o4.links, [o3])
        eq_(o1.link_objects, [])
        eq_(o2.link_objects, [])
        eq_(o3.link_objects, [links[1]])
        eq_(o4.link_objects, [links[1]])
        delete_links({o3: o4})
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [])
        eq_(o4.links, [])
        eq_(o1.link_objects, [])
        eq_(o2.link_objects, [])
        eq_(o3.link_objects, [])
        eq_(o4.link_objects, [])

    def test_delete_one_to_one_link_wrong_multiplicity(self):
        self.c1.association(self.c2, "l: 1 -> [c2] 1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        add_links({o1: o2})
        try:
            o1.delete_links(o2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o1' have wrong multiplicity '0': should be '1'")
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])

    def test_delete_one_to_n_links(self):
        self.c1.association(self.c2, "l: 0..1 -> *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")

        add_links({o1: [o3, o4], o2: [o5]})
        o4.delete_links([o1])
        eq_(o1.links, [o3])
        eq_(o2.links, [o5])
        eq_(o3.links, [o1])
        eq_(o4.links, [])
        eq_(o5.links, [o2])

        o4.add_links([o2])
        eq_(o2.links, [o5, o4])
        delete_links({o1: o3, o2: o2.links})
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [])
        eq_(o4.links, [])
        eq_(o5.links, [])

    def test_delete_one_to_n_links_wrong_multiplicity(self):
        self.c1.association(self.c2, "l: 1 -> *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")

        add_links({o1: [o3, o4], o2: [o5]})

        try:
            o4.delete_links([o1])
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'o4' have wrong multiplicity '0': should be '1'")

    def test_delete_n_to_n_links(self):
        self.c1.association(self.c2, "l: * -> *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")
        o6 = CObject(self.c2, "o6")

        add_links({o1: [o3, o4], o2: [o4, o5]})
        o4.delete_links([o1, o2])
        eq_(o1.links, [o3])
        eq_(o2.links, [o5])
        eq_(o3.links, [o1])
        eq_(o4.links, [])
        eq_(o5.links, [o2])

        add_links({o4: [o1, o2], o6: [o2, o1]})
        delete_links({o1: o6, o2: [o4, o5]})
        eq_(o1.links, [o3, o4])
        eq_(o2.links, [o6])
        eq_(o3.links, [o1])
        eq_(o4.links, [o1])
        eq_(o5.links, [])
        eq_(o6.links, [o2])

    def test_delete_link_no_matching_link(self):
        a = self.c1.association(self.c2, "l: 0..1 -> *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")

        add_links({o1: [o3, o4], o2: [o5]}, association=a)

        try:
            delete_links({o1: o5})
            exception_expected_()
        except CException as e:
            eq_(e.value, "no link found for 'o1 -> o5' in delete links")

        b = self.c1.association(self.c2, "l: 0..1 -> *")
        try:
            delete_links({o1: o5})
            exception_expected_()
        except CException as e:
            eq_(e.value, "no link found for 'o1 -> o5' in delete links")

        try:
            o4.delete_links([o1], association=b)
            exception_expected_()
        except CException as e:
            eq_(e.value, "no link found for 'o4 -> o1' in delete links for given association")

    def test_delete_link_select_by_association(self):
        a = self.c1.association(self.c2, "a: * -> *")
        b = self.c1.association(self.c2, "b: * -> *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")

        add_links({o1: [o3], o2: [o3, o4]}, association=b)
        delete_links({o2: o3})
        eq_(o1.links, [o3])
        eq_(o2.links, [o4])
        eq_(o3.links, [o1])
        eq_(o4.links, [o2])
        add_links({o1: [o3], o2: [o3, o4]}, association=a)

        try:
            delete_links({o1: o3})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link definition in delete links ambiguous for link 'o1->o3': found multiple matches")

        delete_links({o1: o3, o2: o4}, association=b)
        eq_(o1.links, [o3])
        eq_(o2.links, [o3, o4])
        eq_(o3.links, [o1, o2])
        eq_(o4.links, [o2])
        for o in [o1, o2, o3, o4]:
            for lo in o.link_objects:
                eq_(lo.association, a)

        o1.add_links(o3, association=b)
        try:
            o1.delete_links(o3)
            exception_expected_()
        except CException as e:
            eq_(e.value, "link definition in delete links ambiguous for link 'o1->o3': found multiple matches")

        eq_(o1.links, [o3, o3])
        eq_(o2.links, [o3, o4])
        eq_(o3.links, [o1, o2, o1])
        eq_(o4.links, [o2])

        o1.delete_links(o3, association=a)
        eq_(o1.links, [o3])
        eq_(o2.links, [o3, o4])
        eq_(o3.links, [o2, o1])
        eq_(o4.links, [o2])

    def test_delete_link_select_by_role_name(self):
        a = self.c1.association(self.c2, "a: [sourceA] * -> [targetA] *")
        self.c1.association(self.c2, "b: [sourceB] * -> [targetB] *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")

        add_links({o1: [o3], o2: [o3, o4]}, role_name="targetB")
        delete_links({o2: o3})
        eq_(o1.links, [o3])
        eq_(o2.links, [o4])
        eq_(o3.links, [o1])
        eq_(o4.links, [o2])
        add_links({o1: [o3], o2: [o3, o4]}, role_name="targetA")

        delete_links({o1: o3, o2: o4}, role_name="targetB")
        eq_(o1.links, [o3])
        eq_(o2.links, [o3, o4])
        eq_(o3.links, [o1, o2])
        eq_(o4.links, [o2])
        for o in [o1, o2, o3, o4]:
            for lo in o.link_objects:
                eq_(lo.association, a)

        add_links({o1: [o3], o2: [o3, o4]}, role_name="targetB")
        o3.delete_links([o1, o2], role_name="sourceB")
        delete_links({o4: o2}, role_name="sourceB")

        eq_(o1.links, [o3])
        eq_(o2.links, [o3, o4])
        eq_(o3.links, [o1, o2])
        eq_(o4.links, [o2])
        for o in [o1, o2, o3, o4]:
            for lo in o.link_objects:
                eq_(lo.association, a)

    def test_delete_links_wrong_role_name(self):
        self.c1.association(self.c2, "a: [sourceA] * -> [targetA] *")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o1.add_links(o2)
        try:
            o1.delete_links(o2, role_name="target")
            exception_expected_()
        except CException as e:
            eq_(e.value, "no link found for 'o1 -> o2' in delete links for given role name 'target'")

    def test_delete_links_wrong_association(self):
        self.c1.association(self.c2, "a: [sourceA] * -> [targetA] *")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o1.add_links(o2)
        try:
            o1.delete_links(o2, association=o1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "'o1' is not a association")
        b = self.c1.association(self.c2, "b: [sourceB] * -> [targetB] *")
        try:
            o1.delete_links(o2, association=b)
            exception_expected_()
        except CException as e:
            eq_(e.value, "no link found for 'o1 -> o2' in delete links for given association")
        try:
            o1.delete_links(o2, association=b, role_name="x")
            exception_expected_()
        except CException as e:
            eq_(e.value,
                "no link found for 'o1 -> o2' in delete links for given role name 'x' and for given association")

    def test_link_label_none_default(self):
        a1 = self.c1.association(self.c2, name="a1", multiplicity="*")
        a2 = self.c1.association(self.c2, multiplicity="*")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        l1 = set_links({o1: o2}, association=a1)
        l2 = set_links({o1: [o2, o3]}, association=a2)

        eq_(l1[0].label, None)
        eq_(l2[0].label, None)
        eq_(l2[1].label, None)

    def test_link_label_get_set(self):
        a1 = self.c1.association(self.c2, name="a1", multiplicity="*")
        a2 = self.c1.association(self.c2, multiplicity="*")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        l1 = set_links({o1: o2}, association=a1, label="l1")
        l2 = add_links({o1: [o2, o3]}, association=a2, label="l2")

        eq_(l1[0].label, "l1")
        eq_(l2[0].label, "l2")
        eq_(l2[1].label, "l2")

        l2[1].label = "l3"
        eq_(l2[0].label, "l2")
        eq_(l2[1].label, "l3")

        l3 = o1.add_links(o3, association=a1, label="x1")
        eq_(l3[0].label, "x1")

    def test_add_links_with_inherited_common_classifiers(self):
        mcl = CMetaclass("MCL")
        super_a = CClass(mcl, "SuperA")
        super_b = CClass(mcl, "SuperB")
        super_a.association(super_b, "[a] 1 -> [b] *")

        sub_b1 = CClass(mcl, "SubB1", superclasses=[super_b])
        sub_b2 = CClass(mcl, "SubB2", superclasses=[super_b])
        sub_a = CClass(mcl, "SubA", superclasses=[super_a])

        obj_a = CObject(sub_a, "a")
        obj_b1 = CObject(sub_b1, "b1")
        obj_b2 = CObject(sub_b2, "b2")

        add_links({obj_a: [obj_b1, obj_b2]}, role_name="b")
        eq_(set(obj_a.get_links(role_name="b")), {obj_b1, obj_b2})


if __name__ == "__main__":
    nose.main()
