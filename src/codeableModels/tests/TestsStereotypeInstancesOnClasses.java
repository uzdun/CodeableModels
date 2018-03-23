package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;


public class TestsStereotypeInstancesOnClasses {
    @Test
    public void testStereotypeInstancesOnClass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereotype1 = model.createStereotype("ST1", mcl);
        CStereotype stereotype2 = model.createStereotype("ST2", mcl);
        CStereotype stereotype3 = model.createStereotype("ST3", mcl);
        CClass cl = model.createClass("MCL", "CL");
        assertEquals(0, cl.getStereotypeInstances().size());
        cl.addStereotypeInstance(stereotype1);
        assertEquals(cl.getStereotypeInstances(), Collections.singletonList(stereotype1));
        cl.addStereotypeInstance(stereotype2);
        cl.addStereotypeInstance("ST3");
        assertEquals(cl.getStereotypeInstances(), Arrays.asList(stereotype1, stereotype2, stereotype3));
        try {
            cl.addStereotypeInstance(stereotype2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals(
                    "stereotype 'ST2' cannot be added: it is already a stereotype of 'CL'",
                    e.getMessage());
        }
        assertEquals(cl.getStereotypeInstances(), Arrays.asList(stereotype1, stereotype2, stereotype3));
    }

    @Test
    public void testAddStereotypeWhichDoesNotExist() throws CException {
        CModel model = CodeableModels.createModel();
        model.createMetaclass("MCL1");
        try {
            model.createClass("MCL1", "CL2").addStereotypeInstance("Stereotype");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'Stereotype' does not exist", e.getMessage());
        }
    }

    @Test
    public void testAddStereotypeInstance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CStereotype stereotype1 = model.createStereotype("ST1", mcl1);
        CStereotype stereotype2 = model.createStereotype("ST2", mcl1);
        CStereotype stereotype3 = model.createStereotype("ST3", mcl1);
        CStereotype stereotype4 = model.createStereotype("ST4", mcl1);

        assertEquals(0, stereotype1.getStereotypedElementInstances().size());

        CClass cl1 = model.createClass("MCL1", "CL1");
        cl1.addStereotypeInstance(stereotype1);
        CClass cl2 = model.createClass("MCL1", "CL2");
        cl2.addStereotypeInstance("ST3");
        cl2.addStereotypeInstance("ST4");

        CClass cl3 = model.createClass("MCL1", "CL3");
        assertEquals(0, cl3.getStereotypeInstances().size());

        cl3.addStereotypeInstance("ST2");
        assertEquals(1, cl3.getStereotypeInstances().size());
        assertEquals(stereotype2, cl3.getStereotypeInstances().get(0));
        assertEquals(1, stereotype2.getStereotypedElementInstances().size());
        assertEquals(cl3, stereotype2.getStereotypedElementInstances().get(0));

        assertEquals(1, cl1.getStereotypeInstances().size());
        assertEquals(stereotype1, cl1.getStereotypeInstances().get(0));

        assertEquals(2, cl2.getStereotypeInstances().size());
        assertEquals(Arrays.asList(stereotype3, stereotype4), cl2.getStereotypeInstances());

        cl3.addStereotypeInstance(stereotype4);
        assertEquals(2, stereotype4.getStereotypedElementInstances().size());
        assertEquals(Arrays.asList(cl2, cl3), stereotype4.getStereotypedElementInstances());
    }

    @Test
    public void testDeleteStereotypeInstance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CStereotype stereotype1 = model.createStereotype("ST1", mcl1);
        CStereotype stereotype2 = model.createStereotype("ST2", mcl2);
        CStereotype stereotype3 = model.createStereotype("ST3", mcl1);
        CStereotype stereotype4 = model.createStereotype("ST4", mcl1);
        CClass cl1 = model.createClass("MCL1", "CL1");
        cl1.addStereotypeInstance(stereotype1);
        CClass cl2 = model.createClass("MCL1", "CL2");
        cl2.addStereotypeInstance("ST3");
        cl2.addStereotypeInstance("ST4");
        CClass cl3 = model.createClass("MCL1", "CL3");

        try {
            cl3.deleteStereotypeInstance(stereotype1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't remove stereotype 'ST1' on 'CL3': does not exist", e
                    .getMessage());
        }

        try {
            cl1.deleteStereotypeInstance(stereotype2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't remove stereotype 'ST2' on 'CL1': does not exist", e
                    .getMessage());
        }


        cl1.deleteStereotypeInstance("ST1");
        assertEquals(0, cl1.getStereotypeInstances().size());
        assertEquals(0, stereotype1.getStereotypedElementInstances().size());

        cl3.addStereotypeInstance("ST1");
        cl3.deleteStereotypeInstance("ST1");
        cl3.addStereotypeInstance("ST3");
        cl3.addStereotypeInstance("ST4");

        cl2.deleteStereotypeInstance("ST4");
        assertEquals(1, cl2.getStereotypeInstances().size());
        assertEquals(stereotype3, cl2.getStereotypeInstances().get(0));
        assertEquals(1, stereotype4.getStereotypedElementInstances().size());
        assertEquals(Collections.singletonList(cl3), stereotype4.getStereotypedElementInstances());
        assertEquals(2, stereotype3.getStereotypedElementInstances().size());
        assertEquals(Arrays.asList(cl2, cl3), stereotype3.getStereotypedElementInstances());

        cl2.deleteStereotypeInstance("ST3");
        assertEquals(0, cl2.getStereotypeInstances().size());
        assertEquals(1, stereotype3.getStereotypedElementInstances().size());
        assertEquals(Collections.singletonList(cl3), stereotype3.getStereotypedElementInstances());
    }


    @Test
    public void testAddStereotypeInstanceWrongMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CStereotype stereotype1 = model.createStereotype("ST1", mcl2);
        CClass cl = model.createClass("MCL1", "CL");
        try {
            cl.addStereotypeInstance(stereotype1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'ST1' cannot be added to 'CL': no extension by this stereotype found",
                    e.getMessage());
        }
    }

    @Test
    public void testApplyStereotypeInstancesWrongMetaclassInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass stereotypeMetaclass = model.createMetaclass("SM");
        CMetaclass mcl1 = model.createMetaclass("MCL1").addSuperclass(stereotypeMetaclass);
        CMetaclass mcl2 = model.createMetaclass("MCL2").addSuperclass(stereotypeMetaclass);
        CStereotype stereotype1 = model.createStereotype("ST1", mcl1);
        CStereotype stereotype2 = model.createStereotype("ST2", mcl2);
        CStereotype s_stereotype = model.createStereotype("S_ST", stereotypeMetaclass);

        CClass smClass = model.createClass(stereotypeMetaclass, "SMClass");

        try {
            smClass.addStereotypeInstance(stereotype1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'ST1' cannot be added to 'SMClass': no extension by this stereotype found", e.getMessage());
        }
        smClass.addStereotypeInstance(s_stereotype);

        CClass mcl1Class = model.createClass(mcl1, "Mcl1Class");
        mcl1Class.addStereotypeInstance(stereotype1);
        try {
            mcl1Class.addStereotypeInstance(stereotype2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'ST2' cannot be added to 'Mcl1Class': no extension by this stereotype found",
                    e.getMessage());
        }
        mcl1Class.addStereotypeInstance(s_stereotype);

        assertEquals(Collections.singletonList(s_stereotype), smClass.getStereotypeInstances());
        assertEquals(Arrays.asList(stereotype1, s_stereotype), mcl1Class.getStereotypeInstances());
    }

    @Test
    public void testAddStereotypeInstanceMetaclassCorrectByInheritanceOfMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        model.createMetaclass("MCL2").addSuperclass(mcl1);
        CStereotype stereotype1 = model.createStereotype("ST1", mcl1);
        CClass cl = model.createClass("MCL2", "CL");
        cl.addStereotypeInstance("ST1");
        assertEquals(Collections.singletonList(cl), stereotype1.getStereotypedElementInstances());
    }

    @Test
    public void testAddStereotypeInstanceMetaclassWrongInheritanceHierarchy() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2").addSuperclass(mcl1);
        model.createStereotype("ST1", mcl2);
        CClass cl = model.createClass("MCL1", "CL");
        try {
            cl.addStereotypeInstance("ST1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'ST1' cannot be added to 'CL': no extension by this stereotype found", e.getMessage());
        }
    }

    @Test
    public void testAddStereotypeInstanceMetaclassCorrectByInheritanceOfStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CStereotype stereotype1 = model.createStereotype("ST1", mcl2);
        CStereotype stereotype2 = model.createStereotype("ST2").addSuperclass("ST1");
        CClass cl = model.createClass("MCL2", "CL");
        cl.addStereotypeInstance("ST2");
        assertEquals(Collections.singletonList(cl), stereotype2.getStereotypedElementInstances());
        assertEquals(0, stereotype1.getStereotypedElementInstances().size());
    }
}
