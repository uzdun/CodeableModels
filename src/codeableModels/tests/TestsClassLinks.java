package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsClassLinks {
    @Test
    public void testSetOneToOneLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation association = model.createAssociation(mcl1.createEnd("metaclass1", "1"),
                mcl2.createEnd("metaclass2", "1"));
        CAssociationEnd mcl1End = association.getEndByRoleName("metaclass1");
        CAssociationEnd mcl2End = association.getEndByRoleName("metaclass2");

        CClass cl2 = model.createClass(mcl2, "CL2");
        CClass cl1 = model.createClass(mcl1, "CL1");
        cl1.setLink(mcl2End, cl2);
        CClass cl3 = model.createClass(mcl2, "CL3");

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(mcl2End));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(mcl1End));

        cl1.setLink(association.getEndByClassifier(mcl2), "CL3");

        assertEquals(Collections.singletonList(cl3), cl1.getLinks(mcl2End));
        assertEquals(Collections.singletonList(cl1), cl3.getLinks(mcl1End));
    }

    @Test
    public void testSetLinkVariants() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociation assoc = model.createAssociation(mcl1.createEnd("metaclass1", "1"),
                mcl2.createEnd("metaclass2", "1"));
        CAssociationEnd end1 = assoc.getEndByClassifier(mcl1), end2 = assoc.getEndByClassifier(mcl2);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");

        cl1.setLinks(end2, Collections.singletonList(cl2));

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        cl1.setLinks(end2, Collections.singletonList(cl2));

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        cl1.setLinks(end2, Collections.singletonList("CL2"));

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        cl2.setLink(end1, cl1);

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        CLink link = cl2.setLink(end1, "CL1");

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        assertEquals(cl2.getLinkObjects(end1).get(0), link);
    }

    @Test
    public void testAddOneToOneLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        model.createAssociation(end1, end2);

        CClass cl2 = model.createClass(mcl2, "CL2");
        CClass cl1 = model.createClass(mcl1, "CL1");
        cl1.addLink(end2, cl2);
        model.createClass(mcl2, "CL3");

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        try {
            cl1.addLink(end2, "CL3");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '2', but should be '1'", e.getMessage());
        }
    }

    @Test
    public void testAddOneToOneLinkVariants() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        model.createAssociation(end1, end2);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");

        cl1.addLinks(end2, Collections.singletonList(cl2));

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        try {
            cl1.addLinks(end2, Collections.singletonList(cl2));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link between 'CL1' and 'CL2' already exists", e.getMessage());
        }

        cl1.removeLinks(end2, Collections.singletonList(cl2));
        cl1.addLinks(end2, Collections.singletonList(cl2));

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        cl2.removeLinks(end1, Collections.singletonList("CL1"));
        cl2.addLinks(end1, Collections.singletonList("CL1"));

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        cl2.removeLink(end1, "CL1");
        CLink link = cl2.addLink(end1, "CL1");

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        assertEquals(cl2.getLinkObjects(end1).get(0), link);

        cl2.removeLink(end1, cl1);
        cl2.addLink(end1, cl1);

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));
    }

    @Test
    public void testOneToOneRemoveAllLinks() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        model.createAssociation(end1, end2);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");

        cl1.removeAllLinks(end2);

        cl1.setLinks(end2, Collections.singletonList(cl2));

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        cl1.removeAllLinks(end2);

        assertEquals(Collections.emptyList(), cl1.getLinks(end2));
        assertEquals(Collections.emptyList(), cl2.getLinks(end1));

        cl1.setLinks(end2, Collections.singletonList(cl2));

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        cl2.removeAllLinks(end1);

        assertEquals(Collections.emptyList(), cl1.getLinks(end2));
        assertEquals(Collections.emptyList(), cl2.getLinks(end1));
    }

    @Test
    public void testOneToOneRemoveLinks() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        model.createAssociation(end1, end2);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");

        try {
            cl1.removeLink(end2, cl2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link between 'CL1' and 'CL2' can't be removed: it does not exist", e.getMessage());
        }

        try {
            cl1.removeLinks(end2, Collections.singletonList(cl2));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link between 'CL1' and 'CL2' can't be removed: it does not exist", e.getMessage());
        }

        cl1.setLinks(end2, Collections.singletonList(cl2));

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        cl1.removeLinks(end2, Collections.singletonList(cl2));

        assertEquals(Collections.emptyList(), cl1.getLinks(end2));
        assertEquals(Collections.emptyList(), cl2.getLinks(end1));

        cl1.setLink(end2, cl2);

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        cl2.removeLink(end1, cl1);

        assertEquals(Collections.emptyList(), cl1.getLinks(end2));
        assertEquals(Collections.emptyList(), cl2.getLinks(end1));
    }


    @Test
    public void testOneToOneLinkMultiplicity() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        model.createAssociation(end1, end2);
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");

        try {
            cl1.setLinks(end2, Collections.emptyList());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '0', but should be '1'", e.getMessage());
        }

        try {
            cl1.setLink(end2, (CObject) null);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '0', but should be '1'", e.getMessage());
        }


        cl1.addLinks(end2, Collections.emptyList());
        assertEquals(Collections.emptyList(), cl1.getLinks(end2));

        cl1.addLink(end2, (CObject) null);
        assertEquals(Collections.emptyList(), cl1.getLinks(end2));

        CClass cl3 = model.createClass(mcl2, "CL3");

        try {
            cl1.setLinks(end2, Arrays.asList(cl2, cl3));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '2', but should be '1'", e.getMessage());
        }
    }

    @Test
    public void testSetLinksByStrings() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        CClass cl3 = model.createClass(mcl2, "CL3");

        cl1.setLinks(end2, Collections.singletonList("CL2"));
        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));

        cl1.setLinks(end2, Arrays.asList("CL2", "CL3"));
        assertEquals(Arrays.asList(cl2, cl3), cl1.getLinks(end2));


        try {
            cl1.setLinks(end2, Arrays.asList("CL2", "CL4"));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("class 'CL4' unknown", e.getMessage());
        }

        try {
            Integer i = 4;
            cl1.setLinks(end2, Arrays.asList("CL2", i));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("argument '4' is not of type String or CObject", e.getMessage());
        }
    }

    @Test
    public void testSetLinksWithSubclassInstance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CMetaclass mcl3 = model.createMetaclass("MCL3").addSuperclass(mcl2);
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        CClass cl3 = model.createClass(mcl3, "CL3");

        cl1.setLinks(end2, Arrays.asList("CL2", "CL3"));
        assertEquals(Arrays.asList(cl2, cl3), cl1.getLinks(end2));
    }

    @Test
    public void testOneToOneLinkIncompatibleTypes() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        model.createAssociation(end1, end2);
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        CClass cl3 = model.createClass(mcl2, "CL3");

        try {
            cl1.setLinks(end2, Arrays.asList(cl1, cl2, cl3));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link object 'CL1' not compatible with association classifier 'MCL2'", e.getMessage());
        }
    }

    @Test
    public void testOneToOneLinkIsNavigable() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1");
        end1.setNavigable(false);
        CAssociationEnd end2 = mcl2.createEnd("metaclass2", "1");
        end2.setNavigable(false);
        model.createAssociation(end1, end2);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");

        try {
            cl1.setLinks(end2, Collections.singletonList(cl2));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not navigable and thus cannot be accessed from object " +
                    "'CL1'", e.getMessage());
        }

        try {
            cl2.setLinks(end1, Collections.singletonList(cl1));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass1' is not navigable and thus cannot be accessed from object " +
                    "'CL2'", e.getMessage());
        }

        try {
            cl1.getLinks(end2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not navigable and thus cannot be accessed from object " +
                    "'CL1'", e.getMessage());
        }

        try {
            cl2.getLinks(end1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass1' is not navigable and thus cannot be accessed from object " +
                    "'CL2'", e.getMessage());
        }

        try {
            cl1.removeAllLinks(end2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not navigable and thus cannot be accessed from object " +
                    "'CL1'", e.getMessage());
        }

        try {
            cl2.removeAllLinks(end1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass1' is not navigable and thus cannot be accessed from object " +
                    "'CL2'", e.getMessage());
        }

        try {
            cl1.removeLink(end2, cl2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not navigable and thus cannot be accessed from object " +
                    "'CL1'", e.getMessage());
        }

        try {
            cl2.removeLink(end1, cl1);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass1' is not navigable and thus cannot be accessed from object " +
                    "'CL2'", e.getMessage());
        }

        end1.setNavigable(true);

        try {
            cl1.setLink(end2, cl2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not navigable and thus cannot be accessed from object " +
                    "'CL1'", e.getMessage());
        }

        cl2.setLink(end1, cl1);

        try {
            cl1.getLinks(end2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not navigable and thus cannot be accessed from object " +
                    "'CL1'", e.getMessage());
        }

        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        try {
            cl1.removeAllLinks(end2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not navigable and thus cannot be accessed from object " +
                    "'CL1'", e.getMessage());
        }

        cl2.removeAllLinks(end1);
        assertEquals(Collections.emptyList(), cl2.getLinks(end1));


        try {
            cl1.removeLink(end2, cl2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not navigable and thus cannot be accessed from object " +
                    "'CL1'", e.getMessage());
        }

        cl2.addLink(end1, cl1);
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(end1));

        cl2.removeLink(end1, cl1);
        assertEquals(Collections.emptyList(), cl2.getLinks(end1));
    }


    @Test
    public void testOneToOneAssociationUnknown() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1Forward", "1");
        CAssociationEnd end1Back = mcl1.createEnd("metaclass1Back", "1");
        model.createAssociation(end1, end1Back);

        CClass cl2 = model.createClass(mcl2, "CL2");

        try {
            cl2.setLinks(end1, Collections.emptyList());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass1Forward' is not an association target end of 'CL2'", e
                    .getMessage());
        }
    }


    @Test
    public void testOneToNLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2a = model.createClass(mcl2, "CL2a");
        CClass cl2b = model.createClass(mcl2, "CL2b");

        cl1.setLinks(end2, Arrays.asList(cl2a, cl2b));

        assertEquals(Arrays.asList(cl2a, cl2b), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2a.getLinks(end1));
        assertEquals(Collections.singletonList(cl1), cl2b.getLinks(end1));

        cl1.setLinks(end2, Collections.singletonList(cl2a));

        assertEquals(Collections.singletonList(cl2a), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2a.getLinks(end1));
        assertEquals(Collections.emptyList(), cl2b.getLinks(end1));

        cl2b.setLinks(end1, Collections.singletonList(cl1));

        assertEquals(Arrays.asList(cl2a, cl2b), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2a.getLinks(end1));
        assertEquals(Collections.singletonList(cl1), cl2b.getLinks(end1));
    }

    @Test
    public void testOneToNLinkDelete() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2a = model.createClass(mcl2, "CL2a");
        CClass cl2b = model.createClass(mcl2, "CL2b");

        cl1.removeAllLinks(end2);

        cl1.setLinks(end2, Arrays.asList(cl2a, cl2b));

        assertEquals(Arrays.asList(cl2a, cl2b), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2a.getLinks(end1));
        assertEquals(Collections.singletonList(cl1), cl2b.getLinks(end1));

        cl1.removeAllLinks(end2);

        assertEquals(Collections.emptyList(), cl1.getLinks(end2));
        assertEquals(Collections.emptyList(), cl2a.getLinks(end1));
        assertEquals(Collections.emptyList(), cl2b.getLinks(end1));

        cl1.setLinks(end2, Arrays.asList(cl2a, cl2b));

        assertEquals(Arrays.asList(cl2a, cl2b), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2a.getLinks(end1));
        assertEquals(Collections.singletonList(cl1), cl2b.getLinks(end1));

        cl2a.removeAllLinks(end1);

        assertEquals(Collections.singletonList(cl2b), cl1.getLinks(end2));
        assertEquals(Collections.emptyList(), cl2a.getLinks(end1));
        assertEquals(Collections.singletonList(cl1), cl2b.getLinks(end1));
    }

    @Test
    public void testOneTo2NLinkMultiplicity() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "2..*");
        model.createAssociation(end1, end2);
        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2a = model.createClass(mcl2, "CL2a");

        try {
            cl1.setLinks(end2, Collections.emptyList());
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '0', but should be '2..*'", e.getMessage());
        }

        try {
            cl1.setLinks(end2, Collections.singletonList(cl2a));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("link has wrong multiplicity '1', but should be '2..*'", e.getMessage());
        }
    }


    @Test
    public void testNToNLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "*"),
                end2 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);

        CClass cl1a = model.createClass(mcl1, "CL1a");
        CClass cl1b = model.createClass(mcl1, "CL1b");
        CClass cl1c = model.createClass(mcl1, "CL1c");
        CClass cl2a = model.createClass(mcl2, "CL2a");
        CClass cl2b = model.createClass(mcl2, "CL2b");

        cl1a.setLinks(end2, Arrays.asList(cl2a, cl2b));
        cl1b.setLinks(end2, Collections.singletonList(cl2a));
        cl1c.setLinks(end2, Collections.singletonList(cl2b));

        assertEquals(Arrays.asList(cl2a, cl2b), cl1a.getLinks(end2));
        assertEquals(Collections.singletonList(cl2a), cl1b.getLinks(end2));
        assertEquals(Collections.singletonList(cl2b), cl1c.getLinks(end2));
        assertEquals(Arrays.asList(cl1a, cl1b), cl2a.getLinks(end1));
        assertEquals(Arrays.asList(cl1a, cl1c), cl2b.getLinks(end1));

        cl2a.setLinks(end1, Arrays.asList(cl1a, cl1b));
        cl2b.setLinks(end1, Collections.emptyList());

        assertEquals(Collections.singletonList(cl2a), cl1a.getLinks(end2));
        assertEquals(Collections.singletonList(cl2a), cl1b.getLinks(end2));
        assertEquals(Collections.emptyList(), cl1c.getLinks(end2));
        assertEquals(Arrays.asList(cl1a, cl1b), cl2a.getLinks(end1));
        assertEquals(Collections.emptyList(), cl2b.getLinks(end1));
    }

    @Test
    public void testAssociationGetLinks() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "*"),
                end2 = mcl2.createEnd("metaclass2", "*");
        CAssociation association = model.createAssociation(end1, end2);

        CClass cl1a = model.createClass(mcl1, "CL1a");
        CClass cl1b = model.createClass(mcl1, "CL1b");
        CClass cl1c = model.createClass(mcl1, "CL1c");
        CClass cl2a = model.createClass(mcl2, "CL2a");
        CClass cl2b = model.createClass(mcl2, "CL2b");

        cl1a.setLinks(end2, Arrays.asList(cl2a, cl2b));
        cl1b.setLinks(end2, Collections.singletonList(cl2a));
        cl1c.setLinks(end2, Collections.singletonList(cl2b));

        List<CLink> links = association.getLinks();

        assertEquals(4, links.size());
        assertEquals(Arrays.asList(cl1a, cl2a), links.get(0).getLinkedObjects());
        assertEquals(Arrays.asList(cl1a, cl2b), links.get(1).getLinkedObjects());
        assertEquals(Arrays.asList(cl1b, cl2a), links.get(2).getLinkedObjects());
        assertEquals(Arrays.asList(cl1c, cl2b), links.get(3).getLinkedObjects());
    }

    @Test
    public void testNToNLinkRemoveAll() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "*"),
                end2 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);
        CClass cl1a = model.createClass(mcl1, "CL1a");
        CClass cl1b = model.createClass(mcl1, "CL1b");
        CClass cl1c = model.createClass(mcl1, "CL1c");
        CClass cl2a = model.createClass(mcl2, "CL2a");
        CClass cl2b = model.createClass(mcl2, "CL2b");

        cl1a.setLinks(end2, Arrays.asList(cl2a, cl2b));
        cl1b.setLinks(end2, Collections.singletonList(cl2a));
        cl1c.setLinks(end2, Collections.singletonList(cl2b));

        assertEquals(Arrays.asList(cl2a, cl2b), cl1a.getLinks(end2));
        assertEquals(Collections.singletonList(cl2a), cl1b.getLinks(end2));
        assertEquals(Collections.singletonList(cl2b), cl1c.getLinks(end2));
        assertEquals(Arrays.asList(cl1a, cl1b), cl2a.getLinks(end1));
        assertEquals(Arrays.asList(cl1a, cl1c), cl2b.getLinks(end1));

        cl2b.removeAllLinks(end1);

        assertEquals(Collections.singletonList(cl2a), cl1a.getLinks(end2));
        assertEquals(Collections.singletonList(cl2a), cl1b.getLinks(end2));
        assertEquals(Collections.emptyList(), cl1c.getLinks(end2));
        assertEquals(Arrays.asList(cl1a, cl1b), cl2a.getLinks(end1));
        assertEquals(Collections.emptyList(), cl2b.getLinks(end1));
    }

    @Test
    public void testNToNLinkRemoveLinks() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "*"),
                end2 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);
        CClass cl1a = model.createClass(mcl1, "CL1a");
        CClass cl1b = model.createClass(mcl1, "CL1b");
        CClass cl1c = model.createClass(mcl1, "CL1c");
        CClass cl2a = model.createClass(mcl2, "CL2a");
        CClass cl2b = model.createClass(mcl2, "CL2b");

        cl1a.setLinks(end2, Arrays.asList(cl2a, cl2b));
        cl1b.setLinks(end2, Collections.singletonList(cl2a));
        cl1c.setLinks(end2, Collections.singletonList(cl2b));

        assertEquals(Arrays.asList(cl2a, cl2b), cl1a.getLinks(end2));
        assertEquals(Collections.singletonList(cl2a), cl1b.getLinks(end2));
        assertEquals(Collections.singletonList(cl2b), cl1c.getLinks(end2));
        assertEquals(Arrays.asList(cl1a, cl1b), cl2a.getLinks(end1));
        assertEquals(Arrays.asList(cl1a, cl1c), cl2b.getLinks(end1));

        cl2b.removeLinks(end1, Arrays.asList(cl1a, "CL1c"));
        cl1a.removeLink(end2, "CL2a");

        assertEquals(Collections.emptyList(), cl1a.getLinks(end2));
        assertEquals(Collections.singletonList(cl2a), cl1b.getLinks(end2));
        assertEquals(Collections.emptyList(), cl1c.getLinks(end2));
        assertEquals(Collections.singletonList(cl1b), cl2a.getLinks(end1));
        assertEquals(Collections.emptyList(), cl2b.getLinks(end1));
    }


    @Test
    public void testNToNSetSelfLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");

        CAssociationEnd superEnd = mcl1.createEnd("super", "*"),
                subEnd = mcl1.createEnd("sub", "*");
        model.createAssociation(superEnd, subEnd);

        CClass top = model.createClass(mcl1, "Top");
        CClass mid1 = model.createClass(mcl1, "Mid1");
        CClass mid2 = model.createClass(mcl1, "Mid2");
        CClass mid3 = model.createClass(mcl1, "Mid3");
        CClass bottom1 = model.createClass(mcl1, "Bottom1");
        CClass bottom2 = model.createClass(mcl1, "Bottom2");

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
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CAssociationEnd superEnd = mcl1.createEnd("super", "*"),
                subEnd = mcl1.createEnd("sub", "*");
        model.createAssociation(superEnd, subEnd);

        CClass top = model.createClass(mcl1, "Top");
        CClass mid1 = model.createClass(mcl1, "Mid1");
        CClass mid2 = model.createClass(mcl1, "Mid2");
        CClass mid3 = model.createClass(mcl1, "Mid3");
        CClass bottom1 = model.createClass(mcl1, "Bottom1");
        CClass bottom2 = model.createClass(mcl1, "Bottom2");

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
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "*"),
                end3 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);

        CClass cl2 = model.createClass(mcl2, "CL2");
        CClass cl1 = model.createClass(mcl1, "CL1");
        try {
            cl1.setLink(end3, cl2);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not an association target end of 'CL1'", e.getMessage());
        }
        try {
            cl1.setLinks(end3, Collections.singletonList(cl2));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not an association target end of 'CL1'", e.getMessage());
        }
        cl1.setLink(end2, cl2);

        try {
            assertEquals(Collections.singletonList(cl2), cl1.getLinks(end3));
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not an association target end of 'CL1'", e.getMessage());
        }
        assertEquals(Collections.singletonList(cl2), cl1.getLinks(end2));

        try {
            cl1.removeAllLinks(end3);
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("end with role name 'metaclass2' is not an association target end of 'CL1'", e.getMessage());
        }
    }

    @Test
    public void testSetOneToOneLinkInheritance1() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CMetaclass mcl2Sub = model.createMetaclass("MCL2Sub").addSuperclass(mcl2);
        CAssociation association = model.createAssociation(mcl1.createEnd("metaclass1", "1"),
                mcl2.createEnd("metaclass2", "1"));
        CAssociationEnd mcl1End = association.getEndByRoleName("metaclass1");
        CAssociationEnd mcl2End = association.getEndByRoleName("metaclass2");

        CClass cl2 = model.createClass(mcl2Sub, "CL2");
        CClass cl1 = model.createClass(mcl1, "CL1");
        cl1.setLink(mcl2End, cl2);
        CClass cl3 = model.createClass(mcl2Sub, "CL3");

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(mcl2End));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(mcl1End));

        cl1.setLink(association.getEndByClassifier(mcl2), "CL3");

        assertEquals(Collections.singletonList(cl3), cl1.getLinks(mcl2End));
        assertEquals(Collections.singletonList(cl1), cl3.getLinks(mcl1End));
    }


    @Test
    public void testSetOneToOneLinkInheritance2() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CMetaclass mcl1Sub = model.createMetaclass("MCL1Sub").addSuperclass(mcl1);
        CMetaclass mcl2Sub = model.createMetaclass("MCL2Sub").addSuperclass(mcl2).addSuperclass(mcl1);
        CAssociation association = model.createAssociation(mcl1.createEnd("metaclass1", "1"),
                mcl2.createEnd("metaclass2", "1"));
        CAssociationEnd mcl1End = association.getEndByRoleName("metaclass1");
        CAssociationEnd mcl2End = association.getEndByRoleName("metaclass2");

        CClass cl2 = model.createClass(mcl2Sub, "CL2");
        CClass cl1 = model.createClass(mcl1Sub, "CL1");
        cl1.setLink(mcl2End, cl2);
        CClass cl3 = model.createClass(mcl2Sub, "CL3");

        assertEquals(Collections.singletonList(cl2), cl1.getLinks(mcl2End));
        assertEquals(Collections.singletonList(cl1), cl2.getLinks(mcl1End));

        cl1.setLink(association.getEndByClassifier(mcl2), "CL3");

        assertEquals(Collections.singletonList(cl3), cl1.getLinks(mcl2End));
        assertEquals(Collections.singletonList(cl1), cl3.getLinks(mcl1End));
    }


    @Test
    public void testOneToNLinkDeleteInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CMetaclass mcl1Sub = model.createMetaclass("MCL1Sub").addSuperclass(mcl1);
        CMetaclass mcl2Sub = model.createMetaclass("MCL2Sub").addSuperclass(mcl2);
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);
        CClass cl1 = model.createClass(mcl1Sub, "CL1");
        CClass cl2a = model.createClass(mcl2Sub, "CL2a");
        CClass cl2b = model.createClass(mcl2Sub, "CL2b");

        cl1.removeAllLinks(end2);

        cl1.setLinks(end2, Arrays.asList(cl2a, cl2b));

        assertEquals(Arrays.asList(cl2a, cl2b), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2a.getLinks(end1));
        assertEquals(Collections.singletonList(cl1), cl2b.getLinks(end1));

        cl1.removeAllLinks(end2);

        assertEquals(Collections.emptyList(), cl1.getLinks(end2));
        assertEquals(Collections.emptyList(), cl2a.getLinks(end1));
        assertEquals(Collections.emptyList(), cl2b.getLinks(end1));

        cl1.setLinks(end2, Arrays.asList(cl2a, cl2b));

        assertEquals(Arrays.asList(cl2a, cl2b), cl1.getLinks(end2));
        assertEquals(Collections.singletonList(cl1), cl2a.getLinks(end1));
        assertEquals(Collections.singletonList(cl1), cl2b.getLinks(end1));

        cl2a.removeAllLinks(end1);

        assertEquals(Collections.singletonList(cl2b), cl1.getLinks(end2));
        assertEquals(Collections.emptyList(), cl2a.getLinks(end1));
        assertEquals(Collections.singletonList(cl1), cl2b.getLinks(end1));
    }

    @Test
    public void testNToNLinkRemoveAllInheritance() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CMetaclass mcl1Sub = model.createMetaclass("MCL1Sub").addSuperclass(mcl1);
        CMetaclass mcl2Sub = model.createMetaclass("MCL2Sub").addSuperclass(mcl2);
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "*"),
                end2 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);
        CClass cl1a = model.createClass(mcl1Sub, "CL1a");
        CClass cl1b = model.createClass(mcl1Sub, "CL1b");
        CClass cl1c = model.createClass(mcl1Sub, "CL1c");
        CClass cl2a = model.createClass(mcl2Sub, "CL2a");
        CClass cl2b = model.createClass(mcl2Sub, "CL2b");

        cl1a.setLinks(end2, Arrays.asList(cl2a, cl2b));
        cl1b.setLinks(end2, Collections.singletonList(cl2a));
        cl1c.setLinks(end2, Collections.singletonList(cl2b));

        assertEquals(Arrays.asList(cl2a, cl2b), cl1a.getLinks(end2));
        assertEquals(Collections.singletonList(cl2a), cl1b.getLinks(end2));
        assertEquals(Collections.singletonList(cl2b), cl1c.getLinks(end2));
        assertEquals(Arrays.asList(cl1a, cl1b), cl2a.getLinks(end1));
        assertEquals(Arrays.asList(cl1a, cl1c), cl2b.getLinks(end1));

        cl2b.removeAllLinks(end1);

        assertEquals(Collections.singletonList(cl2a), cl1a.getLinks(end2));
        assertEquals(Collections.singletonList(cl2a), cl1b.getLinks(end2));
        assertEquals(Collections.emptyList(), cl1c.getLinks(end2));
        assertEquals(Arrays.asList(cl1a, cl1b), cl2a.getLinks(end1));
        assertEquals(Collections.emptyList(), cl2b.getLinks(end1));
    }

    @Test
    public void testGetLinkObjects() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl1Sub = model.createMetaclass("MCL1SUB").addSuperclass(mcl1);
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CMetaclass mcl2Sub = model.createMetaclass("MCL2SUB").addSuperclass(mcl2);
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "1");
        CAssociation association1 = model.createAssociation(end1, end2);

        CAssociationEnd end3 = mcl1.createEnd("prior", "1"),
                end4 = mcl1.createEnd("next", "1");
        CAssociation association2 = model.createAssociation(end3, end4);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl2, "CL2");
        CClass cl_mcl2Sub = model.createClass(mcl2Sub, "CL_MCL2SUB");
        CClass cl_mcl1Sub = model.createClass(mcl1Sub, "CL_MCL1SUB");

        CLink link, linkOrig;

        linkOrig = cl1.setLink(end2, cl2);
        link = cl1.getLinkObjects(end2).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl1, cl2), link.getLinkedObjects());

        linkOrig = cl1.setLink(end2, cl_mcl2Sub);
        link = cl1.getLinkObjects(end2).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl1, cl_mcl2Sub), link.getLinkedObjects());

        linkOrig = cl1.setLink(end2, cl2);
        link = cl1.getLinkObjects(association1).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl1, cl2), link.getLinkedObjects());

        linkOrig = cl1.setLink(end2, cl_mcl2Sub);
        link = cl1.getLinkObjects(association1).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl1, cl_mcl2Sub), link.getLinkedObjects());

        linkOrig = cl1.setLink(end4, cl1);
        link = cl1.getLinkObjects(end4).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl1, cl1), link.getLinkedObjects());

        linkOrig = cl1.setLink(end4, cl_mcl1Sub);
        link = cl1.getLinkObjects(end4).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl1, cl_mcl1Sub), link.getLinkedObjects());

        linkOrig = cl1.setLink(end4, cl1);
        link = cl1.getLinkObjects(association2).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl1, cl1), link.getLinkedObjects());

        cl1.removeAllLinks(end4);

        linkOrig = cl_mcl1Sub.setLink(end4, cl1);
        link = cl_mcl1Sub.getLinkObjects(association2).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl_mcl1Sub, cl1), link.getLinkedObjects());
    }

    @Test
    public void testGetLinkObjectsSelfLink() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CAssociationEnd end1 = mcl1.createEnd("from", "*"),
                end2 = mcl1.createEnd("to", "*");
        CAssociation association = model.createAssociation(end1, end2);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2 = model.createClass(mcl1, "CL2");

        CLink link, linkOrig;

        // get link objects via association
        linkOrig = cl1.setLink(end2, cl2);
        link = cl1.getLinkObjects(association).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl1, cl2), link.getLinkedObjects());

        // get link objects via end
        linkOrig = cl1.setLink(end2, cl2);
        link = cl1.getLinkObjects(end2).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl1, cl2), link.getLinkedObjects());

        // test the same with the other end
        CClass cl3 = model.createClass(mcl1, "CL3");
        CClass cl4 = model.createClass(mcl1, "CL4");

        // get link objects via association
        linkOrig = cl3.setLink(end1, cl4);
        link = cl3.getLinkObjects(association).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl4, cl3), link.getLinkedObjects());

        // get link objects via end
        linkOrig = cl3.setLink(end1, cl4);
        link = cl3.getLinkObjects(end1).get(0);
        assertEquals(linkOrig, link);
        assertEquals(Arrays.asList(cl4, cl3), link.getLinkedObjects());

    }

    @Test
    public void testGetLinkObjectsSetList() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2a = model.createClass(mcl2, "CL2a");
        CClass cl2b = model.createClass(mcl2, "CL2b");

        List<CLink> linksOrig = cl1.setLinks(end2, Arrays.asList(cl2a, cl2b));
        List<CLink> links = cl1.getLinkObjects(end2);
        assertEquals(linksOrig, links);
        assertEquals(2, links.size());
        assertEquals(cl2a, links.get(0).getLinkedObjectAtTargetEnd(end2));
        assertEquals(cl2b, links.get(1).getLinkedObjectAtTargetEnd(end2));
    }

    @Test
    public void testGetLinkObjectsAddList() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl1 = model.createMetaclass("MCL1");
        CMetaclass mcl2 = model.createMetaclass("MCL2");
        CAssociationEnd end1 = mcl1.createEnd("metaclass1", "1"),
                end2 = mcl2.createEnd("metaclass2", "*");
        model.createAssociation(end1, end2);

        CClass cl1 = model.createClass(mcl1, "CL1");
        CClass cl2a = model.createClass(mcl2, "CL2a");
        CClass cl2b = model.createClass(mcl2, "CL2b");

        List<CLink> linksOrig = cl1.addLinks(end2, Arrays.asList(cl2a, cl2b));
        List<CLink> links = cl1.getLinkObjects(end2);
        assertEquals(linksOrig, links);
        assertEquals(2, links.size());
        assertEquals(cl2a, links.get(0).getLinkedObjectAtTargetEnd(end2));
        assertEquals(cl2b, links.get(1).getLinkedObjectAtTargetEnd(end2));
    }
}
