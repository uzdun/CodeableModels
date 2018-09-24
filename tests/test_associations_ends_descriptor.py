import nose
from nose.tools import ok_, eq_
from testCommons import neq_, exceptionExpected_
from parameterized import parameterized

from codeableModels import CMetaclass, CClass, CObject, CAttribute, CException, CEnum, CStereotype

class TestAssociationsEndsDescriptor():
    
    def setUp(self):
        self.mcl = CMetaclass("MCL")
        self.c1 = CClass(self.mcl, "C1")
        self.c2 = CClass(self.mcl, "C2")
        self.c3 = CClass(self.mcl, "C3")
        self.c4 = CClass(self.mcl, "C4")
        self.c5 = CClass(self.mcl, "C5")
        
    def testEndsStringMalformed(self):
        try:
            a1 = self.c1.association(self.c2, '')
            exceptionExpected_()
        except CException as e: 
            eq_("association descriptor malformed: ''", e.value)       
        try:
            a1 = self.c1.association(self.c2, '->->')
            exceptionExpected_()
        except CException as e: 
            eq_("malformed multiplicity: ''", e.value) 
        try:
            a1 = self.c1.association(self.c2, 'a->b')
            exceptionExpected_()
        except CException as e: 
            eq_("malformed multiplicity: 'a'", e.value) 
        try:
            a1 = self.c1.association(self.c2, '[]->[]')
            exceptionExpected_()
        except CException as e: 
            eq_("malformed multiplicity: '[]'", e.value) 
        try:
            a1 = self.c1.association(self.c2, '[]1->[]*')
            exceptionExpected_()
        except CException as e: 
            eq_("malformed multiplicity: '[]1'", e.value)
        try:
            a1 = self.c1.association(self.c2, '::1->1')
            exceptionExpected_()
        except CException as e: 
            eq_("malformed multiplicity: ':1'", e.value)
        try:
            a1 = self.c1.association(self.c2, '1->1:')
            exceptionExpected_()
        except CException as e: 
            eq_("association descriptor malformed: ''", e.value)

    def testEndsStringAssociation(self):
        a1 = self.c1.association(self.c2, '[a]1->[b]*')
        eq_(a1.roleName, "b")
        eq_(a1.sourceRoleName, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, ' [a b]  1   ->  [ b c_()-] * ')
        eq_(a1.roleName, " b c_()-")
        eq_(a1.sourceRoleName, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, '1..3->    4..*  ')
        eq_(a1.roleName, None)
        eq_(a1.sourceRoleName, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.sourceMultiplicity, "1..3")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, '[ax] -> [bx]')
        eq_(a1.roleName, "bx")
        eq_(a1.sourceRoleName, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)

    def testEndsStringAggregation(self):
        a1 = self.c1.association(self.c2, '[a]1<>-[b]*')
        eq_(a1.roleName, "b")
        eq_(a1.sourceRoleName, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)

        a1 = self.c1.association(self.c2, ' [a b]  1   <>-  [ b c_()-] * ')
        eq_(a1.roleName, " b c_()-")
        eq_(a1.sourceRoleName, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)

        a1 = self.c1.association(self.c2, '1..3<>-    4..*  ')
        eq_(a1.roleName, None)
        eq_(a1.sourceRoleName, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.sourceMultiplicity, "1..3")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)

        a1 = self.c1.association(self.c2, '[ax] <>- [bx]')
        eq_(a1.roleName, "bx")
        eq_(a1.sourceRoleName, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)

    def testEndsStringComposition(self):
        a1 = self.c1.association(self.c2, '[a]1<*>-[b]*')
        eq_(a1.roleName, "b")
        eq_(a1.sourceRoleName, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, ' [a b]  1   <*>-  [ b c_()-] * ')
        eq_(a1.roleName, " b c_()-")
        eq_(a1.sourceRoleName, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, '1..3<*>-    4..*  ')
        eq_(a1.roleName, None)
        eq_(a1.sourceRoleName, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.sourceMultiplicity, "1..3")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)

        a1 = self.c1.association(self.c2, '[ax] <*>- [bx]')
        eq_(a1.roleName, "bx")
        eq_(a1.sourceRoleName, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)


    def testEndsStringAssociationWithName(self):
        a1 = self.c1.association(self.c2, ' assoc a : [a]1->[b]*')
        eq_(a1.roleName, "b")
        eq_(a1.sourceRoleName, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)
        eq_(a1.name, "assoc a")

        a1 = self.c1.association(self.c2, 'a: [a b]  1   ->  [ b c_()-] * ')
        eq_(a1.roleName, " b c_()-")
        eq_(a1.sourceRoleName, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)
        eq_(a1.name, "a")

        a1 = self.c1.association(self.c2, '"legal_name":1..3->    4..*  ')
        eq_(a1.roleName, None)
        eq_(a1.sourceRoleName, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.sourceMultiplicity, "1..3")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)
        eq_(a1.name, '"legal_name"')

        a1 = self.c1.association(self.c2, '[ax] -> [bx]:[ax] -> [bx]')
        eq_(a1.roleName, "bx")
        eq_(a1.sourceRoleName, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, False)
        eq_(a1.name, '[ax] -> [bx]')


    def testEndsStringAggregationWithName(self):
        a1 = self.c1.association(self.c2, ' assoc a : [a]1<>-[b]*')
        eq_(a1.roleName, "b")
        eq_(a1.sourceRoleName, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)
        eq_(a1.name, "assoc a")

        a1 = self.c1.association(self.c2, ': [a b]  1   <>-  [ b c_()-] * ')
        eq_(a1.roleName, " b c_()-")
        eq_(a1.sourceRoleName, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.name, "")

        a1 = self.c1.association(self.c2, '"legal_name":1..3<>-    4..*  ')
        eq_(a1.roleName, None)
        eq_(a1.sourceRoleName, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.sourceMultiplicity, "1..3")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)
        eq_(a1.name, '"legal_name"')
        
        a1 = self.c1.association(self.c2, '[ax] <>- [bx]:[ax] <>- [bx]')
        eq_(a1.roleName, "bx")
        eq_(a1.sourceRoleName, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, False)
        eq_(a1.aggregation, True)
        eq_(a1.name, '[ax] <>- [bx]')


    def testEndsStringCompositionWithName(self):
        a1 = self.c1.association(self.c2, ' assoc a : [a]1<*>-[b]*')
        eq_(a1.roleName, "b")
        eq_(a1.sourceRoleName, "a")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)
        eq_(a1.name, "assoc a")

        a1 = self.c1.association(self.c2, 'a: [a b]  1   <*>-  [ b c_()-] * ')
        eq_(a1.roleName, " b c_()-")
        eq_(a1.sourceRoleName, "a b")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)
        eq_(a1.name, "a")

        a1 = self.c1.association(self.c2, '"legal_name":1..3<*>-    4..*  ')
        eq_(a1.roleName, None)
        eq_(a1.sourceRoleName, None)
        eq_(a1.multiplicity, "4..*")
        eq_(a1.sourceMultiplicity, "1..3")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)
        eq_(a1.name, '"legal_name"')

        a1 = self.c1.association(self.c2, '[ax] <*>- [bx]:[ax] <*>- [bx]')
        eq_(a1.roleName, "bx")
        eq_(a1.sourceRoleName, "ax")
        eq_(a1.multiplicity, "*")
        eq_(a1.sourceMultiplicity, "1")
        eq_(a1.composition, True)
        eq_(a1.aggregation, False)
        eq_(a1.name, '[ax] <*>- [bx]')

if __name__ == "__main__":
    nose.main()