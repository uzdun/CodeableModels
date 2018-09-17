import sys
sys.path.append("..")

import re

import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CClass, CObject, CAttribute, CException, CEnum, CBundle, CStereotype

class TestMetaclassAssociations():
    def setUp(self):
        self.metaclassBundle = CBundle("P")
        self.m1 = CMetaclass("M1", bundles = self.metaclassBundle)
        self.m2 = CMetaclass("M2", bundles = self.metaclassBundle)
        self.m3 = CMetaclass("M3", bundles = self.metaclassBundle)
        self.m4 = CMetaclass("M4", bundles = self.metaclassBundle)
        self.m5 = CMetaclass("M5", bundles = self.metaclassBundle)

    def getAllAssociationsInBundle(self):
        associations = []
        for c in self.metaclassBundle.getElements(type=CMetaclass):
            for a in c.allAssociations:
                if not a in associations:
                    associations.append(a)
        return associations

    def testAssociationCreation(self):
        a1 = self.m1.association(self.m2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.m1.association(self.m2, "[o]*->[s]1")
        a3 = self.m1.association(self.m3, "[a] 0..1 <*>- [n]*")
        a4 = self.m1.association(self.m3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.m4.association(self.m3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.m3.association(self.m2, '[a] 3 <>- [e]*')

        eq_(len(self.getAllAssociationsInBundle()), 6)

        eq_(self.m1.associations[0].roleName, "t")
        eq_(a5.roleName, "n")
        eq_(a2.roleName, "s")
        eq_(a1.multiplicity, "1")
        eq_(a1.sourceMultiplicity, "*")
        eq_(a4.sourceMultiplicity, "0..1")
        eq_(a6.sourceMultiplicity, "3")

        eq_(a1.composition, False)
        eq_(a1.aggregation, False)
        eq_(a3.composition, True)
        eq_(a3.aggregation, False)
        eq_(a5.composition, False)
        eq_(a5.aggregation, True)

        a1.aggregation = True
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)
        a1.composition = True
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)

    def testMixedAssociationTypes(self):
        c1 = CClass(self.m1, "C1")
        s1 = CStereotype("S1")
        try:
            a1 = self.m1.association(s1, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
            exceptionExpected_()
        except CException as e: 
            eq_("metaclass 'M1' is not compatible with association target 'S1'", e.value)

        try:
            a1 = self.m1.association(c1, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
            exceptionExpected_()
        except CException as e: 
            eq_("metaclass 'M1' is not compatible with association target 'C1'", e.value)

    def testGetAssociationByRoleName(self):
        a1 = self.m1.association(self.m2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.m1.association(self.m2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.m1.association(self.m3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)

        a_2 = next(a for a in self.m1.associations if a.roleName == "s")
        eq_(a_2.multiplicity, "1")
        eq_(a_2.sourceRoleName, "o")
        eq_(a_2.sourceMultiplicity, "*")

    def testGetAssociationByName(self):
        a1 = self.m1.association(self.m2, name = "n1", multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.m1.association(self.m2, name = "n2", multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.m1.association(self.m3, "n3: [a] 0..1 <*>- [n] *")

        a_2 = next(a for a in self.m1.associations if a.name == "n2")
        eq_(a_2.multiplicity, "1")
        eq_(a_2.sourceRoleName, "o")
        eq_(a_2.sourceMultiplicity, "*")

        a_3 = next(a for a in self.m1.associations if a.name == "n3")
        eq_(a_3.multiplicity, "*")
        eq_(a_3.roleName, "n")
        eq_(a_3.sourceMultiplicity, "0..1")
        eq_(a_3.sourceRoleName, "a")
        eq_(a_3.composition, True)     


    def testGetAssociations(self):
        a1 = self.m1.association(self.m2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.m1.association(self.m2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.m1.association(self.m3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a4 = self.m1.association(self.m3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.m4.association(self.m3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.m3.association(self.m2, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "3", sourceRoleName = "a", aggregation = True)
        eq_(self.m1.associations, [a1, a2, a3, a4])
        eq_(self.m2.associations, [a1, a2, a6])
        eq_(self.m3.associations, [a3, a4, a5, a6])
        eq_(self.m4.associations, [a5])
        eq_(self.m5.associations, [])

    def testDeleteAssociations(self):
        a1 = self.m1.association(self.m2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.m1.association(self.m2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.m1.association(self.m3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a4 = self.m1.association(self.m3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.m4.association(self.m3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.m3.association(self.m2, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "3", sourceRoleName = "a", aggregation = True)
        a7 = self.m1.association(self.m1, multiplicity = "*", roleName = "x",  
                sourceMultiplicity = "3", sourceRoleName = "y")

        eq_(len(self.getAllAssociationsInBundle()), 7)

        a2.delete()
        a4.delete()
        
        eq_(len(self.getAllAssociationsInBundle()), 5)

        eq_(self.m1.associations, [a1, a3, a7])
        eq_(self.m2.associations, [a1, a6])
        eq_(self.m3.associations, [a3, a5, a6])
        eq_(self.m4.associations, [a5])
        eq_(self.m5.associations, [])


    def testDeleteClassAndGetAssociations(self):
        a1 = self.m1.association(self.m2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.m1.association(self.m2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.m1.association(self.m3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a4 = self.m1.association(self.m3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.m4.association(self.m3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.m3.association(self.m2, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "3", sourceRoleName = "a", aggregation = True)
        a7 = self.m1.association(self.m1, multiplicity = "*", roleName = "x",  
                sourceMultiplicity = "3", sourceRoleName = "y")

        eq_(len(self.getAllAssociationsInBundle()), 7)

        self.m1.delete()
        
        eq_(len(self.getAllAssociationsInBundle()), 2)

        eq_(self.m1.associations, [])
        eq_(self.m2.associations, [a6])
        eq_(self.m3.associations, [a5, a6])
        eq_(self.m4.associations, [a5])
        eq_(self.m5.associations, [])

    def testAllAssociations(self):
        s = CMetaclass("S")
        d = CMetaclass("D", superclasses = s)
        a = s.association(d, "is next: [prior s] * -> [next d] *")
        eq_(d.allAssociations, [a])
        eq_(s.allAssociations, [a])


if __name__ == "__main__":
    nose.main()