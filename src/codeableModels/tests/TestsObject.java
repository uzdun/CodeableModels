package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsObject {
    @Test
    public void testCreationOfNoObjects() throws CException {
        CModel model = CodeableModels.createModel();
        CObject obj = model.getObject("Obj1");
        assertEquals(null, obj);
    }

    @Test
    public void testCreationOfOneObject() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl = model.createClass(mcl, "Class1");
        CObject obj1 = model.createObject("Class1", "Obj1");
        CObject obj2 = model.getObject("Obj1");
        assertEquals(obj1, obj2);
        assertEquals(cl, obj2.getClassifier());
    }

    @Test
    public void testCreationOfAutoNamedObject() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl = model.createClass(mcl, "Class1");
        CObject obj1 = model.createObject("Class1");
        CObject obj2 = model.createObject(cl);
        String obj1Name = obj1.getName(), obj2Name = obj2.getName();
        assertTrue(obj1Name.startsWith("##"));
        assertTrue(obj2Name.startsWith("##"));
        CObject obj3 = model.getObject(obj1Name);
        CObject obj4 = model.getObject(obj2Name);
        assertEquals(obj1, obj3);
        assertEquals(obj2, obj4);
        assertEquals(cl, obj3.getClassifier());
        assertEquals(cl, obj4.getClassifier());
    }

    @Test
    public void testCreationOf3Objects() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CObject obj1 = model.createObject("Class1", "Obj1");
        CObject obj2 = model.createObject("Class2", "Obj2");
        CObject obj3 = model.createObject("Class1", "Obj3");

        CObject o1 = model.getObject("Obj1");
        CObject o2 = model.getObject("Obj2");
        CObject o3 = model.getObject("Obj3");

        assertEquals(obj1, o1);
        assertEquals(obj2, o2);
        assertEquals(obj3, o3);
        assertEquals(cl1, o1.getClassifier());
        assertEquals(cl2, o2.getClassifier());
        assertEquals(cl1, o3.getClassifier());
    }

    @Test
    public void testCreationOf3ObjectsWithoutNameLookup() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CObject obj1 = model.createObject(cl1, "Obj1");
        CObject obj2 = model.createObject(cl2, "Obj2");
        CObject obj3 = model.createObject(cl1, "Obj3");

        CObject o1 = model.getObject("Obj1");
        CObject o2 = model.getObject("Obj2");
        CObject o3 = model.getObject("Obj3");

        assertEquals(obj1, o1);
        assertEquals(obj2, o2);
        assertEquals(obj3, o3);
        assertEquals(cl1, o1.getClassifier());
        assertEquals(cl2, o2.getClassifier());
        assertEquals(cl1, o3.getClassifier());
    }

    @Test
    public void testObjectUniqueNameUsedException() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        model.createClass(mcl, "Class1");
        model.createObject("Class1", "Obj1");
        try {
            model.createObject("Class1", "Obj1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("object 'Obj1' cannot be created, object name already exists", e.getMessage());
        }
    }

    @Test
    public void testObjectCreationClassDoesNotExistException() throws CException {
        CModel model = CodeableModels.createModel();
        try {
            model.createObject("Class1", "Obj1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't find class: 'Class1' to be instantiated", e.getMessage());
        }
    }

    @Test
    public void testGetObjectsAndGetObjectNames() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        List<CObject> objects = model.getObjects();
        List<String> objectNames = model.getObjectNames();
        assertEquals(0, objects.size());
        assertEquals(0, objectNames.size());

        model.createClass(mcl, "Class1");
        model.createClass(mcl, "Class2");
        CObject obj1 = model.createObject("Class1", "Obj1");

        objects = model.getObjects();
        objectNames = model.getObjectNames();
        assertEquals(1, objects.size());
        assertEquals(1, objectNames.size());
        assertEquals("Obj1", objectNames.get(0));
        assertEquals(obj1, objects.get(0));

        model.createObject("Class2", "Obj2");
        model.createObject("Class1", "Obj3");

        objects = model.getObjects();
        objectNames = model.getObjectNames();
        assertEquals(3, objects.size());
        assertEquals(3, objectNames.size());
    }

    @Test
    public void testDeleteObject() throws CException {
        CModel model = CodeableModels.createModel();
        CModel model2 = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CMetaclass mcl2 = model2.createMetaclass("MCL");
        CClass mcl2_cl2 = model2.createClass(mcl2, "CL2");
        try {
            model.deleteObject(null);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("object '' to be deleted does not exist", e.getMessage());
        }
        try {
            model.deleteObject(model2.createObject(mcl2_cl2, "x"));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("object 'x' to be deleted does not exist", e.getMessage());
        }
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");

        CObject obj1 = model.createObject(cl1, "O1");
        model.deleteObject(obj1);

        CObject retrievedObj1 = model.getObject("O1");
        assertEquals(null, retrievedObj1);
        List<CObject> objects = model.getObjects();
        assertEquals(0, objects.size());

        obj1 = model.createObject(cl1, "O1");
        CObject obj2 = model.createObject(cl1, "O2");
        CObject obj3 = model.createObject(cl2, "O3");

        model.deleteObject(obj1);
        try {
            model.deleteObject(model2.createObject(mcl2_cl2, "y"));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("object 'y' to be deleted does not exist", e.getMessage());
        }
        model.deleteObject(obj3);

        retrievedObj1 = model.getObject("O1");
        CObject retrievedObj2 = model.getObject("O2");
        CObject retrievedObj3 = model.getObject("O3");

        assertEquals(null, retrievedObj1);
        assertEquals(obj2, retrievedObj2);
        assertEquals(null, retrievedObj3);

        objects = model.getObjects();
        assertEquals(1, objects.size());
    }

    @Test
    public void testClassInstanceRelation() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");

        List<CObject> instances = cl1.getInstances();
        assertEquals(0, instances.size());

        CObject obj1 = model.createObject(cl1, "O1");
        CObject obj2 = model.createObject(cl1, "O2");
        CObject obj3 = model.createObject(cl2, "O3");

        assertEquals(cl1, obj1.getClassifier());
        assertEquals(cl1, obj2.getClassifier());
        assertEquals(cl2, obj3.getClassifier());

        List<CObject> instances1 = cl1.getInstances();
        assertEquals(2, instances1.size());
        assertTrue(instances1.contains(obj1));
        assertTrue(instances1.contains(obj2));
        assertTrue(!instances1.contains(obj3));

        List<CObject> instances2 = cl2.getInstances();
        assertEquals(1, instances2.size());
        assertTrue(!instances2.contains(obj1));
        assertTrue(!instances2.contains(obj2));
        assertTrue(instances2.contains(obj3));
    }

    @Test
    public void testClassInstanceRelationObjectDeletion() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");

        List<CObject> instances = cl1.getInstances();
        assertEquals(0, instances.size());

        CObject obj1 = model.createObject(cl1, "O1");
        model.deleteObject(obj1);

        instances = cl1.getInstances();
        assertEquals(0, instances.size());

        obj1 = model.createObject(cl1, "O1");
        CObject obj2 = model.createObject(cl1, "O2");
        CObject obj3 = model.createObject(cl2, "O3");

        assertEquals(cl1, obj1.getClassifier());
        assertEquals(cl1, obj2.getClassifier());
        assertEquals(cl2, obj3.getClassifier());

        model.deleteObject(obj1);
        model.deleteObject(obj3);

        List<CObject> instances1 = cl1.getInstances();
        assertEquals(1, instances1.size());
        assertTrue(!instances1.contains(obj1));
        assertTrue(instances1.contains(obj2));
        assertTrue(!instances1.contains(obj3));

        List<CObject> instances2 = cl2.getInstances();
        assertEquals(0, instances2.size());
        assertTrue(!instances2.contains(obj1));
        assertTrue(!instances2.contains(obj2));
        assertTrue(!instances2.contains(obj3));
    }

}
