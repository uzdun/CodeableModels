import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CClass, CObject, CAttribute, CException, CEnum, setLinks, addLinks, deleteLinks

class TestObjectLinks():
    def setUp(self):
        self.mcl = CMetaclass("MCL")
        self.c1 = CClass(self.mcl, "C1")
        self.c2 = CClass(self.mcl, "C2")

    def testLinkMethodsWrongKeywordArgs(self):
        o1 = CObject(self.c1, "o1")
        try:
            addLinks({o1:o1}, associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            o1.addLinks(o1, associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            setLinks({o1: o1}, associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            deleteLinks({o1:o1}, associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            o1.deleteLinks(o1, associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            o1.getLinks(associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            deleteLinks({o1:o1}, stereotypeInstances = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")

    def testSetOneToOneLink(self):
        self.c1.association(self.c2, name = "l", multiplicity = "1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        eq_(o1.links, [])

        setLinks({o1: o2})
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])

        setLinks({o1: o3})
        eq_(o1.links, [o3])
        eq_(o2.links, [])
        eq_(o3.links, [o1])

    def testAddOneToOneLink(self):
        self.c1.association(self.c2, "l: 1 -> [target] 0..1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        eq_(o1.links, [])

        addLinks({o1: o3})
        eq_(o1.links, [o3])
        eq_(o3.links, [o1])

        setLinks({o1: []}, roleName = "target")
        eq_(o1.links, [])

        o1.addLinks(o2)
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])

        try:
            addLinks({o1: o3})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o1' have wrong multiplicity '2': should be '0..1'")
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])
        eq_(o3.links, [])
          
    def testWrongTypesAddLinks(self):
        self.c1.association(self.c2, name = "l", multiplicity = "1")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            addLinks({o1: self.mcl})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            o1.addLinks([o2, self.mcl])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")

    def testWrongTypesSetLinks(self):
        self.c1.association(self.c2, name = "l", multiplicity = "1")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            setLinks({o1: self.mcl})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            setLinks({o1: [o2, self.mcl]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            setLinks({o1: [o2, None]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'None' is neither an object nor a class")
        try:
            setLinks({self.mcl: o2})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link source 'MCL' is neither an object nor a class")
        try:
            setLinks({None: o2})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link should not contain an empty source")
            
    def testWrongFormatSetLinks(self):
        self.c1.association(self.c2, name = "l", multiplicity = "1")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            setLinks([o1, o2])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link definitions should be of the form {<link source 1>: <link target(s) 1>, ..., <link source n>: <link target(s) n>}")

    def testRemoveOneToOneLink(self):
        a = self.c1.association(self.c2, "l: 1 -> [c2] 0..1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c1, "o3")
        o4 = CObject(self.c2, "o4")

        links = setLinks({o1: o2, o3: o4})
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])
        eq_(o3.links, [o4])
        eq_(o4.links, [o3])
        eq_(o1.linkObjects, [links[0]])
        eq_(o2.linkObjects, [links[0]])
        eq_(o3.linkObjects, [links[1]])
        eq_(o4.linkObjects, [links[1]])

        try:
            links = setLinks({o1: None})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "matching association not found for source 'o1' and targets '[]'")

        setLinks({o1: None}, association = a)
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [o4])
        eq_(o4.links, [o3])
        eq_(o1.linkObjects, [])
        eq_(o2.linkObjects, [])
        eq_(o3.linkObjects, [links[1]])
        eq_(o4.linkObjects, [links[1]]) 

    def testSetLinksOneToNLink(self):
        self.c1.association(self.c2, name = "l")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        setLinks({o1: [o2, o3]})
        eq_(o1.links, [o2, o3])
        eq_(o2.links, [o1])
        eq_(o3.links, [o1])
        setLinks({o1: o2})
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])
        eq_(o3.links, [])
        setLinks({o3: o1, o2: o1})
        eq_(o1.links, [o3, o2])
        eq_(o2.links, [o1])
        eq_(o3.links, [o1])

    def testAddLinksOneToNLink(self):
        self.c1.association(self.c2, name = "l")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")
        o6 = CObject(self.c2, "o6")

        addLinks({o1: [o2, o3]})
        eq_(o1.links, [o2, o3])
        eq_(o2.links, [o1])
        eq_(o3.links, [o1])
        addLinks({o1: o4})
        eq_(o1.links, [o2, o3, o4])
        eq_(o2.links, [o1])
        eq_(o3.links, [o1])
        eq_(o4.links, [o1])
        o1.addLinks([o5, o6])
        eq_(o1.links, [o2, o3, o4, o5, o6])      
        eq_(o2.links, [o1])
        eq_(o3.links, [o1])
        eq_(o4.links, [o1])
        eq_(o5.links, [o1])
        eq_(o6.links, [o1])

    def testRemoveOneToNLink(self):
        a = self.c1.association(self.c2, name = "l", multiplicity = "*")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        setLinks({o1: [o2, o3]})
        setLinks({o1: o2})
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])
        eq_(o3.links, [])
        try:
            setLinks({o1: []})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "matching association not found for source 'o1' and targets '[]'")
        setLinks({o1: []}, association = a)
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [])

    def testNToNLink(self):
        a = self.c1.association(self.c2, name = "l", sourceMultiplicity = "*")
        o1a = CObject(self.c1, "o1a")
        o1b = CObject(self.c1, "o1b")
        o1c = CObject(self.c1, "o1c")
        o2a = CObject(self.c2, "o2a")
        o2b = CObject(self.c2, "o2b")

        setLinks({o1a: [o2a, o2b], o1b: [o2a], o1c: [o2b]})
        
        eq_(o1a.links, [o2a, o2b])
        eq_(o1b.links, [o2a])
        eq_(o1c.links, [o2b])
        eq_(o2a.links, [o1a, o1b])
        eq_(o2b.links, [o1a, o1c])

        setLinks({o2a: [o1a, o1b]})
        try:
            setLinks({o2b: []})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "matching association not found for source 'o2b' and targets '[]'")
        setLinks({o2b: []}, association = a)

        eq_(o1a.links, [o2a])
        eq_(o1b.links, [o2a])
        eq_(o1c.links, [])
        eq_(o2a.links, [o1a, o1b])
        eq_(o2b.links, [])

    def testRemoveNToNLink(self):
        self.c1.association(self.c2, name = "l", sourceMultiplicity = "*", multiplicity = "*")
        o1 = CObject(self.c1, "o2")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c1, "o4")
        setLinks({o1: [o2, o3], o4: o2})
        setLinks({o1: o2, o4: [o3, o2]})
        eq_(o1.links, [o2])
        eq_(o2.links, [o1, o4])
        eq_(o3.links, [o4])
        eq_(o4.links, [o3, o2])

    def testNToNSetSelfLink(self):
        self.c1.association(self.c1, name = "a", sourceMultiplicity = "*", multiplicity = "*", sourceRoleName = "super", roleName = "sub")

        top = CObject(self.c1, "Top")
        mid1 = CObject(self.c1, "Mid1")
        mid2 = CObject(self.c1, "Mid2")
        mid3 = CObject(self.c1, "Mid3")
        bottom1 = CObject(self.c1, "Bottom1")
        bottom2 = CObject(self.c1, "Bottom2")

        setLinks({top: [mid1, mid2, mid3]}, roleName = "sub")
        addLinks({mid1: [bottom1, bottom2]}, roleName = "sub")

        eq_(top.links, [mid1, mid2, mid3])
        eq_(mid1.links, [top, bottom1, bottom2])
        eq_(mid2.links, [top])
        eq_(mid3.links, [top])
        eq_(bottom1.links, [mid1])
        eq_(bottom2.links, [mid1])

        eq_(top.getLinks(roleName = "sub"), [mid1, mid2, mid3])
        eq_(mid1.getLinks(roleName = "sub"), [bottom1, bottom2])
        eq_(mid2.getLinks(roleName = "sub"), [])
        eq_(mid3.getLinks(roleName = "sub"), [])
        eq_(bottom1.getLinks(roleName = "sub"), [])
        eq_(bottom2.getLinks(roleName = "sub"), [])

        eq_(top.getLinks(roleName = "super"), [])
        eq_(mid1.getLinks(roleName = "super"), [top])
        eq_(mid2.getLinks(roleName = "super"), [top])
        eq_(mid3.getLinks(roleName = "super"), [top])
        eq_(bottom1.getLinks(roleName = "super"), [mid1])
        eq_(bottom2.getLinks(roleName = "super"), [mid1])

    def testNToNSetSelfLinkDeleteLinks(self):
        self.c1.association(self.c1, name = "a", sourceMultiplicity = "*", multiplicity = "*", sourceRoleName = "super", roleName = "sub")

        top = CObject(self.c1, "Top")
        mid1 = CObject(self.c1, "Mid1")
        mid2 = CObject(self.c1, "Mid2")
        mid3 = CObject(self.c1, "Mid3")
        bottom1 = CObject(self.c1, "Bottom1")
        bottom2 = CObject(self.c1, "Bottom2")

        setLinks({top: [mid1, mid2, mid3], mid1: [bottom1, bottom2]}, roleName = "sub")
        # delete links
        setLinks({top: []}, roleName = "sub")
        eq_(top.links, [])
        eq_(mid1.links, [bottom1, bottom2])
        # change links
        setLinks({mid1: top, mid3: top, bottom1: mid1, bottom2: mid1}, roleName = "super")

        eq_(top.links, [mid1, mid3])
        eq_(mid1.links, [top, bottom1, bottom2])
        eq_(mid2.links, [])
        eq_(mid3.links, [top])
        eq_(bottom1.links, [mid1])
        eq_(bottom2.links, [mid1])

        eq_(top.getLinks(roleName = "sub"), [mid1, mid3])
        eq_(mid1.getLinks(roleName = "sub"), [bottom1, bottom2])
        eq_(mid2.getLinks(roleName = "sub"), [])
        eq_(mid3.getLinks(roleName = "sub"), [])
        eq_(bottom1.getLinks(roleName = "sub"), [])
        eq_(bottom2.getLinks(roleName = "sub"), [])

        eq_(top.getLinks(roleName = "super"), [])
        eq_(mid1.getLinks(roleName = "super"), [top])
        eq_(mid2.getLinks(roleName = "super"), [])
        eq_(mid3.getLinks(roleName = "super"), [top])
        eq_(bottom1.getLinks(roleName = "super"), [mid1])
        eq_(bottom2.getLinks(roleName = "super"), [mid1])

    def testIncompatibleClassifier(self):
        self.c1.association(self.c2, name = "l", multiplicity = "*")
        cl = CClass(self.mcl, "CLX")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(cl, "o3")
        try:
            setLinks({o1: [o2, o3]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "object 'o3' has an incompatible classifier")
        try:
            setLinks({o1: o3})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "matching association not found for source 'o1' and targets '['o3']'")

    def testDuplicateAssignment(self):
        a = self.c1.association(self.c2, "l: *->*")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            setLinks({o1: [o2, o2]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "trying to link the same link twice 'o1 -> o2'' twice for the same association")
        eq_(o1.getLinks(), [])
        eq_(o2.getLinks(), [])
        b = self.c1.association(self.c2, "l: *->*")
        o1.addLinks(o2, association = a)
        o1.addLinks(o2, association = b)        
        eq_(o1.getLinks(), [o2, o2])
        eq_(o2.getLinks(), [o1, o1])

    def testNonExistingRoleName(self):
        self.c1.association(self.c1, roleName = "next", sourceRoleName = "prior", 
            sourceMultiplicity = "1", multiplicity = "1")
        o1 = CObject(self.c1, "o1")
        try:
            setLinks({o1 : o1}, roleName = "target")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "matching association not found for source 'o1' and targets '['o1']'")

    def testLinkAssociationAmbiguous(self):
        self.c1.association(self.c2, name = "a1", roleName = "c2", multiplicity = "*")
        self.c1.association(self.c2, name = "a2", roleName = "c2", multiplicity = "*")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            setLinks({o1:o2})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link specification ambiguous, multiple matching associations found for source 'o1' and targets '['o2']'")
        try:
            setLinks({o1:o2}, roleName = "c2")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link specification ambiguous, multiple matching associations found for source 'o1' and targets '['o2']'")

    def testLinkAndGetLinksByAssociation(self):
        a1 = self.c1.association(self.c2, name = "a1", multiplicity = "*")
        a2 = self.c1.association(self.c2, name = "a2", multiplicity = "*")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        setLinks({o1:o2}, association = a1) 
        setLinks({o1:[o2, o3]}, association = a2) 

        eq_(o1.getLinks(), [o2, o2, o3])
        eq_(o1.links, [o2, o2, o3])

        eq_(o1.getLinks(association = a1), [o2])
        eq_(o1.getLinks(association = a2), [o2, o3])

    def testLinkWithInheritanceInClassifierTargets(self):
        subCl = CClass(self.mcl, superclasses = self.c2)
        a1 = self.c1.association(subCl, name = "a1", multiplicity = "*")
        a2 = self.c1.association(self.c2, name = "a2", multiplicity = "*")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o_sub_1 = CObject(subCl, "o_sub_1")
        o_sub_2 = CObject(subCl, "o_sub_2")
        o_super_1 = CObject(self.c2, "o_super_1")
        o_super_2 = CObject(self.c2, "o_super_2")
        try:
            # ambiguous, list works for both associations 
            setLinks({o1: [o_sub_1, o_sub_2]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link specification ambiguous, multiple matching associations found for source 'o1' and targets '['o_sub_1', 'o_sub_2']'")
        setLinks({o1: [o_sub_1, o_sub_2]}, association = a1)
        setLinks({o1: [o_sub_1]}, association = a2)
        setLinks({o2: [o_super_1, o_super_2]})

        eq_(o1.links, [o_sub_1, o_sub_2, o_sub_1])
        eq_(o1.getLinks(), [o_sub_1, o_sub_2, o_sub_1])
        eq_(o2.getLinks(), [o_super_1, o_super_2])
        eq_(o1.getLinks(association = a1), [o_sub_1, o_sub_2])
        eq_(o1.getLinks(association = a2), [o_sub_1])
        eq_(o2.getLinks(association = a1), [])
        eq_(o2.getLinks(association = a2), [o_super_1, o_super_2])

        # this mixed list is applicable only for a2
        setLinks({o2: [o_sub_1, o_super_1]})
        eq_(o2.getLinks(association = a1), [])
        eq_(o2.getLinks(association = a2), [o_sub_1, o_super_1])

    def testLinkWithInheritanceInClassifierTargets_UsingRoleNames(self):
        subCl = CClass(self.mcl, superclasses = self.c2)
        a1 = self.c1.association(subCl, "a1: * -> [subCl] *")
        a2 = self.c1.association(self.c2, "a2: * -> [c2] *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o_sub_1 = CObject(subCl, "o_sub_1")
        o_sub_2 = CObject(subCl, "o_sub_2")
        o_super_1 = CObject(self.c2, "o_super_1")
        o_super_2 = CObject(self.c2, "o_super_2")
        setLinks({o1: [o_sub_1, o_sub_2]}, roleName = "subCl")
        setLinks({o1: [o_sub_1]}, roleName = "c2")
        setLinks({o2: [o_super_1, o_super_2]})

        eq_(o1.links, [o_sub_1, o_sub_2, o_sub_1])
        eq_(o1.getLinks(), [o_sub_1, o_sub_2, o_sub_1])
        eq_(o2.getLinks(), [o_super_1, o_super_2])
        eq_(o1.getLinks(association = a1), [o_sub_1, o_sub_2])
        eq_(o1.getLinks(association = a2), [o_sub_1])
        eq_(o2.getLinks(association = a1), [])
        eq_(o2.getLinks(association = a2), [o_super_1, o_super_2])
        eq_(o1.getLinks(roleName = "subCl"), [o_sub_1, o_sub_2])
        eq_(o1.getLinks(roleName = "c2"), [o_sub_1])
        eq_(o2.getLinks(roleName = "subCl"), [])
        eq_(o2.getLinks(roleName = "c2"), [o_super_1, o_super_2])

    def testLinkDeleteAssociation(self):
        a = self.c1.association(self.c2, name = "l", sourceMultiplicity = "*", multiplicity = "*")
        o1 = CObject(self.c1, "o2")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c1, "o4")
        setLinks({o1: [o2, o3]})
        setLinks({o4: [o2]})  
        setLinks({o1: [o2]})
        setLinks({o4: [o3, o2]})
        a.delete()
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [])
        eq_(o4.links, [])
        try:
            setLinks({o1: [o2, o3]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "matching association not found for source 'o2' and targets '['o2', 'o3']'")

    def testOneToOneLinkMultiplicity(self):
        a = self.c1.association(self.c2, name = "l", multiplicity = "1", sourceMultiplicity = "1..1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c1, "o4")

        try:
            setLinks({o1: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o1' have wrong multiplicity '0': should be '1'")
        try:
            setLinks({o1: [o2, o3]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o1' have wrong multiplicity '2': should be '1'")

        try:
            setLinks({o2: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o2' have wrong multiplicity '0': should be '1..1'")
        try:
            setLinks({o2: [o1, o4]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o2' have wrong multiplicity '2': should be '1..1'")

    def testOneToNLinkMultiplicity(self):
        a = self.c1.association(self.c2, name = "l", sourceMultiplicity = "1", multiplicity = "1..*")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c1, "o4")

        try:
            setLinks({o1: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o1' have wrong multiplicity '0': should be '1..*'")
        
        setLinks({o1: [o2, o3]})
        eq_(o1.getLinks(association = a), [o2, o3])

        try:
            setLinks({o2: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o2' have wrong multiplicity '0': should be '1'")
        try:
            setLinks({o2: [o1, o4]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o2' have wrong multiplicity '2': should be '1'")


    def testSpecificNToNLinkMultiplicity(self):
        a = self.c1.association(self.c2, name = "l", sourceMultiplicity = "1..2", multiplicity = "2")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c1, "o4")
        o5 = CObject(self.c1, "o5")
        o6 = CObject(self.c2, "o6")
        
        try:
            setLinks({o1: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o1' have wrong multiplicity '0': should be '2'")
        try:
            setLinks({o1: [o2]}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o1' have wrong multiplicity '1': should be '2'")
        try:
            setLinks({o1: [o2, o3, o6]}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o1' have wrong multiplicity '3': should be '2'")

        setLinks({o1: [o2, o3]})
        eq_(o1.getLinks(association = a), [o2, o3])
        setLinks({o2: [o1, o4], o1: o3, o4: o3})
        eq_(o2.getLinks(association = a), [o1, o4])

        try:
            setLinks({o2: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o2' have wrong multiplicity '0': should be '1..2'")
        try:
            setLinks({o2: [o1, o4, o5]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o2' have wrong multiplicity '3': should be '1..2'")

    def testGetLinkObjects(self):
        c1Sub = CClass(self.mcl, "C1Sub", superclasses = self.c1)
        c2Sub = CClass(self.mcl, "C2Sub", superclasses = self.c2)
        a1 = self.c1.association(self.c2, roleName = "c2", sourceRoleName = "c1", 
            sourceMultiplicity = "*", multiplicity = "*")
        a2 = self.c1.association(self.c1, roleName = "next", sourceRoleName = "prior", 
            sourceMultiplicity = "1", multiplicity = "0..1")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o1Sub = CObject(c1Sub, "o1Sub")
        o2Sub = CObject(c2Sub, "o2Sub")

        linkObjects1 = setLinks({o1: o2})
        eq_(linkObjects1, o1.linkObjects)
        link1 = o1.linkObjects[0]
        link2 = [o for o in o1.linkObjects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, o1)
        eq_(link1.target, o2)

        linkObjects2 = setLinks({o1: o2Sub})
        eq_(linkObjects2, o1.linkObjects)
        eq_(len(o1.linkObjects), 1)
        link1 = o1.linkObjects[0]
        link2 = [o for o in o1.linkObjects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, o1)
        eq_(link1.target, o2Sub)

        linkObjects3 = setLinks({o1: o2})
        eq_(linkObjects3, o1.linkObjects)
        eq_(len(o1.linkObjects), 1)
        link1 = o1.linkObjects[0]
        link2 = [o for o in o1.linkObjects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, o1)
        eq_(link1.target, o2)

        linkObjects4 = setLinks({o1: o1}, roleName = "next")
        eq_(linkObjects3 + linkObjects4, o1.linkObjects)
        eq_(len(o1.linkObjects), 2)
        link1 = o1.linkObjects[1]
        link2 = [o for o in o1.linkObjects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, o1)
        eq_(link1.target, o1)

        linkObjects5 = setLinks({o1: o1Sub}, roleName = "next")
        eq_(linkObjects3 + linkObjects5, o1.linkObjects)
        eq_(len(o1.linkObjects), 2)
        link1 = o1.linkObjects[1]
        link2 = [o for o in o1.linkObjects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, o1)
        eq_(link1.target, o1Sub)

        setLinks({o1: o1}, roleName = "next")
        eq_(len(o1.linkObjects), 2)
        link1 = o1.linkObjects[1]
        link2 = [o for o in o1.linkObjects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, o1)
        eq_(link1.target, o1)

        setLinks({o1: []}, association = a1)
        setLinks({o1: []}, association = a2)
        eq_(len(o1.linkObjects), 0)

        setLinks({o1Sub: o1}, roleName = "next")
        eq_(len(o1Sub.linkObjects), 1)
        link1 = o1Sub.linkObjects[0]
        link2 = [o for o in o1Sub.linkObjects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, o1Sub)
        eq_(link1.target, o1)    

    def testGetLinkObjectsSelfLink(self):
        a1 = self.c1.association(self.c1, roleName = "to", sourceRoleName = "from", 
            sourceMultiplicity = "*", multiplicity = "*")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c1, "o3")
        o4 = CObject(self.c1, "o4")

        setLinks({o1: [o2, o3, o1]})
        o4.addLinks([o1, o3])
        link1 = o1.linkObjects[0]
        link2 = [o for o in o1.linkObjects if o.association == a1][0]
        link3 = [o for o in o1.linkObjects if o.roleName == "to"][0]
        link4 = [o for o in o1.linkObjects if o.sourceRoleName == "from"][0]
        eq_(link1, link2)
        eq_(link1, link3)
        eq_(link1, link4)
        eq_(link1.association, a1)
        eq_(link1.source, o1)
        eq_(link1.target, o2)

        eq_(len(o1.linkObjects), 4)
        eq_(len(o2.linkObjects), 1)
        eq_(len(o3.linkObjects), 2)
        eq_(len(o4.linkObjects), 2)

    def testAddLinks(self):
        a1 = self.c1.association(self.c2, "1 -> [role1] *")
        a2 = self.c1.association(self.c2, "* -> [role2] *")
        a3 = self.c1.association(self.c2, "1 -> [role3] 1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")

        addLinks({o1: o2}, roleName = "role1")
        eq_(o1.getLinks(roleName = "role1"), [o2])
        addLinks({o1: [o3, o4]}, roleName = "role1")
        o1.getLinks(roleName = "role1")
        eq_(o1.getLinks(roleName = "role1"), [o2, o3, o4])

        o1.addLinks(o2, roleName = "role2")
        eq_(o1.getLinks(roleName = "role2"), [o2])
        o1.addLinks([o3, o4], roleName = "role2")
        o1.getLinks(roleName = "role2")
        eq_(o1.getLinks(roleName = "role2"), [o2, o3, o4])

        addLinks({o1: o2}, roleName = "role3")
        eq_(o1.getLinks(roleName = "role3"), [o2])
        try:
            addLinks({o1: [o3, o4]}, roleName = "role3")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o1' have wrong multiplicity '3': should be '1'")

        try:
            addLinks({o1: [o3]}, roleName = "role3")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o1' have wrong multiplicity '2': should be '1'")
        eq_(o1.getLinks(roleName = "role3"), [o2])


    def testLinkSourceMultiplicity(self):
        a1 = self.c1.association(self.c2, "[sourceRole1] 1 -> [role1] *")
        a2 = self.c1.association(self.c2, "[sourceRole2] 1 -> [role2] 1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")

        setLinks({o1: o3}, roleName = "role1")
        setLinks({o2: o3}, roleName = "role1")

        eq_(o3.getLinks(roleName = "sourceRole1"), [o2])

    def testAddLinksSourceMultiplicity(self):
        a1 = self.c1.association(self.c2, "[sourceRole1] 1 -> [role1] *")
        a2 = self.c1.association(self.c2, "[sourceRole2] 1 -> [role2] 1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")
        o6 = CObject(self.c2, "o6")

        addLinks({o2: o3}, roleName = "role1")
        addLinks({o2: o4}, roleName = "role1")

        eq_(o3.getLinks(roleName = "sourceRole1"), [o2])

        addLinks({o2: o5}, roleName = "role1")
        eq_(o2.getLinks(roleName = "role1"), [o3, o4, o5])

        try:
            addLinks({o1: [o4]}, roleName = "role1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o4' have wrong multiplicity '2': should be '1'")

        addLinks({o1: o6}, roleName = "role2")
        eq_(o1.getLinks(roleName = "role2"), [o6])
        try:
            addLinks({o1: [o3, o4]}, roleName = "role2")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o1' have wrong multiplicity '3': should be '1'")       
        eq_(o1.getLinks(roleName = "role2"), [o6])


    def testSetLinksMultipleLinksInDefinition(self):
        a1 = self.c1.association(self.c2, "[sourceRole1] * -> [role1] *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c1, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")

        setLinks({o1: o4, o2: [o4], o5: [o1, o2, o3]})
        eq_(o1.getLinks(), [o4, o5])
        eq_(o2.getLinks(), [o4, o5])
        eq_(o3.getLinks(), [o5])
        eq_(o4.getLinks(), [o1, o2])
        eq_(o5.getLinks(), [o1, o2, o3])

    def testAddLinksMultipleLinksInDefinition(self):
        a1 = self.c1.association(self.c2, "[sourceRole1] * -> [role1] *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c1, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")

        addLinks({o1: o4, o2: [o4], o5: [o1, o2, o3]})
        eq_(o1.getLinks(), [o4, o5])
        eq_(o2.getLinks(), [o4, o5])
        eq_(o3.getLinks(), [o5])
        eq_(o4.getLinks(), [o1, o2])
        eq_(o5.getLinks(), [o1, o2, o3])

    def testWrongTypesDeleteLinks(self):
        self.c1.association(self.c2, name = "l", multiplicity = "1")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        try:
            deleteLinks(o1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link definitions should be of the form {<link source 1>: <link target(s) 1>, ..., <link source n>: <link target(s) n>}")
        try:
            deleteLinks({o1: self.mcl})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            deleteLinks({o1: [o2, self.mcl]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            deleteLinks({o1: [o2, None]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'None' is neither an object nor a class")
        try:
            deleteLinks({self.mcl: o2})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link source 'MCL' is neither an object nor a class")
        try:
            deleteLinks({None: o2})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link should not contain an empty source")

    def testDeleteOneToOneLink(self):
        a = self.c1.association(self.c2, "l: 1 -> [c2] 0..1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c1, "o3")
        o4 = CObject(self.c2, "o4")

        links = addLinks({o1: o2, o3: o4})
        o1.deleteLinks(o2)
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [o4])
        eq_(o4.links, [o3])
        eq_(o1.linkObjects, [])
        eq_(o2.linkObjects, [])
        eq_(o3.linkObjects, [links[1]])
        eq_(o4.linkObjects, [links[1]]) 
        deleteLinks({o3: o4})
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [])
        eq_(o4.links, [])
        eq_(o1.linkObjects, [])
        eq_(o2.linkObjects, [])
        eq_(o3.linkObjects, [])
        eq_(o4.linkObjects, [])

    def testDeleteOneToOneLinkWrongMultiplicity(self):
        a = self.c1.association(self.c2, "l: 1 -> [c2] 1")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        addLinks({o1: o2})
        try:
            o1.deleteLinks(o2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o1' have wrong multiplicity '0': should be '1'")
        eq_(o1.links, [o2])
        eq_(o2.links, [o1])

    def testDeleteOneToNLinks(self):
        self.c1.association(self.c2, "l: 0..1 -> *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")

        addLinks({o1: [o3, o4], o2: [o5]})
        o4.deleteLinks([o1])
        eq_(o1.links, [o3])
        eq_(o2.links, [o5])
        eq_(o3.links, [o1])
        eq_(o4.links, [])
        eq_(o5.links, [o2])

        o4.addLinks([o2])
        eq_(o2.links, [o5, o4])
        deleteLinks({o1: o3, o2: o2.links})
        eq_(o1.links, [])
        eq_(o2.links, [])
        eq_(o3.links, [])
        eq_(o4.links, [])
        eq_(o5.links, [])      

    def testDeleteOneToNLinksWrongMultiplicity(self):
        a = self.c1.association(self.c2, "l: 1 -> *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")

        addLinks({o1: [o3, o4], o2: [o5]})
        
        try:
            o4.deleteLinks([o1])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'o4' have wrong multiplicity '0': should be '1'")    


    def testDeleteNToNLinks(self):
        self.c1.association(self.c2, "l: * -> *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")
        o6 = CObject(self.c2, "o6")

        addLinks({o1: [o3, o4], o2: [o4, o5]})
        o4.deleteLinks([o1, o2])
        eq_(o1.links, [o3])
        eq_(o2.links, [o5])
        eq_(o3.links, [o1])
        eq_(o4.links, [])
        eq_(o5.links, [o2])

        addLinks({o4: [o1, o2], o6: [o2, o1]})
        deleteLinks({o1: o6, o2: [o4, o5]})
        eq_(o1.links, [o3, o4])
        eq_(o2.links, [o6])
        eq_(o3.links, [o1])
        eq_(o4.links, [o1])
        eq_(o5.links, [])
        eq_(o6.links, [o2])
        
    def testDeleteLinkNoMatchingLink(self):
        a = self.c1.association(self.c2, "l: 0..1 -> *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")
        o5 = CObject(self.c2, "o5")

        addLinks({o1: [o3, o4], o2: [o5]}, association = a)

        try:
            deleteLinks({o1:o5})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'o1 -> o5' in delete links")  

        b = self.c1.association(self.c2, "l: 0..1 -> *")
        try:
            deleteLinks({o1:o5})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'o1 -> o5' in delete links")  

        try:
            o4.deleteLinks([o1], association = b)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'o4 -> o1' in delete links for given association")  

    def testDeleteLinkSelectByAssociation(self):
        a = self.c1.association(self.c2, "a: * -> *")
        b = self.c1.association(self.c2, "b: * -> *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")

        addLinks({o1: [o3], o2: [o3, o4]}, association = b)
        deleteLinks({o2: o3})
        eq_(o1.links, [o3])
        eq_(o2.links, [o4])
        eq_(o3.links, [o1])
        eq_(o4.links, [o2])
        addLinks({o1: [o3], o2: [o3, o4]}, association = a)
        
        try:
            deleteLinks({o1: o3})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link definition in delete links ambiguous for link 'o1->o3': found multiple matches")

        deleteLinks({o1: o3, o2: o4}, association = b)     
        eq_(o1.links, [o3])
        eq_(o2.links, [o3, o4])
        eq_(o3.links, [o1, o2])
        eq_(o4.links, [o2])
        for o in [o1, o2, o3, o4]:
            for lo in o.linkObjects:
                eq_(lo.association, a)
        
        o1.addLinks(o3, association = b)
        try:
            o1.deleteLinks(o3)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link definition in delete links ambiguous for link 'o1->o3': found multiple matches")
        
        eq_(o1.links, [o3, o3])
        eq_(o2.links, [o3, o4])
        eq_(o3.links, [o1, o2, o1])
        eq_(o4.links, [o2])
        
        o1.deleteLinks(o3, association = a)
        eq_(o1.links, [o3])
        eq_(o2.links, [o3, o4])
        eq_(o3.links, [o2, o1])
        eq_(o4.links, [o2])


    def testDeleteLinkSelectByRoleName(self):
        a = self.c1.association(self.c2, "a: [sourceA] * -> [targetA] *")
        b = self.c1.association(self.c2, "b: [sourceB] * -> [targetB] *")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c1, "o2")
        o3 = CObject(self.c2, "o3")
        o4 = CObject(self.c2, "o4")

        addLinks({o1: [o3], o2: [o3, o4]}, roleName = "targetB")
        deleteLinks({o2: o3})
        eq_(o1.links, [o3])
        eq_(o2.links, [o4])
        eq_(o3.links, [o1])
        eq_(o4.links, [o2])
        addLinks({o1: [o3], o2: [o3, o4]}, roleName = "targetA")
        
        deleteLinks({o1: o3, o2: o4}, roleName = "targetB")     
        eq_(o1.links, [o3])
        eq_(o2.links, [o3, o4])
        eq_(o3.links, [o1, o2])
        eq_(o4.links, [o2])
        for o in [o1, o2, o3, o4]:
            for lo in o.linkObjects:
                eq_(lo.association, a)

        addLinks({o1: [o3], o2: [o3, o4]}, roleName = "targetB")
        o3.deleteLinks([o1, o2], roleName = "sourceB")   
        deleteLinks({o4: o2}, roleName = "sourceB") 

        eq_(o1.links, [o3])
        eq_(o2.links, [o3, o4])
        eq_(o3.links, [o1, o2])
        eq_(o4.links, [o2])
        for o in [o1, o2, o3, o4]:
            for lo in o.linkObjects:
                eq_(lo.association, a)

    def testDeleteLinksWrongRoleName(self):
        a = self.c1.association(self.c2, "a: [sourceA] * -> [targetA] *")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o1.addLinks(o2)
        try:
            o1.deleteLinks(o2, roleName = "target")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'o1 -> o2' in delete links for given role name 'target'")
        
    def testDeleteLinksWrongAssociation(self):
        a = self.c1.association(self.c2, "a: [sourceA] * -> [targetA] *")
        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o1.addLinks(o2)
        try:
            o1.deleteLinks(o2, association = o1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'o1' is not a association")
        b = self.c1.association(self.c2, "b: [sourceB] * -> [targetB] *")
        try:
            o1.deleteLinks(o2, association = b)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'o1 -> o2' in delete links for given association")
        try:
            o1.deleteLinks(o2, association = b, roleName = "x")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'o1 -> o2' in delete links for given role name 'x' and for given association")

    def testLinkLabelDefault(self):
        a1 = self.c1.association(self.c2, name = "a1", multiplicity = "*")
        a2 = self.c1.association(self.c2, multiplicity = "*")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        l1 = setLinks({o1:o2}, association = a1) 
        l2 = setLinks({o1:[o2, o3]}, association = a2) 

        eq_(l1[0].label, "a1")
        eq_(l2[0].label, None)
        eq_(l2[1].label, None)

    def testLinkLabelGetSet(self):
        a1 = self.c1.association(self.c2, name = "a1", multiplicity = "*")
        a2 = self.c1.association(self.c2, multiplicity = "*")

        o1 = CObject(self.c1, "o1")
        o2 = CObject(self.c2, "o2")
        o3 = CObject(self.c2, "o3")

        l1 = setLinks({o1:o2}, association = a1, label = "l1") 
        l2 = addLinks({o1:[o2, o3]}, association = a2, label = "l2") 

        eq_(l1[0].label, "l1")
        eq_(l2[0].label, "l2")
        eq_(l2[1].label, "l2")

        l2[1].label = "l3"
        eq_(l2[0].label, "l2")
        eq_(l2[1].label, "l3")

        l3 = o1.addLinks(o3, association = a1, label = "x1")
        eq_(l3[0].label, "x1")         

if __name__ == "__main__":
    nose.main()