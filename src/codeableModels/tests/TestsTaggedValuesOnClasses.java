package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsTaggedValuesOnClasses {

    @Test
    public void testTaggedValuesOnPrimitiveTypeAttributes() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype stereotype = model.createStereotype("ST");
        CMetaclass mcl = model.createMetaclass("MCL");
        mcl.addStereotype(stereotype);
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotype);

        stereotype.addAttribute("isBoolean", true);
        stereotype.addAttribute("intVal", 1);
        stereotype.addAttribute("longVal", (long) 100);
        stereotype.addAttribute("doubleVal", 1.1);
        stereotype.addAttribute("floatVal", (float) 1.1);
        stereotype.addAttribute("string", "abc");
        stereotype.addAttribute("char", 'a');
        stereotype.addAttribute("byte", (byte) 1);
        stereotype.addAttribute("short", (short) 2);

        assertEquals(true, cl.getTaggedValue("isBoolean"));
        assertEquals(1, cl.getTaggedValue("intVal"));
        assertEquals((long) 100, cl.getTaggedValue("longVal"));
        assertEquals(1.1, cl.getTaggedValue("doubleVal"));
        assertEquals((float) 1.1, cl.getTaggedValue("floatVal"));
        assertEquals("abc", cl.getTaggedValue("string"));
        assertEquals('a', cl.getTaggedValue("char"));
        assertEquals((byte) 1, cl.getTaggedValue("byte"));
        assertEquals((short) 2, cl.getTaggedValue("short"));

        cl.setTaggedValue("isBoolean", false);
        cl.setTaggedValue("intVal", 10);
        cl.setTaggedValue("longVal", (long) 1000);
        cl.setTaggedValue("doubleVal", 100.1);
        cl.setTaggedValue("floatVal", (float) 102.1);
        cl.setTaggedValue("string", "");
        cl.setTaggedValue("char", 'x');
        cl.setTaggedValue("byte", (byte) 15);
        cl.setTaggedValue("short", (short) 12);

        assertEquals(false, cl.getTaggedValue("isBoolean"));
        assertEquals(10, cl.getTaggedValue("intVal"));
        assertEquals((long) 1000, cl.getTaggedValue("longVal"));
        assertEquals(100.1, cl.getTaggedValue("doubleVal"));
        assertEquals((float) 102.1, cl.getTaggedValue("floatVal"));
        assertEquals("", cl.getTaggedValue("string"));
        assertEquals('x', cl.getTaggedValue("char"));
        assertEquals((byte) 15, cl.getTaggedValue("byte"));
        assertEquals((short) 12, cl.getTaggedValue("short"));
    }

    @Test
    public void testTaggedValuesOnPrimitiveTypeAttributesCreateClassAfterAttributeSetting() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereotype = model.createStereotype("ST");
        mcl.addStereotype(stereotype);

        stereotype.addAttribute("isBoolean", true);
        stereotype.addAttribute("intVal", 1);
        stereotype.addAttribute("longVal", (long) 100);
        stereotype.addAttribute("doubleVal", 1.1);
        stereotype.addAttribute("floatVal", (float) 1.1);
        stereotype.addAttribute("string", "abc");
        stereotype.addAttribute("char", 'a');
        stereotype.addAttribute("byte", (byte) 1);
        stereotype.addAttribute("short", (short) 2);

        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotype);

        assertEquals(true, cl.getTaggedValue("isBoolean"));
        assertEquals(1, cl.getTaggedValue("intVal"));
        assertEquals((long) 100, cl.getTaggedValue("longVal"));
        assertEquals(1.1, cl.getTaggedValue("doubleVal"));
        assertEquals((float) 1.1, cl.getTaggedValue("floatVal"));
        assertEquals("abc", cl.getTaggedValue("string"));
        assertEquals('a', cl.getTaggedValue("char"));
        assertEquals((byte) 1, cl.getTaggedValue("byte"));
        assertEquals((short) 2, cl.getTaggedValue("short"));
    }

    @Test
    public void testAttributeOfTaggedValueUnknown() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereotype = model.createStereotype("ST");
        mcl.addStereotype(stereotype);
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotype);

        try {
            cl.getTaggedValue("x");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'x' unknown", e.getMessage());
        }

        cl.addAttribute("isBoolean", true);
        cl.addAttribute("intVal", 1);

        try {
            cl.setTaggedValue("x", 1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'x' unknown", e.getMessage());
        }
    }

    @Test
    public void testObjectTypeTaggedValues() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereotype = model.createStereotype("ST");
        mcl.addStereotype(stereotype);
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotype);

        CClass attrType = model.createClass(mcl, "AttrType");
        CObject attrValue = model.createObject(attrType, "attrValue");

        stereotype.addAttribute("attrTypeObj", attrValue);
        stereotype.getAttribute("attrTypeObj");

        assertEquals(attrValue, cl.getTaggedValue("attrTypeObj"));
        assertEquals("attrValue", ((CObject) cl.getTaggedValue("attrTypeObj")).getName());

        CObject attrValue2 = model.createObject(attrType, "attrValue2");
        cl.setTaggedValue("attrTypeObj", attrValue2);

        assertEquals(attrValue2, cl.getTaggedValue("attrTypeObj"));
        assertEquals("attrValue2", ((CObject) cl.getTaggedValue("attrTypeObj")).getName());

        CObject nonAttrValue = model.createObject(cl, "nonAttrValue");

        try {
            cl.setTaggedValue("attrTypeObj", nonAttrValue);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("type classifier of object 'nonAttrValue' is not matching attribute type of attribute " +
                    "'attrTypeObj'", e.getMessage());
        }
    }

    @Test
    public void testAddObjectAttributeGetSetTaggedValue() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereotype = model.createStereotype("ST");
        mcl.addStereotype(stereotype);
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotype);

        CClass attrType = model.createClass(mcl, "AttrType");
        CObject attrValue = model.createObject(attrType, "attrValue");

        stereotype.addObjectAttribute("attrTypeObj", attrType).addObjectAttribute("attrTypeObj2", attrType);
        assertEquals(null, cl.getTaggedValue("attrTypeObj"));
        cl.setTaggedValue("attrTypeObj", attrValue);
        assertEquals(attrValue, cl.getTaggedValue("attrTypeObj"));
    }


    @Test
    public void testTaggedValuesOnAttributesWithNoDefaultValues() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereotype = model.createStereotype("ST");
        mcl.addStereotype(stereotype);

        stereotype.addBooleanAttribute("isBoolean");
        stereotype.addIntAttribute("intVal");
        stereotype.addLongAttribute("longVal");
        stereotype.addDoubleAttribute("doubleVal");
        stereotype.addFloatAttribute("floatVal");
        stereotype.addStringAttribute("string");
        stereotype.addCharAttribute("char");
        stereotype.addByteAttribute("byte");
        stereotype.addShortAttribute("short");
        CClass attrClass = model.createClass(mcl, "attrClass");
        stereotype.addObjectAttribute("obj1", attrClass);
        stereotype.addObjectAttribute("obj2", "attrClass");
        CEnum enumType = model.createEnum("XYEnum", Arrays.asList("X", "Y"));
        stereotype.addEnumAttribute("enum", enumType);

        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotype);

        assertEquals(null, cl.getTaggedValue("isBoolean"));
        assertEquals(null, cl.getTaggedValue("intVal"));
        assertEquals(null, cl.getTaggedValue("longVal"));
        assertEquals(null, cl.getTaggedValue("doubleVal"));
        assertEquals(null, cl.getTaggedValue("floatVal"));
        assertEquals(null, cl.getTaggedValue("string"));
        assertEquals(null, cl.getTaggedValue("char"));
        assertEquals(null, cl.getTaggedValue("byte"));
        assertEquals(null, cl.getTaggedValue("short"));
        assertEquals(null, cl.getTaggedValue("obj1"));
        assertEquals(null, cl.getTaggedValue("obj2"));
        assertEquals(null, cl.getTaggedValue("enum"));
    }


    @Test
    public void testEnumTypeTaggedValues() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereotype = model.createStereotype("ST");
        mcl.addStereotype(stereotype);
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotype);

        List<String> enumValues = Arrays.asList("A", "B", "C");
        CEnum enumObj = model.createEnum("ABCEnum", enumValues);


        assertEquals(0, stereotype.getAttributes().size());
        stereotype.addEnumAttribute("l1", enumObj).setAttributeDefaultValue("l1", "A");
        stereotype.addEnumAttribute("l2", enumObj);

        assertEquals("A", cl.getTaggedValue("l1"));
        assertEquals(null, cl.getTaggedValue("l2"));

        cl.setTaggedValue("l1", "B");
        cl.setTaggedValue("l2", "C");

        assertEquals("B", cl.getTaggedValue("l1"));
        assertEquals("C", cl.getTaggedValue("l2"));

        try {
            cl.setTaggedValue("l1", "X");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value 'X' not element of enumeration", e.getMessage());
        }
    }

    @Test
    public void testAttributeTypeCheckForTaggedValues() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereotype = model.createStereotype("ST");
        mcl.addStereotype(stereotype);
        stereotype.addBooleanAttribute("a");
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotype);


        try {
            cl.setTaggedValue("a", CodeableModels.createModel());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value for attribute 'a' is not a known attribute type", e.getMessage());
        }
        try {
            cl.setTaggedValue("a", 1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'a' does not match attribute type", e.getMessage());
        }

        stereotype.addIntAttribute("i");
        try {
            cl.setTaggedValue("i", Boolean.TRUE);
        } catch (CException e) {
            assertEquals("value type for attribute 'i' does not match attribute type", e.getMessage());
        }

        stereotype.addShortAttribute("s");
        try {
            cl.setTaggedValue("s", Boolean.TRUE);
        } catch (CException e) {
            assertEquals("value type for attribute 's' does not match attribute type", e.getMessage());
        }

        stereotype.addByteAttribute("b");
        try {
            cl.setTaggedValue("b", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'b' does not match attribute type", e.getMessage());
        }

        stereotype.addLongAttribute("l");
        try {
            cl.setTaggedValue("l", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'l' does not match attribute type", e.getMessage());
        }

        stereotype.addFloatAttribute("f");
        try {
            cl.setTaggedValue("f", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'f' does not match attribute type", e.getMessage());
        }

        stereotype.addDoubleAttribute("d");
        try {
            cl.setTaggedValue("d", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'd' does not match attribute type", e.getMessage());
        }

        CEnum enumType = model.createEnum("XYEnum", Arrays.asList("X", "Y"));
        stereotype.addEnumAttribute("e", enumType);
        try {
            cl.setTaggedValue("e", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'e' does not match attribute type", e.getMessage());
        }

        CClass attrClass = model.createClass(mcl, "AttrClass");
        CClass otherClass = model.createClass(mcl, "OtherClass");
        stereotype.addObjectAttribute("o", attrClass);
        try {
            cl.setTaggedValue("o", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'o' does not match attribute type", e.getMessage());
        }

        try {
            cl.setTaggedValue("o", otherClass);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("type classifier of object 'OtherClass' is not matching attribute type of attribute 'o'", e
                    .getMessage());
        }

    }

    @Test
    public void testDeleteAttributesSetTaggedValue() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereotype = model.createStereotype("ST");
        mcl.addStereotype(stereotype);
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotype);

        stereotype.addAttribute("isBoolean", true);
        stereotype.addAttribute("intVal", 1);

        cl.setTaggedValue("isBoolean", true);

        stereotype.deleteAttribute("isBoolean");

        cl.setTaggedValue("intVal", 1);

        try {
            cl.setTaggedValue("isBoolean", false);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'isBoolean' unknown", e.getMessage());
        }
    }

    @Test
    public void testTaggedValuesInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype top1 = model.createStereotype( "Top1");
        mcl.addStereotype(top1);
        CStereotype top2 = model.createStereotype( "Top2");
        CStereotype stereotypeA = model.createStereotype( "STA").addSuperclass("Top1").addSuperclass("Top2");
        CStereotype stereotypeSubA = model.createStereotype("SubA").addSuperclass("STA");

        top1.addAttribute("int0", 0);
        top2.addAttribute("int1", 1);
        stereotypeA.addAttribute("int2", 2);
        stereotypeSubA.addAttribute("int3", 3);

        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotypeSubA);

        assertEquals(0, cl.getTaggedValue("int0"));
        assertEquals(1, cl.getTaggedValue("int1"));
        assertEquals(2, cl.getTaggedValue("int2"));
        assertEquals(3, cl.getTaggedValue("int3"));

        assertEquals(0, cl.getTaggedValue(top1,"int0"));
        assertEquals(1, cl.getTaggedValue(top2, "int1"));
        assertEquals(2, cl.getTaggedValue(stereotypeA, "int2"));
        assertEquals(3, cl.getTaggedValue(stereotypeSubA, "int3"));

        cl.setTaggedValue("int0", 10);
        cl.setTaggedValue("int1", 11);
        cl.setTaggedValue("int2", 12);
        cl.setTaggedValue("int3", 13);

        assertEquals(10, cl.getTaggedValue("int0"));
        assertEquals(11, cl.getTaggedValue("int1"));
        assertEquals(12, cl.getTaggedValue("int2"));
        assertEquals(13, cl.getTaggedValue("int3"));

        assertEquals(10, cl.getTaggedValue(top1,"int0"));
        assertEquals(11, cl.getTaggedValue(top2, "int1"));
        assertEquals(12, cl.getTaggedValue(stereotypeA, "int2"));
        assertEquals(13, cl.getTaggedValue(stereotypeSubA, "int3"));

        cl.setTaggedValue(top1,"int0", 100);
        cl.setTaggedValue(top2,"int1", 110);
        cl.setTaggedValue(stereotypeA,"int2", 120);
        cl.setTaggedValue(stereotypeSubA,"int3", 130);

        assertEquals(100, cl.getTaggedValue("int0"));
        assertEquals(110, cl.getTaggedValue("int1"));
        assertEquals(120, cl.getTaggedValue("int2"));
        assertEquals(130, cl.getTaggedValue("int3"));

        assertEquals(100, cl.getTaggedValue(top1,"int0"));
        assertEquals(110, cl.getTaggedValue(top2, "int1"));
        assertEquals(120, cl.getTaggedValue(stereotypeA, "int2"));
        assertEquals(130, cl.getTaggedValue(stereotypeSubA, "int3"));
    }


    @Test
    public void testTaggedValuesInheritanceAfterDeleteSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype top1 = model.createStereotype( "Top1");
        mcl.addStereotype(top1);
        CStereotype top2 = model.createStereotype( "Top2");
        CStereotype stereotypeA = model.createStereotype( "STA").addSuperclass("Top1").addSuperclass("Top2");
        CStereotype stereotypeSubA = model.createStereotype("SubA").addSuperclass("STA");

        top1.addAttribute("int0", 0);
        top2.addAttribute("int1", 1);
        stereotypeA.addAttribute("int2", 2);
        stereotypeSubA.addAttribute("int3", 3);

        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotypeSubA);

        ((CClassifier) stereotypeA).deleteSuperclass(top2);

        assertEquals(0, cl.getTaggedValue("int0"));
        try {
            cl.getTaggedValue("int1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'int1' unknown", e.getMessage());
        }
        assertEquals(2, cl.getTaggedValue("int2"));
        assertEquals(3, cl.getTaggedValue("int3"));

        cl.setTaggedValue("int0", 10);
        try {
            cl.setTaggedValue("int1", 11);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'int1' unknown", e.getMessage());
        }
        cl.setTaggedValue("int2", 12);
        cl.setTaggedValue("int3", 13);
    }

    @Test
    public void testTaggedValuesInheritanceMultipleStereotypes() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype top1 = model.createStereotype( "Top1");
        mcl.addStereotype(top1);
        CStereotype top2 = model.createStereotype( "Top2");
        CStereotype stereotypeA = model.createStereotype( "STA").addSuperclass("Top1").addSuperclass("Top2");
        CStereotype stereotypeSubA = model.createStereotype("SubA").addSuperclass("STA");
        CStereotype stereotypeB = model.createStereotype( "STB").addSuperclass("Top1").addSuperclass("Top2");
        CStereotype stereotypeSubB = model.createStereotype("SubB").addSuperclass("STB");
        CStereotype stereotypeC = model.createStereotype( "STC");
        mcl.addStereotype(stereotypeC);
        CStereotype stereotypeSubC = model.createStereotype("SubC").addSuperclass("STC");
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance(stereotypeSubA);
        cl.addStereotypeInstance(stereotypeSubB);
        cl.addStereotypeInstance(stereotypeSubC);

        top1.addAttribute("int0", 0);
        top2.addAttribute("int1", 1);
        stereotypeA.addAttribute("int2", 2);
        stereotypeSubA.addAttribute("int3", 3);
        stereotypeB.addAttribute("int4", 4);
        stereotypeSubB.addAttribute("int5", 5);
        stereotypeC.addAttribute("int6", 6);
        stereotypeSubC.addAttribute("int7", 7);

        assertEquals(0, cl.getTaggedValue("int0"));
        assertEquals(1, cl.getTaggedValue("int1"));
        assertEquals(2, cl.getTaggedValue("int2"));
        assertEquals(3, cl.getTaggedValue("int3"));
        assertEquals(4, cl.getTaggedValue("int4"));
        assertEquals(5, cl.getTaggedValue("int5"));
        assertEquals(6, cl.getTaggedValue("int6"));
        assertEquals(7, cl.getTaggedValue("int7"));

        assertEquals(0, cl.getTaggedValue(top1,"int0"));
        assertEquals(1, cl.getTaggedValue(top2, "int1"));
        assertEquals(2, cl.getTaggedValue(stereotypeA, "int2"));
        assertEquals(3, cl.getTaggedValue(stereotypeSubA, "int3"));
        assertEquals(4, cl.getTaggedValue(stereotypeB, "int4"));
        assertEquals(5, cl.getTaggedValue(stereotypeSubB, "int5"));
        assertEquals(6, cl.getTaggedValue(stereotypeC, "int6"));
        assertEquals(7, cl.getTaggedValue(stereotypeSubC, "int7"));

        cl.setTaggedValue("int0", 10);
        cl.setTaggedValue("int1", 11);
        cl.setTaggedValue("int2", 12);
        cl.setTaggedValue("int3", 13);
        cl.setTaggedValue("int4", 14);
        cl.setTaggedValue("int5", 15);
        cl.setTaggedValue("int6", 16);
        cl.setTaggedValue("int7", 17);

        assertEquals(10, cl.getTaggedValue("int0"));
        assertEquals(11, cl.getTaggedValue("int1"));
        assertEquals(12, cl.getTaggedValue("int2"));
        assertEquals(13, cl.getTaggedValue("int3"));
        assertEquals(14, cl.getTaggedValue("int4"));
        assertEquals(15, cl.getTaggedValue("int5"));
        assertEquals(16, cl.getTaggedValue("int6"));
        assertEquals(17, cl.getTaggedValue("int7"));
    }

    @Test
    public void testTaggedValuesSameNameInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype top1 = model.createStereotype( "Top1");
        mcl.addStereotype(top1);
        CStereotype top2 = model.createStereotype( "Top2");
        CStereotype stereotypeA = model.createStereotype( "STA").addSuperclass("Top1").addSuperclass("Top2");
        CStereotype stereotypeSubA = model.createStereotype("SubA").addSuperclass("STA");

        top1.addAttribute("int", 0);
        top2.addAttribute("int", 1);
        stereotypeA.addAttribute("int", 2);
        stereotypeSubA.addAttribute("int", 3);

        CClass cl1 = model.createClass(mcl, "C1");
        cl1.addStereotypeInstance(stereotypeSubA);
        CClass cl2 = model.createClass(mcl, "C2");
        cl2.addStereotypeInstance(stereotypeA);
        CClass cl3 = model.createClass(mcl, "C3");
        cl3.addStereotypeInstance(top1);

        assertEquals(3, cl1.getTaggedValue("int"));
        assertEquals(2, cl2.getTaggedValue("int"));
        assertEquals(0, cl3.getTaggedValue("int"));

        assertEquals(3, cl1.getTaggedValue(stereotypeSubA, "int"));
        assertEquals(2, cl1.getTaggedValue(stereotypeA, "int"));
        assertEquals(1, cl1.getTaggedValue(top2, "int"));
        assertEquals(0, cl1.getTaggedValue(top1, "int"));
        assertEquals(2, cl2.getTaggedValue(stereotypeA, "int"));
        assertEquals(1, cl2.getTaggedValue(top2, "int"));
        assertEquals(0, cl2.getTaggedValue(top1, "int"));
        assertEquals(0, cl3.getTaggedValue(top1,"int"));

        cl1.setTaggedValue("int", 10);
        cl2.setTaggedValue("int", 11);
        cl3.setTaggedValue("int", 12);

        assertEquals(10, cl1.getTaggedValue("int"));
        assertEquals(11, cl2.getTaggedValue("int"));
        assertEquals(12, cl3.getTaggedValue("int"));

        assertEquals(10, cl1.getTaggedValue(stereotypeSubA, "int"));
        assertEquals(2, cl1.getTaggedValue(stereotypeA, "int"));
        assertEquals(1, cl1.getTaggedValue(top2, "int"));
        assertEquals(0, cl1.getTaggedValue(top1, "int"));
        assertEquals(11, cl2.getTaggedValue(stereotypeA, "int"));
        assertEquals(1, cl2.getTaggedValue(top2, "int"));
        assertEquals(0, cl2.getTaggedValue(top1, "int"));
        assertEquals(12, cl3.getTaggedValue(top1,"int"));

        cl1.setTaggedValue(stereotypeSubA,"int", 130);
        cl1.setTaggedValue(top1,"int", 100);
        cl1.setTaggedValue(top2,"int", 110);
        cl1.setTaggedValue(stereotypeA,"int", 120);

        assertEquals(130, cl1.getTaggedValue("int"));

        assertEquals(100, cl1.getTaggedValue(top1,"int"));
        assertEquals(110, cl1.getTaggedValue(top2, "int"));
        assertEquals(120, cl1.getTaggedValue(stereotypeA, "int"));
        assertEquals(130, cl1.getTaggedValue(stereotypeSubA, "int"));
    }

    @Test
    public void testSetAndDeleteTaggedValues() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereo = model.createStereotype("Stereo");
        mcl.addStereotype(stereo);
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance("Stereo");
        stereo.addAttribute("isBoolean", true);
        stereo.addAttribute("intVal", 1);

        cl.setTaggedValue("isBoolean", true);
        cl.setTaggedValue("intVal", 1);

        assertEquals(true, cl.getTaggedValue("isBoolean"));
        assertEquals(1, cl.getTaggedValue("intVal"));

        stereo.deleteAttribute("isBoolean");

        assertEquals(1, cl.getTaggedValue("intVal"));
        cl.setTaggedValue("intVal", 100);
        assertEquals(100, cl.getTaggedValue("intVal"));

        try {
            cl.setAttributeValue("intVal", 3);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'intVal' unknown for object 'C'", e.getMessage());
        }

        try {
            cl.setTaggedValue("isBoolean", false);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'isBoolean' unknown", e.getMessage());
        }
    }

    @Test
    public void testSetAndGetTaggedValuesWithStereotypeSpecified() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereo = model.createStereotype("Stereo");
        mcl.addStereotype(stereo);
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance("Stereo");
        stereo.addAttribute("isBoolean", true);
        stereo.addAttribute("intVal", 1);

        cl.setTaggedValue(stereo,"isBoolean", true);
        cl.setTaggedValue(stereo,"intVal", 1);

        assertEquals(true, cl.getTaggedValue(stereo,"isBoolean"));
        assertEquals(1, cl.getTaggedValue(stereo,"intVal"));
    }

    @Test
    public void testWrongStereotypeInTaggedValue() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereo = model.createStereotype("Stereo");
        CStereotype stereo2 = model.createStereotype("Stereo2");
        mcl.addStereotype(stereo);
        mcl.addStereotype(stereo2);
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance("Stereo");

        stereo.addAttribute("isBoolean", true);
        stereo2.addAttribute("isBoolean", true);

        cl.setTaggedValue(stereo, "isBoolean", false);

        try {
            cl.setTaggedValue(stereo2, "isBoolean", false);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'Stereo2' is not a stereotype of element", e.getMessage());
        }

        assertEquals(false, cl.getTaggedValue(stereo, "isBoolean"));

        try {
            cl.getTaggedValue(stereo2, "isBoolean");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("stereotype 'Stereo2' is not a stereotype of element", e.getMessage());
        }
    }

    @Test
    public void testUnknownTaggedValueOnStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereo = model.createStereotype("Stereo");
        mcl.addStereotype(stereo);
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance("Stereo");
        try {
            cl.setTaggedValue(stereo, "isBoolean", false);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'isBoolean' unknown for stereotype 'Stereo'", e.getMessage());
        }

        try {
            cl.getTaggedValue(stereo, "isBoolean");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("tagged value 'isBoolean' unknown for stereotype 'Stereo'", e.getMessage());
        }
    }

    @Test
    public void testStereotypeLookup() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CStereotype stereo = model.createStereotype("Stereo");
        CStereotype stereo2 = model.createStereotype("Stereo2");
        mcl.addStereotype(stereo);
        mcl.addStereotype(stereo2);
        CClass cl = model.createClass(mcl, "C");
        cl.addStereotypeInstance("Stereo");
        cl.addStereotypeInstance("Stereo2");

        stereo.addAttribute("isBoolean", true);
        stereo2.addAttribute("isBoolean", true);

        cl.setTaggedValue("isBoolean", false);

        assertEquals(false, cl.getTaggedValue("isBoolean"));
        assertEquals(false, cl.getTaggedValue(stereo,"isBoolean"));
        assertEquals(true, cl.getTaggedValue(stereo2,"isBoolean"));
    }

}
