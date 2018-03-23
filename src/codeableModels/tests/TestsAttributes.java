package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsAttributes {

    @Test
    public void testPrimitiveTypeAttributes() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl = model.createClass(mcl, "C");
        cl.addAttribute("isBoolean", true);
        cl.addAttribute("intVal", 1);
        cl.addAttribute("longVal", (long) 100);
        cl.addAttribute("doubleVal", 1.1);
        cl.addAttribute("floatVal", (float) 1.1);
        cl.addAttribute("string", "abc");
        cl.addAttribute("char", 'a');
        cl.addAttribute("byte", (byte) 1);
        cl.addAttribute("short", (short) 2);

        try {
            cl.addAttribute("isBoolean", true);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'isBoolean' cannot be created, attribute name already exists", e.getMessage());
        }

        List<CAttribute> attributes = cl.getAttributes();
        List<String> attributeNames = cl.getAttributeNames();

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

        CAttribute a0 = cl.getAttribute("X");
        CAttribute a1 = cl.getAttribute("isBoolean");
        CAttribute a2 = cl.getAttribute("intVal");
        CAttribute a3 = cl.getAttribute("longVal");
        CAttribute a4 = cl.getAttribute("doubleVal");
        CAttribute a5 = cl.getAttribute("floatVal");
        CAttribute a6 = cl.getAttribute("string");
        CAttribute a7 = cl.getAttribute("char");
        CAttribute a8 = cl.getAttribute("byte");
        CAttribute a9 = cl.getAttribute("short");

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
    public void testObjectTypeAttribute() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass attrType = model.createClass(mcl, "AttrType");
        CObject attrValue = model.createObject(attrType, "attrValue");

        CClassifier cl = model.createClass(mcl, "C");

        cl.addAttribute("attrTypeObj", attrValue);
        CAttribute objAttr = cl.getAttribute("attrTypeObj");
        List<CAttribute> attributes = cl.getAttributes();

        assertEquals(1, attributes.size());
        assertTrue(attributes.contains(objAttr));

        cl.addAttribute("isBoolean", true);

        attributes = cl.getAttributes();

        assertEquals(2, attributes.size());
        objAttr = cl.getAttribute("attrTypeObj");
        assertTrue(attributes.contains(objAttr));

        assertEquals("Object", objAttr.getType());

        Object d1 = objAttr.getDefaultValue();

        assertTrue(d1 instanceof CObject);

        CObject value = (CObject) d1;

        assertEquals(attrValue, value);
    }


    @Test
    public void testEnumGetValues() throws CException {
        CModel model = CodeableModels.createModel();
        List<String> enumValues = Arrays.asList("A", "B", "C");
        CEnum enumObj = model.createEnum("ABCEnum", enumValues);
        assertEquals(Arrays.asList("A", "B", "C"), enumObj.getValues());
    }

    @Test
    public void testEnumGetName() throws CException {
        CModel model = CodeableModels.createModel();
        List<String> enumValues = Arrays.asList("A", "B", "C");
        CEnum enumObj = model.createEnum("ABCEnum", enumValues);
        assertEquals("ABCEnum", enumObj.getName());
    }

    @Test
    public void testEnumTypeAttribute() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");

        List<String> enumValues = Arrays.asList("A", "B", "C");
        CEnum enumObj = model.createEnum("ABCEnum", enumValues);
        CClassifier cl = model.createClass(mcl, "C");
        assertEquals(0, cl.getAttributes().size());

        assertEquals(false, enumObj.isLegalValue("X"));
        assertEquals(true, enumObj.isLegalValue("A"));

        cl.addEnumAttribute("letters", enumObj).setAttributeDefaultValue("letters", "A");
        cl.addEnumAttribute("letters2", enumObj);

        CAttribute enumAttr = cl.getAttribute("letters");
        CAttribute enumAttr2 = cl.getAttribute("letters2");
        List<CAttribute> attributes = cl.getAttributes();

        assertEquals(2, attributes.size());
        assertTrue(attributes.contains(enumAttr));

        cl.addAttribute("isBoolean", true);

        attributes = cl.getAttributes();

        assertEquals(3, attributes.size());
        enumAttr = cl.getAttribute("letters");
        assertTrue(attributes.contains(enumAttr));

        assertEquals("Enum", enumAttr.getType());

        assertEquals(enumObj, enumAttr.getEnumType());

        Object d1 = enumAttr.getDefaultValue();
        Object d2 = enumAttr2.getDefaultValue();

        assertEquals("A", d1);
        assertEquals(null, d2);

        try {
            cl.addEnumAttribute("letters3", enumObj).setAttributeDefaultValue("letters3", "X");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value 'X' not element of enumeration", e.getMessage());
        }
    }


    @Test
    public void testSetAttributeDefaultValue() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");

        List<String> enumValues = Arrays.asList("A", "B", "C");
        CEnum enumObj = model.createEnum("ABCEnum", enumValues);
        CClassifier cl = model.createClass(mcl, "C");

        cl.addEnumAttribute("letters", enumObj);
        cl.addBooleanAttribute("b");

        try {
            cl.setAttributeDefaultValue("x", "A");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("unknown attribute name 'x' on classifier 'C'", e.getMessage());
        }
        cl.setAttributeDefaultValue("letters", "A");
        cl.setAttributeDefaultValue("b", true);

        Object d1 = cl.getAttribute("letters").getDefaultValue();
        Object d2 = cl.getAttribute("b").getDefaultValue();

        assertEquals("A", d1);
        assertEquals(true, d2);

    }

    @Test
    public void testAttributeTypeCheck() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier cl = model.createClass(mcl, "C");
        cl.addBooleanAttribute("a");
        CAttribute attr = cl.getAttribute("a");
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

        cl.addIntAttribute("i");
        attr = cl.getAttribute("i");
        try {
            attr.setDefaultValue(Boolean.TRUE);
        } catch (CException e) {
            assertEquals("value type for attribute 'i' does not match attribute type", e.getMessage());
        }

        cl.addShortAttribute("s");
        attr = cl.getAttribute("s");
        try {
            attr.setDefaultValue(Boolean.TRUE);
        } catch (CException e) {
            assertEquals("value type for attribute 's' does not match attribute type", e.getMessage());
        }

        cl.addByteAttribute("b");
        attr = cl.getAttribute("b");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'b' does not match attribute type", e.getMessage());
        }

        cl.addLongAttribute("l");
        attr = cl.getAttribute("l");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'l' does not match attribute type", e.getMessage());
        }

        cl.addFloatAttribute("f");
        attr = cl.getAttribute("f");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'f' does not match attribute type", e.getMessage());
        }

        cl.addDoubleAttribute("d");
        attr = cl.getAttribute("d");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'd' does not match attribute type", e.getMessage());
        }

        cl.addStringAttribute("st");
        attr = cl.getAttribute("st");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'st' does not match attribute type", e.getMessage());
        }

        cl.addCharAttribute("ch");
        attr = cl.getAttribute("ch");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'ch' does not match attribute type", e.getMessage());
        }

        CEnum enumType = model.createEnum("XYEnum", Arrays.asList("X", "Y"));
        cl.addEnumAttribute("e", enumType);
        attr = cl.getAttribute("e");
        try {
            attr.setDefaultValue(Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'e' does not match attribute type", e.getMessage());
        }

        CClass attrClass = model.createClass(mcl, "AttrClass");
        CClass otherClass = model.createClass(mcl, "OtherClass");
        cl.addObjectAttribute("o", attrClass);
        attr = cl.getAttribute("o");
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
    public void testDeleteAttributes() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl = model.createClass(mcl, "C");
        cl.addAttribute("isBoolean", true);
        cl.addAttribute("intVal", 1);
        cl.addAttribute("longVal", (long) 100);
        cl.addAttribute("doubleVal", 1.1);
        cl.addAttribute("floatVal", (float) 1.1);
        cl.addAttribute("string", "abc");
        cl.addAttribute("char", 'a');
        cl.addAttribute("byte", (byte) 1);
        cl = cl.addAttribute("short", (short) 2);

        try {
            cl.deleteAttribute("X");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'X' to be deleted not defined on classifier 'C'", e.getMessage());
        }

        cl.deleteAttribute("isBoolean").deleteAttribute("doubleVal").deleteAttribute("short").deleteAttribute("byte");

        List<CAttribute> attributes = cl.getAttributes();
        List<String> attributeNames = cl.getAttributeNames();

        assertEquals(5, attributes.size());
        assertEquals(5, attributeNames.size());

        assertTrue(attributeNames.contains("intVal"));
        assertTrue(attributeNames.contains("longVal"));
        assertTrue(attributeNames.contains("floatVal"));
        assertTrue(attributeNames.contains("string"));
        assertTrue(attributeNames.contains("char"));

        model = CodeableModels.createModel();
        cl = model.createClass(mcl, "C");
        cl = cl.addAttribute("isBoolean", true);

        cl.deleteAttribute("isBoolean");

        attributes = cl.getAttributes();
        attributeNames = cl.getAttributeNames();

        assertEquals(0, attributes.size());
        assertEquals(0, attributeNames.size());
    }
}
