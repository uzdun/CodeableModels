package codeableModels;

import java.util.*;

public interface CModel {

    CMetaclass createMetaclass(String name) throws CException;

    CMetaclass createMetaclass() throws CException;

    CClass createClass(CMetaclass metaclass, String name) throws CException;

    CClass createClass(CMetaclass metaclass) throws CException;

    CClass createClass(String metaclassName, String name) throws CException;

    CClass createClass(String metaclassName) throws CException;

    CStereotype createStereotype(String name) throws CException;

    CStereotype createStereotype() throws CException;

    CStereotype createStereotype(String name, CStereotypedElement stereotypedElement) throws CException;

    CStereotype createStereotype(String name, String stereotypedElementName) throws CException;

    CObject createObject(CClass cl, String name) throws CException;

    CObject createObject(CClass cl) throws CException;

    CObject createObject(String className, String name) throws CException;

    CObject createObject(String className) throws CException;

    CAssociation createAssociation(String name, CAssociationEnd end1, CAssociationEnd end2) throws CException;

    CAssociation createComposition(String name, CAssociationEnd composingEnd, CAssociationEnd composedEnd) throws
            CException;

    CAssociation createAggregation(String name, CAssociationEnd aggregatingEnd, CAssociationEnd aggregatedEnd) throws
            CException;

    CAssociation createAssociation(CAssociationEnd end1, CAssociationEnd end2) throws CException;

    CAssociation createComposition(CAssociationEnd end1, CAssociationEnd end2) throws CException;

    CAssociation createAggregation(CAssociationEnd end1, CAssociationEnd end2) throws CException;

    CModel importModel(CModel model);

    CClassifier getClassifier(String name);

    CMetaclass getMetaclass(String name) throws CException;

    CStereotype getStereotype(String name) throws CException;

    CClass getClass(String name) throws CException;

    CObject getObject(String name);

    CClassifier lookupClassifier(String name);

    CMetaclass lookupMetaclass(String name) throws CException;

    CClass lookupClass(String name) throws CException;

    CStereotype lookupStereotype(String name) throws CException;

    List<String> getClassifierNames();

    List<CClassifier> getClassifiers();

    List<CMetaclass> getMetaclasses();

    List<CClass> getClasses();

    List<CStereotype> getStereotypes();

    List<String> getMetaclassNames();

    List<String> getStereotypeNames();

    List<String> getClassNames();

    void deleteClassifier(CClassifier cl) throws CException;

    List<String> getObjectNames();

    List<CObject> getObjects();

    void deleteObject(CObject o) throws CException;

    List<CModel> getImportedModels();

    List<CModel> getFullModelList();

    List<CAssociation> getAssociations();

    void deleteAssociation(CAssociation assoc) throws CException;

    // returns an array list, as association names don't have to be unique,
    // including null == association with no name
    List<CAssociation> getAssociationsByName(String name);

    CEnum createEnum(String name, List<String> enumValues);

    List<CAssociation> getAssociationsForType(CClassifier type);
}