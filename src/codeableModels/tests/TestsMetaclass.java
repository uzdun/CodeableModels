package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsMetaclass {

    @Test
    public void testCreationOfOneMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass cl = model.createMetaclass("MClass1");
        CMetaclass cl2 = model.getMetaclass("MClass1");
        assertEquals(cl, cl2);
        assertEquals(model, cl2.getModel());
    }

    @Test
    public void testCreationOfAutoNamedMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass();
        String mclName = mcl.getName();
        assertTrue(mclName.startsWith("##"));
        CMetaclass mcl2 = model.getMetaclass(mclName);
        assertEquals(mcl, mcl2);
    }

    @Test
    public void testCreationOf3Metaclasses() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass cl1 = model.createMetaclass("MClass1");
        CMetaclass cl2 = model.createMetaclass("MClass2");
        CMetaclass cl3 = model.createMetaclass("MClass3");
        CMetaclass gcl1 = model.getMetaclass("MClass1");
        CMetaclass gcl2 = model.getMetaclass("MClass2");
        CMetaclass gcl3 = model.getMetaclass("MClass3");
        assertEquals(cl1, gcl1);
        assertEquals(cl2, gcl2);
        assertEquals(cl3, gcl3);
    }

    @Test
    public void testCCreationOfNoMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass gcl1 = model.getMetaclass("MClass1");
        assertEquals(null, gcl1);
    }

    @Test
    public void testMetaclassUniqueNameUsedException() throws CException {
        CModel model = CodeableModels.createModel();
        model.createMetaclass("MClass1");
        try {
            model.createMetaclass("MClass1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("classifier 'MClass1' cannot be created, classifier name already exists", e.getMessage());
        }
    }

    @Test
    public void testLookupMetaclassLocally() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass cl = model.createMetaclass("MClass1");
        CMetaclass cl2 = model.lookupMetaclass("MClass1");
        assertEquals(cl, cl2);
        CClassifier cl3 = model.lookupClassifier("MClass1");
        assertEquals(cl, cl3);

    }

    @Test
    public void testLookup3MetaclassesLocally() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass cl1 = model.createMetaclass("Metaclass1");
        CMetaclass cl2 = model.createMetaclass("Metaclass2");
        CMetaclass cl3 = model.createMetaclass("Metaclass3");
        CMetaclass gcl1 = model.lookupMetaclass("Metaclass1");
        CMetaclass gcl2 = model.lookupMetaclass("Metaclass2");
        CClassifier gcl3 = model.lookupClassifier("Metaclass3");
        assertEquals(cl1, gcl1);
        assertEquals(cl2, gcl2);
        assertEquals(cl3, gcl3);
    }

    @Test
    public void testLookupMetaclassLocallyThatDoesNotExist() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass gcl1 = model.lookupMetaclass("Metaclass1");
        assertEquals(null, gcl1);
    }

    @Test
    public void testGetMetaclassesAndGetMetaclassNames() throws CException {
        CModel model = CodeableModels.createModel();
        List<CMetaclass> metaclasses = model.getMetaclasses();
        List<String> metaclassNames = model.getMetaclassNames();
        assertEquals(0, metaclasses.size());
        assertEquals(0, metaclassNames.size());

        CMetaclass cl1 = model.createMetaclass("Metaclass1");

        metaclasses = model.getMetaclasses();
        metaclassNames = model.getMetaclassNames();
        assertEquals(1, metaclasses.size());
        assertEquals(1, metaclassNames.size());
        assertEquals("Metaclass1", metaclassNames.get(0));
        assertEquals(cl1, metaclasses.get(0));

        CMetaclass cl2 = model.createMetaclass("Metaclass2");
        CMetaclass cl3 = model.createMetaclass("Metaclass3");

        metaclasses = model.getMetaclasses();
        metaclassNames = model.getMetaclassNames();
        assertEquals(3, metaclasses.size());
        assertEquals(3, metaclassNames.size());
        assertTrue(metaclasses.contains(cl1));
        assertTrue(metaclasses.contains(cl2));
        assertTrue(metaclasses.contains(cl3));
    }

    @Test
    public void testDeleteMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CModel model2 = CodeableModels.createModel();
        CMetaclass mcl = model2.createMetaclass("MCL");
        try {
            model.deleteClassifier(null);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("classifier '' to be deleted does not exist", e.getMessage());
        }
        try {
            model.deleteClassifier(model2.createClass(mcl, "x"));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("classifier 'x' to be deleted does not exist", e.getMessage());
        }
        CMetaclass cl1 = model.createMetaclass("MetaClass1");
        model.deleteClassifier(cl1);

        CMetaclass gcl1 = model.getMetaclass("MetaClass1");
        assertEquals(null, gcl1);
        List<CMetaclass> classes = model.getMetaclasses();
        assertEquals(0, classes.size());

        cl1 = model.createMetaclass("MetaClass1");
        CMetaclass cl2 = model.createMetaclass("MetaClass2");
        CMetaclass cl3 = model.createMetaclass("MetaClass3");

        model.deleteClassifier(cl1);
        try {
            model.deleteClassifier(model2.createClass(mcl, "y"));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("classifier 'y' to be deleted does not exist", e.getMessage());
        }
        model.deleteClassifier(cl3);

        gcl1 = model.getMetaclass("MetaClass1");
        CMetaclass gcl2 = model.getMetaclass("MetaClass2");
        CMetaclass gcl3 = model.getMetaclass("MetaClass3");

        assertEquals(null, gcl1);
        assertEquals(cl2, gcl2);
        assertEquals(null, gcl3);

        classes = model.getMetaclasses();
        assertEquals(1, classes.size());
    }


    @Test
    public void testDeleteMetaclassClassRelation() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("Metaclass1");
        CMetaclass mcl2 = model.createMetaclass("Metaclass2");
        CClass cl1 = model.createClass(mcl1, "C1");
        CClass cl2 = model.createClass(mcl1, "C2");
        CClass cl3 = model.createClass(mcl2, "C3");

        model.deleteClassifier(mcl1);

        assertEquals(0, mcl1.getClassInstances().size());
        assertEquals(null, cl1.getMetaclass());
        assertEquals(null, cl2.getMetaclass());
        assertEquals(mcl2, cl3.getMetaclass());

        List<CClass> classes = mcl2.getClassInstances();
        assertEquals(1, classes.size());
        assertTrue(!classes.contains(cl1));
        assertTrue(!classes.contains(cl2));
        assertTrue(classes.contains(cl3));

        classes = model.getClasses();
        assertEquals(1, classes.size());
        assertEquals(cl3, classes.get(0));
    }


}
