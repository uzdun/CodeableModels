package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;


public class TestsStereotypesOnAssociations {

    @Test
    public void testCreationOfOneStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("1"), mcl2.createEnd("1"));
        CStereotype stereotype = model.createStereotype("Stereotype1", assoc1);

        assertEquals(Collections.emptyList(), mcl1.getStereotypes());
        assertEquals(Collections.emptyList(), mcl2.getStereotypes());
        assertEquals(Collections.singletonList(stereotype), assoc1.getStereotypes());
        assertEquals(assoc1, stereotype.getStereotypedElements().get(0));
    }

    @Test
    public void testCreationOfStereotypeOnClassAssociation() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL1");
        CClass cl1 = model.createClass(mcl,"CL1");
        CClass cl2 = model.createClass(mcl,"CL2");
        CAssociation assoc1 = model.createAssociation(cl1.createEnd("1"), cl2.createEnd("1"));
        try {
            model.createStereotype("Stereotype1", assoc1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("association classifiers 'CL1' and/or 'CL2' are not metaclasses", e.getMessage());
        }
    }

    @Test
    public void testCreateAssociationStereotypeByName() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation("assoc1", mcl1.createEnd("1"), mcl2.createEnd("1"));
        CStereotype stereotype = model.createStereotype("Stereotype1", "assoc1");

        assertEquals(Collections.emptyList(), mcl1.getStereotypes());
        assertEquals(Collections.emptyList(), mcl2.getStereotypes());
        assertEquals(Collections.singletonList(stereotype), assoc1.getStereotypes());
        assertEquals(assoc1, stereotype.getStereotypedElements().get(0));
    }

    @Test
    public void testCreateAssociationStereotypeByNameFail() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");

        try {
            model.createStereotype("Stereotype1", "assoc1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't find association 'assoc1' to be stereotyped", e.getMessage());
        }

        model.createAssociation("assoc1", mcl1.createEnd("1"), mcl2.createEnd("1"));
        model.createAssociation("assoc1", mcl1.createEnd("1"), mcl2.createEnd("1"));

        try {
            model.createStereotype("Stereotype1", "assoc1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("found multiple associations with the name 'assoc1', use reference to select stereotype instead", e.getMessage());
        }
    }

    @Test
    public void testCreationOfThreeStereotypes() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("1"), mcl2.createEnd("1"));
        CStereotype st1 = model.createStereotype("Stereotype1", assoc1);
        CStereotype st2 = model.createStereotype("Stereotype2", assoc1);
        CStereotype st3 = model.createStereotype("Stereotype3", assoc1);

        assertEquals(Arrays.asList(st1, st2, st3), assoc1.getStereotypes());
        assertEquals(assoc1, st1.getStereotypedElements().get(0));
        assertEquals(assoc1, st2.getStereotypedElements().get(0));
        assertEquals(assoc1, st3.getStereotypedElements().get(0));
    }

    @Test
    public void testCreationOfThreeStereotypesOnExtendedElement() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("1"), mcl2.createEnd("1"));
        CStereotype st1 = model.createStereotype("Stereotype1");
        CStereotype st2 = model.createStereotype("Stereotype2");
        CStereotype st3 = model.createStereotype("Stereotype3");

        assertEquals(Collections.emptyList(), assoc1.getStereotypes());
        assoc1.addStereotype("Stereotype1");
        assertEquals(Collections.singletonList(st1), assoc1.getStereotypes());
        assoc1.addStereotype("Stereotype2");
        assoc1.addStereotype(st3);
        assertEquals(Arrays.asList(st1, st2, st3), assoc1.getStereotypes());
    }

    @Test
    public void testAddRemoveStereotypes() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype st1 = model.createStereotype("Stereotype1");
        CStereotype st2 = model.createStereotype("Stereotype2");
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("1"), mcl2.createEnd("1"));
        CAssociation assoc2 = model.createAssociation(mcl1.createEnd("1"), mcl2.createEnd("1"));
        assertEquals(Collections.emptyList(), assoc1.getStereotypes());
        assertEquals(Collections.emptyList(), assoc2.getStereotypes());
        assertEquals(Collections.emptyList(), st1.getStereotypedElements());
        assertEquals(Collections.emptyList(), st2.getStereotypedElements());

        assoc1.addStereotype(st1);
        assoc1.addStereotype(st2);
        assoc2.addStereotype(st2);

        assertEquals(Arrays.asList(st1, st2), assoc1.getStereotypes());
        assertEquals(Collections.singletonList(st2), assoc2.getStereotypes());
        assertEquals(Collections.singletonList(assoc1), st1.getStereotypedElements());
        assertEquals(Arrays.asList(assoc1, assoc2), st2.getStereotypedElements());

        assoc1.removeStereotype(st1);
        assertEquals(Collections.singletonList(st2), assoc1.getStereotypes());
        assoc1.removeStereotype(st2);
        assertEquals(Collections.emptyList(), assoc1.getStereotypes());

        assertEquals(Collections.singletonList(st2), assoc2.getStereotypes());
        assertEquals(Collections.emptyList(), st1.getStereotypedElements());
        assertEquals(Collections.singletonList(assoc2), st2.getStereotypedElements());
    }

    @Test
    public void testStereotypeAddStereotypeTwice() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype st1 = model.createStereotype("Stereotype1");
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("1"), mcl2.createEnd("1"));
        CAssociation assoc2 = model.createAssociation("named", mcl1.createEnd("1"), mcl2.createEnd("1"));
        assoc1.addStereotype(st1);
        assoc2.addStereotype(st1);

        try {
            assoc1.addStereotype(st1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'Stereotype1' already exists", e.getMessage());
        }

        try {
            assoc2.addStereotype(st1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'Stereotype1' already exists on 'named'", e.getMessage());
        }

    }

    @Test
    public void testStereotypeRemoveNonExisting() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype st1 = model.createStereotype("Stereotype1");
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("1"), mcl2.createEnd("1"));
        CAssociation assoc2 = model.createAssociation("named", mcl1.createEnd("1"), mcl2.createEnd("1"));

        try {
            assoc1.removeStereotype(st1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't remove stereotype 'Stereotype1': does not exist", e.getMessage());
        }

        try {
            assoc2.removeStereotype(st1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't remove stereotype 'Stereotype1' on 'named': does not exist", e.getMessage());
        }
    }


}
