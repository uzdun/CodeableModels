import sys
sys.path.append("..")

import re

import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CStereotype, CMetaclass, CBundle, CObject, CAttribute, CException, CEnum, CBundle, CAssociation

class TestStereotypesOnAssociations():
    def setUp(self):
        self.m1 = CMetaclass("M1")
        self.m2 = CMetaclass("M2")
        self.a = self.m1.association(self.m2, name = "A", multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2")

    def testCreationOfOneStereotype(self):
        s = CStereotype("S", extended = self.a)
        eq_(s.name, "S")
        eq_(self.a.stereotypes, [s])
        eq_(s.extended, [self.a])

    def testWrongsTypesInListOfExtendedElementTypes(self):
        try:
            s = CStereotype("S", extended = [self.a, self.m1])
            exceptionExpected_()
        except CException as e: 
            eq_("'M1' is not a association", e.value)
        try:
            s = CStereotype("S", extended = [self.a, CBundle("P")])
            exceptionExpected_()
        except CException as e: 
            eq_("'P' is not a association", e.value)
        try:
            s = CStereotype("S", extended = [CBundle("P"), self.a])
            exceptionExpected_()
        except CException as e: 
            eq_("unknown type of extend element: 'P'", e.value)

    def testCreationOf3Stereotypes(self):
        s1 = CStereotype("S1")
        s2 = CStereotype("S2")
        s3 = CStereotype("S3")
        self.a.stereotypes = [s1, s2, s3]
        eq_(s1.extended, [self.a])
        eq_(s2.extended, [self.a])
        eq_(s3.extended, [self.a])
        eq_(set(self.a.stereotypes), set([s1, s2, s3]))
    
    def testCreationOfUnnamedStereotype(self):
        s = CStereotype()
        eq_(s.name, None)
        eq_(self.a.stereotypes, [])
        eq_(s.extended, [])

    def testDeleteStereotype(self):
        s1 = CStereotype("S1")
        s1.delete()
        eq_(s1.name, None)
        eq_(self.a.stereotypes, [])
        s1 = CStereotype("S1", extended = self.a)
        s1.delete()
        eq_(s1.name, None)
        eq_(self.a.stereotypes, [])

        s1 = CStereotype("S1", extended = self.a)
        s2 = CStereotype("S2", extended = self.a)
        s3 = CStereotype("s1", superclasses = s2, attributes = {"i" : 1}, extended = self.a)

        s1.delete()
        eq_(set(self.a.stereotypes), set([s2, s3]))
        s3.delete()
        eq_(set(self.a.stereotypes), set([s2]))

        eq_(s3.superclasses, [])
        eq_(s2.subclasses, [])
        eq_(s3.attributes, [])
        eq_(s3.attributeNames, [])
        eq_(s3.extended, [])
        eq_(s3.name, None)
        eq_(s3.bundles, [])

    def testStereotypeExtensionAddRemove(self):
        s1 = CStereotype("S1")
        eq_(set(s1.extended), set())
        a1 = self.m1.association(self.m2, multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2", stereotypes = [s1])
        eq_(set(s1.extended), set([a1]))
        eq_(set(a1.stereotypes), set([s1]))
        a2 = self.m1.association(self.m2, multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2", stereotypes = s1)
        eq_(set(s1.extended), set([a1, a2]))
        eq_(set(a1.stereotypes), set([s1])) 
        eq_(set(a2.stereotypes), set([s1]))
        s1.extended = [a2]
        eq_(set(s1.extended), set([a2]))
        eq_(set(a1.stereotypes), set()) 
        eq_(set(a2.stereotypes), set([s1]))
        s2 = CStereotype("S2", extended = [a2])
        eq_(set(a2.stereotypes), set([s2, s1]))
        eq_(set(s1.extended), set([a2]))
        eq_(set(s2.extended), set([a2]))
        a2.stereotypes = []
        eq_(set(a2.stereotypes), set())
        eq_(set(s1.extended), set())
        eq_(set(s2.extended), set())

    def testStereotypeRemoveSterotypeOrAssociation(self):
        a1 = self.m1.association(self.m2, multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2")
        s1 = CStereotype("S1", extended = [a1])
        s2 = CStereotype("S2", extended = [a1])
        s3 = CStereotype("S3", extended = [a1])
        s4 = CStereotype("S4", extended = [a1])
        eq_(set(a1.stereotypes), set([s1, s2, s3, s4]))
        s2.delete()
        eq_(set(a1.stereotypes), set([s1, s3, s4]))
        eq_(set(s2.extended), set())
        eq_(set(s1.extended), set([a1]))  
        a1.delete()
        eq_(set(a1.stereotypes), set())
        eq_(set(s1.extended), set())

    def testStereotypesWrongType(self):
        a1 = self.m1.association(self.m2, name = "a1", multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2")
        try:
            a1.stereotypes = [a1]
            exceptionExpected_()
        except CException as e: 
            eq_("'a1' is not a stereotype", e.value)

    def testAssociationStereotypesNullInput(self):
        s = CStereotype() 
        a1 = self.m1.association(self.m2, name = "a1", multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2", stereotypes = None)
        eq_(a1.stereotypes, [])
        eq_(s.extended, [])

    def testAssociationStereotypesNonListInput(self):
        s = CStereotype() 
        a1 = self.m1.association(self.m2, name = "a1", multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2", stereotypes = s)
        eq_(a1.stereotypes, [s])
        eq_(s.extended, [a1])

    def testAssociationStereotypesNonListInputWrongType(self):
        try:
            a1 = self.m1.association(self.m2, name = "a1", multiplicity = "1", roleName = "m1",  
                sourceMultiplicity = "*", sourceRoleName = "m2")
            a1.stereotypes = a1
            exceptionExpected_()
        except CException as e: 
            eq_("a list or a stereotype is required as input", e.value)

    def testMetaclassStereotypesAppend(self):
        s1 = CStereotype()
        s2 = CStereotype()  
        a1 = self.m1.association(self.m2, name = "a1", multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2", stereotypes = s1)
        # should have no effect, as setter must be used
        a1.stereotypes.append(s2)
        eq_(a1.stereotypes, [s1])
        eq_(s1.extended, [a1])
        eq_(s2.extended, [])

    def testStereotypeExtendedNullInput(self):
        a1 = self.m1.association(self.m2, name = "a1", multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2")
        s = CStereotype(extended = None) 
        eq_(a1.stereotypes, [])
        eq_(s.extended, [])

    def testStereotypeExtendedNonListInput(self):
        a1 = self.m1.association(self.m2, name = "a1", multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2")
        s = CStereotype(extended = a1) 
        eq_(a1.stereotypes, [s])
        eq_(s.extended, [a1])

    def testStereotypeExtendedAppend(self):
        a1 = self.m1.association(self.m2, name = "a1", multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2")
        a2 = self.m1.association(self.m2, name = "a2", multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2")
        s = CStereotype(extended = [a1])
        # should have no effect, as setter must be used
        s.extended.append(a2)
        eq_(a1.stereotypes, [s])
        eq_(a2.stereotypes, [])
        eq_(s.extended, [a1])

    def testExtendedAssociationThatIsDeleted(self):
        a1 = self.m1.association(self.m2, name = "a1", multiplicity = "1", roleName = "m1",  
            sourceMultiplicity = "*", sourceRoleName = "m2")
        a1.delete()
        try:
            CStereotype(extended = [a1])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

if __name__ == "__main__":
    nose.main()



