package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsTaggedValuesOnLinks {

    private CModel createModel() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        CAssociation association = model.createAssociation(end1, end2);
        CStereotype stereotype = model.createStereotype("ST", association);
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        cl1.addLink(end2, cl2).addStereotypeInstance(stereotype);
        return model;
    }

    @Test
    public void testTaggedValuesOnPrimitiveTypeAttributes() throws CException {
        CModel model = createModel();
        CStereotype stereotype = model.getStereotype("ST");
        CClass cl1 = model.getClass("CL1");
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);

        stereotype.addAttribute("isBoolean", true);
        stereotype.addAttribute("intVal", 1);
        stereotype.addAttribute("longVal", (long) 100);
        stereotype.addAttribute("doubleVal", 1.1);
        stereotype.addAttribute("floatVal", (float) 1.1);
        stereotype.addAttribute("string", "abc");
        stereotype.addAttribute("char", 'a');
        stereotype.addAttribute("byte", (byte) 1);
        stereotype.addAttribute("short", (short) 2);

        assertEquals(true, link.getTaggedValue("isBoolean"));
        assertEquals(1, link.getTaggedValue("intVal"));
        assertEquals((long) 100, link.getTaggedValue("longVal"));
        assertEquals(1.1, link.getTaggedValue("doubleVal"));
        assertEquals((float) 1.1, link.getTaggedValue("floatVal"));
        assertEquals("abc", link.getTaggedValue("string"));
        assertEquals('a', link.getTaggedValue("char"));
        assertEquals((byte) 1, link.getTaggedValue("byte"));
        assertEquals((short) 2, link.getTaggedValue("short"));

        link.setTaggedValue("isBoolean", false);
        link.setTaggedValue("intVal", 10);
        link.setTaggedValue("longVal", (long) 1000);
        link.setTaggedValue("doubleVal", 100.1);
        link.setTaggedValue("floatVal", (float) 102.1);
        link.setTaggedValue("string", "");
        link.setTaggedValue("char", 'x');
        link.setTaggedValue("byte", (byte) 15);
        link.setTaggedValue("short", (short) 12);

        assertEquals(false, link.getTaggedValue("isBoolean"));
        assertEquals(10, link.getTaggedValue("intVal"));
        assertEquals((long) 1000, link.getTaggedValue("longVal"));
        assertEquals(100.1, link.getTaggedValue("doubleVal"));
        assertEquals((float) 102.1, link.getTaggedValue("floatVal"));
        assertEquals("", link.getTaggedValue("string"));
        assertEquals('x', link.getTaggedValue("char"));
        assertEquals((byte) 15, link.getTaggedValue("byte"));
        assertEquals((short) 12, link.getTaggedValue("short"));
    }

    @Test
    public void testTaggedValuesOnPrimitiveTypeAttributesCreateClassAfterAttributeSetting() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        CAssociation association = model.createAssociation(end1, end2);
        CStereotype stereotype = model.createStereotype("ST", association);

        stereotype.addAttribute("isBoolean", true);
        stereotype.addAttribute("intVal", 1);
        stereotype.addAttribute("longVal", (long) 100);
        stereotype.addAttribute("doubleVal", 1.1);
        stereotype.addAttribute("floatVal", (float) 1.1);
        stereotype.addAttribute("string", "abc");
        stereotype.addAttribute("char", 'a');
        stereotype.addAttribute("byte", (byte) 1);
        stereotype.addAttribute("short", (short) 2);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        cl1.addLink(end2, cl2);
        CLink link = cl1.getLinkObjects(end2).get(0);
        link.addStereotypeInstance(stereotype);

        assertEquals(true, link.getTaggedValue("isBoolean"));
        assertEquals(1, link.getTaggedValue("intVal"));
        assertEquals((long) 100, link.getTaggedValue("longVal"));
        assertEquals(1.1, link.getTaggedValue("doubleVal"));
        assertEquals((float) 1.1, link.getTaggedValue("floatVal"));
        assertEquals("abc", link.getTaggedValue("string"));
        assertEquals('a', link.getTaggedValue("char"));
        assertEquals((byte) 1, link.getTaggedValue("byte"));
        assertEquals((short) 2, link.getTaggedValue("short"));
    }

    @Test
    public void testAttributeOfTaggedValueUnknown() throws CException {
        CModel model = createModel();
        CClass cl1 = model.getClass("CL1");
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);

        try {
            link.getTaggedValue("x");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'x' unknown", e.getMessage());
        }

        try {
            link.setTaggedValue("x", 1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'x' unknown", e.getMessage());
        }
    }

    @Test
    public void testObjectTypeTaggedValues() throws CException {
        CModel model = createModel();
        CMetaclass mcl = model.getMetaclass("MCL1");
        CStereotype stereotype = model.getStereotype("ST");
        CClass cl1 = model.getClass("CL1");
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);

        CClass attrType = model.createClass(mcl, "AttrType");
        CObject attrValue = model.createObject(attrType, "attrValue");

        stereotype.addAttribute("attrTypeObj", attrValue);
        stereotype.getAttribute("attrTypeObj");

        assertEquals(attrValue, link.getTaggedValue("attrTypeObj"));
        assertEquals("attrValue", ((CObject) link.getTaggedValue("attrTypeObj")).getName());

        CObject attrValue2 = model.createObject(attrType, "attrValue2");
        link.setTaggedValue("attrTypeObj", attrValue2);

        assertEquals(attrValue2, link.getTaggedValue("attrTypeObj"));
        assertEquals("attrValue2", ((CObject) link.getTaggedValue("attrTypeObj")).getName());

        CObject nonAttrValue = model.createObject(cl1, "nonAttrValue");

        try {
            link.setTaggedValue("attrTypeObj", nonAttrValue);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("type classifier of object 'nonAttrValue' is not matching attribute type of attribute " +
                    "'attrTypeObj'", e.getMessage());
        }
    }

    @Test
    public void testAddObjectAttributeGetSetTaggedValue() throws CException {
        CModel model = createModel();
        CMetaclass mcl = model.getMetaclass("MCL1");
        CStereotype stereotype = model.getStereotype("ST");
        CClass cl1 = model.getClass("CL1");
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);

        CClass attrType = model.createClass(mcl, "AttrType");
        CObject attrValue = model.createObject(attrType, "attrValue");

        stereotype.addObjectAttribute("attrTypeObj", attrType).addObjectAttribute("attrTypeObj2", attrType);
        assertEquals(null, link.getTaggedValue("attrTypeObj"));
        link.setTaggedValue("attrTypeObj", attrValue);
        assertEquals(attrValue, link.getTaggedValue("attrTypeObj"));
    }


    @Test
    public void testTaggedValuesOnAttributesWithNoDefaultValues() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        CAssociation association = model.createAssociation(end1, end2);
        CStereotype stereotype = model.createStereotype("ST", association);

        stereotype.addBooleanAttribute("isBoolean");
        stereotype.addIntAttribute("intVal");
        stereotype.addLongAttribute("longVal");
        stereotype.addDoubleAttribute("doubleVal");
        stereotype.addFloatAttribute("floatVal");
        stereotype.addStringAttribute("string");
        stereotype.addCharAttribute("char");
        stereotype.addByteAttribute("byte");
        stereotype.addShortAttribute("short");
        CClass attrClass = model.createClass(mcl1, "attrClass");
        stereotype.addObjectAttribute("obj1", attrClass);
        stereotype.addObjectAttribute("obj2", "attrClass");
        CEnum enumType = model.createEnum("XYEnum", Arrays.asList("X", "Y"));
        stereotype.addEnumAttribute("enum", enumType);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        cl1.addLink(end2, cl2);
        CLink link = cl1.getLinkObjects(end2).get(0);
        link.addStereotypeInstance(stereotype);

        assertEquals(null, link.getTaggedValue("isBoolean"));
        assertEquals(null, link.getTaggedValue("intVal"));
        assertEquals(null, link.getTaggedValue("longVal"));
        assertEquals(null, link.getTaggedValue("doubleVal"));
        assertEquals(null, link.getTaggedValue("floatVal"));
        assertEquals(null, link.getTaggedValue("string"));
        assertEquals(null, link.getTaggedValue("char"));
        assertEquals(null, link.getTaggedValue("byte"));
        assertEquals(null, link.getTaggedValue("short"));
        assertEquals(null, link.getTaggedValue("obj1"));
        assertEquals(null, link.getTaggedValue("obj2"));
        assertEquals(null, link.getTaggedValue("enum"));
    }


    @Test
    public void testEnumTypeTaggedValues() throws CException {
        CModel model = createModel();
        CStereotype stereotype = model.getStereotype("ST");
        CClass cl1 = model.getClass("CL1");
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);

        List<String> enumValues = Arrays.asList("A", "B", "C");
        CEnum enumObj = model.createEnum("ABCEnum", enumValues);


        assertEquals(0, stereotype.getAttributes().size());
        stereotype.addEnumAttribute("l1", enumObj).setAttributeDefaultValue("l1", "A");
        stereotype.addEnumAttribute("l2", enumObj);

        assertEquals("A", link.getTaggedValue("l1"));
        assertEquals(null, link.getTaggedValue("l2"));

        link.setTaggedValue("l1", "B");
        link.setTaggedValue("l2", "C");

        assertEquals("B", link.getTaggedValue("l1"));
        assertEquals("C", link.getTaggedValue("l2"));

        try {
            link.setTaggedValue("l1", "X");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value 'X' not element of enumeration", e.getMessage());
        }
    }

    @Test
    public void testAttributeTypeCheckForTaggedValues() throws CException {
        CModel model = createModel();
        CStereotype stereotype = model.getStereotype("ST");
        CMetaclass mcl = model.getMetaclass("MCL1");
        CClass cl1 = model.getClass("CL1");
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);
        stereotype.addBooleanAttribute("a");

        try {
            link.setTaggedValue("a", CodeableModels.createModel());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value for attribute 'a' is not a known attribute type", e.getMessage());
        }
        try {
            link.setTaggedValue("a", 1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'a' does not match attribute type", e.getMessage());
        }

        stereotype.addIntAttribute("i");
        try {
            link.setTaggedValue("i", Boolean.TRUE);
        } catch (CException e) {
            assertEquals("value type for attribute 'i' does not match attribute type", e.getMessage());
        }

        stereotype.addShortAttribute("s");
        try {
            link.setTaggedValue("s", Boolean.TRUE);
        } catch (CException e) {
            assertEquals("value type for attribute 's' does not match attribute type", e.getMessage());
        }

        stereotype.addByteAttribute("b");
        try {
            link.setTaggedValue("b", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'b' does not match attribute type", e.getMessage());
        }

        stereotype.addLongAttribute("l");
        try {
            link.setTaggedValue("l", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'l' does not match attribute type", e.getMessage());
        }

        stereotype.addFloatAttribute("f");
        try {
            link.setTaggedValue("f", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'f' does not match attribute type", e.getMessage());
        }

        stereotype.addDoubleAttribute("d");
        try {
            link.setTaggedValue("d", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'd' does not match attribute type", e.getMessage());
        }

        CEnum enumType = model.createEnum("XYEnum", Arrays.asList("X", "Y"));
        stereotype.addEnumAttribute("e", enumType);
        try {
            link.setTaggedValue("e", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'e' does not match attribute type", e.getMessage());
        }

        CClass attrClass = model.createClass(mcl, "AttrClass");
        CClass otherClass = model.createClass(mcl, "OtherClass");
        stereotype.addObjectAttribute("o", attrClass);
        try {
            link.setTaggedValue("o", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'o' does not match attribute type", e.getMessage());
        }

        try {
            link.setTaggedValue("o", otherClass);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("type classifier of object 'OtherClass' is not matching attribute type of attribute 'o'", e
                    .getMessage());
        }

    }

    @Test
    public void testDeleteAttributesSetTaggedValue() throws CException {
        CModel model = createModel();
        CStereotype stereotype = model.getStereotype("ST");
        CClass cl1 = model.getClass("CL1");
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);

        stereotype.addAttribute("isBoolean", true);
        stereotype.addAttribute("intVal", 1);

        link.setTaggedValue("isBoolean", true);

        stereotype.deleteAttribute("isBoolean");

        link.setTaggedValue("intVal", 1);

        try {
            link.setTaggedValue("isBoolean", false);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'isBoolean' unknown", e.getMessage());
        }
    }

    @Test
    public void testTaggedValuesInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        CAssociation association = model.createAssociation(end1, end2);
        CStereotype top1 = model.createStereotype( "Top1", association);
        CStereotype top2 = model.createStereotype( "Top2");
        CStereotype stereotypeA = model.createStereotype( "STA").addSuperclass("Top1").addSuperclass("Top2");
        CStereotype stereotypeSubA = model.createStereotype("SubA").addSuperclass("STA");

        top1.addAttribute("int0", 0);
        top2.addAttribute("int1", 1);
        stereotypeA.addAttribute("int2", 2);
        stereotypeSubA.addAttribute("int3", 3);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        cl1.addLink(end2, cl2);
        CLink link = cl1.getLinkObjects(end2).get(0);
        link.addStereotypeInstance(stereotypeSubA);

        assertEquals(0, link.getTaggedValue("int0"));
        assertEquals(1, link.getTaggedValue("int1"));
        assertEquals(2, link.getTaggedValue("int2"));
        assertEquals(3, link.getTaggedValue("int3"));

        assertEquals(0, link.getTaggedValue(top1,"int0"));
        assertEquals(1, link.getTaggedValue(top2, "int1"));
        assertEquals(2, link.getTaggedValue(stereotypeA, "int2"));
        assertEquals(3, link.getTaggedValue(stereotypeSubA, "int3"));

        link.setTaggedValue("int0", 10);
        link.setTaggedValue("int1", 11);
        link.setTaggedValue("int2", 12);
        link.setTaggedValue("int3", 13);

        assertEquals(10, link.getTaggedValue("int0"));
        assertEquals(11, link.getTaggedValue("int1"));
        assertEquals(12, link.getTaggedValue("int2"));
        assertEquals(13, link.getTaggedValue("int3"));

        assertEquals(10, link.getTaggedValue(top1,"int0"));
        assertEquals(11, link.getTaggedValue(top2, "int1"));
        assertEquals(12, link.getTaggedValue(stereotypeA, "int2"));
        assertEquals(13, link.getTaggedValue(stereotypeSubA, "int3"));

        link.setTaggedValue(top1,"int0", 100);
        link.setTaggedValue(top2,"int1", 110);
        link.setTaggedValue(stereotypeA,"int2", 120);
        link.setTaggedValue(stereotypeSubA,"int3", 130);

        assertEquals(100, link.getTaggedValue("int0"));
        assertEquals(110, link.getTaggedValue("int1"));
        assertEquals(120, link.getTaggedValue("int2"));
        assertEquals(130, link.getTaggedValue("int3"));

        assertEquals(100, link.getTaggedValue(top1,"int0"));
        assertEquals(110, link.getTaggedValue(top2, "int1"));
        assertEquals(120, link.getTaggedValue(stereotypeA, "int2"));
        assertEquals(130, link.getTaggedValue(stereotypeSubA, "int3"));
    }


    @Test
    public void testTaggedValuesInheritanceAfterDeleteSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        CAssociation association = model.createAssociation(end1, end2);
        CStereotype top1 = model.createStereotype( "Top1", association);
        CStereotype top2 = model.createStereotype( "Top2");
        CStereotype stereotypeA = model.createStereotype( "STA").addSuperclass("Top1").addSuperclass("Top2");
        CStereotype stereotypeSubA = model.createStereotype("SubA").addSuperclass("STA");

        top1.addAttribute("int0", 0);
        top2.addAttribute("int1", 1);
        stereotypeA.addAttribute("int2", 2);
        stereotypeSubA.addAttribute("int3", 3);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        cl1.addLink(end2, cl2);
        CLink link = cl1.getLinkObjects(end2).get(0);
        link.addStereotypeInstance(stereotypeSubA);

        ((CClassifier) stereotypeA).deleteSuperclass(top2);

        assertEquals(0, link.getTaggedValue("int0"));
        try {
            link.getTaggedValue("int1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'int1' unknown", e.getMessage());
        }
        assertEquals(2, link.getTaggedValue("int2"));
        assertEquals(3, link.getTaggedValue("int3"));

        link.setTaggedValue("int0", 10);
        try {
            link.setTaggedValue("int1", 11);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'int1' unknown", e.getMessage());
        }
        link.setTaggedValue("int2", 12);
        link.setTaggedValue("int3", 13);
    }

    @Test
    public void testTaggedValuesInheritanceMultipleStereotypes() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        CAssociation association = model.createAssociation(end1, end2);

        CStereotype top1 = model.createStereotype( "Top1", association);
        CStereotype top2 = model.createStereotype( "Top2");
        CStereotype stereotypeA = model.createStereotype( "STA").addSuperclass("Top1").addSuperclass("Top2");
        CStereotype stereotypeSubA = model.createStereotype("SubA").addSuperclass("STA");
        CStereotype stereotypeB = model.createStereotype( "STB").addSuperclass("Top1").addSuperclass("Top2");
        CStereotype stereotypeSubB = model.createStereotype("SubB").addSuperclass("STB");
        CStereotype stereotypeC = model.createStereotype( "STC", association);
        CStereotype stereotypeSubC = model.createStereotype("SubC").addSuperclass("STC");
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        cl1.addLink(end2, cl2);
        CLink link = cl1.getLinkObjects(end2).get(0);
        link.addStereotypeInstance(stereotypeSubA);
        link.addStereotypeInstance(stereotypeSubB);
        link.addStereotypeInstance(stereotypeSubC);

        top1.addAttribute("int0", 0);
        top2.addAttribute("int1", 1);
        stereotypeA.addAttribute("int2", 2);
        stereotypeSubA.addAttribute("int3", 3);
        stereotypeB.addAttribute("int4", 4);
        stereotypeSubB.addAttribute("int5", 5);
        stereotypeC.addAttribute("int6", 6);
        stereotypeSubC.addAttribute("int7", 7);

        assertEquals(0, link.getTaggedValue("int0"));
        assertEquals(1, link.getTaggedValue("int1"));
        assertEquals(2, link.getTaggedValue("int2"));
        assertEquals(3, link.getTaggedValue("int3"));
        assertEquals(4, link.getTaggedValue("int4"));
        assertEquals(5, link.getTaggedValue("int5"));
        assertEquals(6, link.getTaggedValue("int6"));
        assertEquals(7, link.getTaggedValue("int7"));

        assertEquals(0, link.getTaggedValue(top1,"int0"));
        assertEquals(1, link.getTaggedValue(top2, "int1"));
        assertEquals(2, link.getTaggedValue(stereotypeA, "int2"));
        assertEquals(3, link.getTaggedValue(stereotypeSubA, "int3"));
        assertEquals(4, link.getTaggedValue(stereotypeB, "int4"));
        assertEquals(5, link.getTaggedValue(stereotypeSubB, "int5"));
        assertEquals(6, link.getTaggedValue(stereotypeC, "int6"));
        assertEquals(7, link.getTaggedValue(stereotypeSubC, "int7"));

        link.setTaggedValue("int0", 10);
        link.setTaggedValue("int1", 11);
        link.setTaggedValue("int2", 12);
        link.setTaggedValue("int3", 13);
        link.setTaggedValue("int4", 14);
        link.setTaggedValue("int5", 15);
        link.setTaggedValue("int6", 16);
        link.setTaggedValue("int7", 17);

        assertEquals(10, link.getTaggedValue("int0"));
        assertEquals(11, link.getTaggedValue("int1"));
        assertEquals(12, link.getTaggedValue("int2"));
        assertEquals(13, link.getTaggedValue("int3"));
        assertEquals(14, link.getTaggedValue("int4"));
        assertEquals(15, link.getTaggedValue("int5"));
        assertEquals(16, link.getTaggedValue("int6"));
        assertEquals(17, link.getTaggedValue("int7"));
    }

    @Test
    public void testTaggedValuesSameNameInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        CAssociation association = model.createAssociation(end1, end2);
        CStereotype top1 = model.createStereotype( "Top1", association);
        CStereotype top2 = model.createStereotype( "Top2");
        CStereotype stereotypeA = model.createStereotype( "STA").addSuperclass("Top1").addSuperclass("Top2");
        CStereotype stereotypeSubA = model.createStereotype("SubA").addSuperclass("STA");

        top1.addAttribute("int", 0);
        top2.addAttribute("int", 1);
        stereotypeA.addAttribute("int", 2);
        stereotypeSubA.addAttribute("int", 3);


        CClass cl1a = model.createClass(mcl1, "CL1A");
        CClass cl2a = model.createClass(mcl2, "CL2A");
        CLink link1 = cl1a.addLink(end2, cl2a);
        link1.addStereotypeInstance(stereotypeSubA);

        CClass cl1b = model.createClass(mcl1, "CL1B");
        CClass cl2b = model.createClass(mcl2, "CL2B");
        CLink link2 = cl1b.addLink(end2, cl2b);
        link2.addStereotypeInstance(stereotypeA);

        CClass cl1c = model.createClass(mcl1, "CL1C");
        CClass cl2c = model.createClass(mcl2, "CL2C");
        CLink link3 = cl1c.addLink(end2, cl2c);
        link3.addStereotypeInstance(top1);

        assertEquals(3, link1.getTaggedValue("int"));
        assertEquals(2, link2.getTaggedValue("int"));
        assertEquals(0, link3.getTaggedValue("int"));

        assertEquals(3, link1.getTaggedValue(stereotypeSubA, "int"));
        assertEquals(2, link1.getTaggedValue(stereotypeA, "int"));
        assertEquals(1, link1.getTaggedValue(top2, "int"));
        assertEquals(0, link1.getTaggedValue(top1, "int"));
        assertEquals(2, link2.getTaggedValue(stereotypeA, "int"));
        assertEquals(1, link2.getTaggedValue(top2, "int"));
        assertEquals(0, link2.getTaggedValue(top1, "int"));
        assertEquals(0, link3.getTaggedValue(top1,"int"));

        link1.setTaggedValue("int", 10);
        link2.setTaggedValue("int", 11);
        link3.setTaggedValue("int", 12);

        assertEquals(10, link1.getTaggedValue("int"));
        assertEquals(11, link2.getTaggedValue("int"));
        assertEquals(12, link3.getTaggedValue("int"));

        assertEquals(10, link1.getTaggedValue(stereotypeSubA, "int"));
        assertEquals(2, link1.getTaggedValue(stereotypeA, "int"));
        assertEquals(1, link1.getTaggedValue(top2, "int"));
        assertEquals(0, link1.getTaggedValue(top1, "int"));
        assertEquals(11, link2.getTaggedValue(stereotypeA, "int"));
        assertEquals(1, link2.getTaggedValue(top2, "int"));
        assertEquals(0, link2.getTaggedValue(top1, "int"));
        assertEquals(12, link3.getTaggedValue(top1,"int"));

        link1.setTaggedValue(stereotypeSubA,"int", 130);
        link1.setTaggedValue(top1,"int", 100);
        link1.setTaggedValue(top2,"int", 110);
        link1.setTaggedValue(stereotypeA,"int", 120);

        assertEquals(130, link1.getTaggedValue("int"));

        assertEquals(100, link1.getTaggedValue(top1,"int"));
        assertEquals(110, link1.getTaggedValue(top2, "int"));
        assertEquals(120, link1.getTaggedValue(stereotypeA, "int"));
        assertEquals(130, link1.getTaggedValue(stereotypeSubA, "int"));
    }

    @Test
    public void testSetAndDeleteTaggedValues() throws CException {
        CModel model = createModel();
        CStereotype stereotype = model.getStereotype("ST");
        CClass cl1 = model.getClass("CL1");
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);
        stereotype.addAttribute("isBoolean", true);
        stereotype.addAttribute("intVal", 1);

        link.setTaggedValue("isBoolean", true);
        link.setTaggedValue("intVal", 1);

        assertEquals(true, link.getTaggedValue("isBoolean"));
        assertEquals(1, link.getTaggedValue("intVal"));

        stereotype.deleteAttribute("isBoolean");

        assertEquals(1, link.getTaggedValue("intVal"));
        link.setTaggedValue("intVal", 100);
        assertEquals(100, link.getTaggedValue("intVal"));

        try {
            link.setTaggedValue("isBoolean", false);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'isBoolean' unknown", e.getMessage());
        }
    }

    @Test
    public void testSetAndGetTaggedValuesWithStereotypeSpecified() throws CException {
        CModel model = createModel();
        CStereotype stereo = model.getStereotype("ST");
        CClass cl1 = model.getClass("CL1");
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);
        stereo.addAttribute("isBoolean", true);
        stereo.addAttribute("intVal", 1);

        link.setTaggedValue(stereo,"isBoolean", true);
        link.setTaggedValue(stereo,"intVal", 1);

        assertEquals(true, link.getTaggedValue(stereo,"isBoolean"));
        assertEquals(1, link.getTaggedValue(stereo,"intVal"));
    }

    @Test
    public void testWrongStereotypeInTaggedValue() throws CException {
        CModel model = createModel();
        CClass cl1 = model.getClass("CL1");
        CAssociation association = cl1.getClassifier().getAssociationByRoleName("metaclass2");
        CStereotype stereo = model.createStereotype("Stereo", association);
        CStereotype stereo2 = model.createStereotype("Stereo2", association);
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);
        link.addStereotypeInstance(stereo);

        stereo.addAttribute("isBoolean", true);
        stereo2.addAttribute("isBoolean", true);

        link.setTaggedValue(stereo, "isBoolean", false);

        try {
            link.setTaggedValue(stereo2, "isBoolean", false);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'Stereo2' is not a stereotype of element", e.getMessage());
        }

        assertEquals(false, link.getTaggedValue(stereo, "isBoolean"));

        try {
            link.getTaggedValue(stereo2, "isBoolean");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'Stereo2' is not a stereotype of element", e.getMessage());
        }
    }

    @Test
    public void testUnknownTaggedValueOnStereotype() throws CException {
        CModel model = createModel();
        CStereotype stereo = model.getStereotype("ST");
        CClass cl1 = model.getClass("CL1");
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);
        try {
            link.setTaggedValue(stereo, "isBoolean", false);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'isBoolean' unknown for stereotype 'ST'", e.getMessage());
        }

        try {
            link.getTaggedValue(stereo, "isBoolean");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'isBoolean' unknown for stereotype 'ST'", e.getMessage());
        }
    }

    @Test
    public void testStereotypeLookup() throws CException {
        CModel model = createModel();
        CClass cl1 = model.getClass("CL1");
        CAssociation association = cl1.getClassifier().getAssociationByRoleName("metaclass2");
        CStereotype stereo = model.createStereotype("Stereo", association);
        CStereotype stereo2 = model.createStereotype("Stereo2", association);
        CLink link = cl1.getLinkObjects(cl1.getClassifier().getAssociationByRoleName("metaclass2")).get(0);
        link.addStereotypeInstance(stereo);
        link.addStereotypeInstance(stereo2);

        stereo.addAttribute("isBoolean", true);
        stereo2.addAttribute("isBoolean", true);

        link.setTaggedValue("isBoolean", false);

        assertEquals(false, link.getTaggedValue("isBoolean"));
        assertEquals(false, link.getTaggedValue(stereo,"isBoolean"));
        assertEquals(true, link.getTaggedValue(stereo2,"isBoolean"));
    }




}
