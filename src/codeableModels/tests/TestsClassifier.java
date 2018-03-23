package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsClassifier {

    @Test
    public void getClassifiers() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass c1 = model.createMetaclass("Metaclass1");
        CMetaclass c2 = model.createMetaclass("Metaclass2");
        CClass c3 = model.createClass(c1, "Class1");
        CClass c4 = model.createClass(c2, "Class2");
        CStereotype c5 = model.createStereotype("Stereotype1");

        List<CClassifier> results = model.getClassifiers();

        assertEquals(5, results.size());
        assertTrue(results.contains(c1));
        assertTrue(results.contains(c2));
        assertTrue(results.contains(c3));
        assertTrue(results.contains(c4));
        assertTrue(results.contains(c5));
    }

    @Test
    public void getClassifierNames() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass c1 = model.createMetaclass("Metaclass1");
        CMetaclass c2 = model.createMetaclass("Metaclass2");
        model.createClass(c1, "Class1");
        model.createClass(c2, "Class2");
        model.createStereotype("Stereotype1");

        List<String> results = model.getClassifierNames();

        assertEquals(5, results.size());
        assertTrue(results.contains("Metaclass1"));
        assertTrue(results.contains("Metaclass2"));
        assertTrue(results.contains("Class2"));
        assertTrue(results.contains("Class1"));
        assertTrue(results.contains("Stereotype1"));
    }

    @Test
    public void asMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass c1 = model.createMetaclass("Metaclass1");
        CClass c3 = model.createClass(c1, "Class1");
        CStereotype c5 = model.createStereotype("Stereotype1");

        assertEquals(c1, model.getClassifier("Metaclass1").asMetaclass());
        try {
            assertEquals(c3, model.getClassifier("Class1").asMetaclass());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("'Class1' is not a metaclass", e.getMessage());
        }

        try {
            assertEquals(c5, model.getClassifier("Stereotype1").asMetaclass());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("'Stereotype1' is not a metaclass", e.getMessage());
        }
    }

    @Test
    public void asClass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass c1 = model.createMetaclass("Metaclass1");
        CClass c3 = model.createClass(c1, "Class1");
        CStereotype c5 = model.createStereotype("Stereotype1");

        try {
            assertEquals(c1, model.getClassifier("Metaclass1").asClass());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("'Metaclass1' is not a class", e.getMessage());
        }

        assertEquals(c3, model.getClassifier("Class1").asClass());

        try {
            assertEquals(c5, model.getClassifier("Stereotype1").asClass());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("'Stereotype1' is not a class", e.getMessage());
        }
    }

    @Test
    public void asStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass c1 = model.createMetaclass("Metaclass1");
        CClass c3 = model.createClass(c1, "Class1");
        CStereotype c5 = model.createStereotype("Stereotype1");

        try {
            assertEquals(c1, model.getClassifier("Metaclass1").asStereotype());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("'Metaclass1' is not a stereotype", e.getMessage());
        }

        try {
            assertEquals(c3, model.getClassifier("Class1").asStereotype());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("'Class1' is not a stereotype", e.getMessage());
        }

        assertEquals(c5, model.getClassifier("Stereotype1").asStereotype());
    }


    @Test
    public void hasSuperclassHasSubclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("Metaclass1");
        CMetaclass mcl2 = model.createMetaclass("Metaclass2").addSuperclass(mcl1);
        CMetaclass mcl3 = model.createMetaclass("Metaclass3").addSuperclass(mcl2);
        CMetaclass mcl4 = model.createMetaclass("Metaclass4").addSuperclass(mcl2);
        CMetaclass mcl5 = model.createMetaclass("Metaclass5");

        assertEquals(false, mcl1.hasSuperclass(mcl2));
        assertEquals(false, mcl1.hasSuperclass((CClassifier) null));
        assertEquals(true, mcl2.hasSuperclass(mcl1));
        assertEquals(true, mcl3.hasSuperclass("Metaclass1"));
        assertEquals(true, mcl3.hasSuperclass(mcl2));
        assertEquals(true, mcl4.hasSuperclass(mcl2));
        assertEquals(false, mcl5.hasSuperclass("Metaclass2"));
        assertEquals(false, mcl5.hasSuperclass(""));

        assertEquals(false, mcl3.hasSubclass(mcl2));
        assertEquals(false, mcl3.hasSubclass((CClassifier) null));
        assertEquals(false, mcl2.hasSubclass("Metaclass1"));
        assertEquals(true, mcl1.hasSubclass(mcl3));
        assertEquals(true, mcl1.hasSubclass(mcl2));
        assertEquals(false, mcl5.hasSubclass("Metaclass2"));
        assertEquals(false, mcl5.hasSubclass(""));
    }
}
