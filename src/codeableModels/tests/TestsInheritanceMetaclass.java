package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsInheritanceMetaclass {

    @Test
    public void testNoInheritanceMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top = model.createMetaclass("Top");
        assertEquals(0, top.getSuperclasses().size());
        assertEquals(0, top.getSubclasses().size());
        assertEquals(0, top.getAllSuperclasses().size());
    }

    @Test
    public void testMetaclassAddSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top = model.createMetaclass("Top");
        try {
            top.addSuperclass("X");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't find superclass 'X'", e.getMessage());
        }
    }

    @Test
    public void testSimpleInheritanceMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top = model.createMetaclass("Top");
        CMetaclass l1a = model.createMetaclass("L1a").addSuperclass("Top");
        CMetaclass l1b = model.createMetaclass("L1b").addSuperclass(top);
        CMetaclass l2a = model.createMetaclass("L2a").addSuperclass("L1a");
        CMetaclass l2b = model.createMetaclass("L2b").addSuperclass("L1a");
        CMetaclass l2c = model.createMetaclass("L2c").addSuperclass(top);

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
    public void testInheritanceDoubleAssignmentMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top = model.createMetaclass("Top");
        CMetaclass l1a = model.createMetaclass("L1a").addSuperclass("Top");
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
    public void testInheritanceDeleteTopMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top = model.createMetaclass("Top");
        CMetaclass l1a = model.createMetaclass("L1a").addSuperclass("Top");
        CMetaclass l1b = model.createMetaclass("L1b").addSuperclass(top);
        CMetaclass l2a = model.createMetaclass("L2a").addSuperclass("L1a");
        CMetaclass l2b = model.createMetaclass("L2b").addSuperclass("L1a");
        CMetaclass l2c = model.createMetaclass("L2c").addSuperclass(top);

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
    public void testInheritanceDeleteInnerMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top = model.createMetaclass("Top");
        CMetaclass l1a = model.createMetaclass("L1a").addSuperclass("Top");
        CMetaclass l1b = model.createMetaclass("L1b").addSuperclass(top);
        CMetaclass l2a = model.createMetaclass("L2a").addSuperclass("L1a");
        CMetaclass l2b = model.createMetaclass("L2b").addSuperclass("L1a");
        CMetaclass l2c = model.createMetaclass("L2c").addSuperclass(top);

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
    public void testMetaclassMultipleInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top1 = model.createMetaclass("Top1");
        CMetaclass top2 = model.createMetaclass("Top2");
        CMetaclass top3 = model.createMetaclass("Top3");
        CMetaclass l1a = model.createMetaclass("L1A").addSuperclass("Top1").addSuperclass("Top3");
        CMetaclass l1b = model.createMetaclass("L1B").addSuperclass("Top2").addSuperclass("Top3");
        CMetaclass l2a = model.createMetaclass("L2A").addSuperclass("L1A");
        CMetaclass l2b = model.createMetaclass("L2B").addSuperclass("L1A").addSuperclass("L1B");
        CMetaclass l2c = model.createMetaclass("L2C").addSuperclass("L1B").addSuperclass("L1A");

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
    public void testMetaclassAsWrongTypeOfSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top1 = model.createMetaclass("Top1");
        try {
            model.createClass(top1, "Sub1").addSuperclass("Top1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("cannot add superclass 'Top1' to 'Sub1': not a class", e.getMessage());
        }
        try {
            model.createStereotype("StereoSub1").addSuperclass("Top1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("cannot add superclass 'Top1' to 'StereoSub1': not a stereotype", e.getMessage());
        }
    }

    @Test
    public void testClassifierPathNoInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top = model.createMetaclass("Top");
        CClass cl = model.createClass(top, "CL");
        assertEquals(Collections.singletonList(top), cl.getClassifierPath());
    }

    @Test
    public void testClassifierPathSimpleInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top = model.createMetaclass("Top");
        CMetaclass l1a = model.createMetaclass("L1a").addSuperclass("Top");
        CMetaclass l2b = model.createMetaclass("L2b").addSuperclass("L1a");
        CMetaclass l2c = model.createMetaclass("L2c").addSuperclass(top);

        CClass cl1 = model.createClass(l2c, "CL1");
        assertEquals(Arrays.asList(l2c, top), cl1.getClassifierPath());
        CClass cl2 = model.createClass(l2b, "CL2");
        assertEquals(Arrays.asList(l2b, l1a, top), cl2.getClassifierPath());
    }

    @Test
    public void testClassifierPathMultipleInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top = model.createMetaclass("Top");
        CMetaclass top2 = model.createMetaclass("Top2");
        CMetaclass l1a = model.createMetaclass("L1a").addSuperclass("Top").addSuperclass("Top2");
        CMetaclass l1b = model.createMetaclass("L1b").addSuperclass("Top");
        CMetaclass l2c = model.createMetaclass("L2c").addSuperclass(l1b).addSuperclass(l1a);

        CClass cl1 = model.createClass(l2c, "CL1");
        assertEquals(Arrays.asList(l2c, l1b, top, l1a, top2), cl1.getClassifierPath());
        CClass cl2 = model.createClass(l1a, "CL2");
        assertEquals(Arrays.asList(l1a, top, top2), cl2.getClassifierPath());
    }

    @Test
    public void testInstanceOf() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass a = model.createMetaclass("A");
        CMetaclass b = model.createMetaclass("B").addSuperclass(a);
        CMetaclass c = model.createMetaclass("C");

        CClass bClass = model.createClass(b, "bClass");
        assertEquals(true, bClass.instanceOf(a));
        assertEquals(true, bClass.instanceOf(b));
        assertEquals(false, bClass.instanceOf(c));
        assertEquals(true, bClass.instanceOf("A"));
        assertEquals(true, bClass.instanceOf("B"));
        assertEquals(false, bClass.instanceOf("C"));
    }

    @Test
    public void testGetAllClassInstances() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass a = model.createMetaclass("A");
        CMetaclass b = model.createMetaclass("B").addSuperclass(a);
        CMetaclass c = model.createMetaclass("C").addSuperclass(b);

        CClass aClass = model.createClass(a, "aClass");
        CClass b1Class = model.createClass(b, "b1Class");
        CClass b2Class = model.createClass(b, "b2Class");
        CClass cClass = model.createClass(c, "cClass");

        assertEquals(Collections.singletonList(aClass), a.getClassInstances());
        assertEquals(Arrays.asList(aClass, b1Class, b2Class, cClass), a.getAllClassInstances());
        assertEquals(Arrays.asList(b1Class, b2Class), b.getClassInstances());
        assertEquals(Arrays.asList(b1Class, b2Class, cClass), b.getAllClassInstances());
        assertEquals(Collections.singletonList(cClass), c.getClassInstances());
        assertEquals(Collections.singletonList(cClass), c.getAllClassInstances());
    }
}
