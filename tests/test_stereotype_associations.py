import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CStereotype, CClass, CObject, CAttribute, CException, CEnum, CBundle

class TestStereotypeAssociations():
    
    def setUp(self):
        self.stereotypeBundle = CBundle("Elements")
        self.s1 = CStereotype("S1", bundles = self.stereotypeBundle)
        self.s2 = CStereotype("S2", bundles = self.stereotypeBundle)
        self.s3 = CStereotype("S3", bundles = self.stereotypeBundle)
        self.s4 = CStereotype("S4", bundles = self.stereotypeBundle)
        self.s5 = CStereotype("S5", bundles = self.stereotypeBundle)

    def getAllAssociationsInBundle(self):
        associations = []
        for c in self.stereotypeBundle.getElements(type=CStereotype):
            for a in c.allAssociations:
                if not a in associations:
                    associations.append(a)
        return associations

    def testAssociationCreation(self):
        a1 = self.s1.association(self.s2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.s1.association(self.s2, "[o]*->[s]1")
        a3 = self.s1.association(self.s3, "[a] 0..1 <*>- [n]*")
        a4 = self.s1.association(self.s3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.s4.association(self.s3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.s3.association(self.s2, '[a] 0..3 <>- [e]*')

        eq_(len(self.getAllAssociationsInBundle()), 6)

        eq_(self.s1.associations[0].roleName, "t")
        eq_(a5.roleName, "n")
        eq_(a2.roleName, "s")
        eq_(a1.multiplicity, "1")
        eq_(a1.sourceMultiplicity, "*")
        eq_(a4.sourceMultiplicity, "0..1")
        eq_(a6.sourceMultiplicity, "0..3")

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
        m1 = CMetaclass("M1")
        c1 = CClass(m1, "C1")
        try:
            a1 = self.s1.association(c1, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
            exceptionExpected_()
        except CException as e: 
            eq_("stereotype 'S1' is not compatible with association target 'C1'", e.value)

        try:
            a1 = self.s1.association(m1, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
            exceptionExpected_()
        except CException as e: 
            eq_("stereotype 'S1' is not compatible with association target 'M1'", e.value)

    def testGetAssociationByRoleName(self):
        a1 = self.s1.association(self.s2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.s1.association(self.s2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.s1.association(self.s3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)

        a_2 = next(a for a in self.s1.associations if a.roleName == "s")
        eq_(a_2.multiplicity, "1")
        eq_(a_2.sourceRoleName, "o")
        eq_(a_2.sourceMultiplicity, "*")

    def testGetAssociationByName(self):
        a1 = self.s1.association(self.s2, name = "n1", multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.s1.association(self.s2, name = "n2", multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.s1.association(self.s3, "n3: [a] 0..1 <*>- [n] *")

        a_2 = next(a for a in self.s1.associations if a.name == "n2")
        eq_(a_2.multiplicity, "1")
        eq_(a_2.sourceRoleName, "o")
        eq_(a_2.sourceMultiplicity, "*")

        a_3 = next(a for a in self.s1.associations if a.name == "n3")
        eq_(a_3.multiplicity, "*")
        eq_(a_3.roleName, "n")
        eq_(a_3.sourceMultiplicity, "0..1")
        eq_(a_3.sourceRoleName, "a")
        eq_(a_3.composition, True)   

    def testGetAssociations(self):
        a1 = self.s1.association(self.s2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.s1.association(self.s2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.s1.association(self.s3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a4 = self.s1.association(self.s3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.s4.association(self.s3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.s3.association(self.s2, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "1..3", sourceRoleName = "a", aggregation = True)
        eq_(self.s1.associations, [a1, a2, a3, a4])
        eq_(self.s2.associations, [a1, a2, a6])
        eq_(self.s3.associations, [a3, a4, a5, a6])
        eq_(self.s4.associations, [a5])
        eq_(self.s5.associations, [])

    def testDeleteAssociations(self):
        a1 = self.s1.association(self.s2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.s1.association(self.s2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.s1.association(self.s3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a4 = self.s1.association(self.s3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.s4.association(self.s3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.s3.association(self.s2, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..3", sourceRoleName = "a", aggregation = True)
        a7 = self.s1.association(self.s1, multiplicity = "*", roleName = "x",  
                sourceMultiplicity = "1..3", sourceRoleName = "y")

        eq_(len(self.getAllAssociationsInBundle()), 7)

        a2.delete()
        a4.delete()
        
        eq_(len(self.getAllAssociationsInBundle()), 5)

        eq_(self.s1.associations, [a1, a3, a7])
        eq_(self.s2.associations, [a1, a6])
        eq_(self.s3.associations, [a3, a5, a6])
        eq_(self.s4.associations, [a5])
        eq_(self.s5.associations, [])


    def testDeleteClassAndGetAssociations(self):
        a1 = self.s1.association(self.s2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.s1.association(self.s2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.s1.association(self.s3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a4 = self.s1.association(self.s3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.s4.association(self.s3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.s3.association(self.s2, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..3", sourceRoleName = "a", aggregation = True)
        a7 = self.s1.association(self.s1, multiplicity = "*", roleName = "x",  
                sourceMultiplicity = "1..3", sourceRoleName = "y")

        eq_(len(self.getAllAssociationsInBundle()), 7)

        self.s1.delete()
        
        eq_(len(self.getAllAssociationsInBundle()), 2)

        eq_(self.s1.associations, [])
        eq_(self.s2.associations, [a6])
        eq_(self.s3.associations, [a5, a6])
        eq_(self.s4.associations, [a5])
        eq_(self.s5.associations, [])

    def testAllAssociations(self):
        s = CStereotype("S")
        d = CStereotype("D", superclasses = s)
        a = s.association(d, "is next: [prior s] * -> [next d] *")
        eq_(d.allAssociations, [a])
        eq_(s.allAssociations, [a])

if __name__ == "__main__":
    nose.main()