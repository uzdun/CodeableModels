package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsAttributeValues {

    @Test
    public void testValuesOnPrimitiveTypeAttributes() throws CException {
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
        cl.addAttribute("short", (short) 2);

        CObject obj = model.createObject(cl, "o");

        assertEquals(true, obj.getAttributeValue("isBoolean"));
        assertEquals(1, obj.getAttributeValue("intVal"));
        assertEquals((long) 100, obj.getAttributeValue("longVal"));
        assertEquals(1.1, obj.getAttributeValue("doubleVal"));
        assertEquals((float) 1.1, obj.getAttributeValue("floatVal"));
        assertEquals("abc", obj.getAttributeValue("string"));
        assertEquals('a', obj.getAttributeValue("char"));
        assertEquals((byte) 1, obj.getAttributeValue("byte"));
        assertEquals((short) 2, obj.getAttributeValue("short"));

        obj.setAttributeValue("isBoolean", false);
        obj.setAttributeValue("intVal", 10);
        obj.setAttributeValue("longVal", (long) 1000);
        obj.setAttributeValue("doubleVal", 100.1);
        obj.setAttributeValue("floatVal", (float) 102.1);
        obj.setAttributeValue("string", "");
        obj.setAttributeValue("char", 'x');
        obj.setAttributeValue("byte", (byte) 15);
        obj.setAttributeValue("short", (short) 12);

        assertEquals(false, obj.getAttributeValue("isBoolean"));
        assertEquals(10, obj.getAttributeValue("intVal"));
        assertEquals((long) 1000, obj.getAttributeValue("longVal"));
        assertEquals(100.1, obj.getAttributeValue("doubleVal"));
        assertEquals((float) 102.1, obj.getAttributeValue("floatVal"));
        assertEquals("", obj.getAttributeValue("string"));
        assertEquals('x', obj.getAttributeValue("char"));
        assertEquals((byte) 15, obj.getAttributeValue("byte"));
        assertEquals((short) 12, obj.getAttributeValue("short"));
    }

    @Test
    public void testAttributeOfValueUnknown() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl = model.createClass(mcl, "C");
        CObject obj = model.createObject(cl, "o");

        try {
            obj.getAttributeValue("x");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'x' unknown for object 'o'", e.getMessage());
        }

        cl.addAttribute("isBoolean", true);
        cl.addAttribute("intVal", 1);

        try {
            obj.setAttributeValue("x", 1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'x' unknown for object 'o'", e.getMessage());
        }
    }

    @Test
    public void testObjectTypeAttributeValues() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass attrType = model.createClass(mcl, "AttrType");
        CObject attrValue = model.createObject(attrType, "attrValue");

        CClass cl = model.createClass(mcl, "C");

        cl.addAttribute("attrTypeObj", attrValue);
        CAttribute attribute = cl.getAttribute("attrTypeObj");

        CObject obj = model.createObject(cl, "o");

        assertEquals(attrValue, obj.getAttributeValue("attrTypeObj"));
        assertEquals("attrValue", ((CObject) obj.getAttributeValue("attrTypeObj")).getName());

        CObject attrValue2 = model.createObject(attrType, "attrValue2");
        obj.setAttributeValue("attrTypeObj", attrValue2);

        assertEquals(attrValue2, obj.getAttributeValue("attrTypeObj"));
        assertEquals("attrValue2", ((CObject) obj.getAttributeValue("attrTypeObj")).getName());

        CObject nonAttrValue = model.createObject(cl, "nonAttrValue");

        try {
            obj.setAttributeValue("attrTypeObj", nonAttrValue);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("type classifier of object 'nonAttrValue' is not matching attribute type of attribute " +
                    "'attrTypeObj'", e.getMessage());
        }

        assertEquals(attrType, attribute.getTypeClassifier());
    }

    @Test
    public void testAddObjectAttributeGetSetValue() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass attrType = model.createClass(mcl, "AttrType");
        CObject attrValue = model.createObject(attrType, "attrValue");
        CClass cl = model.createClass(mcl, "C");
        CClass cl2 = model.createClass(mcl, "C2");
        CObject obj = model.createObject(cl, "o");
        CObject obj2 = model.createObject(cl, "o2");

        cl.addObjectAttribute("attrTypeObj", attrType).addObjectAttribute("attrTypeObj2", "AttrType");
        // test the super-interface on CClassifier method directly for once
        ((CClassifier) cl2).addObjectAttribute("attrTypeObj", attrType).addObjectAttribute("attrTypeObj2", "AttrType");

        assertEquals(null, obj.getAttributeValue("attrTypeObj"));
        assertEquals(null, obj2.getAttributeValue("attrTypeObj"));

        obj.setAttributeValue("attrTypeObj", attrValue);
        obj2.setAttributeValue("attrTypeObj", attrValue);
        assertEquals(attrValue, obj.getAttributeValue("attrTypeObj"));
        assertEquals(attrValue, obj2.getAttributeValue("attrTypeObj"));
    }

    @Test
    public void testAddObjectAttributeGetSetValueWithStringClassifier() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass attrType = model.createClass(mcl, "AttrType");
        CObject attrValue = model.createObject(attrType, "attrValue");
        CClass cl = model.createClass(mcl, "C");
        CObject obj = model.createObject(cl, "o");

        cl.addObjectAttribute("attrTypeObj", "AttrType");
        assertEquals(null, obj.getAttributeValue("attrTypeObj"));
        obj.setAttributeValue("attrTypeObj", attrValue);
        assertEquals(attrValue, obj.getAttributeValue("attrTypeObj"));
    }

    @Test
    public void testValuesOnAttributesWithNoDefaultValues() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl = model.createClass(mcl, "C");
        cl.addBooleanAttribute("isBoolean");
        cl.addIntAttribute("intVal");
        cl.addLongAttribute("longVal");
        cl.addDoubleAttribute("doubleVal");
        cl.addFloatAttribute("floatVal");
        cl.addStringAttribute("string");
        cl.addCharAttribute("char");
        cl.addByteAttribute("byte");
        cl.addShortAttribute("short");
        CClass attrClass = model.createClass(mcl, "attrClass");
        cl.addObjectAttribute("obj1", attrClass);
        cl.addObjectAttribute("obj2", "attrClass");
        CEnum enumType = model.createEnum("XYEnum", Arrays.asList("X", "Y"));
        cl.addEnumAttribute("enum", enumType);

        CObject obj = model.createObject(cl, "o");

        assertEquals(null, obj.getAttributeValue("isBoolean"));
        assertEquals(null, obj.getAttributeValue("intVal"));
        assertEquals(null, obj.getAttributeValue("longVal"));
        assertEquals(null, obj.getAttributeValue("doubleVal"));
        assertEquals(null, obj.getAttributeValue("floatVal"));
        assertEquals(null, obj.getAttributeValue("string"));
        assertEquals(null, obj.getAttributeValue("char"));
        assertEquals(null, obj.getAttributeValue("byte"));
        assertEquals(null, obj.getAttributeValue("short"));
        assertEquals(null, obj.getAttributeValue("obj1"));
        assertEquals(null, obj.getAttributeValue("obj2"));
        assertEquals(null, obj.getAttributeValue("enum"));
    }


    @Test
    public void testEnumTypeAttributeValues() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");

        List<String> enumValues = Arrays.asList("A", "B", "C");
        CEnum enumObj = model.createEnum("ABCEnum", enumValues);

        CClass cl = model.createClass(mcl, "C");
        assertEquals(0, cl.getAttributes().size());
        cl.addEnumAttribute("l1", enumObj).setAttributeDefaultValue("l1", "A");
        cl.addEnumAttribute("l2", enumObj);
        CObject obj = model.createObject(cl, "o");

        assertEquals("A", obj.getAttributeValue("l1"));
        assertEquals(null, obj.getAttributeValue("l2"));

        obj.setAttributeValue("l1", "B");
        obj.setAttributeValue("l2", "C");

        assertEquals("B", obj.getAttributeValue("l1"));
        assertEquals("C", obj.getAttributeValue("l2"));

        try {
            obj.setAttributeValue("l1", "X");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value 'X' not element of enumeration", e.getMessage());
        }
    }

    @Test
    public void testAttributeTypeCheckForObjAttrValues() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl = model.createClass(mcl, "C");
        cl.addBooleanAttribute("a");
        CObject obj = model.createObject(cl, "o");
        try {
            obj.setAttributeValue("a", CodeableModels.createModel());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value for attribute 'a' is not a known attribute type", e.getMessage());
        }
        try {
            obj.setAttributeValue("a", 1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'a' does not match attribute type", e.getMessage());
        }

        cl.addIntAttribute("i");
        try {
            obj.setAttributeValue("i", Boolean.TRUE);
        } catch (CException e) {
            assertEquals("value type for attribute 'i' does not match attribute type", e.getMessage());
        }

        cl.addShortAttribute("s");
        try {
            obj.setAttributeValue("s", Boolean.TRUE);
        } catch (CException e) {
            assertEquals("value type for attribute 's' does not match attribute type", e.getMessage());
        }

        cl.addByteAttribute("b");
        try {
            obj.setAttributeValue("b", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'b' does not match attribute type", e.getMessage());
        }

        cl.addLongAttribute("l");
        try {
            obj.setAttributeValue("l", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'l' does not match attribute type", e.getMessage());
        }

        cl.addFloatAttribute("f");
        try {
            obj.setAttributeValue("f", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'f' does not match attribute type", e.getMessage());
        }

        cl.addDoubleAttribute("d");
        try {
            obj.setAttributeValue("d", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'd' does not match attribute type", e.getMessage());
        }

        CEnum enumType = model.createEnum("XYEnum", Arrays.asList("X", "Y"));
        cl.addEnumAttribute("e", enumType);
        try {
            obj.setAttributeValue("e", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'e' does not match attribute type", e.getMessage());
        }

        CClass attrClass = model.createClass(mcl, "AttrClass");
        CClass otherClass = model.createClass(mcl, "OtherClass");
        cl.addObjectAttribute("o", attrClass);
        try {
            obj.setAttributeValue("o", Boolean.TRUE);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("value type for attribute 'o' does not match attribute type", e.getMessage());
        }

        try {
            obj.setAttributeValue("o", otherClass);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("type classifier of object 'OtherClass' is not matching attribute type of attribute 'o'", e
                    .getMessage());
        }

    }

    @Test
    public void testDeleteAttributesSetValue() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl = model.createClass(mcl, "C");
        CObject obj = model.createObject(cl, "o");
        cl.addAttribute("isBoolean", true);
        cl.addAttribute("intVal", 1);

        obj.setAttributeValue("isBoolean", true);

        cl.deleteAttribute("isBoolean");

        try {
            obj.getAttributeValue("isBoolean");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'isBoolean' unknown for object 'o'", e.getMessage());
        }

        obj.setAttributeValue("intVal", 1);

        try {
            obj.setAttributeValue("isBoolean", false);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'isBoolean' unknown for object 'o'", e.getMessage());
        }
    }

    @Test
    public void testDeleteAttributesSetValueOnClassifier() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl = model.createClass(mcl, "C");
        CObject obj = model.createObject(cl, "o");
        cl.addAttribute("isBoolean", true);
        cl.addAttribute("intVal", 1);

        obj.setAttributeValue("isBoolean", true);

        ((CClassifier) cl).deleteAttribute("isBoolean");

        try {
            obj.getAttributeValue("isBoolean");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'isBoolean' unknown for object 'o'", e.getMessage());
        }

        obj.setAttributeValue("intVal", 1);

        try {
            obj.setAttributeValue("isBoolean", false);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'isBoolean' unknown for object 'o'", e.getMessage());
        }
    }

    @Test
    public void testAttributeValuesInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top1 = model.createClass(mcl, "Top1");
        CClass top2 = model.createClass(mcl, "Top2");
        CClass classA = model.createClass(mcl, "ClassA").addSuperclass("Top1").addSuperclass("Top2");
        CClass subclassA = model.createClass(mcl, "SubA").addSuperclass("ClassA");

        top1.addAttribute("int0", 0);
        top2.addAttribute("int1", 1);
        classA.addAttribute("int2", 2);
        subclassA.addAttribute("int3", 3);

        CObject obj = model.createObject(subclassA, "o");

        assertEquals(0, obj.getAttributeValue("int0"));
        assertEquals(1, obj.getAttributeValue("int1"));
        assertEquals(2, obj.getAttributeValue("int2"));
        assertEquals(3, obj.getAttributeValue("int3"));

        assertEquals(0, obj.getAttributeValue(top1,"int0"));
        assertEquals(1, obj.getAttributeValue(top2, "int1"));
        assertEquals(2, obj.getAttributeValue(classA, "int2"));
        assertEquals(3, obj.getAttributeValue(subclassA, "int3"));

        obj.setAttributeValue("int0", 10);
        obj.setAttributeValue("int1", 11);
        obj.setAttributeValue("int2", 12);
        obj.setAttributeValue("int3", 13);

        assertEquals(10, obj.getAttributeValue("int0"));
        assertEquals(11, obj.getAttributeValue("int1"));
        assertEquals(12, obj.getAttributeValue("int2"));
        assertEquals(13, obj.getAttributeValue("int3"));

        assertEquals(10, obj.getAttributeValue(top1,"int0"));
        assertEquals(11, obj.getAttributeValue(top2, "int1"));
        assertEquals(12, obj.getAttributeValue(classA, "int2"));
        assertEquals(13, obj.getAttributeValue(subclassA, "int3"));

        obj.setAttributeValue(top1,"int0", 100);
        obj.setAttributeValue(top2,"int1", 110);
        obj.setAttributeValue(classA,"int2", 120);
        obj.setAttributeValue(subclassA,"int3", 130);

        assertEquals(100, obj.getAttributeValue("int0"));
        assertEquals(110, obj.getAttributeValue("int1"));
        assertEquals(120, obj.getAttributeValue("int2"));
        assertEquals(130, obj.getAttributeValue("int3"));

        assertEquals(100, obj.getAttributeValue(top1,"int0"));
        assertEquals(110, obj.getAttributeValue(top2, "int1"));
        assertEquals(120, obj.getAttributeValue(classA, "int2"));
        assertEquals(130, obj.getAttributeValue(subclassA, "int3"));
    }

    @Test
    public void testAttributeValuesInheritanceAfterDeleteSuperclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top1 = model.createClass(mcl, "Top1");
        CClass top2 = model.createClass(mcl, "Top2");
        CClass classA = model.createClass(mcl, "ClassA").addSuperclass("Top1").addSuperclass("Top2");
        CClass subclassA = model.createClass(mcl, "SubA").addSuperclass("ClassA");

        top1.addAttribute("int0", 0);
        top2.addAttribute("int1", 1);
        classA.addAttribute("int2", 2);
        subclassA.addAttribute("int3", 3);

        CObject obj = model.createObject(subclassA, "o");

        ((CClassifier) classA).deleteSuperclass("Top2");

        assertEquals(0, obj.getAttributeValue("int0"));
        try {
            obj.getAttributeValue("int1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'int1' unknown for object 'o'", e.getMessage());
        }
        assertEquals(2, obj.getAttributeValue("int2"));
        assertEquals(3, obj.getAttributeValue("int3"));

        obj.setAttributeValue("int0", 10);
        try {
            obj.setAttributeValue("int1", 11);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'int1' unknown for object 'o'", e.getMessage());
        }
    }


    @Test
    public void testAttributeValuesSameNameInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass top1 = model.createClass(mcl, "Top1");
        CClass top2 = model.createClass(mcl, "Top2");
        CClass classA = model.createClass(mcl, "ClassA").addSuperclass("Top1").addSuperclass("Top2");
        CClass subclassA = model.createClass(mcl, "SubA").addSuperclass("ClassA");

        top1.addAttribute("int", 0);
        top2.addAttribute("int", 1);
        classA.addAttribute("int", 2);
        subclassA.addAttribute("int", 3);

        CObject obj1 = model.createObject(subclassA, "o1");
        CObject obj2 = model.createObject(classA, "o2");
        CObject obj3 = model.createObject(top1, "o3");

        assertEquals(3, obj1.getAttributeValue("int"));
        assertEquals(2, obj2.getAttributeValue("int"));
        assertEquals(0, obj3.getAttributeValue("int"));

        assertEquals(3, obj1.getAttributeValue(subclassA, "int"));
        assertEquals(2, obj1.getAttributeValue(classA, "int"));
        assertEquals(1, obj1.getAttributeValue(top2, "int"));
        assertEquals(0, obj1.getAttributeValue(top1, "int"));
        assertEquals(2, obj2.getAttributeValue(classA, "int"));
        assertEquals(1, obj2.getAttributeValue(top2, "int"));
        assertEquals(0, obj2.getAttributeValue(top1, "int"));
        assertEquals(0, obj3.getAttributeValue(top1,"int"));

        obj1.setAttributeValue("int", 10);
        obj2.setAttributeValue("int", 11);
        obj3.setAttributeValue("int", 12);

        assertEquals(10, obj1.getAttributeValue("int"));
        assertEquals(11, obj2.getAttributeValue("int"));
        assertEquals(12, obj3.getAttributeValue("int"));

        assertEquals(10, obj1.getAttributeValue(subclassA, "int"));
        assertEquals(2, obj1.getAttributeValue(classA, "int"));
        assertEquals(1, obj1.getAttributeValue(top2, "int"));
        assertEquals(0, obj1.getAttributeValue(top1, "int"));
        assertEquals(11, obj2.getAttributeValue(classA, "int"));
        assertEquals(1, obj2.getAttributeValue(top2, "int"));
        assertEquals(0, obj2.getAttributeValue(top1, "int"));
        assertEquals(12, obj3.getAttributeValue(top1,"int"));

        obj1.setAttributeValue(subclassA,"int", 130);
        obj1.setAttributeValue(top1,"int", 100);
        obj1.setAttributeValue(top2,"int", 110);
        obj1.setAttributeValue(classA,"int", 120);

        assertEquals(130, obj1.getAttributeValue("int"));

        assertEquals(100, obj1.getAttributeValue(top1,"int"));
        assertEquals(110, obj1.getAttributeValue(top2, "int"));
        assertEquals(120, obj1.getAttributeValue(classA, "int"));
        assertEquals(130, obj1.getAttributeValue(subclassA, "int"));
    }


    @Test
    public void testCreateAndDeleteAttributeValuesMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl = model.createClass(mcl, "C");
        mcl.addAttribute("isBoolean", true);
        mcl.addAttribute("intVal", 1);

        cl.setAttributeValue("isBoolean", true);
        cl.setAttributeValue("intVal", 1);

        assertEquals(true, cl.getAttributeValue("isBoolean"));
        assertEquals(1, cl.getAttributeValue("intVal"));

        mcl.deleteAttribute("isBoolean");

        assertEquals(1, cl.getAttributeValue("intVal"));
        cl.setAttributeValue("intVal", 100);
        assertEquals(100, cl.getAttributeValue("intVal"));

        try {
            cl.setAttributeValue("isBoolean", false);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("attribute 'isBoolean' unknown for object 'C'", e.getMessage());
        }
    }


    @Test
    public void testAttributeValuesInheritanceMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass top1 = model.createMetaclass( "Top1");
        CMetaclass top2 = model.createMetaclass("Top2");
        CMetaclass classA = model.createMetaclass( "ClassA").addSuperclass("Top1").addSuperclass("Top2");
        CMetaclass subclassA = model.createMetaclass( "SubA").addSuperclass("ClassA");

        top1.addAttribute("int0", 0);
        top2.addAttribute("int1", 1);
        classA.addAttribute("int2", 2);
        subclassA.addAttribute("int3", 3);

        CClass cl = model.createClass(subclassA, "CL");

        assertEquals(0, cl.getAttributeValue("int0"));
        assertEquals(1, cl.getAttributeValue("int1"));
        assertEquals(2, cl.getAttributeValue("int2"));
        assertEquals(3, cl.getAttributeValue("int3"));

        assertEquals(0, cl.getAttributeValue(top1,"int0"));
        assertEquals(1, cl.getAttributeValue(top2, "int1"));
        assertEquals(2, cl.getAttributeValue(classA, "int2"));
        assertEquals(3, cl.getAttributeValue(subclassA, "int3"));

        cl.setAttributeValue("int0", 10);
        cl.setAttributeValue("int1", 11);
        cl.setAttributeValue("int2", 12);
        cl.setAttributeValue("int3", 13);

        assertEquals(10, cl.getAttributeValue("int0"));
        assertEquals(11, cl.getAttributeValue("int1"));
        assertEquals(12, cl.getAttributeValue("int2"));
        assertEquals(13, cl.getAttributeValue("int3"));

        assertEquals(10, cl.getAttributeValue(top1,"int0"));
        assertEquals(11, cl.getAttributeValue(top2, "int1"));
        assertEquals(12, cl.getAttributeValue(classA, "int2"));
        assertEquals(13, cl.getAttributeValue(subclassA, "int3"));

        cl.setAttributeValue(top1,"int0", 100);
        cl.setAttributeValue(top2,"int1", 110);
        cl.setAttributeValue(classA,"int2", 120);
        cl.setAttributeValue(subclassA,"int3", 130);

        assertEquals(100, cl.getAttributeValue("int0"));
        assertEquals(110, cl.getAttributeValue("int1"));
        assertEquals(120, cl.getAttributeValue("int2"));
        assertEquals(130, cl.getAttributeValue("int3"));

        assertEquals(100, cl.getAttributeValue(top1,"int0"));
        assertEquals(110, cl.getAttributeValue(top2, "int1"));
        assertEquals(120, cl.getAttributeValue(classA, "int2"));
        assertEquals(130, cl.getAttributeValue(subclassA, "int3"));
    }

    @Test
    public void testAttributeValuesSameNameInheritanceMetaclass() throws CException {
        CModel model = CodeableModels.createModel();
        model.createMetaclass("MCL");
        CMetaclass top1 = model.createMetaclass( "Top1");
        CMetaclass top2 = model.createMetaclass("Top2");
        CMetaclass classA = model.createMetaclass( "ClassA").addSuperclass("Top1").addSuperclass("Top2");
        CMetaclass subclassA = model.createMetaclass( "SubA").addSuperclass("ClassA");

        top1.addAttribute("int", 0);
        top2.addAttribute("int", 1);
        classA.addAttribute("int", 2);
        subclassA.addAttribute("int", 3);

        CClass cl1 = model.createClass(subclassA, "C1");
        CClass cl2 = model.createClass(classA, "C2");
        CClass cl3 = model.createClass(top1, "C3");

        assertEquals(3, cl1.getAttributeValue("int"));
        assertEquals(2, cl2.getAttributeValue("int"));
        assertEquals(0, cl3.getAttributeValue("int"));

        assertEquals(3, cl1.getAttributeValue(subclassA, "int"));
        assertEquals(2, cl1.getAttributeValue(classA, "int"));
        assertEquals(1, cl1.getAttributeValue(top2, "int"));
        assertEquals(0, cl1.getAttributeValue(top1, "int"));
        assertEquals(2, cl2.getAttributeValue(classA, "int"));
        assertEquals(1, cl2.getAttributeValue(top2, "int"));
        assertEquals(0, cl2.getAttributeValue(top1, "int"));
        assertEquals(0, cl3.getAttributeValue(top1,"int"));

        cl1.setAttributeValue("int", 10);
        cl2.setAttributeValue("int", 11);
        cl3.setAttributeValue("int", 12);

        assertEquals(10, cl1.getAttributeValue("int"));
        assertEquals(11, cl2.getAttributeValue("int"));
        assertEquals(12, cl3.getAttributeValue("int"));

        assertEquals(10, cl1.getAttributeValue(subclassA, "int"));
        assertEquals(2, cl1.getAttributeValue(classA, "int"));
        assertEquals(1, cl1.getAttributeValue(top2, "int"));
        assertEquals(0, cl1.getAttributeValue(top1, "int"));
        assertEquals(11, cl2.getAttributeValue(classA, "int"));
        assertEquals(1, cl2.getAttributeValue(top2, "int"));
        assertEquals(0, cl2.getAttributeValue(top1, "int"));
        assertEquals(12, cl3.getAttributeValue(top1,"int"));

        cl1.setAttributeValue(subclassA,"int", 130);
        cl1.setAttributeValue(top1,"int", 100);
        cl1.setAttributeValue(top2,"int", 110);
        cl1.setAttributeValue(classA,"int", 120);

        assertEquals(130, cl1.getAttributeValue("int"));

        assertEquals(100, cl1.getAttributeValue(top1,"int"));
        assertEquals(110, cl1.getAttributeValue(top2, "int"));
        assertEquals(120, cl1.getAttributeValue(classA, "int"));
        assertEquals(130, cl1.getAttributeValue(subclassA, "int"));
    }



}
