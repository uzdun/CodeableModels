package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsInheritanceClass {

    @Test
    public void testClassNoInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top = model.createClass(mcl, "Top");
        assertEquals(0, top.getSuperclasses().size());
        assertEquals(0, top.getSubclasses().size());
        assertEquals(0, top.getAllSuperclasses().size());
    }

    @Test
    public void testClassAddSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top = model.createClass(mcl, "Top");
        try {
            top.addSuperclass("X");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't find superclass 'X'", e.getMessage());
        }
    }

    @Test
    public void testClassSimpleInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top = model.createClass(mcl, "Top");
        CClass l1a = model.createClass(mcl, "L1a").addSuperclass("Top");
        CClass l1b = model.createClass(mcl, "L1b").addSuperclass(top);
        CClass l2a = model.createClass(mcl, "L2a").addSuperclass("L1a");
        CClass l2b = model.createClass(mcl, "L2b").addSuperclass("L1a");
        CClass l2c = model.createClass(mcl, "L2c").addSuperclass(top);

        assertEquals(3, top.getSubclasses().size());
        assertEquals(0, top.getSuperclasses().size());
        assertEquals(0, top.getAllSuperclasses().size());
        assertEquals(2, l1a.getSubclasses().size());
        assertEquals(1, l1a.getSuperclasses().size());
        assertEquals(1, l1a.getAllSuperclasses().size());
        assertEquals(0, l1b.getSubclasses().size());
        assertEquals(1, l1b.getSuperclasses().size());
        assertEquals(1, l1b.getAllSuperclasses().size());
        assertEquals(0, l2a.getSubclasses().size());
        assertEquals(1, l2a.getSuperclasses().size());
        assertEquals(2, l2a.getAllSuperclasses().size());
        assertEquals(0, l2b.getSubclasses().size());
        assertEquals(1, l2b.getSuperclasses().size());
        assertEquals(2, l2b.getAllSuperclasses().size());
        assertEquals(0, l2c.getSubclasses().size());
        assertEquals(1, l2c.getSuperclasses().size());
        assertEquals(1, l2c.getAllSuperclasses().size());

        List<CClassifier> l1aSuper = l1a.getSuperclasses();
        List<CClassifier> l1aSub = l1a.getSubclasses();

        assertTrue(l1aSuper.contains(top));
        assertTrue(l1aSub.contains(l2a));
        assertTrue(l1aSub.contains(l2b));

        List<CClassifier> l2aAllSuper = l2a.getAllSuperclasses();

        assertTrue(l2aAllSuper.contains(l1a));
        assertTrue(l2aAllSuper.contains(top));
    }

    @Test
    public void testClassInheritanceDoubleAssignment() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top = model.createClass(mcl, "Top");
        CClass l1a = model.createClass(mcl, "L1a").addSuperclass("Top");
        try {
            l1a.addSuperclass(top);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("'Top' is already a superclass of 'L1a'", e.getMessage());
        }

        assertEquals(1, top.getSubclasses().size());
        assertEquals(0, top.getSuperclasses().size());
        assertEquals(0, top.getAllSuperclasses().size());
        assertEquals(0, l1a.getSubclasses().size());
        assertEquals(1, l1a.getSuperclasses().size());
        assertEquals(1, l1a.getAllSuperclasses().size());
    }

    @Test
    public void testInheritanceDeleteTopClass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top = model.createClass(mcl, "Top");
        CClass l1a = model.createClass(mcl, "L1a").addSuperclass("Top");
        CClass l1b = model.createClass(mcl, "L1b").addSuperclass(top);
        CClass l2a = model.createClass(mcl, "L2a").addSuperclass("L1a");
        CClass l2b = model.createClass(mcl, "L2b").addSuperclass("L1a");
        CClass l2c = model.createClass(mcl, "L2c").addSuperclass(top);

        model.deleteClassifier(top);

        assertEquals(0, top.getSubclasses().size());
        assertEquals(0, top.getSuperclasses().size());
        assertEquals(0, top.getAllSuperclasses().size());
        assertEquals(2, l1a.getSubclasses().size());
        assertEquals(0, l1a.getSuperclasses().size());
        assertEquals(0, l1a.getAllSuperclasses().size());
        assertEquals(0, l1b.getSubclasses().size());
        assertEquals(0, l1b.getSuperclasses().size());
        assertEquals(0, l1b.getAllSuperclasses().size());
        assertEquals(0, l2a.getSubclasses().size());
        assertEquals(1, l2a.getSuperclasses().size());
        assertEquals(1, l2a.getAllSuperclasses().size());
        assertEquals(0, l2b.getSubclasses().size());
        assertEquals(1, l2b.getSuperclasses().size());
        assertEquals(1, l2b.getAllSuperclasses().size());
        assertEquals(0, l2c.getSubclasses().size());
        assertEquals(0, l2c.getSuperclasses().size());
        assertEquals(0, l2c.getAllSuperclasses().size());

        List<CClassifier> l1aSuper = l1a.getSuperclasses();
        List<CClassifier> l1aSub = l1a.getSubclasses();

        assertTrue(!l1aSuper.contains(top));
        assertTrue(l1aSub.contains(l2a));
        assertTrue(l1aSub.contains(l2b));

        List<CClassifier> l2aAllSuper = l2a.getAllSuperclasses();

        assertTrue(l2aAllSuper.contains(l1a));

    }

    @Test
    public void testInheritanceDeleteInnerClass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top = model.createClass(mcl, "Top");
        CClass l1a = model.createClass(mcl, "L1a").addSuperclass("Top");
        CClass l1b = model.createClass(mcl, "L1b").addSuperclass(top);
        CClass l2a = model.createClass(mcl, "L2a").addSuperclass("L1a");
        CClass l2b = model.createClass(mcl, "L2b").addSuperclass("L1a");
        CClass l2c = model.createClass(mcl, "L2c").addSuperclass(top);

        model.deleteClassifier(l1a);

        assertEquals(2, top.getSubclasses().size());
        assertEquals(0, top.getSuperclasses().size());
        assertEquals(0, top.getAllSuperclasses().size());
        assertEquals(0, l1a.getSubclasses().size());
        assertEquals(0, l1a.getSuperclasses().size());
        assertEquals(0, l1a.getAllSuperclasses().size());
        assertEquals(0, l1b.getSubclasses().size());
        assertEquals(1, l1b.getSuperclasses().size());
        assertEquals(1, l1b.getAllSuperclasses().size());
        assertEquals(0, l2a.getSubclasses().size());
        assertEquals(0, l2a.getSuperclasses().size());
        assertEquals(0, l2a.getAllSuperclasses().size());
        assertEquals(0, l2b.getSubclasses().size());
        assertEquals(0, l2b.getSuperclasses().size());
        assertEquals(0, l2b.getAllSuperclasses().size());
        assertEquals(0, l2c.getSubclasses().size());
        assertEquals(1, l2c.getSuperclasses().size());
        assertEquals(1, l2c.getAllSuperclasses().size());

        List<CClassifier> l1aSuper = l1a.getSuperclasses();
        List<CClassifier> l1aSub = l1a.getSubclasses();

        assertTrue(!l1aSuper.contains(top));
        assertTrue(!l1aSub.contains(l2a));
        assertTrue(!l1aSub.contains(l2b));
    }

    @Test
    public void testDeleteSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top = model.createClass(mcl, "Top");
        CClass l1a = model.createClass(mcl, "L1a").addSuperclass("Top");
        CClass l1b = model.createClass(mcl, "L1b").addSuperclass(top);
        CClass l2a = model.createClass(mcl, "L2a").addSuperclass("L1a");
        CClass l2b = model.createClass(mcl, "L2b").addSuperclass("L1a");
        CClass l2c = model.createClass(mcl, "L2c").addSuperclass(top).addSuperclass("L1a").addSuperclass("L1b");
        CClass x = model.createClass(mcl, "X");

        try {
            top.deleteSuperclass(x);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't remove subclass 'Top' from classifier 'X': is not a subclass", e.getMessage());
        }

        try {
            l1a.deleteSuperclass("X");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't remove subclass 'L1a' from classifier 'X': is not a subclass", e.getMessage());
        }

        l1a.deleteSuperclass("Top");
        l2b.deleteSuperclass(l1a);
        l2c.deleteSuperclass(l1a);

        assertEquals(top.getSubclasses(), Arrays.asList(l1b, l2c));
        assertEquals(top.getSuperclasses(), Collections.emptyList());
        assertEquals(top.getAllSuperclasses(), Collections.emptyList());

        assertEquals(l1a.getSubclasses(), Collections.singletonList(l2a));
        assertEquals(l1a.getSuperclasses(), Collections.emptyList());
        assertEquals(l1a.getAllSuperclasses(), Collections.emptyList());

        assertEquals(l2b.getSubclasses(), Collections.emptyList());
        assertEquals(l2b.getSuperclasses(), Collections.emptyList());
        assertEquals(l2b.getAllSuperclasses(), Collections.emptyList());

        assertEquals(l2c.getSubclasses(), Collections.emptyList());
        assertEquals(l2c.getSuperclasses(), Arrays.asList(top, l1b));
        assertEquals(l2c.getAllSuperclasses(), Arrays.asList(top, l1b));

    }


    @Test
    public void testClassMultipleInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top1 = model.createClass(mcl, "Top1");
        CClass top2 = model.createClass(mcl, "Top2");
        CClass top3 = model.createClass(mcl, "Top3");
        CClass l1a = model.createClass(mcl, "L1A").addSuperclass("Top1").addSuperclass("Top3");
        CClass l1b = model.createClass(mcl, "L1B").addSuperclass("Top2").addSuperclass("Top3");
        CClass l2a = model.createClass(mcl, "L2A").addSuperclass("L1A");
        CClass l2b = model.createClass(mcl, "L2B").addSuperclass("L1A").addSuperclass("L1B");
        CClass l2c = model.createClass(mcl, "L2C").addSuperclass("L1B").addSuperclass("L1A");

        assertEquals(l1a.getSubclasses(), Arrays.asList(l2a, l2b, l2c));
        assertEquals(l1a.getSuperclasses(), Arrays.asList(top1, top3));
        assertEquals(l1a.getAllSuperclasses(), Arrays.asList(top1, top3));

        assertEquals(l1b.getSubclasses(), Arrays.asList(l2b, l2c));
        assertEquals(l1b.getSuperclasses(), Arrays.asList(top2, top3));
        assertEquals(l1b.getAllSuperclasses(), Arrays.asList(top2, top3));

        assertEquals(l2a.getSubclasses(), Collections.emptyList());
        assertEquals(l2a.getSuperclasses(), Collections.singletonList(l1a));
        assertEquals(l2a.getAllSuperclasses(), Arrays.asList(l1a, top1, top3));

        assertEquals(l2b.getSubclasses(), Collections.emptyList());
        assertEquals(l2b.getSuperclasses(), Arrays.asList(l1a, l1b));
        assertEquals(l2b.getAllSuperclasses(), Arrays.asList(l1a, top1, top3, l1b, top2));

        assertEquals(l2c.getSubclasses(), Collections.emptyList());
        assertEquals(l2c.getSuperclasses(), Arrays.asList(l1b, l1a));
        assertEquals(l2c.getAllSuperclasses(), Arrays.asList(l1b, top2, top3, l1a, top1));
    }

    @Test
    public void testClassAsWrongTypeOfSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        model.createClass(mcl, "Top1");
        try {
            model.createMetaclass("Sub1").addSuperclass("Top1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("cannot add superclass 'Top1' to 'Sub1': not a metaclass", e.getMessage());
        }
        try {
            model.createStereotype("StereoSub1").addSuperclass("Top1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("cannot add superclass 'Top1' to 'StereoSub1': not a stereotype", e.getMessage());
        }
    }

    @Test
    public void testClassDuplicatedSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass l1a = model.createClass(mcl, "L1a");
        CClass l1b = model.createClass(mcl, "L1b");
        CClass l2 = model.createClass(mcl, "L2").addSuperclass(l1a).addSuperclass(l1b);
        try {
            l2.addSuperclass(l1a);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals(
                    "'L1a' is already a superclass of 'L2'",
                    e.getMessage());
        }
        assertEquals(l2.getSuperclasses(), Arrays.asList(l1a, l1b));
    }

    @Test
    public void testClassifierPathNoInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top = model.createClass(mcl, "Top");

        CObject obj = model.createObject(top, "o");
        assertEquals(Collections.singletonList(top), obj.getClassifierPath());
    }

    @Test
    public void testClassifierPathSimpleInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top = model.createClass(mcl, "Top");
        CClass l1a = model.createClass(mcl, "L1a").addSuperclass("Top");
        CClass l2b = model.createClass(mcl, "L2b").addSuperclass("L1a");
        CClass l2c = model.createClass(mcl, "L2c").addSuperclass(top);

        CObject obj1 = model.createObject(l2c, "o1");
        assertEquals(Arrays.asList(l2c, top), obj1.getClassifierPath());
        CObject obj2 = model.createObject(l2b, "o2");
        assertEquals(Arrays.asList(l2b, l1a, top), obj2.getClassifierPath());
    }

    @Test
    public void testClassifierPathMultipleInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top = model.createClass(mcl, "Top");
        CClass top2 = model.createClass(mcl, "Top2");
        CClass l1a = model.createClass(mcl, "L1a").addSuperclass("Top").addSuperclass("Top2");
        CClass l1b = model.createClass(mcl, "L1b").addSuperclass("Top");
        CClass l2c = model.createClass(mcl, "L2c").addSuperclass(l1b).addSuperclass(l1a);

        CObject obj1 = model.createObject(l2c, "o1");
        assertEquals(Arrays.asList(l2c, l1b, top, l1a, top2), obj1.getClassifierPath());
        CObject obj2 = model.createObject(l1a, "o2");
        assertEquals(Arrays.asList(l1a, top, top2), obj2.getClassifierPath());
    }

    @Test
    public void testInstanceOf() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass a = model.createClass(mcl, "A");
        CClass b = model.createClass(mcl, "B").addSuperclass(a);
        CClass c = model.createClass(mcl, "C");

        CObject bObj = model.createObject(b, "bObj");
        assertEquals(true, bObj.instanceOf(a));
        assertEquals(true, bObj.instanceOf(b));
        assertEquals(false, bObj.instanceOf(c));
        assertEquals(true, bObj.instanceOf("A"));
        assertEquals(true, bObj.instanceOf("B"));
        assertEquals(false, bObj.instanceOf("C"));
    }

    @Test
    public void testGetAllInstances() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass a = model.createClass(mcl, "A");
        CClass b = model.createClass(mcl, "B").addSuperclass(a);
        CClass c = model.createClass(mcl, "C").addSuperclass(b);

        CObject aObject = model.createObject(a, "aObject");
        CObject b1Object = model.createObject(b, "b1Object");
        CObject b2Object = model.createObject(b, "b2Object");
        CObject cObject = model.createObject(c, "cObject");

        assertEquals(Collections.singletonList(aObject), a.getInstances());
        assertEquals(Arrays.asList(aObject, b1Object, b2Object, cObject), a.getAllInstances());
        assertEquals(Arrays.asList(b1Object, b2Object), b.getInstances());
        assertEquals(Arrays.asList(b1Object, b2Object, cObject), b.getAllInstances());
        assertEquals(Collections.singletonList(cObject), c.getInstances());
        assertEquals(Collections.singletonList(cObject), c.getAllInstances());
    }
}