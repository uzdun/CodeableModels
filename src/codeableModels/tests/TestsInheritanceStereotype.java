package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsInheritanceStereotype {

    @Test
    public void testNoInheritanceStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype top = model.createStereotype("Top");
        assertEquals(0, top.getSuperclasses().size());
        assertEquals(0, top.getSubclasses().size());
        assertEquals(0, top.getAllSuperclasses().size());
    }

    @Test
    public void testStereotypeAddSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype top = model.createStereotype("Top");
        try {
            top.addSuperclass("X");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("can't find superclass 'X'", e.getMessage());
        }
    }

    @Test
    public void testSimpleInheritanceStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype top = model.createStereotype("Top");
        CStereotype l1a = model.createStereotype("L1a").addSuperclass("Top");
        CStereotype l1b = model.createStereotype("L1b").addSuperclass(top);
        CStereotype l2a = model.createStereotype("L2a").addSuperclass("L1a");
        CStereotype l2b = model.createStereotype("L2b").addSuperclass("L1a");
        CStereotype l2c = model.createStereotype("L2c").addSuperclass(top);

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
    public void testInheritanceDoubleAssignmentStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype top = model.createStereotype("Top");
        CStereotype l1a = model.createStereotype("L1a").addSuperclass("Top");
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
    public void testInheritanceDeleteTopStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype top = model.createStereotype("Top");
        CStereotype l1a = model.createStereotype("L1a").addSuperclass("Top");
        CStereotype l1b = model.createStereotype("L1b").addSuperclass(top);
        CStereotype l2a = model.createStereotype("L2a").addSuperclass("L1a");
        CStereotype l2b = model.createStereotype("L2b").addSuperclass("L1a");
        CStereotype l2c = model.createStereotype("L2c").addSuperclass(top);

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
    public void testInheritanceDeleteInnerStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype top = model.createStereotype("Top");
        CStereotype l1a = model.createStereotype("L1a").addSuperclass("Top");
        CStereotype l1b = model.createStereotype("L1b").addSuperclass(top);
        CStereotype l2a = model.createStereotype("L2a").addSuperclass("L1a");
        CStereotype l2b = model.createStereotype("L2b").addSuperclass("L1a");
        CStereotype l2c = model.createStereotype("L2c").addSuperclass(top);

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
    public void testStereotypeMultipleInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype top1 = model.createStereotype("Top1");
        CStereotype top2 = model.createStereotype("Top2");
        CStereotype top3 = model.createStereotype("Top3");
        CStereotype l1a = model.createStereotype("L1A").addSuperclass("Top1").addSuperclass("Top3");
        CStereotype l1b = model.createStereotype("L1B").addSuperclass("Top2").addSuperclass("Top3");
        CStereotype l2a = model.createStereotype("L2A").addSuperclass("L1A");
        CStereotype l2b = model.createStereotype("L2B").addSuperclass("L1A").addSuperclass("L1B");
        CStereotype l2c = model.createStereotype("L2C").addSuperclass("L1B").addSuperclass("L1A");

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
    public void testStereotypeAsWrongTypeOfSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        model.createStereotype("Top1");
        CMetaclass mcl = model.createMetaclass("MCL");
        try {
            model.createClass(mcl, "Sub1").addSuperclass("Top1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("cannot add superclass 'Top1' to 'Sub1': not a class", e.getMessage());
        }
        try {
            model.createMetaclass("MetaSub1").addSuperclass("Top1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("cannot add superclass 'Top1' to 'MetaSub1': not a metaclass", e.getMessage());
        }
    }

    @Test
    public void testExtendedClassesOfInheritingStereotypes_SuperclassHasNone() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2").addSuperclass(mcl1);
        CStereotype stereotype1 = model.createStereotype("ST1");
        CStereotype stereotype2 = model.createStereotype("ST2").addSuperclass("ST1");
        mcl2.addStereotype("ST2");

        assertEquals(0, stereotype1.getStereotypedElements().size());
        assertEquals(mcl2, stereotype2.getStereotypedElements().get(0));
        assertEquals(Collections.singletonList(stereotype2), mcl2.getStereotypes());
    }

    @Test
    public void testExtendedClassesOfInheritingStereotypes_SuperclassHasTheSame() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CStereotype stereotype1 = model.createStereotype("ST1", mcl1);
        CStereotype stereotype2 = model.createStereotype("ST2", mcl1).addSuperclass("ST1");

        assertEquals(mcl1, stereotype1.getStereotypedElements().get(0));
        assertEquals(mcl1, stereotype2.getStereotypedElements().get(0));
        assertEquals(Arrays.asList(stereotype1, stereotype2), mcl1.getStereotypes());
    }

    @Test
    public void testExtendedClassesOfInheritingStereotypes_RemoveSuperclassStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CStereotype stereotype1 = model.createStereotype("ST1", mcl1);
        CStereotype stereotype2 = model.createStereotype("ST2", mcl1).addSuperclass("ST1");
        mcl1.removeStereotype(stereotype1);

        assertEquals(0, stereotype1.getStereotypedElements().size());
        assertEquals(mcl1, stereotype2.getStereotypedElements().get(0));
        assertEquals(Collections.singletonList(stereotype2), mcl1.getStereotypes());
    }

    @Test
    public void testExtendedClassesOfInheritingStereotypes_SuperclassIsSetToTheSame() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CStereotype stereotype1 = model.createStereotype("ST1");
        CStereotype stereotype2 = model.createStereotype("ST2", mcl1).addSuperclass("ST1");
        mcl1.addStereotype(stereotype1);

        assertEquals(mcl1, stereotype1.getStereotypedElements().get(0));
        assertEquals(mcl1, stereotype2.getStereotypedElements().get(0));
        assertEquals(Arrays.asList(stereotype2, stereotype1), mcl1.getStereotypes());
    }

    @Test
    public void testExtendedClassesOfInheritingStereotypes_SuperclassHasMetaclassesSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2").addSuperclass(mcl1);
        CStereotype stereotype1 = model.createStereotype("ST1", mcl1);
        CStereotype stereotype2 = model.createStereotype("ST2", mcl2).addSuperclass("ST1");

        assertEquals(mcl1, stereotype1.getStereotypedElements().get(0));
        assertEquals(mcl2, stereotype2.getStereotypedElements().get(0));
        assertEquals(Collections.singletonList(stereotype1), mcl1.getStereotypes());
        assertEquals(Collections.singletonList(stereotype2), mcl2.getStereotypes());
    }

    @Test
    public void testExtendedClassesOfInheritingStereotypes_SuperclassIsSetToMetaclassesSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2").addSuperclass(mcl1);
        CStereotype stereotype1 = model.createStereotype("ST1");
        CStereotype stereotype2 = model.createStereotype("ST2", mcl2).addSuperclass("ST1");
        mcl1.addStereotype("ST1");

        assertEquals(mcl1, stereotype1.getStereotypedElements().get(0));
        assertEquals(mcl2, stereotype2.getStereotypedElements().get(0));
        assertEquals(Collections.singletonList(stereotype1), mcl1.getStereotypes());
        assertEquals(Collections.singletonList(stereotype2), mcl2.getStereotypes());
    }

    @Test
    public void testExtendedClassesOfInheritingStereotypes_SuperclassHasMetaclassesSuperclassIndirectly() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2").addSuperclass(mcl1);
        CMetaclass mcl3 = model.createMetaclass("MCL3").addSuperclass(mcl2);
        CStereotype stereotype1 = model.createStereotype("ST1", mcl1);
        CStereotype stereotype2 = model.createStereotype("ST2", mcl3).addSuperclass("ST1");

        assertEquals(mcl1, stereotype1.getStereotypedElements().get(0));
        assertEquals(mcl3, stereotype2.getStereotypedElements().get(0));
        assertEquals(Collections.singletonList(stereotype1), mcl1.getStereotypes());
        assertEquals(Collections.singletonList(stereotype2), mcl3.getStereotypes());
    }

    @Test
    public void testExtendedClassesOfInheritingStereotypes_SuperclassIsSetToMetaclassesSuperclassIndirectly() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2").addSuperclass(mcl1);
        CMetaclass mcl3 = model.createMetaclass("MCL3").addSuperclass(mcl2);
        CStereotype stereotype1 = model.createStereotype("ST1");
        CStereotype stereotype2 = model.createStereotype("ST2", mcl3).addSuperclass("ST1");
        mcl1.addStereotype("ST1");

        assertEquals(mcl1, stereotype1.getStereotypedElements().get(0));
        assertEquals(mcl3, stereotype2.getStereotypedElements().get(0));
        assertEquals(Collections.singletonList(stereotype1), mcl1.getStereotypes());
        assertEquals(Collections.singletonList(stereotype2), mcl3.getStereotypes());
    }

}
