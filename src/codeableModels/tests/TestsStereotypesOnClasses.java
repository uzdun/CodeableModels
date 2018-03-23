package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;


public class TestsStereotypesOnClasses {

    @Test
    public void testCreationOfOneStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype st = model.createStereotype("Stereotype1");
        CClassifier st2 = model.getClassifier("Stereotype1");
        assertEquals(st, st2);
        assertEquals(model, st2.getModel());
    }

    @Test
    public void testCreationOfAutoNamedStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype st = model.createStereotype();
        String stName = st.getName();
        assertTrue(stName.startsWith("##"));
        CStereotype st2 = model.getStereotype(stName);
        assertEquals(st, st2);
    }

    @Test
    public void testCreationOf3Stereotypes() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype st1 = model.createStereotype("Stereotype1");
        CStereotype st2 = model.createStereotype("Stereotype2");
        CStereotype st3 = model.createStereotype("Stereotype3");
        CStereotype gst1 = model.getStereotype("Stereotype1");
        CStereotype gst2 = model.getStereotype("Stereotype2");
        CStereotype gst3 = model.getStereotype("Stereotype3");
        assertEquals(st1, gst1);
        assertEquals(st2, gst2);
        assertEquals(st3, gst3);
    }

    @Test
    public void testCreationOfOneStereotypeWithMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype st = model.createStereotype("Stereotype1", mcl);
        CClassifier st2 = model.getClassifier("Stereotype1");
        assertEquals(st, st2);
        assertEquals(model, st2.getModel());
    }

    @Test
    public void testCreationOf3StereotypesWithoutMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        model.createMetaclass("MCL");
        CStereotype st1 = model.createStereotype("Stereotype1", "MCL");
        CStereotype st2 = model.createStereotype("Stereotype2", "MCL");
        CStereotype st3 = model.createStereotype("Stereotype3", "MCL");
        CStereotype gst1 = model.getStereotype("Stereotype1");
        CStereotype gst2 = model.getStereotype("Stereotype2");
        CStereotype gst3 = model.getStereotype("Stereotype3");
        assertEquals(st1, gst1);
        assertEquals(st2, gst2);
        assertEquals(st3, gst3);
    }

    @Test
    public void testStereotypeUniqueNameUsedException() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        model.createStereotype("Stereotype1", mcl);
        try {
            model.createStereotype("Stereotype1", mcl);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("classifier 'Stereotype1' cannot be created, classifier name already exists", e.getMessage());
        }
    }

    @Test
    public void testStereotypeExtensionAddRemove() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype st = model.createStereotype("Stereotype1");
        assertEquals(0, st.getStereotypedElements().size());
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        mcl1.addStereotype("Stereotype1");
        assertEquals(mcl1, st.getStereotypedElements().get(0));
        assertEquals(st, mcl1.getStereotypes().get(0));
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        mcl1.removeStereotype("Stereotype1");
        mcl1.addStereotype(st);
        mcl2.addStereotype(st);
        assertEquals(Arrays.asList(mcl1, mcl2), st.getStereotypedElements());
        assertEquals(st, mcl2.getStereotypes().get(0));
        CStereotype st2 = model.createStereotype("Stereotype2", mcl1);
        assertEquals(mcl1, st2.getStereotypedElements().get(0));
        assertEquals(Arrays.asList(st, st2), mcl1.getStereotypes());

        mcl1.removeStereotype(st);
        assertEquals(mcl2, st.getStereotypedElements().get(0));
        assertEquals(mcl1, st2.getStereotypedElements().get(0));
        assertEquals(st2, mcl1.getStereotypes().get(0));

        mcl1.removeStereotype("Stereotype2");
        assertEquals(mcl2, st.getStereotypedElements().get(0));
        assertEquals(0, st2.getStereotypedElements().size());
        assertEquals(0, mcl1.getStereotypes().size());
    }

    @Test
    public void testStereotypeAddStereotypeTwice() throws CException {
        CModel model = CodeableModels.createModel();

        CMetaclass mcl1 = model.createMetaclass("MCL1");
        model.createStereotype("Stereotype1");
        mcl1.addStereotype("Stereotype1");

        try {
            mcl1.addStereotype("Stereotype1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'Stereotype1' already exists on 'MCL1'", e.getMessage());
        }
    }

    @Test
    public void testStereotypeRemoveNonExisting() throws CException {
        CModel model = CodeableModels.createModel();

        CMetaclass mcl1 = model.createMetaclass("MCL1");
        model.createStereotype("Stereotype1");

        try {
            mcl1.removeStereotype("Stereotype1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't remove stereotype 'Stereotype1' on 'MCL1': does not exist", e.getMessage());
        }
    }


    @Test
    public void testStereotypeExtensionExceptions() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        model.createClass(mcl1, "CL1");
        model.createStereotype("S1", mcl1);

        try {
            model.createStereotype("S1", "CL1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("'CL1' is not a metaclass", e.getMessage());
        }

        try {
            model.createStereotype("Stereotype1", "S1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("'S1' is not a metaclass", e.getMessage());
        }
        try {
            model.createStereotype("Stereotype2", "CL1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("'CL1' is not a metaclass", e.getMessage());
        }
    }

    @Test
    public void testAddRemoveStereotypes() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype st1 = model.createStereotype("Stereotype1");
        CStereotype st2 = model.createStereotype("Stereotype2");
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        assertEquals(Collections.emptyList(), mcl1.getStereotypes());
        mcl1.addStereotype(st1);
        assertEquals(Collections.singletonList(st1), mcl1.getStereotypes());
        mcl1.addStereotype(st2);
        assertEquals(Arrays.asList(st1, st2), mcl1.getStereotypes());
        mcl1.removeStereotype(st1);
        assertEquals(Collections.singletonList(st2), mcl1.getStereotypes());
        mcl1.removeStereotype(st2);
        assertEquals(Collections.emptyList(), mcl1.getStereotypes());
    }

    @Test
    public void testStereotypeExtensionsOfMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        List<CStereotype> result = mcl1.getStereotypes();
        assertEquals(0, result.size());

        CStereotype st1 = model.createStereotype("Stereotype1", mcl1);
        result = mcl1.getStereotypes();
        assertEquals(1, result.size());
        assertEquals(st1, result.get(0));

        CStereotype st2 = model.createStereotype("Stereotype2", mcl1);
        CStereotype st3 = model.createStereotype("Stereotype3", mcl1);
        result = mcl1.getStereotypes();
        assertEquals(Arrays.asList(st1, st2, st3), result);

        CStereotype st4 = model.createStereotype("Stereotype4", mcl1);
        model.deleteClassifier(st2);
        result = mcl1.getStereotypes();
        assertEquals(Arrays.asList(st1, st3, st4), result);
        assertEquals(mcl1, st1.getStereotypedElements().get(0));
        assertEquals(0, st2.getStereotypedElements().size());

        model.deleteClassifier(mcl1);
        result = mcl1.getStereotypes();
        assertEquals(Collections.emptyList(), result);
        assertEquals(0, st1.getStereotypedElements().size());
    }

    @Test
    public void testLookupStereotypeLocally() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype st = model.createStereotype("Stereotype1");
        CClassifier st2 = model.lookupClassifier("Stereotype1");
        assertEquals(st, st2);
    }

    @Test
    public void testLookup3StereotypesLocally() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype st1 = model.createStereotype("Stereotype1");
        CStereotype st2 = model.createStereotype("Stereotype2");
        CStereotype st3 = model.createStereotype("Stereotype3");
        CClassifier gst1 = model.lookupClassifier("Stereotype1");
        CClassifier gst2 = model.lookupClassifier("Stereotype2");
        CStereotype gst3 = model.lookupStereotype("Stereotype3");
        assertEquals(st1, gst1);
        assertEquals(st2, gst2);
        assertEquals(st3, gst3);
    }

    @Test
    public void testGetStereotypesAndGetStereotypeNames() throws CException {
        CModel model = CodeableModels.createModel();
        List<CStereotype> stereotypes = model.getStereotypes();
        List<String> stereotypeNames = model.getStereotypeNames();
        assertEquals(0, stereotypes.size());
        assertEquals(0, stereotypeNames.size());

        CStereotype cl1 = model.createStereotype("S1");

        stereotypes = model.getStereotypes();
        stereotypeNames = model.getStereotypeNames();
        assertEquals(1, stereotypes.size());
        assertEquals(1, stereotypeNames.size());
        assertEquals("S1", stereotypeNames.get(0));
        assertEquals(cl1, stereotypes.get(0));

        CStereotype cl2 = model.createStereotype("S2");
        CStereotype cl3 = model.createStereotype("S3");
        model.createMetaclass("MCL");
        model.createClass("MCL", "Stereotype2");
        model.createClass("MCL", "Stereotype3");

        stereotypes = model.getStereotypes();
        stereotypeNames = model.getStereotypeNames();
        assertEquals(3, stereotypes.size());
        assertEquals(3, stereotypeNames.size());
        assertTrue(stereotypes.contains(cl1));
        assertTrue(stereotypes.contains(cl2));
        assertTrue(stereotypes.contains(cl3));
    }


    @Test
    public void testStereotypeSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("A");
        CClassifier cl2 = model.createStereotype("AType", mcl1);
        CClassifier cl3 = model.createStereotype("B");
        CClassifier cl4 = model.createClass("A", "X");
        try {
            cl3.addSuperclass("A");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals(
                    "cannot add superclass 'A' to 'B': not a stereotype",
                    e.getMessage());
        }
        try {
            cl3.addSuperclass(cl4);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals(
                    "cannot add superclass 'X' to 'B': not a stereotype",
                    e.getMessage());
        }
        cl3.addSuperclass(cl2);
        List<CClassifier> scs = cl3.getSuperclasses();
        assertEquals(1, scs.size());
        assertTrue(scs.contains(cl2));
    }

    @Test
    public void testChangingExtendedMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CStereotype stereotype1 = model.createStereotype("ST1", mcl2);
        assertEquals(mcl2, stereotype1.getStereotypedElements().get(0));
        assertEquals(Collections.emptyList(), mcl1.getStereotypes());
        assertEquals(Collections.singletonList(stereotype1), mcl2.getStereotypes());
        mcl1.addStereotype(stereotype1);
        mcl2.removeStereotype(stereotype1);
        assertEquals(mcl1, stereotype1.getStereotypedElements().get(0));
        assertEquals(Collections.singletonList(stereotype1), mcl1.getStereotypes());
        assertEquals(Collections.emptyList(), mcl2.getStereotypes());

        mcl1.removeStereotype(stereotype1);
        assertEquals(0, stereotype1.getStereotypedElements().size());
        assertEquals(Collections.emptyList(), mcl1.getStereotypes());
        assertEquals(Collections.emptyList(), mcl2.getStereotypes());

        mcl1.addStereotype(stereotype1);
        assertEquals(mcl1, stereotype1.getStereotypedElements().get(0));
        assertEquals(Collections.singletonList(stereotype1), mcl1.getStereotypes());
        assertEquals(Collections.emptyList(), mcl2.getStereotypes());
    }
}
