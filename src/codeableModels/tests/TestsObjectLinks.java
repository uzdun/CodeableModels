package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsObjectLinks {

    @Test
    public void testSetOneToOneLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociation association = model.createAssociation(cl1.createEnd("class1", "1"),
                cl2.createEnd("class2", "1"));
        CAssociationEnd cl1End = association.getEndByRoleName("class1");
        CAssociationEnd cl2End = association.getEndByRoleName("class2");

        CObject obj2 = model.createObject(cl2, "obj2");
        CObject obj1 = model.createObject(cl1, "obj1");
        obj1.setLink(cl2End, obj2);
        CObject obj3 = model.createObject(cl2, "obj3");

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(cl2End));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(cl1End));

        obj1.setLink(association.getEndByClassifier(cl2), "obj3");

        assertEquals(Collections.singletonList(obj3), obj1.getLinks(cl2End));
        assertEquals(Collections.singletonList(obj1), obj3.getLinks(cl1End));
    }

    @Test
    public void testSetLinkVariants() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociation association = model.createAssociation(cl1.createEnd("class1", "1"),
                cl2.createEnd("class2", "1"));
        CAssociationEnd end1 = association.getEndByClassifier(cl1), end2 = association.getEndByClassifier(cl2);

        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2 = model.createObject(cl2, "obj2");

        obj1.setLinks(end2, Collections.singletonList(obj2));

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj1.setLinks(end2, Collections.singletonList(obj2));

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj1.setLinks(end2, Collections.singletonList("obj2"));

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj2.setLink(end1, obj1);

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj2.setLink(end1, "obj1");

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));
    }

    @Test
    public void testAddOneToOneLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "1");
        model.createAssociation(end1, end2);

        CObject obj2 = model.createObject(cl2, "obj2");
        CObject obj1 = model.createObject(cl1, "obj1");
        obj1.addLink(end2, obj2);
        model.createObject(cl2, "obj3");

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        try {
            obj1.addLink(end2, "obj3");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '2', but should be '1'", e.getMessage());
        }
    }

    @Test
    public void testAddOneToOneLinkVariants() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "1");
        model.createAssociation(end1, end2);

        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2 = model.createObject(cl2, "obj2");

        obj1.addLinks(end2, Collections.singletonList(obj2));

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        try {
            obj1.addLinks(end2, Collections.singletonList(obj2));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link between 'obj1' and 'obj2' already exists", e.getMessage());
        }

        obj1.removeLinks(end2, Collections.singletonList(obj2));
        obj1.addLinks(end2, Collections.singletonList(obj2));

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj2.removeLinks(end1, Collections.singletonList("obj1"));
        obj2.addLinks(end1, Collections.singletonList("obj1"));

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj2.removeLink(end1, "obj1");
        obj2.addLink(end1, "obj1");

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj2.removeLink(end1, obj1);
        obj2.addLink(end1, obj1);

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));
    }

    @Test
    public void testOneToOneRemoveAllLinks() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "1");
        model.createAssociation(end1, end2);

        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2 = model.createObject(cl2, "obj2");

        obj1.removeAllLinks(end2);

        obj1.setLinks(end2, Collections.singletonList(obj2));

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj1.removeAllLinks(end2);

        assertEquals(Collections.emptyList(), obj1.getLinks(end2));
        assertEquals(Collections.emptyList(), obj2.getLinks(end1));

        obj1.setLinks(end2, Collections.singletonList(obj2));

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj2.removeAllLinks(end1);

        assertEquals(Collections.emptyList(), obj1.getLinks(end2));
        assertEquals(Collections.emptyList(), obj2.getLinks(end1));
    }

    @Test
    public void testOneToOneRemoveLinks() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "1");
        model.createAssociation(end1, end2);

        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2 = model.createObject(cl2, "obj2");

        try {
            obj1.removeLink(end2, obj2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link between 'obj1' and 'obj2' can't be removed: it does not exist", e.getMessage());
        }

        try {
            obj1.removeLinks(end2, Collections.singletonList(obj2));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link between 'obj1' and 'obj2' can't be removed: it does not exist", e.getMessage());
        }

        obj1.setLinks(end2, Collections.singletonList(obj2));

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj1.removeLinks(end2, Collections.singletonList(obj2));

        assertEquals(Collections.emptyList(), obj1.getLinks(end2));
        assertEquals(Collections.emptyList(), obj2.getLinks(end1));

        obj1.setLink(end2, obj2);

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj2.removeLink(end1, obj1);

        assertEquals(Collections.emptyList(), obj1.getLinks(end2));
        assertEquals(Collections.emptyList(), obj2.getLinks(end1));
    }


    @Test
    public void testOneToOneLinkMultiplicity() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "1");
        model.createAssociation(end1, end2);
        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2 = model.createObject(cl2, "obj2");

        try {
            obj1.setLinks(end2, Collections.emptyList());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '0', but should be '1'", e.getMessage());
        }

        try {
            obj1.setLink(end2, (CObject) null);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '0', but should be '1'", e.getMessage());
        }


        obj1.addLinks(end2, Collections.emptyList());
        assertEquals(Collections.emptyList(), obj1.getLinks(end2));

        obj1.addLink(end2, (CObject) null);
        assertEquals(Collections.emptyList(), obj1.getLinks(end2));

        CObject obj3 = model.createObject(cl2, "obj3");

        try {
            obj1.setLinks(end2, Arrays.asList(obj2, obj3));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '2', but should be '1'", e.getMessage());
        }
    }

    @Test
    public void testSetLinksByStrings() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);
        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2 = model.createObject(cl2, "obj2");
        CObject obj3 = model.createObject(cl2, "obj3");

        obj1.setLinks(end2, Collections.singletonList("obj2"));
        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));

        obj1.setLinks(end2, Arrays.asList("obj2", "obj3"));
        assertEquals(Arrays.asList(obj2, obj3), obj1.getLinks(end2));


        try {
            obj1.setLinks(end2, Arrays.asList("obj2", "obj4"));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("object 'obj4' unknown", e.getMessage());
        }

        try {
            Integer i = 4;
            obj1.setLinks(end2, Arrays.asList("obj2", i));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("argument '4' is not of type String or CObject", e.getMessage());
        }
    }

    @Test
    public void testSetLinksWithSubclassInstance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl3 = model.createClass(mcl,"CL3").addSuperclass(cl2);
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);
        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2 = model.createObject(cl2, "obj2");
        CObject obj3 = model.createObject(cl3, "obj3");

        obj1.setLinks(end2, Arrays.asList("obj2", "obj3"));
        assertEquals(Arrays.asList(obj2, obj3), obj1.getLinks(end2));
    }

    @Test
    public void testOneToOneLinkIncompatibleTypes() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "1");
        model.createAssociation(end1, end2);
        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2 = model.createObject(cl2, "obj2");
        CObject obj3 = model.createObject(cl2, "obj3");

        try {
            obj1.setLinks(end2, Arrays.asList(obj1, obj2, obj3));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link object 'obj1' not compatible with association classifier 'Class2'", e.getMessage());
        }
    }

    @Test
    public void testOneToOneLinkIsNavigable() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd end1 = cl1.createEnd("class1", "1");
        end1.setNavigable(false);
        CAssociationEnd end2 = cl2.createEnd("class2", "1");
        end2.setNavigable(false);
        model.createAssociation(end1, end2);

        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2 = model.createObject(cl2, "obj2");

        try {
            obj1.setLinks(end2, Collections.singletonList(obj2));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not navigable and thus cannot be accessed from object 'obj1'", e.getMessage());
        }

        try {
            obj2.setLinks(end1, Collections.singletonList(obj1));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class1' is not navigable and thus cannot be accessed from object 'obj2'", e.getMessage());
        }

        try {
            obj1.getLinks(end2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not navigable and thus cannot be accessed from object 'obj1'", e.getMessage());
        }

        try {
            obj2.getLinks(end1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class1' is not navigable and thus cannot be accessed from object 'obj2'", e.getMessage());
        }

        try {
            obj1.removeAllLinks(end2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not navigable and thus cannot be accessed from object 'obj1'", e.getMessage());
        }

        try {
            obj2.removeAllLinks(end1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class1' is not navigable and thus cannot be accessed from object 'obj2'", e.getMessage());
        }

        try {
            obj1.removeLink(end2, obj2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not navigable and thus cannot be accessed from object 'obj1'", e.getMessage());
        }

        try {
            obj2.removeLink(end1, obj1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class1' is not navigable and thus cannot be accessed from object 'obj2'", e.getMessage());
        }

        end1.setNavigable(true);

        try {
            obj1.setLink(end2, obj2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not navigable and thus cannot be accessed from object 'obj1'", e.getMessage());
        }

        obj2.setLink(end1, obj1);

        try {
            obj1.getLinks(end2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not navigable and thus cannot be accessed from object 'obj1'", e.getMessage());
        }

        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        try {
            obj1.removeAllLinks(end2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not navigable and thus cannot be accessed from object 'obj1'", e.getMessage());
        }

        obj2.removeAllLinks(end1);
        assertEquals(Collections.emptyList(), obj2.getLinks(end1));


        try {
            obj1.removeLink(end2, obj2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not navigable and thus cannot be accessed from object 'obj1'", e.getMessage());
        }

        obj2.addLink(end1, obj1);
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(end1));

        obj2.removeLink(end1, obj1);
        assertEquals(Collections.emptyList(), obj2.getLinks(end1));
    }


    @Test
    public void testOneToOneAssociationUnknown() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd end1 = cl1.createEnd("class1Forward", "1");
        CAssociationEnd end1Back = cl1.createEnd("class1Back", "1");
        model.createAssociation(end1, end1Back);

        CObject obj2 = model.createObject(cl2, "obj2");

        try {
            obj2.setLinks(end1, Collections.emptyList());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class1Forward' is not an association target end of 'obj2'", e.getMessage());
        }
    }


    @Test
    public void testOneToNLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);
        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2a = model.createObject(cl2, "obj2a");
        CObject obj2b = model.createObject(cl2, "obj2b");

        obj1.setLinks(end2, Arrays.asList(obj2a, obj2b));

        assertEquals(Arrays.asList(obj2a, obj2b), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2a.getLinks(end1));
        assertEquals(Collections.singletonList(obj1), obj2b.getLinks(end1));

        obj1.setLinks(end2, Collections.singletonList(obj2a));

        assertEquals(Collections.singletonList(obj2a), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2a.getLinks(end1));
        assertEquals(Collections.emptyList(), obj2b.getLinks(end1));

        obj2b.setLinks(end1, Collections.singletonList(obj1));

        assertEquals(Arrays.asList(obj2a, obj2b), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2a.getLinks(end1));
        assertEquals(Collections.singletonList(obj1), obj2b.getLinks(end1));
    }

    @Test
    public void testOneToNLinkDelete() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);
        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2a = model.createObject(cl2, "obj2a");
        CObject obj2b = model.createObject(cl2, "obj2b");

        obj1.removeAllLinks(end2);

        obj1.setLinks(end2, Arrays.asList(obj2a, obj2b));

        assertEquals(Arrays.asList(obj2a, obj2b), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2a.getLinks(end1));
        assertEquals(Collections.singletonList(obj1), obj2b.getLinks(end1));

        obj1.removeAllLinks(end2);

        assertEquals(Collections.emptyList(), obj1.getLinks(end2));
        assertEquals(Collections.emptyList(), obj2a.getLinks(end1));
        assertEquals(Collections.emptyList(), obj2b.getLinks(end1));

        obj1.setLinks(end2, Arrays.asList(obj2a, obj2b));

        assertEquals(Arrays.asList(obj2a, obj2b), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2a.getLinks(end1));
        assertEquals(Collections.singletonList(obj1), obj2b.getLinks(end1));

        obj2a.removeAllLinks(end1);

        assertEquals(Collections.singletonList(obj2b), obj1.getLinks(end2));
        assertEquals(Collections.emptyList(), obj2a.getLinks(end1));
        assertEquals(Collections.singletonList(obj1), obj2b.getLinks(end1));
    }

    @Test
    public void testOneTo2NLinkMultiplicity() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "2..*");
        model.createAssociation(end1, end2);
        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2a = model.createObject(cl2, "obj2a");

        try {
            obj1.setLinks(end2, Collections.emptyList());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '0', but should be '2..*'", e.getMessage());
        }

        try {
            obj1.setLinks(end2, Collections.singletonList(obj2a));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '1', but should be '2..*'", e.getMessage());
        }
    }


    @Test
    public void testNToNLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "*"),
                end2 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);

        CObject obj1a = model.createObject(cl1, "obj1a");
        CObject obj1b = model.createObject(cl1, "obj1b");
        CObject obj1c = model.createObject(cl1, "obj1c");
        CObject obj2a = model.createObject(cl2, "obj2a");
        CObject obj2b = model.createObject(cl2, "obj2b");

        obj1a.setLinks(end2, Arrays.asList(obj2a, obj2b));
        obj1b.setLinks(end2, Collections.singletonList(obj2a));
        obj1c.setLinks(end2, Collections.singletonList(obj2b));

        assertEquals(Arrays.asList(obj2a, obj2b), obj1a.getLinks(end2));
        assertEquals(Collections.singletonList(obj2a), obj1b.getLinks(end2));
        assertEquals(Collections.singletonList(obj2b), obj1c.getLinks(end2));
        assertEquals(Arrays.asList(obj1a, obj1b), obj2a.getLinks(end1));
        assertEquals(Arrays.asList(obj1a, obj1c), obj2b.getLinks(end1));

        obj2a.setLinks(end1, Arrays.asList(obj1a, obj1b));
        obj2b.setLinks(end1, Collections.emptyList());

        assertEquals(Collections.singletonList(obj2a), obj1a.getLinks(end2));
        assertEquals(Collections.singletonList(obj2a), obj1b.getLinks(end2));
        assertEquals(Collections.emptyList(), obj1c.getLinks(end2));
        assertEquals(Arrays.asList(obj1a, obj1b), obj2a.getLinks(end1));
        assertEquals(Collections.emptyList(), obj2b.getLinks(end1));
    }

    @Test
    public void testAssociationGetLinks() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "*"),
                end2 = cl2.createEnd("class2", "*");
        CAssociation association = model.createAssociation(end1, end2);

        CObject obj1a = model.createObject(cl1, "obj1a");
        CObject obj1b = model.createObject(cl1, "obj1b");
        CObject obj1c = model.createObject(cl1, "obj1c");
        CObject obj2a = model.createObject(cl2, "obj2a");
        CObject obj2b = model.createObject(cl2, "obj2b");

        obj1a.setLinks(end2, Arrays.asList(obj2a, obj2b));
        obj1b.setLinks(end2, Collections.singletonList(obj2a));
        obj1c.setLinks(end2, Collections.singletonList(obj2b));

        List<CLink> links = association.getLinks();

        assertEquals(4, links.size());
        assertEquals(Arrays.asList(obj1a, obj2a), links.get(0).getLinkedObjects());
        assertEquals(Arrays.asList(obj1a, obj2b), links.get(1).getLinkedObjects());
        assertEquals(Arrays.asList(obj1b, obj2a), links.get(2).getLinkedObjects());
        assertEquals(Arrays.asList(obj1c, obj2b), links.get(3).getLinkedObjects());
    }

    @Test
    public void testNToNLinkRemoveAll() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "*"),
                end2 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);
        CObject obj1a = model.createObject(cl1, "obj1a");
        CObject obj1b = model.createObject(cl1, "obj1b");
        CObject obj1c = model.createObject(cl1, "obj1c");
        CObject obj2a = model.createObject(cl2, "obj2a");
        CObject obj2b = model.createObject(cl2, "obj2b");

        obj1a.setLinks(end2, Arrays.asList(obj2a, obj2b));
        obj1b.setLinks(end2, Collections.singletonList(obj2a));
        obj1c.setLinks(end2, Collections.singletonList(obj2b));

        assertEquals(Arrays.asList(obj2a, obj2b), obj1a.getLinks(end2));
        assertEquals(Collections.singletonList(obj2a), obj1b.getLinks(end2));
        assertEquals(Collections.singletonList(obj2b), obj1c.getLinks(end2));
        assertEquals(Arrays.asList(obj1a, obj1b), obj2a.getLinks(end1));
        assertEquals(Arrays.asList(obj1a, obj1c), obj2b.getLinks(end1));

        obj2b.removeAllLinks(end1);

        assertEquals(Collections.singletonList(obj2a), obj1a.getLinks(end2));
        assertEquals(Collections.singletonList(obj2a), obj1b.getLinks(end2));
        assertEquals(Collections.emptyList(), obj1c.getLinks(end2));
        assertEquals(Arrays.asList(obj1a, obj1b), obj2a.getLinks(end1));
        assertEquals(Collections.emptyList(), obj2b.getLinks(end1));
    }

    @Test
    public void testNToNLinkRemoveLinks() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "*"),
                end2 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);
        CObject obj1a = model.createObject(cl1, "obj1a");
        CObject obj1b = model.createObject(cl1, "obj1b");
        CObject obj1c = model.createObject(cl1, "obj1c");
        CObject obj2a = model.createObject(cl2, "obj2a");
        CObject obj2b = model.createObject(cl2, "obj2b");

        obj1a.setLinks(end2, Arrays.asList(obj2a, obj2b));
        obj1b.setLinks(end2, Collections.singletonList(obj2a));
        obj1c.setLinks(end2, Collections.singletonList(obj2b));

        assertEquals(Arrays.asList(obj2a, obj2b), obj1a.getLinks(end2));
        assertEquals(Collections.singletonList(obj2a), obj1b.getLinks(end2));
        assertEquals(Collections.singletonList(obj2b), obj1c.getLinks(end2));
        assertEquals(Arrays.asList(obj1a, obj1b), obj2a.getLinks(end1));
        assertEquals(Arrays.asList(obj1a, obj1c), obj2b.getLinks(end1));

        obj2b.removeLinks(end1, Arrays.asList(obj1a, "obj1c"));
        obj1a.removeLink(end2, "obj2a");

        assertEquals(Collections.emptyList(), obj1a.getLinks(end2));
        assertEquals(Collections.singletonList(obj2a), obj1b.getLinks(end2));
        assertEquals(Collections.emptyList(), obj1c.getLinks(end2));
        assertEquals(Collections.singletonList(obj1b), obj2a.getLinks(end1));
        assertEquals(Collections.emptyList(), obj2b.getLinks(end1));
    }


    @Test
    public void testNToNSetSelfLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");

        CAssociationEnd superEnd = cl1.createEnd("super", "*"),
                subEnd =  cl1.createEnd("sub", "*");
        model.createAssociation(superEnd, subEnd);

        CObject top = model.createObject(cl1, "Top");
        CObject mid1 = model.createObject(cl1, "Mid1");
        CObject mid2 = model.createObject(cl1, "Mid2");
        CObject mid3 = model.createObject(cl1, "Mid3");
        CObject bottom1 = model.createObject(cl1, "Bottom1");
        CObject bottom2 = model.createObject(cl1, "Bottom2");

        top.setLinks(subEnd, Arrays.asList(mid1, mid2, mid3));
        mid1.setLinks(subEnd, Arrays.asList(bottom1, bottom2));

        assertEquals(Collections.emptyList(), top.getLinks(superEnd));
        assertEquals(Arrays.asList(mid1, mid2, mid3), top.getLinks(subEnd));
        assertEquals(Collections.singletonList(top), mid1.getLinks(superEnd));
        assertEquals(Arrays.asList(bottom1, bottom2), mid1.getLinks(subEnd));
        assertEquals(Collections.singletonList(top), mid2.getLinks(superEnd));
        assertEquals(Collections.emptyList(), mid2.getLinks(subEnd));
        assertEquals(Collections.singletonList(top), mid3.getLinks(superEnd));
        assertEquals(Collections.emptyList(), mid3.getLinks(subEnd));
        assertEquals(Collections.singletonList(mid1), bottom1.getLinks(superEnd));
        assertEquals(Collections.emptyList(), bottom1.getLinks(subEnd));
        assertEquals(Collections.singletonList(mid1), bottom2.getLinks(superEnd));
        assertEquals(Collections.emptyList(), bottom2.getLinks(subEnd));
    }

    @Test
    public void testNToNAddSelfLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CAssociationEnd superEnd = cl1.createEnd("super", "*"),
                subEnd =  cl1.createEnd("sub", "*");
        model.createAssociation(superEnd, subEnd);

        CObject top = model.createObject(cl1, "Top");
        CObject mid1 = model.createObject(cl1, "Mid1");
        CObject mid2 = model.createObject(cl1, "Mid2");
        CObject mid3 = model.createObject(cl1, "Mid3");
        CObject bottom1 = model.createObject(cl1, "Bottom1");
        CObject bottom2 = model.createObject(cl1, "Bottom2");

        top.addLinks(subEnd, Arrays.asList(mid1, mid2, mid3));
        mid1.addLinks(subEnd, Arrays.asList(bottom1, bottom2));

        assertEquals(Collections.emptyList(), top.getLinks(superEnd));
        assertEquals(Arrays.asList(mid1, mid2, mid3), top.getLinks(subEnd));
        assertEquals(Collections.singletonList(top), mid1.getLinks(superEnd));
        assertEquals(Arrays.asList(bottom1, bottom2), mid1.getLinks(subEnd));
        assertEquals(Collections.singletonList(top), mid2.getLinks(superEnd));
        assertEquals(Collections.emptyList(), mid2.getLinks(subEnd));
        assertEquals(Collections.singletonList(top), mid3.getLinks(superEnd));
        assertEquals(Collections.emptyList(), mid3.getLinks(subEnd));
        assertEquals(Collections.singletonList(mid1), bottom1.getLinks(superEnd));
        assertEquals(Collections.emptyList(), bottom1.getLinks(subEnd));
        assertEquals(Collections.singletonList(mid1), bottom2.getLinks(superEnd));
        assertEquals(Collections.emptyList(), bottom2.getLinks(subEnd));

    }



    @Test
    public void testUnknownEnd() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "*"),
                end3 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);

        CObject obj2 = model.createObject(cl2, "obj2");
        CObject obj1 = model.createObject(cl1, "obj1");
        try {
            obj1.setLink(end3, obj2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not an association target end of 'obj1'", e.getMessage());
        }
        try {
            obj1.setLinks(end3, Collections.singletonList(obj2));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not an association target end of 'obj1'", e.getMessage());
        }
        obj1.setLink(end2, obj2);

        try {
            assertEquals(Collections.singletonList(obj2), obj1.getLinks(end3));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not an association target end of 'obj1'", e.getMessage());
        }
        assertEquals(Collections.singletonList(obj2), obj1.getLinks(end2));

        try {
            obj1.removeAllLinks(end3);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'class2' is not an association target end of 'obj1'", e.getMessage());
        }
    }

    @Test
    public void testSetOneToOneLinkInheritance1() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl2Sub = model.createClass(mcl,"CL2Sub").addSuperclass(cl2);
        CAssociation association = model.createAssociation(cl1.createEnd("class1", "1"),
                cl2.createEnd("class2", "1"));
        CAssociationEnd cl1End = association.getEndByRoleName("class1");
        CAssociationEnd cl2End = association.getEndByRoleName("class2");

        CObject obj2 = model.createObject(cl2Sub, "obj2");
        CObject obj1 = model.createObject(cl1, "obj1");
        obj1.setLink(cl2End, obj2);
        CObject obj3 = model.createObject(cl2Sub, "obj3");

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(cl2End));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(cl1End));

        obj1.setLink(association.getEndByClassifier(cl2), "obj3");

        assertEquals(Collections.singletonList(obj3), obj1.getLinks(cl2End));
        assertEquals(Collections.singletonList(obj1), obj3.getLinks(cl1End));
    }


    @Test
    public void testSetOneToOneLinkInheritance2() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl1Sub = model.createClass(mcl,"CL1Sub").addSuperclass(cl1);
        CClass cl2Sub = model.createClass(mcl,"CL2Sub").addSuperclass(cl2).addSuperclass(cl1);
        CAssociation association = model.createAssociation(cl1.createEnd("class1", "1"),
                cl2.createEnd("class2", "1"));
        CAssociationEnd cl1End = association.getEndByRoleName("class1");
        CAssociationEnd cl2End = association.getEndByRoleName("class2");

        CObject obj2 = model.createObject(cl2Sub, "obj2");
        CObject obj1 = model.createObject(cl1Sub, "obj1");
        obj1.setLink(cl2End, obj2);
        CObject obj3 = model.createObject(cl2Sub, "obj3");

        assertEquals(Collections.singletonList(obj2), obj1.getLinks(cl2End));
        assertEquals(Collections.singletonList(obj1), obj2.getLinks(cl1End));

        obj1.setLink(association.getEndByClassifier(cl2), "obj3");

        assertEquals(Collections.singletonList(obj3), obj1.getLinks(cl2End));
        assertEquals(Collections.singletonList(obj1), obj3.getLinks(cl1End));
    }


    @Test
    public void testOneToNLinkDeleteInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl1Sub = model.createClass(mcl, "CL1Sub").addSuperclass(cl1);
        CClass cl2Sub = model.createClass(mcl,"CL2Sub").addSuperclass(cl2);
        CAssociationEnd  end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);
        CObject obj1 = model.createObject(cl1Sub, "obj1");
        CObject obj2a = model.createObject(cl2Sub, "obj2a");
        CObject obj2b = model.createObject(cl2Sub, "obj2b");

        obj1.removeAllLinks(end2);

        obj1.setLinks(end2, Arrays.asList(obj2a, obj2b));

        assertEquals(Arrays.asList(obj2a, obj2b), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2a.getLinks(end1));
        assertEquals(Collections.singletonList(obj1), obj2b.getLinks(end1));

        obj1.removeAllLinks(end2);

        assertEquals(Collections.emptyList(), obj1.getLinks(end2));
        assertEquals(Collections.emptyList(), obj2a.getLinks(end1));
        assertEquals(Collections.emptyList(), obj2b.getLinks(end1));

        obj1.setLinks(end2, Arrays.asList(obj2a, obj2b));

        assertEquals(Arrays.asList(obj2a, obj2b), obj1.getLinks(end2));
        assertEquals(Collections.singletonList(obj1), obj2a.getLinks(end1));
        assertEquals(Collections.singletonList(obj1), obj2b.getLinks(end1));

        obj2a.removeAllLinks(end1);

        assertEquals(Collections.singletonList(obj2b), obj1.getLinks(end2));
        assertEquals(Collections.emptyList(), obj2a.getLinks(end1));
        assertEquals(Collections.singletonList(obj1), obj2b.getLinks(end1));
    }

    @Test
    public void testNToNLinkRemoveAllInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl1Sub = model.createClass(mcl,"CL1Sub").addSuperclass(cl1);
        CClass cl2Sub = model.createClass(mcl,"CL2Sub").addSuperclass(cl2);
        CAssociationEnd  end1 = cl1.createEnd("class1", "*"),
                end2 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);
        CObject obj1a = model.createObject(cl1Sub, "obj1a");
        CObject obj1b = model.createObject(cl1Sub, "obj1b");
        CObject obj1c = model.createObject(cl1Sub, "obj1c");
        CObject obj2a = model.createObject(cl2Sub, "obj2a");
        CObject obj2b = model.createObject(cl2Sub, "obj2b");

        obj1a.setLinks(end2, Arrays.asList(obj2a, obj2b));
        obj1b.setLinks(end2, Collections.singletonList(obj2a));
        obj1c.setLinks(end2, Collections.singletonList(obj2b));

        assertEquals(Arrays.asList(obj2a, obj2b), obj1a.getLinks(end2));
        assertEquals(Collections.singletonList(obj2a), obj1b.getLinks(end2));
        assertEquals(Collections.singletonList(obj2b), obj1c.getLinks(end2));
        assertEquals(Arrays.asList(obj1a, obj1b), obj2a.getLinks(end1));
        assertEquals(Arrays.asList(obj1a, obj1c), obj2b.getLinks(end1));

        obj2b.removeAllLinks(end1);

        assertEquals(Collections.singletonList(obj2a), obj1a.getLinks(end2));
        assertEquals(Collections.singletonList(obj2a), obj1b.getLinks(end2));
        assertEquals(Collections.emptyList(), obj1c.getLinks(end2));
        assertEquals(Arrays.asList(obj1a, obj1b), obj2a.getLinks(end1));
        assertEquals(Collections.emptyList(), obj2b.getLinks(end1));
    }

    @Test
    public void testGetLinkObjects() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");
        CClass cl1Sub = model.createClass(mcl,"CL1Sub").addSuperclass(cl1);
        CClass cl2Sub = model.createClass(mcl,"CL2Sub").addSuperclass(cl2);
        CAssociationEnd  end1 = cl1.createEnd("class1", "*"),
                end2 = cl2.createEnd("class2", "*");
        CAssociation association1 = model.createAssociation(end1, end2);

        CAssociationEnd end3 = cl1.createEnd("prior", "1"),
                end4 = cl1.createEnd("next", "1");
        CAssociation association2 = model.createAssociation(end3, end4);

        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2 = model.createObject(cl2, "obj2");
        CObject obj_cl1Sub = model.createObject(cl1Sub, "obj1_cl1Sub");
        CObject obj_cl2Sub = model.createObject(cl2Sub, "obj2_cl2Sub");

        CLink link, linkOrig;

        linkOrig = obj1.setLink(end2, obj2);
        link = obj1.getLinkObjects(end2).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj1, obj2), link.getLinkedObjects());

        assertEquals(association1, link.getAssociation());

        assertEquals(obj1, link.getLinkedObjectByName("obj1"));
        assertEquals(obj2, link.getLinkedObjectByName("obj2"));
        assertEquals(null, link.getLinkedObjectByName("obj3"));

        assertEquals(obj1, link.getLinkedObjectByClassifier(cl1));
        assertEquals(obj2, link.getLinkedObjectByClassifier(cl2));
        assertEquals(null, link.getLinkedObjectByClassifier(model.createClass(mcl, "ClassX")));

        linkOrig = obj1.setLink(end2, obj_cl2Sub);
        link = obj1.getLinkObjects(end2).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj1, obj_cl2Sub), link.getLinkedObjects());

        linkOrig = obj1.setLink(end2, obj2);
        link = obj1.getLinkObjects(association1).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj1, obj2), link.getLinkedObjects());

        linkOrig = obj1.setLink(end2, obj_cl2Sub);
        link = obj1.getLinkObjects(association1).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj1, obj_cl2Sub), link.getLinkedObjects());

        linkOrig = obj1.setLink(end4, obj1);
        link = obj1.getLinkObjects(end4).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj1, obj1), link.getLinkedObjects());

        linkOrig = obj1.setLink(end4, obj_cl1Sub);
        link = obj1.getLinkObjects(end4).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj1, obj_cl1Sub), link.getLinkedObjects());

        linkOrig = obj1.setLink(end4, obj1);
        link = obj1.getLinkObjects(association2).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj1, obj1), link.getLinkedObjects());

        obj1.removeAllLinks(end4);

        linkOrig = obj_cl1Sub.setLink(end4, obj1);
        link = obj_cl1Sub.getLinkObjects(association2).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj_cl1Sub, obj1), link.getLinkedObjects());
    }

    @Test
    public void testGetLinkObjectsSelfLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");

        CAssociationEnd end1 = cl1.createEnd("from", "*"),
                end2 = cl1.createEnd("to", "*");
        CAssociation association = model.createAssociation(end1, end2);

        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2 = model.createObject(cl1, "obj2");

        CLink link, linkOrig;

        // get link objects via association
        linkOrig = obj1.setLink(end2, obj2);
        link = obj1.getLinkObjects(association).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj1, obj2), link.getLinkedObjects());

        // get link objects via end
        linkOrig = obj1.setLink(end2, obj2);
        link = obj1.getLinkObjects(end2).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj1, obj2), link.getLinkedObjects());

        // test the same with the other end
        CObject obj3 = model.createObject(cl1, "obj3");
        CObject obj4 = model.createObject(cl1, "obj4");

        // get link objects via association
        linkOrig = obj3.setLink(end1, obj4);
        link = obj3.getLinkObjects(association).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj4, obj3), link.getLinkedObjects());

        // get link objects via end
        linkOrig = obj3.setLink(end1, obj4);
        link = obj3.getLinkObjects(end1).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(obj4, obj3), link.getLinkedObjects());

    }

    @Test
    public void testGetLinkObjectsSetList() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");

        CAssociationEnd end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);

        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2a = model.createObject(cl2, "obj2a");
        CObject obj2b = model.createObject(cl2, "obj2b");

        List<CLink> linksOrig = obj1.setLinks(end2, Arrays.asList(obj2a, obj2b));
        List<CLink> links = obj1.getLinkObjects(end2);
        assertEquals(linksOrig, links);
        assertEquals(2, links.size());
        assertEquals(obj2a, links.get(0).getLinkedObjectAtTargetEnd(end2));
        assertEquals(obj2b, links.get(1).getLinkedObjectAtTargetEnd(end2));
    }

    @Test
    public void testGetLinkObjectsAddList() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClass cl1 = model.createClass(mcl, "Class1");
        CClass cl2 = model.createClass(mcl, "Class2");

        CAssociationEnd end1 = cl1.createEnd("class1", "1"),
                end2 = cl2.createEnd("class2", "*");
        model.createAssociation(end1, end2);

        CObject obj1 = model.createObject(cl1, "obj1");
        CObject obj2a = model.createObject(cl2, "obj2a");
        CObject obj2b = model.createObject(cl2, "obj2b");

        List<CLink> linksOrig = obj1.addLinks(end2, Arrays.asList(obj2a, obj2b));
        List<CLink> links = obj1.getLinkObjects(end2);
        assertEquals(linksOrig, links);
        assertEquals(2, links.size());
        assertEquals(obj2a, links.get(0).getLinkedObjectAtTargetEnd(end2));
        assertEquals(obj2b, links.get(1).getLinkedObjectAtTargetEnd(end2));
    }


}
