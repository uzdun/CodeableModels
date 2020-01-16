import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeable_models import CMetaclass, CStereotype, CClass, CObject, CAttribute, CException, CEnum, CBundle

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
        for c in self.stereotypeBundle.get_elements(type=CStereotype):
            for a in c.all_associations:
                if not a in associations:
                    associations.append(a)
        return associations

    def testAssociationCreation(self):
        a1 = self.s1.association(self.s2, multiplicity = "1", role_name = "t",
                source_multiplicity = "*", source_role_name = "i")
        a2 = self.s1.association(self.s2, "[o]*->[s]1")
        a3 = self.s1.association(self.s3, "[a] 0..1 <*>- [n]*")
        a4 = self.s1.association(self.s3, multiplicity = "*", role_name = "e",
                source_multiplicity = "0..1", source_role_name = "a", composition = True)
        a5 = self.s4.association(self.s3, multiplicity = "*", role_name = "n",
                source_multiplicity = "0..1", source_role_name = "a", aggregation = True)
        a6 = self.s3.association(self.s2, '[a] 0..3 <>- [e]*')

        eq_(len(self.getAllAssociationsInBundle()), 6)

        eq_(self.s1.associations[0].role_name, "t")
        eq_(a5.role_name, "n")
        eq_(a2.role_name, "s")
        eq_(a1.multiplicity, "1")
        eq_(a1.source_multiplicity, "*")
        eq_(a4.source_multiplicity, "0..1")
        eq_(a6.source_multiplicity, "0..3")

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
            a1 = self.s1.association(c1, multiplicity = "1", role_name = "t",
                source_multiplicity = "*", source_role_name = "i")
            exceptionExpected_()
        except CException as e: 
            eq_("stereotype 'S1' is not compatible with association target 'C1'", e.value)

        try:
            a1 = self.s1.association(m1, multiplicity = "1", role_name = "t",
                source_multiplicity = "*", source_role_name = "i")
            exceptionExpected_()
        except CException as e: 
            eq_("stereotype 'S1' is not compatible with association target 'M1'", e.value)

    def testGetAssociationByrole_name(self):
        a1 = self.s1.association(self.s2, multiplicity = "1", role_name = "t",
                source_multiplicity = "*", source_role_name = "i")
        a2 = self.s1.association(self.s2, multiplicity = "1", role_name = "s",
                source_multiplicity = "*", source_role_name = "o")
        a3 = self.s1.association(self.s3, multiplicity = "*", role_name = "n",
                source_multiplicity = "0..1", source_role_name = "a", composition = True)

        a_2 = next(a for a in self.s1.associations if a.role_name == "s")
        eq_(a_2.multiplicity, "1")
        eq_(a_2.source_role_name, "o")
        eq_(a_2.source_multiplicity, "*")

    def testGetAssociationByName(self):
        a1 = self.s1.association(self.s2, name = "n1", multiplicity = "1", role_name = "t",
                source_multiplicity = "*", source_role_name = "i")
        a2 = self.s1.association(self.s2, name = "n2", multiplicity = "1", role_name = "s",
                source_multiplicity = "*", source_role_name = "o")
        a3 = self.s1.association(self.s3, "n3: [a] 0..1 <*>- [n] *")

        a_2 = next(a for a in self.s1.associations if a.name == "n2")
        eq_(a_2.multiplicity, "1")
        eq_(a_2.source_role_name, "o")
        eq_(a_2.source_multiplicity, "*")

        a_3 = next(a for a in self.s1.associations if a.name == "n3")
        eq_(a_3.multiplicity, "*")
        eq_(a_3.role_name, "n")
        eq_(a_3.source_multiplicity, "0..1")
        eq_(a_3.source_role_name, "a")
        eq_(a_3.composition, True)   

    def testGetAssociations(self):
        a1 = self.s1.association(self.s2, multiplicity = "1", role_name = "t",
                source_multiplicity = "*", source_role_name = "i")
        a2 = self.s1.association(self.s2, multiplicity = "1", role_name = "s",
                source_multiplicity = "*", source_role_name = "o")
        a3 = self.s1.association(self.s3, multiplicity = "*", role_name = "n",
                source_multiplicity = "0..1", source_role_name = "a", composition = True)
        a4 = self.s1.association(self.s3, multiplicity = "*", role_name = "e",
                source_multiplicity = "0..1", source_role_name = "a", composition = True)
        a5 = self.s4.association(self.s3, multiplicity = "*", role_name = "n",
                source_multiplicity = "0..1", source_role_name = "a", aggregation = True)
        a6 = self.s3.association(self.s2, multiplicity = "*", role_name = "e",
                source_multiplicity = "1..3", source_role_name = "a", aggregation = True)
        eq_(self.s1.associations, [a1, a2, a3, a4])
        eq_(self.s2.associations, [a1, a2, a6])
        eq_(self.s3.associations, [a3, a4, a5, a6])
        eq_(self.s4.associations, [a5])
        eq_(self.s5.associations, [])

    def testDeleteAssociations(self):
        a1 = self.s1.association(self.s2, multiplicity = "1", role_name = "t",
                source_multiplicity = "*", source_role_name = "i")
        a2 = self.s1.association(self.s2, multiplicity = "1", role_name = "s",
                source_multiplicity = "*", source_role_name = "o")
        a3 = self.s1.association(self.s3, multiplicity = "*", role_name = "n",
                source_multiplicity = "0..1", source_role_name = "a", composition = True)
        a4 = self.s1.association(self.s3, multiplicity = "*", role_name = "e",
                source_multiplicity = "0..1", source_role_name = "a", composition = True)
        a5 = self.s4.association(self.s3, multiplicity = "*", role_name = "n",
                source_multiplicity = "0..1", source_role_name = "a", aggregation = True)
        a6 = self.s3.association(self.s2, multiplicity = "*", role_name = "e",
                source_multiplicity = "0..3", source_role_name = "a", aggregation = True)
        a7 = self.s1.association(self.s1, multiplicity = "*", role_name = "x",
                source_multiplicity = "1..3", source_role_name = "y")

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
        a1 = self.s1.association(self.s2, multiplicity = "1", role_name = "t",
                source_multiplicity = "*", source_role_name = "i")
        a2 = self.s1.association(self.s2, multiplicity = "1", role_name = "s",
                source_multiplicity = "*", source_role_name = "o")
        a3 = self.s1.association(self.s3, multiplicity = "*", role_name = "n",
                source_multiplicity = "0..1", source_role_name = "a", composition = True)
        a4 = self.s1.association(self.s3, multiplicity = "*", role_name = "e",
                source_multiplicity = "0..1", source_role_name = "a", composition = True)
        a5 = self.s4.association(self.s3, multiplicity = "*", role_name = "n",
                source_multiplicity = "0..1", source_role_name = "a", aggregation = True)
        a6 = self.s3.association(self.s2, multiplicity = "*", role_name = "e",
                source_multiplicity = "0..3", source_role_name = "a", aggregation = True)
        a7 = self.s1.association(self.s1, multiplicity = "*", role_name = "x",
                source_multiplicity = "1..3", source_role_name = "y")

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
        eq_(d.all_associations, [a])
        eq_(s.all_associations, [a])

if __name__ == "__main__":
    nose.main()