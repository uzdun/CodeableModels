import nose
from nose.tools import eq_

from codeable_models import CMetaclass, CClass, CObject, CException, set_links, add_links, delete_links
from tests.testing_commons import exception_expected_


class TestClassLinks:
    def setup(self):
        self.m1 = CMetaclass("M1")
        self.m2 = CMetaclass("M2")
        self.mcl = CMetaclass("MCL")

    def test_link_methods_wrong_keyword_args(self):
        c1 = CClass(self.m1, "C1")
        try:
            add_links({c1: c1}, associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            c1.add_links(c1, associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            set_links({c1: c1}, associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            c1.delete_links(c1, associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            delete_links({c1: c1}, associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            c1.get_links(associationX=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")
        try:
            delete_links({c1: c1}, stereotype_instances=None)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown keywords argument")

    def test_set_one_to_one_link(self):
        self.m1.association(self.m2, name="l", multiplicity="1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")

        eq_(c1.links, [])

        set_links({c1: c2})
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])

        set_links({c1: c3})
        eq_(c1.links, [c3])
        eq_(c2.links, [])
        eq_(c3.links, [c1])

    def test_add_one_to_one_link(self):
        self.m1.association(self.m2, "l: 1 -> [target] 0..1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")

        eq_(c1.links, [])

        add_links({c1: c3})
        eq_(c1.links, [c3])
        eq_(c3.links, [c1])

        set_links({c1: []}, role_name="target")
        eq_(c1.links, [])

        c1.add_links(c2)
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])

        try:
            add_links({c1: c3})
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c1' have wrong multiplicity '2': should be '0..1'")
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])
        eq_(c3.links, [])

    def test_wrong_types_add_links(self):
        self.m1.association(self.m2, name="l", multiplicity="1")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            add_links({c1: self.mcl})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            c1.add_links([c2, self.mcl])
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")

    def test_wrong_types_set_links(self):
        self.m1.association(self.m2, name="l", multiplicity="1")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            set_links({c1: self.mcl})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            set_links({c1: [c2, self.mcl]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            set_links({c1: [c2, None]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'None' is neither an object nor a class")
        try:
            set_links({self.mcl: c2})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link source 'MCL' is neither an object nor a class")
        try:
            set_links({None: c2})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link should not contain an empty source")

    def test_wrong_format_set_links(self):
        self.m1.association(self.m2, name="l", multiplicity="1")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            set_links([c1, c2])
            exception_expected_()
        except CException as e:
            eq_(e.value, "link definitions should be of the form {<link source 1>: " +
                "<link target(s) 1>, ..., <link source n>: <link target(s) n>}")

    def test_remove_one_to_one_link(self):
        a = self.m1.association(self.m2, "l: 1 -> [c2] 0..1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m1, "c3")
        c4 = CClass(self.m2, "c4")

        links = set_links({c1: c2, c3: c4})
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])
        eq_(c3.links, [c4])
        eq_(c4.links, [c3])
        eq_(c1.link_objects, [links[0]])
        eq_(c2.link_objects, [links[0]])
        eq_(c3.link_objects, [links[1]])
        eq_(c4.link_objects, [links[1]])

        try:
            links = set_links({c1: None})
            exception_expected_()
        except CException as e:
            eq_(e.value, "matching association not found for source 'c1' and targets '[]'")

        set_links({c1: None}, association=a)
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [c4])
        eq_(c4.links, [c3])
        eq_(c1.link_objects, [])
        eq_(c2.link_objects, [])
        eq_(c3.link_objects, [links[1]])
        eq_(c4.link_objects, [links[1]])

    def test_set_links_one_to_n_link(self):
        self.m1.association(self.m2, name="l")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")

        set_links({c1: [c2, c3]})
        eq_(c1.links, [c2, c3])
        eq_(c2.links, [c1])
        eq_(c3.links, [c1])
        set_links({c1: c2})
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])
        eq_(c3.links, [])
        set_links({c3: c1, c2: c1})
        eq_(c1.links, [c3, c2])
        eq_(c2.links, [c1])
        eq_(c3.links, [c1])

    def test_add_links_one_to_n_link(self):
        self.m1.association(self.m2, name="l")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")
        c6 = CClass(self.m2, "c6")

        add_links({c1: [c2, c3]})
        eq_(c1.links, [c2, c3])
        eq_(c2.links, [c1])
        eq_(c3.links, [c1])
        add_links({c1: c4})
        eq_(c1.links, [c2, c3, c4])
        eq_(c2.links, [c1])
        eq_(c3.links, [c1])
        eq_(c4.links, [c1])
        c1.add_links([c5, c6])
        eq_(c1.links, [c2, c3, c4, c5, c6])
        eq_(c2.links, [c1])
        eq_(c3.links, [c1])
        eq_(c4.links, [c1])
        eq_(c5.links, [c1])
        eq_(c6.links, [c1])

    def test_remove_one_to_n_link(self):
        a = self.m1.association(self.m2, name="l", multiplicity="*")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        set_links({c1: [c2, c3]})
        set_links({c1: c2})
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])
        eq_(c3.links, [])
        try:
            set_links({c1: []})
            exception_expected_()
        except CException as e:
            eq_(e.value, "matching association not found for source 'c1' and targets '[]'")
        set_links({c1: []}, association=a)
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [])

    def test_n_to_n_link(self):
        a = self.m1.association(self.m2, name="l", source_multiplicity="*")
        c1a = CClass(self.m1, "c1a")
        c1b = CClass(self.m1, "c1b")
        c1c = CClass(self.m1, "c1c")
        c2a = CClass(self.m2, "c2a")
        c2b = CClass(self.m2, "c2b")

        set_links({c1a: [c2a, c2b], c1b: [c2a], c1c: [c2b]})

        eq_(c1a.links, [c2a, c2b])
        eq_(c1b.links, [c2a])
        eq_(c1c.links, [c2b])
        eq_(c2a.links, [c1a, c1b])
        eq_(c2b.links, [c1a, c1c])

        set_links({c2a: [c1a, c1b]})
        try:
            set_links({c2b: []})
            exception_expected_()
        except CException as e:
            eq_(e.value, "matching association not found for source 'c2b' and targets '[]'")
        set_links({c2b: []}, association=a)

        eq_(c1a.links, [c2a])
        eq_(c1b.links, [c2a])
        eq_(c1c.links, [])
        eq_(c2a.links, [c1a, c1b])
        eq_(c2b.links, [])

    def test_remove_n_to_n_link(self):
        self.m1.association(self.m2, name="l", source_multiplicity="*", multiplicity="*")
        c1 = CClass(self.m1, "c2")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m1, "c4")
        set_links({c1: [c2, c3], c4: c2})
        set_links({c1: c2, c4: [c3, c2]})
        eq_(c1.links, [c2])
        eq_(c2.links, [c1, c4])
        eq_(c3.links, [c4])
        eq_(c4.links, [c3, c2])

    def test_n_to_n_set_self_link(self):
        self.m1.association(self.m1, name="a", source_multiplicity="*", multiplicity="*", source_role_name="super",
                            role_name="sub")

        top = CClass(self.m1, "Top")
        mid1 = CClass(self.m1, "Mid1")
        mid2 = CClass(self.m1, "Mid2")
        mid3 = CClass(self.m1, "Mid3")
        bottom1 = CClass(self.m1, "Bottom1")
        bottom2 = CClass(self.m1, "Bottom2")

        set_links({top: [mid1, mid2, mid3]}, role_name="sub")
        mid1.add_links([bottom1, bottom2], role_name="sub")

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
        self.m1.association(self.m1, name="a", source_multiplicity="*", multiplicity="*", source_role_name="super",
                            role_name="sub")

        top = CClass(self.m1, "Top")
        mid1 = CClass(self.m1, "Mid1")
        mid2 = CClass(self.m1, "Mid2")
        mid3 = CClass(self.m1, "Mid3")
        bottom1 = CClass(self.m1, "Bottom1")
        bottom2 = CClass(self.m1, "Bottom2")

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
        self.m1.association(self.m2, name="l", multiplicity="*")
        cl = CClass(self.mcl, "CLX")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CObject(cl, "c3")
        try:
            set_links({c1: [c2, c3]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'c3' is an object, but source is an class")
        try:
            set_links({c1: c3})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'c3' is an object, but source is an class")

    def test_duplicate_assignment(self):
        a = self.m1.association(self.m2, "l: *->*")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            set_links({c1: [c2, c2]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "trying to link the same link twice 'c1 -> c2'' twice for the same association")
        eq_(c1.get_links(), [])
        eq_(c2.get_links(), [])

        b = self.m1.association(self.m2, "l: *->*")
        c1.add_links(c2, association=a)
        c1.add_links(c2, association=b)
        eq_(c1.get_links(), [c2, c2])
        eq_(c2.get_links(), [c1, c1])

    def test_non_existing_role_name(self):
        self.m1.association(self.m1, role_name="next", source_role_name="prior",
                            source_multiplicity="1", multiplicity="1")
        c1 = CClass(self.m1, "c1")
        try:
            set_links({c1: c1}, role_name="target")
            exception_expected_()
        except CException as e:
            eq_(e.value, "matching association not found for source 'c1' and targets '['c1']'")

    def test_link_association_ambiguous(self):
        self.m1.association(self.m2, name="a1", role_name="c2", multiplicity="*")
        self.m1.association(self.m2, name="a2", role_name="c2", multiplicity="*")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            set_links({c1: c2})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link specification ambiguous, multiple matching associations found " +
                "for source 'c1' and targets '['c2']'")
        try:
            set_links({c1: c2}, role_name="c2")
            exception_expected_()
        except CException as e:
            eq_(e.value, "link specification ambiguous, multiple matching associations found " +
                "for source 'c1' and targets '['c2']'")

    def test_link_and_get_links_by_association(self):
        a1 = self.m1.association(self.m2, name="a1", multiplicity="*")
        a2 = self.m1.association(self.m2, name="a2", multiplicity="*")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")

        set_links({c1: c2}, association=a1)
        set_links({c1: [c2, c3]}, association=a2)

        eq_(c1.get_links(), [c2, c2, c3])
        eq_(c1.links, [c2, c2, c3])

        eq_(c1.get_links(association=a1), [c2])
        eq_(c1.get_links(association=a2), [c2, c3])

    def test_link_with_inheritance_in_classifier_targets(self):
        sub_class = CMetaclass(superclasses=self.m2)
        a1 = self.m1.association(sub_class, name="a1", multiplicity="*")
        a2 = self.m1.association(self.m2, name="a2", multiplicity="*")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c_sub_1 = CClass(sub_class, "c_sub_1")
        c_sub_2 = CClass(sub_class, "c_sub_2")
        c_super_1 = CClass(self.m2, "c_super_1")
        c_super_2 = CClass(self.m2, "c_super_2")
        try:
            # ambiguous, list works for both associations 
            set_links({c1: [c_sub_1, c_sub_2]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link specification ambiguous, multiple matching associations found " +
                "for source 'c1' and targets '['c_sub_1', 'c_sub_2']'")
        set_links({c1: [c_sub_1, c_sub_2]}, association=a1)
        set_links({c1: [c_sub_1]}, association=a2)
        set_links({c2: [c_super_1, c_super_2]})

        eq_(c1.links, [c_sub_1, c_sub_2, c_sub_1])
        eq_(c1.get_links(), [c_sub_1, c_sub_2, c_sub_1])
        eq_(c2.get_links(), [c_super_1, c_super_2])
        eq_(c1.get_links(association=a1), [c_sub_1, c_sub_2])
        eq_(c1.get_links(association=a2), [c_sub_1])
        eq_(c2.get_links(association=a1), [])
        eq_(c2.get_links(association=a2), [c_super_1, c_super_2])

        # this mixed list is applicable only for a2
        set_links({c2: [c_sub_1, c_super_1]})
        eq_(c2.get_links(association=a1), [])
        eq_(c2.get_links(association=a2), [c_sub_1, c_super_1])

    def test_link_with_inheritance_in_classifier_targets_using_role_names(self):
        sub_class = CMetaclass(superclasses=self.m2)
        a1 = self.m1.association(sub_class, "a1: * -> [sub_class] *")
        a2 = self.m1.association(self.m2, "a2: * -> [c2] *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c_sub_1 = CClass(sub_class, "c_sub_1")
        c_sub_2 = CClass(sub_class, "c_sub_2")
        c_super_1 = CClass(self.m2, "c_super_1")
        c_super_2 = CClass(self.m2, "c_super_2")
        set_links({c1: [c_sub_1, c_sub_2]}, role_name="sub_class")
        set_links({c1: [c_sub_1]}, role_name="c2")
        set_links({c2: [c_super_1, c_super_2]})

        eq_(c1.links, [c_sub_1, c_sub_2, c_sub_1])
        eq_(c1.get_links(), [c_sub_1, c_sub_2, c_sub_1])
        eq_(c2.get_links(), [c_super_1, c_super_2])
        eq_(c1.get_links(association=a1), [c_sub_1, c_sub_2])
        eq_(c1.get_links(association=a2), [c_sub_1])
        eq_(c2.get_links(association=a1), [])
        eq_(c2.get_links(association=a2), [c_super_1, c_super_2])
        eq_(c1.get_links(role_name="sub_class"), [c_sub_1, c_sub_2])
        eq_(c1.get_links(role_name="c2"), [c_sub_1])
        eq_(c2.get_links(role_name="sub_class"), [])
        eq_(c2.get_links(role_name="c2"), [c_super_1, c_super_2])

    def test_link_delete_association(self):
        a = self.m1.association(self.m2, name="l", source_multiplicity="*", multiplicity="*")
        c1 = CClass(self.m1, "c2")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m1, "c4")
        set_links({c1: [c2, c3]})
        set_links({c4: [c2]})
        set_links({c1: [c2]})
        set_links({c4: [c3, c2]})
        a.delete()
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [])
        eq_(c4.links, [])
        try:
            set_links({c1: [c2, c3]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "matching association not found for source 'c2' and targets '['c2', 'c3']'")

    def test_one_to_one_link_multiplicity(self):
        a = self.m1.association(self.m2, name="l", multiplicity="1", source_multiplicity="1..1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m1, "c4")

        try:
            set_links({c1: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c1' have wrong multiplicity '0': should be '1'")
        try:
            set_links({c1: [c2, c3]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c1' have wrong multiplicity '2': should be '1'")

        try:
            set_links({c2: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c2' have wrong multiplicity '0': should be '1..1'")
        try:
            set_links({c2: [c1, c4]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c2' have wrong multiplicity '2': should be '1..1'")

    def test_one_to_n_link_multiplicity(self):
        a = self.m1.association(self.m2, name="l", source_multiplicity="1", multiplicity="1..*")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m1, "c4")

        try:
            set_links({c1: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c1' have wrong multiplicity '0': should be '1..*'")

        set_links({c1: [c2, c3]})
        eq_(c1.get_links(association=a), [c2, c3])

        try:
            set_links({c2: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c2' have wrong multiplicity '0': should be '1'")
        try:
            set_links({c2: [c1, c4]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c2' have wrong multiplicity '2': should be '1'")

    def test_specific_n_to_n_link_multiplicity(self):
        a = self.m1.association(self.m2, name="l", source_multiplicity="1..2", multiplicity="2")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m1, "c4")
        c5 = CClass(self.m1, "c5")
        c6 = CClass(self.m2, "c6")

        try:
            set_links({c1: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c1' have wrong multiplicity '0': should be '2'")
        try:
            set_links({c1: [c2]}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c1' have wrong multiplicity '1': should be '2'")
        try:
            set_links({c1: [c2, c3, c6]}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c1' have wrong multiplicity '3': should be '2'")

        set_links({c1: [c2, c3]})
        eq_(c1.get_links(association=a), [c2, c3])
        set_links({c2: [c1, c4], c1: c3, c4: c3})
        eq_(c2.get_links(association=a), [c1, c4])

        try:
            set_links({c2: []}, association=a)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c2' have wrong multiplicity '0': should be '1..2'")
        try:
            set_links({c2: [c1, c4, c5]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c2' have wrong multiplicity '3': should be '1..2'")

    def test_get_link_objects(self):
        c1_sub_class = CMetaclass("C1Sub", superclasses=self.m1)
        c2_sub_class = CMetaclass("C2Sub", superclasses=self.m2)
        a1 = self.m1.association(self.m2, role_name="c2", source_role_name="c1",
                                 source_multiplicity="*", multiplicity="*")
        a2 = self.m1.association(self.m1, role_name="next", source_role_name="prior",
                                 source_multiplicity="1", multiplicity="0..1")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c1_sub_class = CClass(c1_sub_class, "c1_sub_class")
        c2_sub_class = CClass(c2_sub_class, "c2_sub_class")

        link_objects1 = set_links({c1: c2})
        eq_(link_objects1, c1.link_objects)
        link1 = c1.link_objects[0]
        link2 = [o for o in c1.link_objects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, c1)
        eq_(link1.target, c2)

        link_objects2 = set_links({c1: c2_sub_class})
        eq_(link_objects2, c1.link_objects)
        eq_(len(c1.link_objects), 1)
        link1 = c1.link_objects[0]
        link2 = [o for o in c1.link_objects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, c1)
        eq_(link1.target, c2_sub_class)

        link_objects3 = set_links({c1: c2})
        eq_(link_objects3, c1.link_objects)
        eq_(len(c1.link_objects), 1)
        link1 = c1.link_objects[0]
        link2 = [o for o in c1.link_objects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, c1)
        eq_(link1.target, c2)

        link_objects4 = set_links({c1: c1}, role_name="next")
        eq_(link_objects3 + link_objects4, c1.link_objects)
        eq_(len(c1.link_objects), 2)
        link1 = c1.link_objects[1]
        link2 = [o for o in c1.link_objects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, c1)
        eq_(link1.target, c1)

        link_objects5 = set_links({c1: c1_sub_class}, role_name="next")
        eq_(link_objects3 + link_objects5, c1.link_objects)
        eq_(len(c1.link_objects), 2)
        link1 = c1.link_objects[1]
        link2 = [o for o in c1.link_objects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, c1)
        eq_(link1.target, c1_sub_class)

        set_links({c1: c1}, role_name="next")
        eq_(len(c1.link_objects), 2)
        link1 = c1.link_objects[1]
        link2 = [o for o in c1.link_objects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, c1)
        eq_(link1.target, c1)

        set_links({c1: []}, association=a1)
        set_links({c1: []}, association=a2)
        eq_(len(c1.link_objects), 0)

        set_links({c1_sub_class: c1}, role_name="next")
        eq_(len(c1_sub_class.link_objects), 1)
        link1 = c1_sub_class.link_objects[0]
        link2 = [o for o in c1_sub_class.link_objects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, c1_sub_class)
        eq_(link1.target, c1)

    def test_get_link_objects_self_link(self):
        a1 = self.m1.association(self.m1, role_name="to", source_role_name="from",
                                 source_multiplicity="*", multiplicity="*")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m1, "c3")
        c4 = CClass(self.m1, "c4")

        set_links({c1: [c2, c3, c1]})
        add_links({c4: [c1, c3]})
        link1 = c1.link_objects[0]
        link2 = [o for o in c1.link_objects if o.association == a1][0]
        link3 = [o for o in c1.link_objects if o.role_name == "to"][0]
        link4 = [o for o in c1.link_objects if o.source_role_name == "from"][0]
        eq_(link1, link2)
        eq_(link1, link3)
        eq_(link1, link4)
        eq_(link1.association, a1)
        eq_(link1.source, c1)
        eq_(link1.target, c2)

        eq_(len(c1.link_objects), 4)
        eq_(len(c2.link_objects), 1)
        eq_(len(c3.link_objects), 2)
        eq_(len(c4.link_objects), 2)

    def test_add_links(self):
        self.m1.association(self.m2, "1 -> [role1] *")
        self.m1.association(self.m2, "* -> [role2] *")
        self.m1.association(self.m2, "1 -> [role3] 1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")

        add_links({c1: c2}, role_name="role1")
        eq_(c1.get_links(role_name="role1"), [c2])
        add_links({c1: [c3, c4]}, role_name="role1")
        c1.get_links(role_name="role1")
        eq_(c1.get_links(role_name="role1"), [c2, c3, c4])

        c1.add_links(c2, role_name="role2")
        eq_(c1.get_links(role_name="role2"), [c2])
        c1.add_links([c3, c4], role_name="role2")
        c1.get_links(role_name="role2")
        eq_(c1.get_links(role_name="role2"), [c2, c3, c4])

        c1.add_links(c2, role_name="role3")
        eq_(c1.get_links(role_name="role3"), [c2])
        try:
            add_links({c1: [c3, c4]}, role_name="role3")
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c1' have wrong multiplicity '3': should be '1'")

        try:
            add_links({c1: [c3]}, role_name="role3")
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c1' have wrong multiplicity '2': should be '1'")
        eq_(c1.get_links(role_name="role3"), [c2])

    def test_link_source_multiplicity(self):
        self.m1.association(self.m2, "[sourceRole1] 1 -> [role1] *")
        self.m1.association(self.m2, "[sourceRole2] 1 -> [role2] 1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        CClass(self.m2, "c4")
        CClass(self.m2, "c5")

        set_links({c1: c3}, role_name="role1")
        set_links({c2: c3}, role_name="role1")

        eq_(c3.get_links(role_name="sourceRole1"), [c2])

    def test_add_links_source_multiplicity(self):
        self.m1.association(self.m2, "[sourceRole1] 1 -> [role1] *")
        self.m1.association(self.m2, "[sourceRole2] 1 -> [role2] 1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")
        c6 = CClass(self.m2, "c6")

        add_links({c2: c3}, role_name="role1")
        add_links({c2: c4}, role_name="role1")

        eq_(c3.get_links(role_name="sourceRole1"), [c2])

        add_links({c2: c5}, role_name="role1")
        eq_(c2.get_links(role_name="role1"), [c3, c4, c5])

        try:
            add_links({c1: [c4]}, role_name="role1")
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c4' have wrong multiplicity '2': should be '1'")

        add_links({c1: c6}, role_name="role2")
        eq_(c1.get_links(role_name="role2"), [c6])
        try:
            add_links({c1: [c3, c4]}, role_name="role2")
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c1' have wrong multiplicity '3': should be '1'")
        eq_(c1.get_links(role_name="role2"), [c6])

    def test_set_links_multiple_links_in_definition(self):
        self.m1.association(self.m2, "[sourceRole1] * -> [role1] *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m1, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")

        set_links({c1: c4, c2: [c4], c5: [c1, c2, c3]})
        eq_(c1.get_links(), [c4, c5])
        eq_(c2.get_links(), [c4, c5])
        eq_(c3.get_links(), [c5])
        eq_(c4.get_links(), [c1, c2])
        eq_(c5.get_links(), [c1, c2, c3])

    def test_add_links_multiple_links_in_definition(self):
        self.m1.association(self.m2, "[sourceRole1] * -> [role1] *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m1, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")

        add_links({c1: c4, c2: [c4], c5: [c1, c2, c3]})
        eq_(c1.get_links(), [c4, c5])
        eq_(c2.get_links(), [c4, c5])
        eq_(c3.get_links(), [c5])
        eq_(c4.get_links(), [c1, c2])
        eq_(c5.get_links(), [c1, c2, c3])

    def test_wrong_types_delete_links(self):
        self.m1.association(self.m2, name="l", multiplicity="1")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            delete_links(c1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "link definitions should be of the form " +
                "{<link source 1>: <link target(s) 1>, ..., <link source n>: <link target(s) n>}")
        try:
            delete_links({c1: self.mcl})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            delete_links({c1: [c2, self.mcl]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            delete_links({c1: [c2, None]})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link target 'None' is neither an object nor a class")
        try:
            delete_links({self.mcl: c2})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link source 'MCL' is neither an object nor a class")
        try:
            delete_links({None: c2})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link should not contain an empty source")

    def test_delete_one_to_one_link(self):
        self.m1.association(self.m2, "l: 1 -> [c2] 0..1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m1, "c3")
        c4 = CClass(self.m2, "c4")

        links = add_links({c1: c2, c3: c4})
        c1.delete_links(c2)
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [c4])
        eq_(c4.links, [c3])
        eq_(c1.link_objects, [])
        eq_(c2.link_objects, [])
        eq_(c3.link_objects, [links[1]])
        eq_(c4.link_objects, [links[1]])
        delete_links({c3: c4})
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [])
        eq_(c4.links, [])
        eq_(c1.link_objects, [])
        eq_(c2.link_objects, [])
        eq_(c3.link_objects, [])
        eq_(c4.link_objects, [])

    def test_delete_one_to_one_link_wrong_multiplicity(self):
        self.m1.association(self.m2, "l: 1 -> [c2] 1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        add_links({c1: c2})
        try:
            c1.delete_links(c2)
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c1' have wrong multiplicity '0': should be '1'")
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])

    def test_delete_one_to_n_links(self):
        self.m1.association(self.m2, "l: 0..1 -> *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")

        add_links({c1: [c3, c4], c2: [c5]})
        c4.delete_links([c1])
        eq_(c1.links, [c3])
        eq_(c2.links, [c5])
        eq_(c3.links, [c1])
        eq_(c4.links, [])
        eq_(c5.links, [c2])

        c4.add_links([c2])
        eq_(c2.links, [c5, c4])
        delete_links({c1: c3, c2: c2.links})
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [])
        eq_(c4.links, [])
        eq_(c5.links, [])

    def test_delete_one_to_n_links_wrong_multiplicity(self):
        self.m1.association(self.m2, "l: 1 -> *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")

        add_links({c1: [c3, c4], c2: [c5]})

        try:
            c4.delete_links([c1])
            exception_expected_()
        except CException as e:
            eq_(e.value, "links of object 'c4' have wrong multiplicity '0': should be '1'")

    def test_delete_n_to_n_links(self):
        self.m1.association(self.m2, "l: * -> *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")
        c6 = CClass(self.m2, "c6")

        add_links({c1: [c3, c4], c2: [c4, c5]})
        c4.delete_links([c1, c2])
        eq_(c1.links, [c3])
        eq_(c2.links, [c5])
        eq_(c3.links, [c1])
        eq_(c4.links, [])
        eq_(c5.links, [c2])

        add_links({c4: [c1, c2], c6: [c2, c1]})
        delete_links({c1: c6, c2: [c4, c5]})
        eq_(c1.links, [c3, c4])
        eq_(c2.links, [c6])
        eq_(c3.links, [c1])
        eq_(c4.links, [c1])
        eq_(c5.links, [])
        eq_(c6.links, [c2])

    def test_delete_link_no_matching_link(self):
        a = self.m1.association(self.m2, "l: 0..1 -> *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")

        add_links({c1: [c3, c4], c2: [c5]}, association=a)

        try:
            delete_links({c1: c5})
            exception_expected_()
        except CException as e:
            eq_(e.value, "no link found for 'c1 -> c5' in delete links")

        b = self.m1.association(self.m2, "l: 0..1 -> *")
        try:
            delete_links({c1: c5})
            exception_expected_()
        except CException as e:
            eq_(e.value, "no link found for 'c1 -> c5' in delete links")

        try:
            c4.delete_links([c1], association=b)
            exception_expected_()
        except CException as e:
            eq_(e.value, "no link found for 'c4 -> c1' in delete links for given association")

    def test_delete_link_select_by_association(self):
        a = self.m1.association(self.m2, "a: * -> *")
        b = self.m1.association(self.m2, "b: * -> *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")

        add_links({c1: [c3], c2: [c3, c4]}, association=b)
        delete_links({c2: c3})
        eq_(c1.links, [c3])
        eq_(c2.links, [c4])
        eq_(c3.links, [c1])
        eq_(c4.links, [c2])
        add_links({c1: [c3], c2: [c3, c4]}, association=a)

        try:
            delete_links({c1: c3})
            exception_expected_()
        except CException as e:
            eq_(e.value, "link definition in delete links ambiguous for link 'c1->c3': found multiple matches")

        delete_links({c1: c3, c2: c4}, association=b)
        eq_(c1.links, [c3])
        eq_(c2.links, [c3, c4])
        eq_(c3.links, [c1, c2])
        eq_(c4.links, [c2])
        for o in [c1, c2, c3, c4]:
            for lo in o.link_objects:
                eq_(lo.association, a)

        c1.add_links(c3, association=b)
        try:
            c1.delete_links(c3)
            exception_expected_()
        except CException as e:
            eq_(e.value, "link definition in delete links ambiguous for link 'c1->c3': found multiple matches")

        eq_(c1.links, [c3, c3])
        eq_(c2.links, [c3, c4])
        eq_(c3.links, [c1, c2, c1])
        eq_(c4.links, [c2])

        c1.delete_links(c3, association=a)
        eq_(c1.links, [c3])
        eq_(c2.links, [c3, c4])
        eq_(c3.links, [c2, c1])
        eq_(c4.links, [c2])

    def test_delete_link_select_by_role_name(self):
        a = self.m1.association(self.m2, "a: [sourceA] * -> [targetA] *")
        self.m1.association(self.m2, "b: [sourceB] * -> [targetB] *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")

        add_links({c1: [c3], c2: [c3, c4]}, role_name="targetB")
        delete_links({c2: c3})
        eq_(c1.links, [c3])
        eq_(c2.links, [c4])
        eq_(c3.links, [c1])
        eq_(c4.links, [c2])
        add_links({c1: [c3], c2: [c3, c4]}, role_name="targetA")

        delete_links({c1: c3, c2: c4}, role_name="targetB")
        eq_(c1.links, [c3])
        eq_(c2.links, [c3, c4])
        eq_(c3.links, [c1, c2])
        eq_(c4.links, [c2])
        for o in [c1, c2, c3, c4]:
            for lo in o.link_objects:
                eq_(lo.association, a)

        add_links({c1: [c3], c2: [c3, c4]}, role_name="targetB")
        c3.delete_links([c1, c2], role_name="sourceB")
        delete_links({c4: c2}, role_name="sourceB")

        eq_(c1.links, [c3])
        eq_(c2.links, [c3, c4])
        eq_(c3.links, [c1, c2])
        eq_(c4.links, [c2])
        for o in [c1, c2, c3, c4]:
            for lo in o.link_objects:
                eq_(lo.association, a)

    def test_delete_links_wrong_role_name(self):
        self.m1.association(self.m2, "a: [sourceA] * -> [targetA] *")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c1.add_links(c2)
        try:
            c1.delete_links(c2, role_name="target")
            exception_expected_()
        except CException as e:
            eq_(e.value, "no link found for 'c1 -> c2' in delete links for given role name 'target'")

    def test_delete_links_wrong_association(self):
        self.m1.association(self.m2, "a: [sourceA] * -> [targetA] *")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c1.add_links(c2)
        try:
            c1.delete_links(c2, association=c1)
            exception_expected_()
        except CException as e:
            eq_(e.value, "'c1' is not a association")
        b = self.m1.association(self.m2, "b: [sourceB] * -> [targetB] *")
        try:
            c1.delete_links(c2, association=b)
            exception_expected_()
        except CException as e:
            eq_(e.value, "no link found for 'c1 -> c2' in delete links for given association")
        try:
            c1.delete_links(c2, association=b, role_name="x")
            exception_expected_()
        except CException as e:
            eq_(e.value,
                "no link found for 'c1 -> c2' in delete links for given role name 'x' and for given association")

    def test_link_label_none_default(self):
        a1 = self.m1.association(self.m2, name="a1", multiplicity="*")
        a2 = self.m1.association(self.m2, multiplicity="*")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")

        l1 = set_links({c1: c2}, association=a1)
        l2 = set_links({c1: [c2, c3]}, association=a2)

        eq_(l1[0].label, None)
        eq_(l2[0].label, None)
        eq_(l2[1].label, None)

    def test_link_label_get_set(self):
        a1 = self.m1.association(self.m2, name="a1", multiplicity="*")
        a2 = self.m1.association(self.m2, multiplicity="*")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")

        l1 = set_links({c1: c2}, association=a1, label="l1")
        l2 = add_links({c1: [c2, c3]}, association=a2, label="l2")

        eq_(l1[0].label, "l1")
        eq_(l2[0].label, "l2")
        eq_(l2[1].label, "l2")

        l2[1].label = "l3"
        eq_(l2[0].label, "l2")
        eq_(l2[1].label, "l3")

        l3 = c1.add_links(c3, association=a1, label="x1")
        eq_(l3[0].label, "x1")


if __name__ == "__main__":
    nose.main()
