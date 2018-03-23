package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsClass {

    @Test
    public void testCreationOfOneClass() throws CException {
        CModel model = CodeableModels.createModel();
        model.createMetaclass("MCL");
        CClass cl = model.createClass("MCL", "Class1");
        CClass cl2 = model.getClass("Class1");
        assertEquals(cl, cl2);
        assertEquals(model, cl2.getModel());
    }

    @Test
    public void testCreationOfAutoNamedClass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass("MCL");
        CClass cl2 = model.createClass(mcl);
        String cl1Name = cl1.getName(), cl2Name = cl2.getName();
        assertTrue(cl1Name.startsWith("##"));
        assertTrue(cl2Name.startsWith("##"));
        CObject cl3 = model.getClass(cl1Name);
        CObject cl4 = model.getClass(cl2Name);
        assertEquals(cl1, cl3);
        assertEquals(cl2, cl4);
        assertEquals(mcl, cl3.getClassifier());
        assertEquals(mcl, cl4.getClassifier());
    }

    @Test
    public void testCreationOf3Classes() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl3 = model.createClass(mcl, "Class3");
        CClass gcl1 = model.getClass("Class1");
        CClass gcl2 = model.getClass("Class2");
        CClass gcl3 = model.getClass("Class3");
        assertEquals(cl1, gcl1);
        assertEquals(cl2, gcl2);
        assertEquals(cl3, gcl3);
    }

    @Test
    public void testCCreationOfNoClass() throws CException {
        CModel model = CodeableModels.createModel();
        CClass gcl1 = model.getClass("Class1");
        assertEquals(null, gcl1);
    }

    @Test
    public void testClassUniqueNameUsedException() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        model.createClass(mcl, "Class1");
        try {
            model.createClass(mcl, "Class1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("classifier 'Class1' cannot be created, classifier name already exists", e.getMessage());
        }
    }

    @Test
    public void testLookupClassifierLocally() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl = model.createClass(mcl, "Class1");
        CClass cl2 = model.lookupClass("Class1");
        assertEquals(cl, cl2);
    }

    @Test
    public void testLookup3ClassesLocally() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl3 = model.createClass(mcl, "Class3");
        CClass gcl1 = model.lookupClass("Class1");
        CClass gcl2 = model.lookupClass("Class2");
        CClass gcl3 = model.lookupClass("Class3");
        assertEquals(cl1, gcl1);
        assertEquals(cl2, gcl2);
        assertEquals(cl3, gcl3);
    }

    @Test
    public void testLookupClassifierLocallyThatDoesNotExist() throws CException {
        CModel model = CodeableModels.createModel();
        CClass gcl1 = model.lookupClass("Class1");
        assertEquals(null, gcl1);
    }

    @Test
    public void testGetClassesAndGetClassNames() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        List<CClass> classes = model.getClasses();
        List<String> classNames = model.getClassNames();
        assertEquals(0, classes.size());
        assertEquals(0, classNames.size());

        CClass cl1 = model.createClass(mcl, "Class1");

        classes = model.getClasses();
        classNames = model.getClassNames();
        assertEquals(1, classes.size());
        assertEquals(1, classNames.size());
        assertEquals("Class1", classNames.get(0));
        assertEquals(cl1, classes.get(0));

        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl3 = model.createClass(mcl, "Class3");

        classes = model.getClasses();
        classNames = model.getClassNames();
        assertEquals(3, classes.size());
        assertEquals(3, classNames.size());
        assertTrue(classes.contains(cl1));
        assertTrue(classes.contains(cl2));
        assertTrue(classes.contains(cl3));
    }

    @Test
    public void testDeleteClass() throws CException {
        CModel model = CodeableModels.createModel();
        CModel model2 = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        try {
            model.deleteClassifier(null);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("classifier '' to be deleted does not exist", e.getMessage());
        }
        try {
            model.deleteClassifier(model2.createMetaclass("x"));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("classifier 'x' to be deleted does not exist", e.getMessage());
        }
        CClass cl1 = model.createClass(mcl, "Class1");
        model.deleteClassifier(cl1);

        CClass gcl1 = model.getClass("Class1");
        assertEquals(null, gcl1);
        List<CClass> classes = model.getClasses();
        assertEquals(0, classes.size());

        cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl3 = model.createClass(mcl, "Class3");

        model.deleteClassifier(cl1);
        try {
            model.deleteClassifier(model2.createMetaclass("y"));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("classifier 'y' to be deleted does not exist", e.getMessage());
        }
        model.deleteClassifier(cl3);

        gcl1 = model.getClass("Class1");
        CClass gcl2 = model.getClass("Class2");
        CClass gcl3 = model.getClass("Class3");

        assertEquals(null, gcl1);
        assertEquals(cl2, gcl2);
        assertEquals(null, gcl3);

        classes = model.getClasses();
        assertEquals(1, classes.size());
    }


    @Test
    public void testDeleteClassInstanceRelation() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CObject obj1 = model.createObject(cl1, "O1");
        CObject obj2 = model.createObject(cl1, "O2");
        CObject obj3 = model.createObject(cl2, "O3");

        model.deleteClassifier(cl1);

        assertEquals(0, cl1.getInstances().size());
        assertEquals(null, obj1.getClassifier());
        assertEquals(null, obj2.getClassifier());
        assertEquals(cl2, obj3.getClassifier());

        List<CObject> instances2 = cl2.getInstances();
        assertEquals(1, instances2.size());
        assertTrue(!instances2.contains(obj1));
        assertTrue(!instances2.contains(obj2));
        assertTrue(instances2.contains(obj3));

        List<CObject> objects = model.getObjects();
        assertEquals(1, objects.size());
        assertEquals(obj3, objects.get(0));
    }

}
