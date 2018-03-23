package codeableModels.tests;

import codeableModels.*;
import org.junit.*;

import java.util.*;

import static org.junit.Assert.*;

public class TestsImportModel {

    private static CModel buildModel1() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass mcl = model.createMetaclass("MCL");
        CClassifier a = model.createClass(mcl, "A");
        CClassifier b = model.createClass(mcl, "B");
        CClassifier c = model.createClass(mcl, "C");
        model.createAssociation(c.createEnd("c", "*"), a.createEnd("a", "1"));
        model.createAssociation(a.createEnd("a", "*"), b.createEnd("b", "1"));
        model.createClass(mcl, "X").addSuperclass("A");
        return model;
    }

    private static CModel buildMetaModel1() throws CException {
        CModel model = CodeableModels.createModel();
        CMetaclass a = model.createMetaclass("A");
        model.createStereotype("Stereotype1");
        a.addStereotype("Stereotype1");
        CMetaclass b = model.createMetaclass("B");
        model.createStereotype("Stereotype2");
        b.addStereotype("Stereotype2");
        CMetaclass c = model.createMetaclass("C");
        model.createAssociation(c.createEnd("c", "*"), a.createEnd("a", "1"));
        model.createAssociation(a.createEnd("a", "*"), b.createEnd("b", "1"));
        model.createMetaclass("X").addSuperclass("A");
        return model;
    }

    @Test
    public void testImportModel() throws CException {
        CModel model1 = buildModel1();
        CModel model = CodeableModels.createModel();
        model.importModel(model1);
        CObject xObj = model.createObject("X", "x");
        CClassifier xClass = model1.getClassifier("X");
        CClassifier aClass = model1.getClassifier("A");

        assertEquals(Collections.singletonList(model1), model.getImportedModels());
        assertEquals(Arrays.asList(model, model1), model.getFullModelList());
        assertEquals(xClass, xObj.getClassifier());
        assertEquals(2, aClass.getAssociations().size());
        assertEquals(1, xClass.getSuperclasses().size());
        assertEquals(aClass, xClass.getSuperclasses().get(0));
    }

    @Test
    public void testImportModelLinks() throws CException {
        CModel model1 = buildModel1();
        CModel model = CodeableModels.createModel();
        model.importModel(model1);
        CObject aObj = model.createObject("A", "a");
        CObject bObj = model.createObject("B", "b");
        CAssociation association = bObj.getClassifier().getAssociationByRoleName("a");
        CAssociationEnd aEnd = association.getEndByRoleName("a");
        CAssociationEnd bEnd = association.getEndByRoleName("b");
        bObj.addLink(aEnd, aObj);
        assertEquals(Collections.singletonList(bObj), aObj.getLinks(bEnd));
        assertEquals(Collections.singletonList(aObj), bObj.getLinks(aEnd));
    }

    @Test
    public void testImportImportedModelLinks() throws CException {
        CModel model1 = buildModel1();
        CModel model2 = CodeableModels.createModel().importModel(model1);
        model2.createClass("MCL","BSub").addSuperclass("B");
        CModel model = CodeableModels.createModel();
        model.importModel(model2);
        CObject aObj = model.createObject("A", "a");
        CObject bObj = model.createObject("BSub", "b");
        CAssociation association = bObj.getClassifier().getAssociationByRoleName("a");
        CAssociationEnd aEnd = association.getEndByRoleName("a");
        CAssociationEnd bEnd = association.getEndByRoleName("b");
        bObj.addLink(aEnd, aObj);
        assertEquals(Collections.singletonList(bObj), aObj.getLinks(bEnd));
        assertEquals(Collections.singletonList(aObj), bObj.getLinks(aEnd));
    }

    @Test
    public void testImportMultipleModels() throws CException {
        CModel model1 = CodeableModels.createModel();
        CModel model2 = CodeableModels.createModel().importModel(model1);
        CModel model3 = CodeableModels.createModel();
        CModel model4 = CodeableModels.createModel().importModel(model2).importModel(model3);

        model1.createMetaclass("MCL");
        model2.createClass("MCL", "CL");
        model3.createMetaclass("MCL2");
        model4.createClass("MCL", "CL2");
        model4.createClass("MCL2", "CL3");
        model4.createObject("CL", "O");

        assertEquals(Collections.singletonList(model1), model2.getImportedModels());
        assertEquals(Collections.emptyList(), model3.getImportedModels());
        assertEquals(Arrays.asList(model2, model3), model4.getImportedModels());

        assertEquals(Arrays.asList(model2, model1), model2.getFullModelList());
        assertEquals(Collections.singletonList(model3), model3.getFullModelList());
        assertEquals(Arrays.asList(model4, model2, model1, model3), model4.getFullModelList());
    }

    @Test
    public void testImportImportedModel() throws CException {
        CModel model1 = buildModel1();

        // import model
        CModel model2 = CodeableModels.createModel().importModel(model1);
        CMetaclass mcl = model2.createMetaclass("MCL");
        model2.createClass(mcl, "Y").addSuperclass("B");

        // import imported model
        CModel model = CodeableModels.createModel();
        model.importModel(model2);
        CObject xObj = model.createObject("X", "x");
        CObject yObj = model.createObject("Y", "y");
        CClassifier xClass = model.lookupClass("X");
        CClassifier yClass = model.lookupClass("Y");
        CClassifier aClass = model.lookupClass("A");
        CClassifier bClass = model.lookupClass("B");

        assertEquals(xClass, xObj.getClassifier());
        assertEquals(yClass, yObj.getClassifier());
        assertEquals(2, aClass.getAssociations().size());
        assertEquals(1, xClass.getSuperclasses().size());
        assertEquals(1, yClass.getSuperclasses().size());
        assertEquals(aClass, xClass.getSuperclasses().get(0));
        assertEquals(bClass, yClass.getSuperclasses().get(0));

        CClassifier x2Class = model1.lookupClass("X");
        CClassifier y2Class = model1.lookupClass("Y");
        CClassifier a2Class = model1.lookupClass("A");
        CClassifier x3Class = model2.lookupClass("X");
        CClassifier y3Class = model2.lookupClass("Y");
        CClassifier a3Class = model2.lookupClass("A");

        assertEquals(xClass, x2Class);
        assertEquals(xClass, x3Class);
        assertEquals(null, y2Class);
        assertEquals(yClass, y3Class);
        assertEquals(aClass, a2Class);
        assertEquals(aClass, a3Class);
    }

    @Test
    public void testImportMetaModel() throws CException {
        CModel model1 = buildMetaModel1();
        CModel model = CodeableModels.createModel();
        model.importModel(model1);
        CClass xClass = model.createClass("X", "x");
        CClassifier xMetaclass = model1.getClassifier("X");
        CClassifier aMetaclass = model1.getClassifier("A");

        assertEquals(xMetaclass, xClass.getMetaclass());
        assertEquals(2, aMetaclass.getAssociations().size());
        assertEquals(1, xMetaclass.getSuperclasses().size());
        assertEquals(aMetaclass, xMetaclass.getSuperclasses().get(0));
    }

    @Test
    public void testImportMetaModelLinks() throws CException {
        CModel model1 = buildMetaModel1();
        CModel model = CodeableModels.createModel();
        model.importModel(model1);
        CClass aClass = model.createClass("A", "a");
        CClass bClass = model.createClass("B", "b");
        CAssociation association = bClass.getClassifier().getAssociationByRoleName("a");
        CAssociationEnd aAssociationEnd = association.getEndByClassifier(aClass.getClassifier());
        CAssociationEnd bAssociationEnd = association.getEndByClassifier(bClass.getClassifier());
        bClass.addLink(aAssociationEnd, aClass);
        assertEquals(Collections.singletonList(bClass), aClass.getLinks(bAssociationEnd));
        assertEquals(Collections.singletonList(aClass), bClass.getLinks(aAssociationEnd));
    }


    @Test
    public void testImportImportedMetaModelLinks() throws CException {
        CModel model1 = buildMetaModel1();
        CModel model2 = CodeableModels.createModel().importModel(model1);
        CModel model = CodeableModels.createModel();
        model.importModel(model2);
        CClass aClass = model.createClass("A", "a");
        CClass bClass = model.createClass("B", "b");
        CAssociation association = bClass.getClassifier().getAssociationByRoleName("a");
        CAssociationEnd aAssociationEnd = association.getEndByClassifier(aClass.getClassifier());
        CAssociationEnd bAssociationEnd = association.getEndByClassifier(bClass.getClassifier());
        bClass.addLink(aAssociationEnd, aClass);
        assertEquals(Collections.singletonList(bClass), aClass.getLinks(bAssociationEnd));
        assertEquals(Collections.singletonList(aClass), bClass.getLinks(aAssociationEnd));
    }

    @Test
    public void testImportImportedMetaModel() throws CException {
        CModel model1 = buildMetaModel1();

        // import model
        CModel model2 = CodeableModels.createModel().importModel(model1);
        model2.createMetaclass("Y").addSuperclass("B");

        // import imported model
        CModel model = CodeableModels.createModel();
        model.importModel(model2);
        CClass xClass = model.createClass("X", "x");
        CClass yClass = model.createClass("Y", "y");
        CClassifier xMetaclass = model.lookupMetaclass("X");
        CClassifier yMetaclass = model.lookupMetaclass("Y");
        CClassifier aMetaclass = model.lookupMetaclass("A");
        CClassifier bMetaclass = model.lookupMetaclass("B");

        assertEquals(xMetaclass, xClass.getMetaclass());
        assertEquals(yMetaclass, yClass.getMetaclass());
        assertEquals(2, aMetaclass.getAssociations().size());
        assertEquals(1, xMetaclass.getSuperclasses().size());
        assertEquals(1, yMetaclass.getSuperclasses().size());
        assertEquals(aMetaclass, xMetaclass.getSuperclasses().get(0));
        assertEquals(bMetaclass, yMetaclass.getSuperclasses().get(0));

        CClassifier x2Class = model1.lookupMetaclass("X");
        CClassifier y2Class = model1.lookupMetaclass("Y");
        CClassifier a2Class = model1.lookupMetaclass("A");
        CClassifier x3Class = model2.lookupMetaclass("X");
        CClassifier y3Class = model2.lookupMetaclass("Y");
        CClassifier a3Class = model2.lookupMetaclass("A");

        assertEquals(xMetaclass, x2Class);
        assertEquals(xMetaclass, x3Class);
        assertEquals(null, y2Class);
        assertEquals(yMetaclass, y3Class);
        assertEquals(aMetaclass, a2Class);
        assertEquals(aMetaclass, a3Class);
    }


    @Test
    public void testImportStereotype() throws CException {
        CModel model1 = buildMetaModel1();

        CModel model2 = CodeableModels.createModel().importModel(model1);
        model2.createClass("A", "C1");
        model2.createClass("A", "C2").addStereotypeInstance("Stereotype1");

        assertEquals(model1.getMetaclass("A").getStereotypes().get(0), model2.getClass("C2").getStereotypeInstances().get(0));
    }


    @Test
    public void testImportStereotypeNameConflict() throws CException {
        CModel model1 = buildMetaModel1();

        CModel model2 = CodeableModels.createModel().importModel(model1);
        model2.createClass("A", "M1");
        CClass cl = model2.createClass("A", "Stereotype1");

        // name conflict ...
        try {
            cl.addStereotypeInstance("Stereotype1");
            fail("exception not thrown");
        } catch (CException e) {
            assertEquals("'Stereotype1' is not a stereotype", e.getMessage());
        }

        // ... can be resolved by looking up the object reference
        cl.addStereotypeInstance(model1.getStereotype("Stereotype1"));

        assertEquals(model1.getMetaclass("A").getStereotypes().get(0), model2.getClass("Stereotype1").getStereotypeInstances().get(0));
    }


}
