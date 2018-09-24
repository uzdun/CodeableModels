import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CClass, CObject, CAttribute, CException, CEnum, CStereotype

class TestClassAssociations():
    
    def setUp(self):
        self.mcl = CMetaclass("MCL")
        self.c1 = CClass(self.mcl, "C1")
        self.c2 = CClass(self.mcl, "C2")
        self.c3 = CClass(self.mcl, "C3")
        self.c4 = CClass(self.mcl, "C4")
        self.c5 = CClass(self.mcl, "C5")

    def getAllAssociationsOfMetaclass(self):
        associations = []
        for c in self.mcl.allClasses:
            for a in c.allAssociations:
                if not a in associations:
                    associations.append(a)
        return associations

    def testAssociationCreation(self):
        a1 = self.c1.association(self.c2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.c1.association(self.c2, "[o]*->[s]1")
        a3 = self.c1.association(self.c3, "[a] 0..1 <*>- [n]*")
        a4 = self.c1.association(self.c3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.c4.association(self.c3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.c3.association(self.c2, '[a] 3 <>- [e]*')

        eq_(len(self.getAllAssociationsOfMetaclass()), 6)

        eq_(self.c1.associations[0].roleName, "t")
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
        m1 = CMetaclass("M1")
        s1 = CStereotype("S1")
        try:
            a1 = self.c1.association(s1, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
            exceptionExpected_()
        except CException as e: 
            eq_("class 'C1' is not compatible with association target 'S1'", e.value)

        try:
            a1 = self.c1.association(m1, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
            exceptionExpected_()
        except CException as e: 
            eq_("class 'C1' is not compatible with association target 'M1'", e.value)

    def testGetAssociationByRoleName(self):
        a1 = self.c1.association(self.c2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.c1.association(self.c2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.c1.association(self.c3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)

        a_2 = next(a for a in self.c1.associations if a.roleName == "s")
        eq_(a_2.multiplicity, "1")
        eq_(a_2.sourceRoleName, "o")
        eq_(a_2.sourceMultiplicity, "*")

    def testGetAssociationByName(self):
        a1 = self.c1.association(self.c2, name = "n1", multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.c1.association(self.c2, name = "n2", multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.c1.association(self.c3, "n3: [a] 0..1 <*>- [n] *")

        a_2 = next(a for a in self.c1.associations if a.name == "n2")
        eq_(a_2.multiplicity, "1")
        eq_(a_2.sourceRoleName, "o")
        eq_(a_2.sourceMultiplicity, "*")

        a_3 = next(a for a in self.c1.associations if a.name == "n3")
        eq_(a_3.multiplicity, "*")
        eq_(a_3.roleName, "n")
        eq_(a_3.sourceMultiplicity, "0..1")
        eq_(a_3.sourceRoleName, "a")
        eq_(a_3.composition, True)     

    def testGetAssociations(self):
        a1 = self.c1.association(self.c2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.c1.association(self.c2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.c1.association(self.c3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a4 = self.c1.association(self.c3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.c4.association(self.c3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.c3.association(self.c2, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "3", sourceRoleName = "a", aggregation = True)
        eq_(self.c1.associations, [a1, a2, a3, a4])
        eq_(self.c2.associations, [a1, a2, a6])
        eq_(self.c3.associations, [a3, a4, a5, a6])
        eq_(self.c4.associations, [a5])
        eq_(self.c5.associations, [])

    def testDeleteAssociations(self):
        a1 = self.c1.association(self.c2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.c1.association(self.c2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.c1.association(self.c3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a4 = self.c1.association(self.c3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.c4.association(self.c3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.c3.association(self.c2, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "3", sourceRoleName = "a", aggregation = True)
        a7 = self.c1.association(self.c1, multiplicity = "*", roleName = "x",  
                sourceMultiplicity = "3", sourceRoleName = "y")

        eq_(len(self.getAllAssociationsOfMetaclass()), 7)

        a2.delete()
        a4.delete()
        
        eq_(len(self.getAllAssociationsOfMetaclass()), 5)

        eq_(self.c1.associations, [a1, a3, a7])
        eq_(self.c2.associations, [a1, a6])
        eq_(self.c3.associations, [a3, a5, a6])
        eq_(self.c4.associations, [a5])
        eq_(self.c5.associations, [])


    def testDeleteClassAndGetAssociations(self):
        a1 = self.c1.association(self.c2, multiplicity = "1", roleName = "t",  
                sourceMultiplicity = "*", sourceRoleName = "i")
        a2 = self.c1.association(self.c2, multiplicity = "1", roleName = "s",  
                sourceMultiplicity = "*", sourceRoleName = "o")
        a3 = self.c1.association(self.c3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a4 = self.c1.association(self.c3, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", composition = True)
        a5 = self.c4.association(self.c3, multiplicity = "*", roleName = "n",  
                sourceMultiplicity = "0..1", sourceRoleName = "a", aggregation = True)
        a6 = self.c3.association(self.c2, multiplicity = "*", roleName = "e",  
                sourceMultiplicity = "3", sourceRoleName = "a", aggregation = True)
        a7 = self.c1.association(self.c1, multiplicity = "*", roleName = "x",  
                sourceMultiplicity = "3", sourceRoleName = "y")

        eq_(len(self.getAllAssociationsOfMetaclass()), 7)

        self.c1.delete()
        
        eq_(len(self.getAllAssociationsOfMetaclass()), 2)

        eq_(self.c1.associations, [])
        eq_(self.c2.associations, [a6])
        eq_(self.c3.associations, [a5, a6])
        eq_(self.c4.associations, [a5])
        eq_(self.c5.associations, [])


    def testAllAssociations(self):
        s = CClass(self.mcl, "S")
        d = CClass(self.mcl, "D", superclasses = s)
        a = s.association(d, "is next: [prior s] * -> [next d] *")
        eq_(d.allAssociations, [a])
        eq_(s.allAssociations, [a])

        
if __name__ == "__main__":
    nose.main()