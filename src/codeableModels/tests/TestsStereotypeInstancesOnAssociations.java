package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;


public class TestsStereotypeInstancesOnAssociations {
    @Test
    public void testStereotypeInstancesOnAssociations() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("1"), mcl2.createEnd("1"));
        CStereotype stereotype1 = model.createStereotype("ST1", assoc1);
        CStereotype stereotype2 = model.createStereotype("ST2", assoc1);
        CStereotype stereotype3 = model.createStereotype("ST3", assoc1);
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        CLink link = cl1.setLink(assoc1.getEnds().get(1), cl2);

        assertEquals(0, link.getStereotypeInstances().size());

        link.addStereotypeInstance(stereotype1);
        assertEquals(link.getStereotypeInstances(), Collections.singletonList(stereotype1));
        link.addStereotypeInstance(stereotype2);
        link.addStereotypeInstance("ST3");
        assertEquals(link.getStereotypeInstances(), Arrays.asList(stereotype1, stereotype2, stereotype3));
        try {
            link.addStereotypeInstance(stereotype2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals(
                    "stereotype 'ST2' cannot be added: it is already a stereotype of '[CL1 -> CL2]'",
                    e.getMessage());
        }
        assertEquals(link.getStereotypeInstances(), Arrays.asList(stereotype1, stereotype2, stereotype3));
    }

    @Test
    public void testAddStereotypeWhichDoesNotExist() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("1"), mcl2.createEnd("1"));
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        CLink link = cl1.setLink(assoc1.getEnds().get(1), cl2);
        try {
            link.addStereotypeInstance("Stereotype");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'Stereotype' does not exist", e.getMessage());
        }
    }

    @Test
    public void testAddStereotypeInstance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("*"), mcl2.createEnd("*"));
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        cl1.setLink(assoc1.getEnds().get(1), cl2);
        CStereotype stereotype1 = model.createStereotype("ST1", assoc1);
        CStereotype stereotype2 = model.createStereotype("ST2", assoc1);
        CStereotype stereotype3 = model.createStereotype("ST3", assoc1);
        CStereotype stereotype4 = model.createStereotype("ST4", assoc1);

        assertEquals(0, stereotype1.getStereotypedElementInstances().size());

        CLink link1 = cl1.setLink(assoc1.getEnds().get(1), cl2);
        link1.addStereotypeInstance(stereotype1);
        CLink link2 = cl1.setLink(assoc1.getEnds().get(1), cl2);
        link2.addStereotypeInstance("ST3");
        link2.addStereotypeInstance("ST4");

        CLink link3 = cl1.setLink(assoc1.getEnds().get(1), cl2);
        assertEquals(0, link3.getStereotypeInstances().size());

        link3.addStereotypeInstance("ST2");
        assertEquals(1, link3.getStereotypeInstances().size());
        assertEquals(stereotype2, link3.getStereotypeInstances().get(0));
        assertEquals(1, stereotype2.getStereotypedElementInstances().size());
        assertEquals(link3, stereotype2.getStereotypedElementInstances().get(0));

        assertEquals(1, link1.getStereotypeInstances().size());
        assertEquals(stereotype1, link1.getStereotypeInstances().get(0));

        assertEquals(2, link2.getStereotypeInstances().size());
        assertEquals(Arrays.asList(stereotype3, stereotype4), link2.getStereotypeInstances());

        link3.addStereotypeInstance(stereotype4);
        assertEquals(2, stereotype4.getStereotypedElementInstances().size());
        assertEquals(Arrays.asList(link2, link3), stereotype4.getStereotypedElementInstances());
    }

    @Test
    public void testDeleteStereotypeInstance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("*"), mcl2.createEnd("*"));
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        cl1.setLink(assoc1.getEnds().get(1), cl2);
        CStereotype stereotype1 = model.createStereotype("ST1", assoc1);
        CStereotype stereotype2 = model.createStereotype("ST2", assoc1);
        CStereotype stereotype3 = model.createStereotype("ST3", assoc1);
        CStereotype stereotype4 = model.createStereotype("ST4", assoc1);
        CLink link1 = cl1.setLink(assoc1.getEnds().get(1), cl2);
        link1.addStereotypeInstance(stereotype1);
        CLink link2 = cl1.setLink(assoc1.getEnds().get(1), cl2);
        link2.addStereotypeInstance("ST3");
        link2.addStereotypeInstance("ST4");
        CLink link3 = cl1.setLink(assoc1.getEnds().get(1), cl2);

        try {
            link3.deleteStereotypeInstance(stereotype1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't remove stereotype 'ST1' on '[CL1 -> CL2]': does not exist", e
                    .getMessage());
        }

        try {
            link1.deleteStereotypeInstance(stereotype2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't remove stereotype 'ST2' on '[CL1 -> CL2]': does not exist", e
                    .getMessage());
        }


        link1.deleteStereotypeInstance("ST1");
        assertEquals(0, link1.getStereotypeInstances().size());
        assertEquals(0, stereotype1.getStereotypedElementInstances().size());

        link3.addStereotypeInstance("ST1");
        link3.deleteStereotypeInstance("ST1");
        link3.addStereotypeInstance("ST3");
        link3.addStereotypeInstance("ST4");

        link2.deleteStereotypeInstance("ST4");
        assertEquals(1, link2.getStereotypeInstances().size());
        assertEquals(stereotype3, link2.getStereotypeInstances().get(0));
        assertEquals(1, stereotype4.getStereotypedElementInstances().size());
        assertEquals(Collections.singletonList(link3), stereotype4.getStereotypedElementInstances());
        assertEquals(2, stereotype3.getStereotypedElementInstances().size());
        assertEquals(Arrays.asList(link2, link3), stereotype3.getStereotypedElementInstances());

        link2.deleteStereotypeInstance("ST3");
        assertEquals(0, link2.getStereotypeInstances().size());
        assertEquals(1, stereotype3.getStereotypedElementInstances().size());
        assertEquals(Collections.singletonList(link3), stereotype3.getStereotypedElementInstances());
    }

    @Test
    public void testAddStereotypeInstanceWrongMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("*"), mcl2.createEnd("*"));
        CAssociation assoc2 = model.createAssociation(mcl1.createEnd("*"), mcl2.createEnd("*"));
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        CLink link = cl1.setLink(assoc1.getEnds().get(1), cl2);

        CStereotype stereotype1 = model.createStereotype("ST1", assoc2);
        try {
            link.addStereotypeInstance(stereotype1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'ST1' cannot be added to '[CL1 -> CL2]': no extension by this stereotype found",
                    e.getMessage());
        }
    }


    @Test
    public void testAddStereotypeInstanceAssociationCorrectByInheritanceOfStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("*"), mcl2.createEnd("*"));
        model.createAssociation(mcl1.createEnd("*"), mcl2.createEnd("*"));
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        CLink link = cl1.setLink(assoc1.getEnds().get(1), cl2);

        CStereotype stereotype1 = model.createStereotype("ST1", assoc1);
        CStereotype stereotype2 = model.createStereotype("ST2").addSuperclass("ST1");

        link.addStereotypeInstance("ST2");
        assertEquals(Collections.singletonList(link), stereotype2.getStereotypedElementInstances());
        assertEquals(0, stereotype1.getStereotypedElementInstances().size());
    }
}
