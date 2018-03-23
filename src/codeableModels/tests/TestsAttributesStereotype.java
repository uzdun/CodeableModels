package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsAttributesStereotype {

    /* Attribute on a stereotype are used as tagged values on CObjects */

    @Test
    public void testPrimitiveTypeAttributesStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype stereo = model.createStereotype("ST");
        stereo.addAttribute("isBoolean", true);
        stereo.addAttribute("intVal", 1);
        stereo.addAttribute("longVal", (long) 100);
        stereo.addAttribute("doubleVal", 1.1);
        stereo.addAttribute("floatVal", (float) 1.1);
        stereo.addAttribute("string", "abc");
        stereo.addAttribute("char", 'a');
        stereo.addAttribute("byte", (byte) 1);
        stereo.addAttribute("short", (short) 2);

        try {
            stereo.addAttribute("isBoolean", true);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'isBoolean' cannot be created, attribute name already exists", e.getMessage());
        }


        List<CAttribute> attributes = stereo.getAttributes();
        List<String> attributeNames = stereo.getAttributeNames();

        assertEquals(9, attributes.size());
        assertEquals(9, attributeNames.size());

        assertTrue(attributeNames.contains("isBoolean"));
        assertTrue(attributeNames.contains("intVal"));
        assertTrue(attributeNames.contains("longVal"));
        assertTrue(attributeNames.contains("doubleVal"));
        assertTrue(attributeNames.contains("floatVal"));
        assertTrue(attributeNames.contains("string"));
        assertTrue(attributeNames.contains("char"));
        assertTrue(attributeNames.contains("byte"));
        assertTrue(attributeNames.contains("short"));

        CAttribute a0 = stereo.getAttribute("X");
        CAttribute a1 = stereo.getAttribute("isBoolean");
        CAttribute a2 = stereo.getAttribute("intVal");
        CAttribute a3 = stereo.getAttribute("longVal");
        CAttribute a4 = stereo.getAttribute("doubleVal");
        CAttribute a5 = stereo.getAttribute("floatVal");
        CAttribute a6 = stereo.getAttribute("string");
        CAttribute a7 = stereo.getAttribute("char");
        CAttribute a8 = stereo.getAttribute("byte");
        CAttribute a9 = stereo.getAttribute("short");

        assertEquals(null, a0);

        assertTrue(attributes.contains(a1));
        assertTrue(attributes.contains(a2));
        assertTrue(attributes.contains(a3));
        assertTrue(attributes.contains(a4));
        assertTrue(attributes.contains(a5));
        assertTrue(attributes.contains(a6));
        assertTrue(attributes.contains(a7));
        assertTrue(attributes.contains(a8));
        assertTrue(attributes.contains(a9));

        assertEquals("Boolean", a1.getType());
        assertEquals("Int", a2.getType());
        assertEquals("Long", a3.getType());
        assertEquals("Double", a4.getType());
        assertEquals("Float", a5.getType());
        assertEquals("String", a6.getType());
        assertEquals("Char", a7.getType());
        assertEquals("Byte", a8.getType());
        assertEquals("Short", a9.getType());


        Object d1 = a1.getDefaultValue();
        Object d2 = a2.getDefaultValue();
        Object d3 = a3.getDefaultValue();
        Object d4 = a4.getDefaultValue();
        Object d5 = a5.getDefaultValue();
        Object d6 = a6.getDefaultValue();
        Object d7 = a7.getDefaultValue();
        Object d8 = a8.getDefaultValue();
        Object d9 = a9.getDefaultValue();

        assertTrue(d1 instanceof Boolean);
        assertTrue(d2 instanceof Integer);
        assertTrue(d3 instanceof Long);
        assertTrue(d4 instanceof Double);
        assertTrue(d5 instanceof Float);
        assertTrue(d6 instanceof String);
        assertTrue(d7 instanceof Character);
        assertTrue(d8 instanceof Byte);
        assertTrue(d9 instanceof Short);

        assertEquals(true, d1);
        assertEquals(1, ((Integer) d2).intValue());
        assertEquals(100, ((Long) d3).longValue());
        assertEquals(1.1, (Double) d4, 0.001);
        assertEquals(1.1, (Float) d5, 0.001);
        assertEquals("abc", d6);
        assertEquals('a', ((Character) d7).charValue());
        assertEquals(1, ((Byte) d8).byteValue());
        assertEquals(2, ((Short) d9).shortValue());
    }

    @Test
    public void testObjectTypeAttributeStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype stereo = model.createStereotype("ST");
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass attrType = model.createClass(mcl, "AttrType");
        CObject attrValue = model.createObject(attrType, "attrValue");

        stereo.addAttribute("attrTypeObj", attrValue);
        CAttribute objAttr = stereo.getAttribute("attrTypeObj");
        List<CAttribute> attributes = stereo.getAttributes();

        assertEquals(1, attributes.size());
        assertTrue(attributes.contains(objAttr));

        stereo.addAttribute("isBoolean", true);

        attributes = stereo.getAttributes();

        assertEquals(2, attributes.size());
        objAttr = stereo.getAttribute("attrTypeObj");
        assertTrue(attributes.contains(objAttr));

        assertEquals("Object", objAttr.getType());

        Object d1 = objAttr.getDefaultValue();

        assertTrue(d1 instanceof CObject);

        CObject value = (CObject) d1;

        assertEquals(attrValue, value);
    }

    @Test
    public void testEnumTypeAttributeStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype stereotype = model.createStereotype("ST");

        List<String> enumValues = Arrays.asList("A", "B", "C");
        CEnum enumObj = model.createEnum("ABCEnum", enumValues);
        assertEquals(0, stereotype.getAttributes().size());

        assertEquals(false, enumObj.isLegalValue("X"));
        assertEquals(true, enumObj.isLegalValue("A"));

        stereotype.addEnumAttribute("letters", enumObj).setAttributeDefaultValue("letters", "A");
        stereotype.addEnumAttribute("letters2", enumObj);

        CAttribute enumAttr = stereotype.getAttribute("letters");
        CAttribute enumAttr2 = stereotype.getAttribute("letters2");
        List<CAttribute> attributes = stereotype.getAttributes();

        assertEquals(2, attributes.size());
        assertTrue(attributes.contains(enumAttr));

        stereotype.addAttribute("isBoolean", true);

        attributes = stereotype.getAttributes();

        assertEquals(3, attributes.size());
        enumAttr = stereotype.getAttribute("letters");
        assertTrue(attributes.contains(enumAttr));

        assertEquals("Enum", enumAttr.getType());

        Object d1 = enumAttr.getDefaultValue();
        Object d2 = enumAttr2.getDefaultValue();

        assertEquals("A", d1);
        assertEquals(null, d2);

        try {
            stereotype.addEnumAttribute("letters3", enumObj).setAttributeDefaultValue("letters3", "X");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value 'X' not element of enumeration", e.getMessage());
        }
    }


    @Test
    public void testSetAttributeDefaultValueStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype stereotype = model.createStereotype("ST");

        List<String> enumValues = Arrays.asList("A", "B", "C");
        CEnum enumObj = model.createEnum("ABCEnum", enumValues);

        stereotype.addEnumAttribute("letters", enumObj);
        stereotype.addBooleanAttribute("b");

        try {
            stereotype.setAttributeDefaultValue("x", "A");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("unknown attribute name 'x' on classifier 'ST'", e.getMessage());
        }
        stereotype.setAttributeDefaultValue("letters", "A");
        stereotype.setAttributeDefaultValue("b", true);

        Object d1 = stereotype.getAttribute("letters").getDefaultValue();
        Object d2 = stereotype.getAttribute("b").getDefaultValue();

        assertEquals("A", d1);
        assertEquals(true, d2);

    }

    @Test
    public void testAttributeTypeCheckMetaclassStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype stereotype = model.createStereotype("ST");
        stereotype.addBooleanAttribute("a");
        CAttribute attr = stereotype.getAttribute("a");
        try {
            attr.setDefaultValue(CodeableModels.createModel());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value for attribute 'a' is not a known attribute type", e.getMessage());
        }
        try {
            attr.setDefaultValue(1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'a' does not match attribute type", e.getMessage());
        }

        stereotype.addIntAttribute("i");
        attr = stereotype.getAttribute("i");
        try {
            attr.setDefaultValue(Boolean.TRUE);
        } catch (CException e) {
            assertEquals("value type for attribute 'i' does not match attribute type", e.getMessage());
        }

        stereotype.addShortAttribute("s");
        attr = stereotype.getAttribute("s");
        try {
            attr.setDefaultValue(Boolean.TRUE);
        } catch (CException e) {
            assertEquals("value type for attribute 's' does not match attribute type", e.getMessage());
        }

        stereotype.addByteAttribute("b");
        attr = stereotype.getAttribute("b");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'b' does not match attribute type", e.getMessage());
        }

        stereotype.addLongAttribute("l");
        attr = stereotype.getAttribute("l");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'l' does not match attribute type", e.getMessage());
        }

        stereotype.addFloatAttribute("f");
        attr = stereotype.getAttribute("f");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'f' does not match attribute type", e.getMessage());
        }

        stereotype.addDoubleAttribute("d");
        attr = stereotype.getAttribute("d");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'd' does not match attribute type", e.getMessage());
        }

        CEnum enumType = model.createEnum("XYEnum", Arrays.asList("X", "Y"));
        stereotype.addEnumAttribute("e", enumType);
        attr = stereotype.getAttribute("e");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'e' does not match attribute type", e.getMessage());
        }

        CMetaclass mcl = model.createMetaclass("MCL");
        CClass attrClass = model.createClass(mcl, "AttrClass");
        CClass otherClass = model.createClass(mcl, "OtherClass");
        stereotype.addObjectAttribute("o", attrClass);
        attr = stereotype.getAttribute("o");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'o' does not match attribute type", e.getMessage());
        }

        try {
            attr.setDefaultValue(otherClass);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("type classifier of object 'OtherClass' is not matching attribute type of attribute 'o'", e.getMessage());
        }

    }

    @Test
    public void testCreateAndDeleteAttributesStereotype() throws CException {
        CModel model = CodeableModels.createModel();
        CStereotype stereo = model.createStereotype("Stereo");
        stereo.addAttribute("isBoolean", true);
        stereo.addAttribute("intVal", 1);
        stereo.addAttribute("longVal", (long) 100);
        stereo.addAttribute("doubleVal", 1.1);
        stereo.addAttribute("floatVal", (float) 1.1);
        stereo.addAttribute("string", "abc");
        stereo.addAttribute("char", 'a');
        stereo.addAttribute("byte", (byte) 1);
        stereo = stereo.addAttribute("short", (short) 2);

        try {
            stereo.deleteAttribute("X");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'X' to be deleted not defined on classifier 'Stereo'", e.getMessage());
        }

        stereo = stereo.deleteAttribute("isBoolean").deleteAttribute("doubleVal").deleteAttribute("short").deleteAttribute("byte");

        List<CAttribute> attributes = stereo.getAttributes();
        List<String> attributeNames = stereo.getAttributeNames();

        assertEquals(5, attributes.size());
        assertEquals(5, attributeNames.size());

        assertTrue(attributeNames.contains("intVal"));
        assertTrue(attributeNames.contains("longVal"));
        assertTrue(attributeNames.contains("floatVal"));
        assertTrue(attributeNames.contains("string"));
        assertTrue(attributeNames.contains("char"));

        model = CodeableModels.createModel();
        stereo = model.createStereotype("Stereo");
        stereo.addAttribute("isBoolean", true);

        stereo.deleteAttribute("isBoolean");

        attributes = stereo.getAttributes();
        attributeNames = stereo.getAttributeNames();

        assertEquals(0, attributes.size());
        assertEquals(0, attributeNames.size());
    }


}
