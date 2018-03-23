package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsAssociationsInModel {

    @Test
    public void testAssociationCreationInModelWithoutName() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl1 = model.createClass(mcl, "Class1");
        CClassifier cl2 = model.createClass(mcl, "Class2");
        CClassifier cl3 = model.createClass(mcl, "Class3");
        CClassifier cl4 = model.createClass(mcl, "Class4");

        CAssociation assoc1 = model.createAssociation(cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        CAssociation assoc2 = model.createAssociation(cl1.createEnd("o", "*"), cl2.createEnd("s", "1"));
        CAssociation assoc3 = model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        CAssociation assoc4 = model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("e", "*"));
        CAssociation assoc5 = model.createAggregation(cl4.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        CAssociation assoc6 = model.createAggregation(cl3.createEnd("a", "3", false), cl2.createEnd("e", "*", false));

        List<CAssociation> associations1 = model.getAssociationsByName(null);
        assertEquals(6, associations1.size());

        List<CAssociationEnd> assoc1Ends = assoc1.getEnds();
        assertEquals("i", assoc1Ends.get(0).getRoleName());
        assertEquals("n", assoc5.getEndByClassifier(cl3).getRoleName());
        assertEquals("s", assoc2.getEndByClassifier(cl2).getRoleName());
        assertEquals("1", assoc1Ends.get(1).getMultiplicityString());
        assertEquals("*", assoc1Ends.get(0).getMultiplicityString());
        assertEquals("0..1", assoc4.getEndByRoleName("a").getMultiplicityString());
        assertEquals("3", assoc6.getEndByRoleName("a").getMultiplicityString());
        assertEquals(true, assoc1Ends.get(0).isNavigable());
        assoc1Ends.get(0).setNavigable(false);
        assertEquals(false, assoc1Ends.get(0).isNavigable());
        assertEquals(false, assoc6.getEndByRoleName("a").isNavigable());
        assertEquals(false, assoc6.getEndByRoleName("e").isNavigable());

        assertEquals(false, assoc1.isComposition());
        assertEquals(false, assoc1.isAggregation());
        assertEquals(true, assoc3.isComposition());
        assertEquals(false, assoc3.isAggregation());
        assertEquals(false, assoc5.isComposition());
        assertEquals(true, assoc5.isAggregation());

        assoc1.setAggregation(true);
        assertEquals(false, assoc1.isComposition());
        assertEquals(true, assoc1.isAggregation());
        assoc1.setComposition(true);
        assertEquals(true, assoc1.isComposition());
        assertEquals(false, assoc1.isAggregation());

        assertEquals(assoc1.getModel(), model);
    }

    @Test
    public void testRoleNameGuessing() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl1 = model.createClass(mcl, "Class1");
        CClassifier cl2 = model.createClass(mcl, "Class2");

        CAssociation assoc1 = model.createAssociation(cl1.createEnd("*"), cl2.createEnd("1"));

        assertEquals("class1", assoc1.getEnds().get(0).getRoleName());
        assertEquals("class2", assoc1.getEnds().get(1).getRoleName());
    }

    @Test
    public void testGuessRoleNamesOnEnds() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl1 = model.createClass(mcl, "Decision");
        CClassifier cl2 = model.createClass(mcl, "Model");
        CClassifier cl3 = model.createClass(mcl, "Class3");

        CAssociation assoc1 = model.createAssociation(cl1.createEnd("*"), cl2.createEnd("1"));
        CAssociation assoc2 = model.createAssociation(cl2.createEnd("*"), cl3.createEnd("1"));

        assertEquals("decision", assoc1.getEnds().get(0).getRoleName());
        assertEquals("model", assoc1.getEnds().get(1).getRoleName());
        assertEquals("model", assoc2.getEnds().get(0).getRoleName());
        assertEquals("class3", assoc2.getEnds().get(1).getRoleName());
    }

    @Test
    public void testGetEndMethods() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl2 = model.createClass(mcl, "Class2");
        CClassifier cl1 = model.createClass(mcl, "Class1").addSuperclass(cl2);
        CClassifier cl3 = model.createClass(mcl, "Class3");
        CAssociationEnd endCL1 = cl1.createEnd("cl", "*");
        CAssociationEnd endCL2 = cl2.createEnd("cl", "*");
        CAssociationEnd endCL3 = cl3.createEnd("cl3", "*");
        CAssociation assoc1 = model.createAssociation("CL1-CL2", endCL1, endCL2);
        CAssociation assoc2 = model.createAssociation("CL2-CL1", endCL2, endCL1);
        CAssociation assoc3 = model.createAssociation("CL3-CL1", endCL3, endCL1);

        assertEquals(endCL1, assoc1.getEndByClassifier(cl1));
        assertEquals(endCL2, assoc1.getEndByClassifier(cl2));
        assertEquals(endCL1, assoc1.getEnds().get(0));
        assertEquals(endCL2, assoc1.getEnds().get(1));
        assertEquals(endCL1, assoc1.getEndByRoleName("cl"));
        assertEquals(endCL1, assoc2.getEndByClassifier(cl1));
        assertEquals(endCL2, assoc2.getEndByClassifier(cl2));
        assertEquals(endCL2, assoc2.getEnds().get(0));
        assertEquals(endCL1, assoc2.getEnds().get(1));
        assertEquals(endCL2, assoc2.getEndByRoleName("cl"));
        assertEquals(endCL1, assoc3.getEndByClassifier(cl1));
        assertEquals(endCL1, assoc3.getEndByClassifier(cl2));
        assertEquals(endCL3, assoc3.getEndByClassifier(cl3));
        assertEquals(endCL3, assoc3.getEnds().get(0));
        assertEquals(endCL1, assoc3.getEnds().get(1));
        assertEquals(endCL1, assoc3.getEndByRoleName("cl"));
        assertEquals(endCL3, assoc3.getEndByRoleName("cl3"));

        assertEquals(endCL1, assoc1.getOtherEnd(endCL2));
        assertEquals(endCL2, assoc1.getOtherEnd(endCL1));
        assertEquals(endCL1, assoc2.getOtherEnd(endCL2));
        assertEquals(endCL2, assoc2.getOtherEnd(endCL1));
        assertEquals(endCL1, assoc3.getOtherEnd(endCL3));
        assertEquals(endCL3, assoc3.getOtherEnd(endCL1));

        assertEquals(null, assoc3.getEndByRoleName("x"));
        assertEquals(null, assoc1.getEndByClassifier(cl3));

        try {
            assertEquals(endCL1, assoc1.getOtherEnd(endCL3));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end unknown in association: 'cl3'", e.getMessage());
        }
    }


    @Test
    public void testAssociationCreationInModelWithName() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl1 = model.createClass(mcl, "Class1");
        CClassifier cl2 = model.createClass(mcl, "Class2");
        CClassifier cl3 = model.createClass(mcl, "Class3");
        CClassifier cl4 = model.createClass(mcl, "Class4");

        CAssociation assoc1 = model.createAssociation("a", cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        CAssociation assoc2 = model.createAssociation("b", cl1.createEnd("o", "*"), cl2.createEnd("s", "1"));
        CAssociation assoc3 = model.createComposition("c", cl1.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        CAssociation assoc4 = model.createComposition("d", cl1.createEnd("a", "0..1"), cl3.createEnd("e", "*"));
        CAssociation assoc5 = model.createAggregation("e", cl4.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        CAssociation assoc6 = model.createAggregation("f", cl3.createEnd("a", "3"), cl2.createEnd("e", "*"));

        List<CAssociation> associations1 = model.getAssociationsByName("a");
        assertEquals(associations1.size(), 1);
        List<CAssociation> associations2 = model.getAssociationsByName("f");
        assertEquals(1, associations2.size());
        List<CAssociation> associations3 = model.getAssociationsByName("x");
        assertEquals(0, associations3.size());
        List<CAssociation> associations4 = model.getAssociationsByName(null);
        assertEquals(0, associations4.size());

        assertEquals(assoc1, associations1.get(0));
        assertEquals(assoc6, associations2.get(0));

        List<CAssociationEnd> assoc1Ends = assoc1.getEnds();
        assertEquals("i", assoc1Ends.get(0).getRoleName());
        assertEquals("n", assoc5.getEndByClassifier(cl3).getRoleName());
        assertEquals("s", assoc2.getEndByClassifier(cl2).getRoleName());
        assertEquals("1", assoc1Ends.get(1).getMultiplicityString());
        assertEquals("*", assoc1Ends.get(0).getMultiplicityString());
        assertEquals("0..1", assoc4.getEndByRoleName("a").getMultiplicityString());
        assertEquals("3", assoc6.getEndByRoleName("a").getMultiplicityString());
        assertEquals(true, assoc1Ends.get(0).isNavigable());
        assoc1Ends.get(0).setNavigable(false);
        assertEquals(false, assoc1Ends.get(0).isNavigable());

        assertEquals(false, assoc1.isComposition());
        assertEquals(false, assoc1.isAggregation());
        assertEquals(true, assoc3.isComposition());
        assertEquals(false, assoc3.isAggregation());
        assertEquals(false, assoc5.isComposition());
        assertEquals(true, assoc5.isAggregation());

        assoc1.setAggregation(true);
        assertEquals(false, assoc1.isComposition());
        assertEquals(true, assoc1.isAggregation());
        assoc1.setComposition(true);
        assertEquals(true, assoc1.isComposition());
        assertEquals(false, assoc1.isAggregation());

        assertEquals(assoc1.getModel(), model);
    }

    @Test
    public void testGetAssociations() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl1 = model.createClass(mcl, "Class1");
        CClassifier cl2 = model.createClass(mcl, "Class2");
        CClassifier cl3 = model.createClass(mcl, "Class3");
        CClassifier cl4 = model.createClass(mcl, "Class4");

        CAssociation assoc1 = model.createAssociation(cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        CAssociation assoc2 = model.createAssociation(cl1.createEnd("o", "*"), cl2.createEnd("s", "1"));
        CAssociation assoc3 = model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        CAssociation assoc4 = model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("e", "*"));
        CAssociation assoc5 = model.createAggregation(cl4.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        CAssociation assoc6 = model.createAggregation(cl3.createEnd("a", "3"), cl2.createEnd("e", "*"));
        List<CAssociation> associations = model.getAssociations();

        assertTrue(associations.contains(assoc1));
        assertTrue(associations.contains(assoc2));
        assertTrue(associations.contains(assoc3));
        assertTrue(associations.contains(assoc4));
        assertTrue(associations.contains(assoc5));
        assertTrue(associations.contains(assoc6));
        assertEquals(assoc1.getModel(), model);

        CModel model2 = CodeableModels.createModel();
        CAssociation assoc7 = model2.createAssociation(cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        assertTrue(!associations.contains(assoc7));
        assertEquals(assoc7.getModel(), model2);
    }

    @Test
    public void testGetAssociationsEmptyModel() throws CException {
        CModel model = CodeableModels.createModel();
        List<CAssociation> associations = model.getAssociations();
        assertEquals(0, associations.size());
    }

    @Test
    public void testDeleteAssociations() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl1 = model.createClass(mcl, "Class1");
        CClassifier cl2 = model.createClass(mcl, "Class2");
        CClassifier cl3 = model.createClass(mcl, "Class3");
        CClassifier cl4 = model.createClass(mcl, "Class4");

        model.createAssociation("a", cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        CAssociation assoc2 = model.createAssociation("b", cl1.createEnd("o", "*"), cl2.createEnd("s", "1"));
        model.createComposition("c", cl1.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        CAssociation assoc4 = model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("e", "*"));
        model.createAggregation(cl4.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        model.createAggregation(cl3.createEnd("a", "3"), cl2.createEnd("e", "*"));

        List<CAssociation> associations = model.getAssociations();
        assertEquals(6, associations.size());
        List<CAssociation> associations4 = model.getAssociationsByName(null);
        assertEquals(3, associations4.size());

        model.deleteAssociation(assoc2);
        model.deleteAssociation(assoc4);

        associations = model.getAssociations();
        assertEquals(4, associations.size());

        assertEquals(null, assoc2.getModel());

        List<CAssociation> associations1 = model.getAssociationsByName("a");
        assertEquals(1, associations1.size());
        List<CAssociation> associations2 = model.getAssociationsByName("b");
        assertEquals(0, associations2.size());
        List<CAssociation> associations3 = model.getAssociationsByName("c");
        assertEquals(1, associations3.size());
        associations4 = model.getAssociationsByName(null);
        assertEquals(2, associations4.size());
    }

    private int countContains(List<?> list, Object o) {
        int count = 0;
        for (Object l : list) {
            if (l == o)
                count++;
        }
        return count;
    }


    @Test
    public void testGetAssociationsFromClass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl1 = model.createClass(mcl, "Class1");
        CClassifier cl2 = model.createClass(mcl, "Class2");
        CClassifier cl3 = model.createClass(mcl, "Class3");
        CClassifier cl4 = model.createClass(mcl, "Class4");
        CClassifier cl5 = model.createClass(mcl, "Class5");


        CAssociation assoc1 = model.createAssociation(cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        CAssociation assoc2 = model.createAssociation(cl1.createEnd("o", "*"), cl2.createEnd("s", "1"));
        CAssociation assoc3 = model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        CAssociation assoc4 = model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("e", "*"));
        CAssociation assoc5 = model.createComposition(cl1.createEnd("a", "0..1"), cl1.createEnd("e", "*"));
        model.createAggregation(cl4.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        model.createAggregation(cl3.createEnd("a", "3"), cl2.createEnd("e", "*"));

        List<CAssociation> associations1 = cl1.getAssociations();
        List<CAssociation> associations2 = cl2.getAssociations();
        List<CAssociation> associations3 = cl3.getAssociations();
        List<CAssociation> associations4 = cl4.getAssociations();
        List<CAssociation> associations5 = cl5.getAssociations();

        assertEquals(6, associations1.size());
        assertEquals(3, associations2.size());
        assertEquals(4, associations3.size());
        assertEquals(1, associations4.size());
        assertEquals(0, associations5.size());

        assertTrue(associations1.contains(assoc1));
        assertTrue(associations1.contains(assoc2));
        assertTrue(associations1.contains(assoc3));
        assertTrue(associations1.contains(assoc4));
        // a self referencing associations should be twice in the class' assoc list
        assertEquals(2, countContains(associations1, assoc5));
    }

    @Test
    public void testGetAssociationsFromClassDeleteAssociations() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl1 = model.createClass(mcl, "Class1");
        CClassifier cl2 = model.createClass(mcl, "Class2");
        CClassifier cl3 = model.createClass(mcl, "Class3");
        CClassifier cl4 = model.createClass(mcl, "Class4");
        CClassifier cl5 = model.createClass(mcl, "Class5");

        CAssociation assoc1 = model.createAssociation(cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        CAssociation assoc2 = model.createAssociation(cl1.createEnd("o", "*"), cl2.createEnd("s", "1"));
        CAssociation assoc3 = model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        CAssociation assoc4 = model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("e", "*"));
        CAssociation assoc5 = model.createComposition(cl1.createEnd("a", "0..1"), cl1.createEnd("e", "*"));
        model.createAggregation(cl4.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        model.createAggregation(cl3.createEnd("a", "3"), cl2.createEnd("e", "*"));

        model.deleteAssociation(assoc1);
        model.deleteAssociation(assoc3);
        model.deleteAssociation(assoc5);

        List<CAssociation> associations1 = cl1.getAssociations();
        List<CAssociation> associations2 = cl2.getAssociations();
        List<CAssociation> associations3 = cl3.getAssociations();
        List<CAssociation> associations4 = cl4.getAssociations();
        List<CAssociation> associations5 = cl5.getAssociations();

        assertEquals(2, associations1.size());
        assertEquals(2, associations2.size());
        assertEquals(3, associations3.size());
        assertEquals(1, associations4.size());
        assertEquals(0, associations5.size());

        assertTrue(!associations1.contains(assoc1));
        assertTrue(associations1.contains(assoc2));
        assertTrue(!associations1.contains(assoc3));
        assertTrue(associations1.contains(assoc4));
        assertTrue(!associations1.contains(assoc5));
    }

    @Test
    public void testDeleteClassGetAssociations() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl1 = model.createClass(mcl, "Class1");
        CClassifier cl2 = model.createClass(mcl, "Class2");
        CClassifier cl3 = model.createClass(mcl, "Class3");
        CClassifier cl4 = model.createClass(mcl, "Class4");
        CClassifier cl5 = model.createClass(mcl, "Class5");


        CAssociation assoc1 = model.createAssociation(cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        CAssociation assoc2 = model.createAssociation(cl1.createEnd("o", "*"), cl2.createEnd("s", "1"));
        CAssociation assoc3 = model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        CAssociation assoc4 = model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("e", "*"));
        CAssociation assoc5 = model.createComposition(cl1.createEnd("a", "0..1"), cl1.createEnd("e", "*"));
        CAssociation assoc6 = model.createAggregation(cl4.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        CAssociation assoc7 = model.createAggregation(cl3.createEnd("a", "3"), cl2.createEnd("e", "*"));

        model.deleteClassifier(cl1);

        List<CAssociation> associations1 = cl1.getAssociations();
        List<CAssociation> associations2 = cl2.getAssociations();
        List<CAssociation> associations3 = cl3.getAssociations();
        List<CAssociation> associations4 = cl4.getAssociations();
        List<CAssociation> associations5 = cl5.getAssociations();

        assertEquals(0, associations1.size());
        assertEquals(1, associations2.size());
        assertEquals(2, associations3.size());
        assertEquals(1, associations4.size());
        assertEquals(0, associations5.size());

        List<CAssociation> associationsM = model.getAssociations();
        assertEquals(2, associationsM.size());

        assertTrue(!associationsM.contains(assoc1));
        assertTrue(!associationsM.contains(assoc2));
        assertTrue(!associationsM.contains(assoc3));
        assertTrue(!associationsM.contains(assoc4));
        assertTrue(!associationsM.contains(assoc5));
        assertTrue(associationsM.contains(assoc6));
        assertTrue(associationsM.contains(assoc7));
    }


    @Test
    public void testCreateAndDeleteAssociationsMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CClassifier mcl1 = model.createMetaclass("MClass1");
        CClassifier mcl2 = model.createMetaclass("MClass2");
        CClassifier mcl3 = model.createMetaclass("MClass3");
        CClassifier mcl4 = model.createMetaclass("MClass4");
        CClassifier mcl5 = model.createMetaclass("MClass5");


        CAssociation assoc1 = model.createAssociation(mcl1.createEnd("i", "*"), mcl2.createEnd("t", "1"));
        CAssociation assoc2 = model.createAssociation(mcl1.createEnd("o", "*"), mcl2.createEnd("s", "1"));
        CAssociation assoc3 = model.createComposition(mcl1.createEnd("a", "0..1"), mcl3.createEnd("n", "*"));
        CAssociation assoc4 = model.createComposition(mcl1.createEnd("a", "0..1"), mcl3.createEnd("e", "*"));
        CAssociation assoc5 = model.createComposition(mcl1.createEnd("a", "0..1"), mcl1.createEnd("e", "*"));
        CAssociation assoc6 = model.createAggregation(mcl4.createEnd("a", "0..1"), mcl3.createEnd("n", "*"));
        CAssociation assoc7 = model.createAggregation(mcl3.createEnd("a", "3"), mcl2.createEnd("e", "*"));

        model.deleteClassifier(mcl1);

        List<CAssociation> associations1 = mcl1.getAssociations();
        List<CAssociation> associations2 = mcl2.getAssociations();
        List<CAssociation> associations3 = mcl3.getAssociations();
        List<CAssociation> associations4 = mcl4.getAssociations();
        List<CAssociation> associations5 = mcl5.getAssociations();

        assertEquals(0, associations1.size());
        assertEquals(1, associations2.size());
        assertEquals(2, associations3.size());
        assertEquals(1, associations4.size());
        assertEquals(0, associations5.size());

        List<CAssociation> associationsM = model.getAssociations();
        assertEquals(2, associationsM.size());

        assertTrue(!associationsM.contains(assoc1));
        assertTrue(!associationsM.contains(assoc2));
        assertTrue(!associationsM.contains(assoc3));
        assertTrue(!associationsM.contains(assoc4));
        assertTrue(!associationsM.contains(assoc5));
        assertTrue(associationsM.contains(assoc6));
        assertTrue(associationsM.contains(assoc7));
    }

    @Test
    public void testCreateAndDeleteAssociationsStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CClassifier stereotype1 = model.createStereotype("Stereotype1");
        CClassifier stereotype2 = model.createStereotype("Stereotype2");
        CClassifier stereotype3 = model.createStereotype("Stereotype3");
        CClassifier stereotype4 = model.createStereotype("Stereotype4");
        CClassifier stereotype5 = model.createStereotype("Stereotype5");


        CAssociation assoc1 = model.createAssociation(stereotype1.createEnd("i", "*"), stereotype2.createEnd("t", "1"));
        CAssociation assoc2 = model.createAssociation(stereotype1.createEnd("o", "*"), stereotype2.createEnd("s", "1"));
        CAssociation assoc3 = model.createComposition(stereotype1.createEnd("a", "0..1"), stereotype3.createEnd("n", "*"));
        CAssociation assoc4 = model.createComposition(stereotype1.createEnd("a", "0..1"), stereotype3.createEnd("e", "*"));
        CAssociation assoc5 = model.createComposition(stereotype1.createEnd("a", "0..1"), stereotype1.createEnd("e", "*"));
        CAssociation assoc6 = model.createAggregation(stereotype4.createEnd("a", "0..1"), stereotype3.createEnd("n", "*"));
        CAssociation assoc7 = model.createAggregation(stereotype3.createEnd("a", "3"), stereotype2.createEnd("e", "*"));

        model.deleteClassifier(stereotype1);

        List<CAssociation> associations1 = stereotype1.getAssociations();
        List<CAssociation> associations2 = stereotype2.getAssociations();
        List<CAssociation> associations3 = stereotype3.getAssociations();
        List<CAssociation> associations4 = stereotype4.getAssociations();
        List<CAssociation> associations5 = stereotype5.getAssociations();

        assertEquals(0, associations1.size());
        assertEquals(1, associations2.size());
        assertEquals(2, associations3.size());
        assertEquals(1, associations4.size());
        assertEquals(0, associations5.size());

        List<CAssociation> associationsM = model.getAssociations();
        assertEquals(2, associationsM.size());

        assertTrue(!associationsM.contains(assoc1));
        assertTrue(!associationsM.contains(assoc2));
        assertTrue(!associationsM.contains(assoc3));
        assertTrue(!associationsM.contains(assoc4));
        assertTrue(!associationsM.contains(assoc5));
        assertTrue(associationsM.contains(assoc6));
        assertTrue(associationsM.contains(assoc7));
    }


    @Test
    public void testAssociationEndGetMultiplicity() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl1 = model.createClass(mcl, "Class1");
        CClassifier cl2 = model.createClass(mcl, "Class2");
        CAssociation assoc1 = model.createAssociation(cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));

        assertEquals(0, assoc1.getEndByClassifier(cl1).getMultiplicity().getLowerMultiplicity());
        assertEquals(1, assoc1.getEndByClassifier(cl2).getMultiplicity().getLowerMultiplicity());
        assertEquals(CMultiplicity.STAR_MULTIPLICITY, assoc1.getEndByClassifier(cl1).getMultiplicity().getUpperMultiplicity());
        assertEquals(1, assoc1.getEndByClassifier(cl2).getMultiplicity().getUpperMultiplicity());
    }

    @Test
    public void testGetAssociationByRoleName() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl3 = model.createClass(mcl, "Class3");

        CAssociation assoc1 = model.createAssociation("x", cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        model.createAssociation("y", cl1.createEnd("o", "*"), cl2.createEnd("s", "1"));
        model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("e", "*"));

        assertEquals(assoc1, cl1.getAssociationByRoleName("t"));
        assertEquals(null, cl1.getAssociationByRoleName("i"));
    }

    @Test
    public void testGetAssociationByName() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl3 = model.createClass(mcl, "Class3");

        CAssociation assoc1 = model.createAssociation("x", cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        model.createAssociation("y", cl1.createEnd("o", "*"), cl2.createEnd("s", "1"));
        model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("n", "*"));
        model.createComposition(cl1.createEnd("a", "0..1"), cl3.createEnd("e", "*"));

        assertEquals(assoc1, cl1.getAssociationByName("x"));
        assertEquals(null, cl1.getAssociationByName("z"));
    }

    @Test
    public void testGetClassifierAssociationByRoleName() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl1Sub = model.createClass(mcl, "Class1Sub").addSuperclass(cl1);

        CAssociation assoc1 = model.createAssociation("x", cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        CObject obj1 = model.createObject(cl1);
        CObject obj1Sub = model.createObject(cl1Sub);

        assertEquals(assoc1, obj1.getClassifier().getAssociationByRoleName("t"));
        assertEquals(null, obj1.getClassifier().getAssociationByRoleName("i"));
        assertEquals(assoc1, obj1Sub.getClassifier().getAssociationByRoleName("t"));
        assertEquals(null, obj1Sub.getClassifier().getAssociationByRoleName("i"));
    }

    @Test
    public void testGetClassifierAssociationByName() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl1Sub = model.createClass(mcl, "Class1Sub").addSuperclass(cl1);

        CAssociation assoc1 = model.createAssociation("x", cl1.createEnd("i", "*"), cl2.createEnd("t", "1"));
        CObject obj1 = model.createObject(cl1);
        CObject obj1Sub = model.createObject(cl1Sub);

        assertEquals(assoc1, obj1.getClassifier().getAssociationByName("x"));
        assertEquals(null, obj1.getClassifier().getAssociationByName("z"));
        assertEquals(assoc1, obj1Sub.getClassifier().getAssociationByName("x"));
        assertEquals(null, obj1Sub.getClassifier().getAssociationByName("z"));
    }


}
