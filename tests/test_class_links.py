import sys
sys.path.append("..")

import re

import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CClass, CObject, CAttribute, CException, CEnum, setLinks, addLinks, deleteLinks

class TestClassLinks():
    def setUp(self):
        self.m1 = CMetaclass("M1")
        self.m2 = CMetaclass("M2")
        self.mcl = CMetaclass("MCL")
        
    def testLinkMethodsWrongKeywordArgs(self):
        c1 = CClass(self.m1, "C1")
        try:
            addLinks({c1:c1}, associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            c1.addLinks(c1, associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            setLinks({c1: c1}, associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            c1.deleteLinks(c1, associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            deleteLinks({c1: c1}, associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            c1.getLinks(associationX = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")
        try:
            deleteLinks({c1:c1}, stereotypeInstances = None)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown keywords argument")

    def testSetOneToOneLink(self):
        self.m1.association(self.m2, name = "l", multiplicity = "1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")

        eq_(c1.links, [])

        setLinks({c1: c2})
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])

        setLinks({c1: c3})
        eq_(c1.links, [c3])
        eq_(c2.links, [])
        eq_(c3.links, [c1])

    def testAddOneToOneLink(self):
        self.m1.association(self.m2, "l: 1 -> [target] 0..1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")

        eq_(c1.links, [])

        addLinks({c1: c3})
        eq_(c1.links, [c3])
        eq_(c3.links, [c1])

        setLinks({c1: []}, roleName = "target")
        eq_(c1.links, [])

        c1.addLinks(c2)
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])

        try:
            addLinks({c1: c3})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c1' have wrong multiplicity '2': should be '0..1'")
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])
        eq_(c3.links, [])
          
    def testWrongTypesAddLinks(self):
        self.m1.association(self.m2, name = "l", multiplicity = "1")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            addLinks({c1: self.mcl})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            c1.addLinks([c2, self.mcl])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")

    def testWrongTypesSetLinks(self):
        self.m1.association(self.m2, name = "l", multiplicity = "1")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            setLinks({c1: self.mcl})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            setLinks({c1: [c2, self.mcl]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            setLinks({c1: [c2, None]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'None' is neither an object nor a class")
        try:
            setLinks({self.mcl: c2})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link source 'MCL' is neither an object nor a class")
        try:
            setLinks({None: c2})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link should not contain an empty source")
            
    def testWrongFormatSetLinks(self):
        self.m1.association(self.m2, name = "l", multiplicity = "1")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            setLinks([c1, c2])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link definitions should be of the form {<link source 1>: <link target(s) 1>, ..., <link source n>: <link target(s) n>}")

    def testRemoveOneToOneLink(self):
        a = self.m1.association(self.m2, "l: 1 -> [c2] 0..1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m1, "c3")
        c4 = CClass(self.m2, "c4")

        links = setLinks({c1: c2, c3: c4})
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])
        eq_(c3.links, [c4])
        eq_(c4.links, [c3])
        eq_(c1.linkObjects, [links[0]])
        eq_(c2.linkObjects, [links[0]])
        eq_(c3.linkObjects, [links[1]])
        eq_(c4.linkObjects, [links[1]])

        try:
            links = setLinks({c1: None})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "matching association not found for source 'c1' and targets '[]'")

        setLinks({c1: None}, association = a)
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [c4])
        eq_(c4.links, [c3])
        eq_(c1.linkObjects, [])
        eq_(c2.linkObjects, [])
        eq_(c3.linkObjects, [links[1]])
        eq_(c4.linkObjects, [links[1]]) 

    def testSetLinksOneToNLink(self):
        self.m1.association(self.m2, name = "l")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")

        setLinks({c1: [c2, c3]})
        eq_(c1.links, [c2, c3])
        eq_(c2.links, [c1])
        eq_(c3.links, [c1])
        setLinks({c1: c2})
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])
        eq_(c3.links, [])
        setLinks({c3: c1, c2: c1})
        eq_(c1.links, [c3, c2])
        eq_(c2.links, [c1])
        eq_(c3.links, [c1])

    def testAddLinksOneToNLink(self):
        self.m1.association(self.m2, name = "l")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")
        c6 = CClass(self.m2, "c6")

        addLinks({c1: [c2, c3]})
        eq_(c1.links, [c2, c3])
        eq_(c2.links, [c1])
        eq_(c3.links, [c1])
        addLinks({c1: c4})
        eq_(c1.links, [c2, c3, c4])
        eq_(c2.links, [c1])
        eq_(c3.links, [c1])
        eq_(c4.links, [c1])
        c1.addLinks([c5, c6])
        eq_(c1.links, [c2, c3, c4, c5, c6])      
        eq_(c2.links, [c1])
        eq_(c3.links, [c1])
        eq_(c4.links, [c1])
        eq_(c5.links, [c1])
        eq_(c6.links, [c1])

    def testRemoveOneToNLink(self):
        a = self.m1.association(self.m2, name = "l", multiplicity = "*")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        setLinks({c1: [c2, c3]})
        setLinks({c1: c2})
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])
        eq_(c3.links, [])
        try:
            setLinks({c1: []})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "matching association not found for source 'c1' and targets '[]'")
        setLinks({c1: []}, association = a)
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [])

    def testNToNLink(self):
        a = self.m1.association(self.m2, name = "l", sourceMultiplicity = "*")
        c1a = CClass(self.m1, "c1a")
        c1b = CClass(self.m1, "c1b")
        c1c = CClass(self.m1, "c1c")
        c2a = CClass(self.m2, "c2a")
        c2b = CClass(self.m2, "c2b")

        setLinks({c1a: [c2a, c2b], c1b: [c2a], c1c: [c2b]})
        
        eq_(c1a.links, [c2a, c2b])
        eq_(c1b.links, [c2a])
        eq_(c1c.links, [c2b])
        eq_(c2a.links, [c1a, c1b])
        eq_(c2b.links, [c1a, c1c])

        setLinks({c2a: [c1a, c1b]})
        try:
            setLinks({c2b: []})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "matching association not found for source 'c2b' and targets '[]'")
        setLinks({c2b: []}, association = a)


        eq_(c1a.links, [c2a])
        eq_(c1b.links, [c2a])
        eq_(c1c.links, [])
        eq_(c2a.links, [c1a, c1b])
        eq_(c2b.links, [])

    def testRemoveNToNLink(self):
        self.m1.association(self.m2, name = "l", sourceMultiplicity = "*", multiplicity = "*")
        c1 = CClass(self.m1, "c2")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m1, "c4")
        setLinks({c1: [c2, c3], c4: c2})
        setLinks({c1: c2, c4: [c3, c2]})
        eq_(c1.links, [c2])
        eq_(c2.links, [c1, c4])
        eq_(c3.links, [c4])
        eq_(c4.links, [c3, c2])

    def testNToNSetSelfLink(self):
        self.m1.association(self.m1, name = "a", sourceMultiplicity = "*", multiplicity = "*", sourceRoleName = "super", roleName = "sub")

        top = CClass(self.m1, "Top")
        mid1 = CClass(self.m1, "Mid1")
        mid2 = CClass(self.m1, "Mid2")
        mid3 = CClass(self.m1, "Mid3")
        bottom1 = CClass(self.m1, "Bottom1")
        bottom2 = CClass(self.m1, "Bottom2")

        setLinks({top: [mid1, mid2, mid3]}, roleName = "sub")
        mid1.addLinks([bottom1, bottom2], roleName = "sub")

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
        self.m1.association(self.m1, name = "a", sourceMultiplicity = "*", multiplicity = "*", sourceRoleName = "super", roleName = "sub")

        top = CClass(self.m1, "Top")
        mid1 = CClass(self.m1, "Mid1")
        mid2 = CClass(self.m1, "Mid2")
        mid3 = CClass(self.m1, "Mid3")
        bottom1 = CClass(self.m1, "Bottom1")
        bottom2 = CClass(self.m1, "Bottom2")

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
        self.m1.association(self.m2, name = "l", multiplicity = "*")
        cl = CClass(self.mcl, "CLX")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CObject(cl, "c3")
        try:
            setLinks({c1: [c2, c3]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'c3' is an object, but source is an class")
        try:
            setLinks({c1: c3})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'c3' is an object, but source is an class")

    def testDuplicateAssignment(self):
        a = self.m1.association(self.m2, "l: *->*")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            setLinks({c1: [c2, c2]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "trying to link the same link twice 'c1 -> c2'' twice for the same association")
        eq_(c1.getLinks(), [])
        eq_(c2.getLinks(), [])

        b = self.m1.association(self.m2, "l: *->*")
        c1.addLinks(c2, association = a)
        c1.addLinks(c2, association = b)  
        eq_(c1.getLinks(), [c2, c2])
        eq_(c2.getLinks(), [c1, c1])

    def testNonExistingRoleName(self):
        self.m1.association(self.m1, roleName = "next", sourceRoleName = "prior", 
            sourceMultiplicity = "1", multiplicity = "1")
        c1 = CClass(self.m1, "c1")
        try:
            setLinks({c1 : c1}, roleName = "target")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "matching association not found for source 'c1' and targets '['c1']'")

    def testLinkAssociationAmbiguous(self):
        self.m1.association(self.m2, name = "a1", roleName = "c2", multiplicity = "*")
        self.m1.association(self.m2, name = "a2", roleName = "c2", multiplicity = "*")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            setLinks({c1:c2})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link specification ambiguous, multiple matching associations found for source 'c1' and targets '['c2']'")
        try:
            setLinks({c1:c2}, roleName = "c2")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link specification ambiguous, multiple matching associations found for source 'c1' and targets '['c2']'")

    def testLinkAndGetLinksByAssociation(self):
        a1 = self.m1.association(self.m2, name = "a1", multiplicity = "*")
        a2 = self.m1.association(self.m2, name = "a2", multiplicity = "*")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")

        setLinks({c1:c2}, association = a1) 
        setLinks({c1:[c2, c3]}, association = a2) 

        eq_(c1.getLinks(), [c2, c2, c3])
        eq_(c1.links, [c2, c2, c3])

        eq_(c1.getLinks(association = a1), [c2])
        eq_(c1.getLinks(association = a2), [c2, c3])

    def testLinkWithInheritanceInClassifierTargets(self):
        subCl = CMetaclass(superclasses = self.m2)
        a1 = self.m1.association(subCl, name = "a1", multiplicity = "*")
        a2 = self.m1.association(self.m2, name = "a2", multiplicity = "*")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c_sub_1 = CClass(subCl, "c_sub_1")
        c_sub_2 = CClass(subCl, "c_sub_2")
        c_super_1 = CClass(self.m2, "c_super_1")
        c_super_2 = CClass(self.m2, "c_super_2")
        try:
            # ambiguous, list works for both associations 
            setLinks({c1: [c_sub_1, c_sub_2]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link specification ambiguous, multiple matching associations found for source 'c1' and targets '['c_sub_1', 'c_sub_2']'")
        setLinks({c1: [c_sub_1, c_sub_2]}, association = a1)
        setLinks({c1: [c_sub_1]}, association = a2)
        setLinks({c2: [c_super_1, c_super_2]})

        eq_(c1.links, [c_sub_1, c_sub_2, c_sub_1])
        eq_(c1.getLinks(), [c_sub_1, c_sub_2, c_sub_1])
        eq_(c2.getLinks(), [c_super_1, c_super_2])
        eq_(c1.getLinks(association = a1), [c_sub_1, c_sub_2])
        eq_(c1.getLinks(association = a2), [c_sub_1])
        eq_(c2.getLinks(association = a1), [])
        eq_(c2.getLinks(association = a2), [c_super_1, c_super_2])

        # this mixed list is applicable only for a2
        setLinks({c2: [c_sub_1, c_super_1]})
        eq_(c2.getLinks(association = a1), [])
        eq_(c2.getLinks(association = a2), [c_sub_1, c_super_1])

    def testLinkWithInheritanceInClassifierTargets_UsingRoleNames(self):
        subCl = CMetaclass(superclasses = self.m2)
        a1 = self.m1.association(subCl, "a1: * -> [subCl] *")
        a2 = self.m1.association(self.m2, "a2: * -> [c2] *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c_sub_1 = CClass(subCl, "c_sub_1")
        c_sub_2 = CClass(subCl, "c_sub_2")
        c_super_1 = CClass(self.m2, "c_super_1")
        c_super_2 = CClass(self.m2, "c_super_2")
        setLinks({c1: [c_sub_1, c_sub_2]}, roleName = "subCl")
        setLinks({c1: [c_sub_1]}, roleName = "c2")
        setLinks({c2: [c_super_1, c_super_2]})

        eq_(c1.links, [c_sub_1, c_sub_2, c_sub_1])
        eq_(c1.getLinks(), [c_sub_1, c_sub_2, c_sub_1])
        eq_(c2.getLinks(), [c_super_1, c_super_2])
        eq_(c1.getLinks(association = a1), [c_sub_1, c_sub_2])
        eq_(c1.getLinks(association = a2), [c_sub_1])
        eq_(c2.getLinks(association = a1), [])
        eq_(c2.getLinks(association = a2), [c_super_1, c_super_2])
        eq_(c1.getLinks(roleName = "subCl"), [c_sub_1, c_sub_2])
        eq_(c1.getLinks(roleName = "c2"), [c_sub_1])
        eq_(c2.getLinks(roleName = "subCl"), [])
        eq_(c2.getLinks(roleName = "c2"), [c_super_1, c_super_2])

    def testLinkDeleteAssociation(self):
        a = self.m1.association(self.m2, name = "l", sourceMultiplicity = "*", multiplicity = "*")
        c1 = CClass(self.m1, "c2")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m1, "c4")
        setLinks({c1: [c2, c3]})
        setLinks({c4: [c2]})  
        setLinks({c1: [c2]})
        setLinks({c4: [c3, c2]})
        a.delete()
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [])
        eq_(c4.links, [])
        try:
            setLinks({c1: [c2, c3]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "matching association not found for source 'c2' and targets '['c2', 'c3']'")

    def testOneToOneLinkMultiplicity(self):
        a = self.m1.association(self.m2, name = "l", multiplicity = "1", sourceMultiplicity = "1..1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m1, "c4")

        try:
            setLinks({c1: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c1' have wrong multiplicity '0': should be '1'")
        try:
            setLinks({c1: [c2, c3]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c1' have wrong multiplicity '2': should be '1'")

        try:
            setLinks({c2: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c2' have wrong multiplicity '0': should be '1..1'")
        try:
            setLinks({c2: [c1, c4]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c2' have wrong multiplicity '2': should be '1..1'")

    def testOneToNLinkMultiplicity(self):
        a = self.m1.association(self.m2, name = "l", sourceMultiplicity = "1", multiplicity = "1..*")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m1, "c4")

        try:
            setLinks({c1: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c1' have wrong multiplicity '0': should be '1..*'")
        
        setLinks({c1: [c2, c3]})
        eq_(c1.getLinks(association = a), [c2, c3])

        try:
            setLinks({c2: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c2' have wrong multiplicity '0': should be '1'")
        try:
            setLinks({c2: [c1, c4]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c2' have wrong multiplicity '2': should be '1'")


    def testSpecificNToNLinkMultiplicity(self):
        a = self.m1.association(self.m2, name = "l", sourceMultiplicity = "1..2", multiplicity = "2")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m1, "c4")
        c5 = CClass(self.m1, "c5")
        c6 = CClass(self.m2, "c6")

        try:
            setLinks({c1: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c1' have wrong multiplicity '0': should be '2'")
        try:
            setLinks({c1: [c2]}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c1' have wrong multiplicity '1': should be '2'")
        try:
            setLinks({c1: [c2, c3, c6]}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c1' have wrong multiplicity '3': should be '2'")

        setLinks({c1: [c2, c3]})
        eq_(c1.getLinks(association = a), [c2, c3])
        setLinks({c2: [c1, c4], c1: c3, c4: c3})
        eq_(c2.getLinks(association = a), [c1, c4])

        try:
            setLinks({c2: []}, association = a)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c2' have wrong multiplicity '0': should be '1..2'")
        try:
            setLinks({c2: [c1, c4, c5]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c2' have wrong multiplicity '3': should be '1..2'")

    def testGetLinkObjects(self):
        c1Sub = CMetaclass("C1Sub", superclasses = self.m1)
        c2Sub = CMetaclass("C2Sub", superclasses = self.m2)
        a1 = self.m1.association(self.m2, roleName = "c2", sourceRoleName = "c1", 
            sourceMultiplicity = "*", multiplicity = "*")
        a2 = self.m1.association(self.m1, roleName = "next", sourceRoleName = "prior", 
            sourceMultiplicity = "1", multiplicity = "0..1")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c1Sub = CClass(c1Sub, "c1Sub")
        c2Sub = CClass(c2Sub, "c2Sub")

        linkObjects1 = setLinks({c1: c2})
        eq_(linkObjects1, c1.linkObjects)
        link1 = c1.linkObjects[0]
        link2 = [o for o in c1.linkObjects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, c1)
        eq_(link1.target, c2)

        linkObjects2 = setLinks({c1: c2Sub})
        eq_(linkObjects2, c1.linkObjects)
        eq_(len(c1.linkObjects), 1)
        link1 = c1.linkObjects[0]
        link2 = [o for o in c1.linkObjects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, c1)
        eq_(link1.target, c2Sub)

        linkObjects3 = setLinks({c1: c2})
        eq_(linkObjects3, c1.linkObjects)
        eq_(len(c1.linkObjects), 1)
        link1 = c1.linkObjects[0]
        link2 = [o for o in c1.linkObjects if o.association == a1][0]
        eq_(link1, link2)
        eq_(link1.association, a1)
        eq_(link1.source, c1)
        eq_(link1.target, c2)

        linkObjects4 = setLinks({c1: c1}, roleName = "next")
        eq_(linkObjects3 + linkObjects4, c1.linkObjects)
        eq_(len(c1.linkObjects), 2)
        link1 = c1.linkObjects[1]
        link2 = [o for o in c1.linkObjects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, c1)
        eq_(link1.target, c1)

        linkObjects5 = setLinks({c1: c1Sub}, roleName = "next")
        eq_(linkObjects3 + linkObjects5, c1.linkObjects)
        eq_(len(c1.linkObjects), 2)
        link1 = c1.linkObjects[1]
        link2 = [o for o in c1.linkObjects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, c1)
        eq_(link1.target, c1Sub)

        setLinks({c1: c1}, roleName = "next")
        eq_(len(c1.linkObjects), 2)
        link1 = c1.linkObjects[1]
        link2 = [o for o in c1.linkObjects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, c1)
        eq_(link1.target, c1)

        setLinks({c1: []}, association = a1)
        setLinks({c1: []}, association = a2)
        eq_(len(c1.linkObjects), 0)

        setLinks({c1Sub: c1}, roleName = "next")
        eq_(len(c1Sub.linkObjects), 1)
        link1 = c1Sub.linkObjects[0]
        link2 = [o for o in c1Sub.linkObjects if o.association == a2][0]
        eq_(link1, link2)
        eq_(link1.association, a2)
        eq_(link1.source, c1Sub)
        eq_(link1.target, c1)    

    def testGetLinkObjectsSelfLink(self):
        a1 = self.m1.association(self.m1, roleName = "to", sourceRoleName = "from", 
            sourceMultiplicity = "*", multiplicity = "*")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m1, "c3")
        c4 = CClass(self.m1, "c4")

        setLinks({c1: [c2, c3, c1]})
        addLinks({c4: [c1, c3]})
        link1 = c1.linkObjects[0]
        link2 = [o for o in c1.linkObjects if o.association == a1][0]
        link3 = [o for o in c1.linkObjects if o.roleName == "to"][0]
        link4 = [o for o in c1.linkObjects if o.sourceRoleName == "from"][0]
        eq_(link1, link2)
        eq_(link1, link3)
        eq_(link1, link4)
        eq_(link1.association, a1)
        eq_(link1.source, c1)
        eq_(link1.target, c2)

        eq_(len(c1.linkObjects), 4)
        eq_(len(c2.linkObjects), 1)
        eq_(len(c3.linkObjects), 2)
        eq_(len(c4.linkObjects), 2)

    def testAddLinks(self):
        a1 = self.m1.association(self.m2, "1 -> [role1] *")
        a2 = self.m1.association(self.m2, "* -> [role2] *")
        a3 = self.m1.association(self.m2, "1 -> [role3] 1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")

        addLinks({c1: c2}, roleName = "role1")
        eq_(c1.getLinks(roleName = "role1"), [c2])
        addLinks({c1: [c3, c4]}, roleName = "role1")
        c1.getLinks(roleName = "role1")
        eq_(c1.getLinks(roleName = "role1"), [c2, c3, c4])

        c1.addLinks(c2, roleName = "role2")
        eq_(c1.getLinks(roleName = "role2"), [c2])
        c1.addLinks([c3, c4], roleName = "role2")
        c1.getLinks(roleName = "role2")
        eq_(c1.getLinks(roleName = "role2"), [c2, c3, c4])

        c1.addLinks(c2, roleName = "role3")
        eq_(c1.getLinks(roleName = "role3"), [c2])
        try:
            addLinks({c1: [c3, c4]}, roleName = "role3")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c1' have wrong multiplicity '3': should be '1'")

        try:
            addLinks({c1: [c3]}, roleName = "role3")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c1' have wrong multiplicity '2': should be '1'")
        eq_(c1.getLinks(roleName = "role3"), [c2])


    def testLinkSourceMultiplicity(self):
        a1 = self.m1.association(self.m2, "[sourceRole1] 1 -> [role1] *")
        a2 = self.m1.association(self.m2, "[sourceRole2] 1 -> [role2] 1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")

        setLinks({c1: c3}, roleName = "role1")
        setLinks({c2: c3}, roleName = "role1")

        eq_(c3.getLinks(roleName = "sourceRole1"), [c2])

    def testAddLinksSourceMultiplicity(self):
        a1 = self.m1.association(self.m2, "[sourceRole1] 1 -> [role1] *")
        a2 = self.m1.association(self.m2, "[sourceRole2] 1 -> [role2] 1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")
        c6 = CClass(self.m2, "c6")

        addLinks({c2: c3}, roleName = "role1")
        addLinks({c2: c4}, roleName = "role1")

        eq_(c3.getLinks(roleName = "sourceRole1"), [c2])

        addLinks({c2: c5}, roleName = "role1")
        eq_(c2.getLinks(roleName = "role1"), [c3, c4, c5])

        try:
            addLinks({c1: [c4]}, roleName = "role1")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c4' have wrong multiplicity '2': should be '1'")

        addLinks({c1: c6}, roleName = "role2")
        eq_(c1.getLinks(roleName = "role2"), [c6])
        try:
            addLinks({c1: [c3, c4]}, roleName = "role2")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c1' have wrong multiplicity '3': should be '1'")       
        eq_(c1.getLinks(roleName = "role2"), [c6])

    def testSetLinksMultipleLinksInDefinition(self):
        a1 = self.m1.association(self.m2, "[sourceRole1] * -> [role1] *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m1, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")

        setLinks({c1: c4, c2: [c4], c5: [c1, c2, c3]})
        eq_(c1.getLinks(), [c4, c5])
        eq_(c2.getLinks(), [c4, c5])
        eq_(c3.getLinks(), [c5])
        eq_(c4.getLinks(), [c1, c2])
        eq_(c5.getLinks(), [c1, c2, c3])

    def testAddLinksMultipleLinksInDefinition(self):
        a1 = self.m1.association(self.m2, "[sourceRole1] * -> [role1] *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m1, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")

        addLinks({c1: c4, c2: [c4], c5: [c1, c2, c3]})
        eq_(c1.getLinks(), [c4, c5])
        eq_(c2.getLinks(), [c4, c5])
        eq_(c3.getLinks(), [c5])
        eq_(c4.getLinks(), [c1, c2])
        eq_(c5.getLinks(), [c1, c2, c3])


    def testWrongTypesDeleteLinks(self):
        self.m1.association(self.m2, name = "l", multiplicity = "1")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        try:
            deleteLinks(c1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link definitions should be of the form {<link source 1>: <link target(s) 1>, ..., <link source n>: <link target(s) n>}")
        try:
            deleteLinks({c1: self.mcl})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            deleteLinks({c1: [c2, self.mcl]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'MCL' is neither an object nor a class")
        try:
            deleteLinks({c1: [c2, None]})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link target 'None' is neither an object nor a class")
        try:
            deleteLinks({self.mcl: c2})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link source 'MCL' is neither an object nor a class")
        try:
            deleteLinks({None: c2})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link should not contain an empty source")

    def testDeleteOneToOneLink(self):
        a = self.m1.association(self.m2, "l: 1 -> [c2] 0..1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c3 = CClass(self.m1, "c3")
        c4 = CClass(self.m2, "c4")

        links = addLinks({c1: c2, c3: c4})
        c1.deleteLinks(c2)
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [c4])
        eq_(c4.links, [c3])
        eq_(c1.linkObjects, [])
        eq_(c2.linkObjects, [])
        eq_(c3.linkObjects, [links[1]])
        eq_(c4.linkObjects, [links[1]]) 
        deleteLinks({c3: c4})
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [])
        eq_(c4.links, [])
        eq_(c1.linkObjects, [])
        eq_(c2.linkObjects, [])
        eq_(c3.linkObjects, [])
        eq_(c4.linkObjects, [])

    def testDeleteOneToOneLinkWrongMultiplicity(self):
        a = self.m1.association(self.m2, "l: 1 -> [c2] 1")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        addLinks({c1: c2})
        try:
            c1.deleteLinks(c2)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c1' have wrong multiplicity '0': should be '1'")
        eq_(c1.links, [c2])
        eq_(c2.links, [c1])

    def testDeleteOneToNLinks(self):
        self.m1.association(self.m2, "l: 0..1 -> *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")

        addLinks({c1: [c3, c4], c2: [c5]})
        c4.deleteLinks([c1])
        eq_(c1.links, [c3])
        eq_(c2.links, [c5])
        eq_(c3.links, [c1])
        eq_(c4.links, [])
        eq_(c5.links, [c2])

        c4.addLinks([c2])
        eq_(c2.links, [c5, c4])
        deleteLinks({c1: c3, c2: c2.links})
        eq_(c1.links, [])
        eq_(c2.links, [])
        eq_(c3.links, [])
        eq_(c4.links, [])
        eq_(c5.links, [])      

    def testDeleteOneToNLinksWrongMultiplicity(self):
        a = self.m1.association(self.m2, "l: 1 -> *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")

        addLinks({c1: [c3, c4], c2: [c5]})
        
        try:
            c4.deleteLinks([c1])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "links of object 'c4' have wrong multiplicity '0': should be '1'")    


    def testDeleteNToNLinks(self):
        self.m1.association(self.m2, "l: * -> *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")
        c6 = CClass(self.m2, "c6")

        addLinks({c1: [c3, c4], c2: [c4, c5]})
        c4.deleteLinks([c1, c2])
        eq_(c1.links, [c3])
        eq_(c2.links, [c5])
        eq_(c3.links, [c1])
        eq_(c4.links, [])
        eq_(c5.links, [c2])

        addLinks({c4: [c1, c2], c6: [c2, c1]})
        deleteLinks({c1: c6, c2: [c4, c5]})
        eq_(c1.links, [c3, c4])
        eq_(c2.links, [c6])
        eq_(c3.links, [c1])
        eq_(c4.links, [c1])
        eq_(c5.links, [])
        eq_(c6.links, [c2])
        
    def testDeleteLinkNoMatchingLink(self):
        a = self.m1.association(self.m2, "l: 0..1 -> *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")
        c5 = CClass(self.m2, "c5")

        addLinks({c1: [c3, c4], c2: [c5]}, association = a)

        try:
            deleteLinks({c1:c5})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'c1 -> c5' in delete links")  

        b = self.m1.association(self.m2, "l: 0..1 -> *")
        try:
            deleteLinks({c1:c5})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'c1 -> c5' in delete links")  

        try:
            c4.deleteLinks([c1], association = b)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'c4 -> c1' in delete links for given association")  

    def testDeleteLinkSelectByAssociation(self):
        a = self.m1.association(self.m2, "a: * -> *")
        b = self.m1.association(self.m2, "b: * -> *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")

        addLinks({c1: [c3], c2: [c3, c4]}, association = b)
        deleteLinks({c2: c3})
        eq_(c1.links, [c3])
        eq_(c2.links, [c4])
        eq_(c3.links, [c1])
        eq_(c4.links, [c2])
        addLinks({c1: [c3], c2: [c3, c4]}, association = a)
        
        try:
            deleteLinks({c1: c3})
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link definition in delete links ambiguous for link 'c1->c3': found multiple matches")

        deleteLinks({c1: c3, c2: c4}, association = b)     
        eq_(c1.links, [c3])
        eq_(c2.links, [c3, c4])
        eq_(c3.links, [c1, c2])
        eq_(c4.links, [c2])
        for o in [c1, c2, c3, c4]:
            for lo in o.linkObjects:
                eq_(lo.association, a)
        
        c1.addLinks(c3, association = b)
        try:
            c1.deleteLinks(c3)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "link definition in delete links ambiguous for link 'c1->c3': found multiple matches")
        
        eq_(c1.links, [c3, c3])
        eq_(c2.links, [c3, c4])
        eq_(c3.links, [c1, c2, c1])
        eq_(c4.links, [c2])
        
        c1.deleteLinks(c3, association = a)
        eq_(c1.links, [c3])
        eq_(c2.links, [c3, c4])
        eq_(c3.links, [c2, c1])
        eq_(c4.links, [c2])


    def testDeleteLinkSelectByRoleName(self):
        a = self.m1.association(self.m2, "a: [sourceA] * -> [targetA] *")
        b = self.m1.association(self.m2, "b: [sourceB] * -> [targetB] *")

        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m1, "c2")
        c3 = CClass(self.m2, "c3")
        c4 = CClass(self.m2, "c4")

        addLinks({c1: [c3], c2: [c3, c4]}, roleName = "targetB")
        deleteLinks({c2: c3})
        eq_(c1.links, [c3])
        eq_(c2.links, [c4])
        eq_(c3.links, [c1])
        eq_(c4.links, [c2])
        addLinks({c1: [c3], c2: [c3, c4]}, roleName = "targetA")
        
        deleteLinks({c1: c3, c2: c4}, roleName = "targetB")     
        eq_(c1.links, [c3])
        eq_(c2.links, [c3, c4])
        eq_(c3.links, [c1, c2])
        eq_(c4.links, [c2])
        for o in [c1, c2, c3, c4]:
            for lo in o.linkObjects:
                eq_(lo.association, a)

        addLinks({c1: [c3], c2: [c3, c4]}, roleName = "targetB")
        c3.deleteLinks([c1, c2], roleName = "sourceB")   
        deleteLinks({c4: c2}, roleName = "sourceB") 

        eq_(c1.links, [c3])
        eq_(c2.links, [c3, c4])
        eq_(c3.links, [c1, c2])
        eq_(c4.links, [c2])
        for o in [c1, c2, c3, c4]:
            for lo in o.linkObjects:
                eq_(lo.association, a)

    def testDeleteLinksWrongRoleName(self):
        a = self.m1.association(self.m2, "a: [sourceA] * -> [targetA] *")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c1.addLinks(c2)
        try:
            c1.deleteLinks(c2, roleName = "target")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'c1 -> c2' in delete links for given role name 'target'")
        
    def testDeleteLinksWrongAssociation(self):
        a = self.m1.association(self.m2, "a: [sourceA] * -> [targetA] *")
        c1 = CClass(self.m1, "c1")
        c2 = CClass(self.m2, "c2")
        c1.addLinks(c2)
        try:
            c1.deleteLinks(c2, association = c1)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "'c1' is not a association")
        b = self.m1.association(self.m2, "b: [sourceB] * -> [targetB] *")
        try:
            c1.deleteLinks(c2, association = b)
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'c1 -> c2' in delete links for given association")
        try:
            c1.deleteLinks(c2, association = b, roleName = "x")
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "no link found for 'c1 -> c2' in delete links for given role name 'x' and for given association")


if __name__ == "__main__":
    nose.main()