import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeable_models import CStereotype, CMetaclass, CClass, CObject, CAttribute, CException, CEnum, CAssociation, CBundle

class TestStereotypesOnMetaclasses():
    def setUp(self):
        self.mcl = CMetaclass("MCL")
        self.mcl = CMetaclass("MCL")

    def testCreationOfOneStereotype(self):
        s = CStereotype("S", extended = self.mcl)
        eq_(s.name, "S")
        eq_(self.mcl.stereotypes, [s])
        eq_(s.extended, [self.mcl])

    def testWrongsTypesInListOfExtendedElementTypes(self):
        try:
            s = CStereotype("S", extended = [self.mcl, self.mcl.association(self.mcl, name = "A")])
            exceptionExpected_()
        except CException as e: 
            eq_("'A' is not a metaclass", e.value)
        try:
            s = CStereotype("S", extended = [self.mcl, CBundle("P")])
            exceptionExpected_()
        except CException as e: 
            eq_("'P' is not a metaclass", e.value)
        try:
            s = CStereotype("S", extended = [CBundle("P"), self.mcl])
            exceptionExpected_()
        except CException as e: 
            eq_("unknown type of extend element: 'P'", e.value)


    def testCreationOf3Stereotypes(self):
        s1 = CStereotype("S1")
        s2 = CStereotype("S2")
        s3 = CStereotype("S3")
        self.mcl.stereotypes = [s1, s2, s3]
        eq_(s1.extended, [self.mcl])
        eq_(s2.extended, [self.mcl])
        eq_(s3.extended, [self.mcl])
        eq_(set(self.mcl.stereotypes), set([s1, s2, s3]))
    
    def testCreationOfUnnamedStereotype(self):
        s = CStereotype()
        eq_(s.name, None)
        eq_(self.mcl.stereotypes, [])
        eq_(s.extended, [])

    def testDeleteStereotype(self):
        s1 = CStereotype("S1")
        s1.delete()
        eq_(s1.name, None)
        eq_(self.mcl.stereotypes, [])
        s1 = CStereotype("S1", extended = self.mcl)
        s1.delete()
        eq_(s1.name, None)
        eq_(self.mcl.stereotypes, [])

        s1 = CStereotype("S1", extended = self.mcl)
        s2 = CStereotype("S2", extended = self.mcl)
        s3 = CStereotype("s1", superclasses = s2, attributes = {"i" : 1}, extended = self.mcl)

        s1.delete()
        eq_(set(self.mcl.stereotypes), set([s2, s3]))
        s3.delete()
        eq_(set(self.mcl.stereotypes), set([s2]))

        eq_(s3.superclasses, [])
        eq_(s2.subclasses, [])
        eq_(s3.attributes, [])
        eq_(s3.attribute_names, [])
        eq_(s3.extended, [])
        eq_(s3.name, None)
        eq_(s3.bundles, [])

    def testStereotypeExtensionAddRemove(self):
        s1 = CStereotype("S1")
        eq_(set(s1.extended), set())
        mcl1 = CMetaclass(stereotypes = [s1])
        eq_(set(s1.extended), set([mcl1]))
        eq_(set(mcl1.stereotypes), set([s1]))
        mcl2 = CMetaclass(stereotypes = s1)
        eq_(set(s1.extended), set([mcl1, mcl2]))
        eq_(set(mcl1.stereotypes), set([s1])) 
        eq_(set(mcl2.stereotypes), set([s1]))
        s1.extended = [mcl2]
        eq_(set(s1.extended), set([mcl2]))
        eq_(set(mcl1.stereotypes), set()) 
        eq_(set(mcl2.stereotypes), set([s1]))
        s2 = CStereotype("S2", extended = [mcl2])
        eq_(set(mcl2.stereotypes), set([s2, s1]))
        eq_(set(s1.extended), set([mcl2]))
        eq_(set(s2.extended), set([mcl2]))
        mcl2.stereotypes = []
        eq_(set(mcl2.stereotypes), set())
        eq_(set(s1.extended), set())
        eq_(set(s2.extended), set())

    def testStereotypeRemoveSterotypeOrMetaclass(self):
        mcl = CMetaclass("MCL1")
        s1 = CStereotype("S1", extended = [mcl])
        s2 = CStereotype("S2", extended = [mcl])
        s3 = CStereotype("S3", extended = [mcl])
        s4 = CStereotype("S4", extended = [mcl])
        eq_(set(mcl.stereotypes), set([s1, s2, s3, s4]))
        s2.delete()
        eq_(set(mcl.stereotypes), set([s1, s3, s4]))
        eq_(set(s2.extended), set())
        eq_(set(s1.extended), set([mcl]))  
        mcl.delete()
        eq_(set(mcl.stereotypes), set())
        eq_(set(s1.extended), set())

    def testStereotypesWrongType(self):
        try:
            self.mcl.stereotypes = [self.mcl]
            exceptionExpected_()
        except CException as e: 
            eq_("'MCL' is not a stereotype", e.value)

    def testExtendedWrongType(self):
        try:
            cl = CClass(self.mcl) 
            CStereotype("S1", extended = [cl])
            exceptionExpected_()
        except CException as e: 
            eq_("unknown type of extend element: ''", e.value)

    def testMetaclassStereotypesNullInput(self):
        s = CStereotype() 
        m = CMetaclass(stereotypes = None)
        eq_(m.stereotypes, [])
        eq_(s.extended, [])

    def testMetaclassStereotypesNonListInput(self):
        s = CStereotype() 
        m = CMetaclass(stereotypes = s)
        eq_(m.stereotypes, [s])
        eq_(s.extended, [m])

    def testMetaclassStereotypesNonListInputWrongType(self):
        try:
            CMetaclass(stereotypes = self.mcl)
            exceptionExpected_()
        except CException as e: 
            eq_("a list or a stereotype is required as input", e.value)

    def testMetaclassStereotypesAppend(self):
        s1 = CStereotype()
        s2 = CStereotype()  
        m = CMetaclass(stereotypes = [s1])
        # should have no effect, as setter must be used
        m.stereotypes.append(s2)
        eq_(m.stereotypes, [s1])
        eq_(s1.extended, [m])
        eq_(s2.extended, [])

    def testStereotypeExtendedNullInput(self):
        m = CMetaclass()
        s = CStereotype(extended = None) 
        eq_(m.stereotypes, [])
        eq_(s.extended, [])

    def testStereotypeExtendedNonListInput(self):
        m = CMetaclass()
        s = CStereotype(extended = m) 
        eq_(m.stereotypes, [s])
        eq_(s.extended, [m])

    def testStereotypeExtendedNonListInputWrongType(self):
        try:
            s = CStereotype(extended = CClass(self.mcl))
            exceptionExpected_()
        except CException as e: 
            eq_("extended requires a list or a metaclass as input", e.value)

    def testStereotypeExtendedAppend(self):
        m1 = CMetaclass()
        m2 = CMetaclass()
        s = CStereotype(extended = [m1])
        # should have no effect, as setter must be used
        s.extended.append(m2)
        eq_(m1.stereotypes, [s])
        eq_(m2.stereotypes, [])
        eq_(s.extended, [m1])

    def testExtendedMetaclassThatIsDeleted(self):
        m1 = CMetaclass("M1")
        m1.delete()
        try:
            CStereotype(extended = [m1])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "cannot access named element that has been deleted")

    def testExtendedMetaclassThatAreNone(self):
        try:
            CStereotype(extended = [None])
            exceptionExpected_()
        except CException as e: 
            eq_(e.value, "unknown type of extend element: 'None'")

if __name__ == "__main__":
    nose.main()



