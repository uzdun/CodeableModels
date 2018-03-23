package codeableModels;

import java.util.*;

public interface CClassifier extends CNamedElement {

    CAssociationEnd createEnd(String roleName, String multiplicity) throws CException;

    CAssociationEnd createEnd(String multiplicity) throws CException;

    CAssociationEnd createEnd(String roleName, String multiplicity, boolean isNavigable) throws CException;

    List<CAssociation> getAssociations();

    CAssociation getAssociationByRoleName(String roleName);

    CAssociation getAssociationByName(String name);

    CAssociation getAssociationByEnd(CAssociationEnd associationEnd);

    List<CAttribute> getAttributes();

    List<String> getAttributeNames();

    CAttribute getAttribute(String name);

    CClassifier addObjectAttribute(String name, CClassifier classifier) throws CException;

    CClassifier addObjectAttribute(String name, String classifierName) throws CException;

    CClassifier addStringAttribute(String name) throws CException;

    CClassifier addIntAttribute(String name) throws CException;

    CClassifier addBooleanAttribute(String name) throws CException;

    CClassifier addFloatAttribute(String name) throws CException;

    CClassifier addDoubleAttribute(String name) throws CException;

    CClassifier addLongAttribute(String name) throws CException;

    CClassifier addCharAttribute(String name) throws CException;

    CClassifier addByteAttribute(String name) throws CException;

    CClassifier addShortAttribute(String name) throws CException;

    CClassifier addEnumAttribute(String name, CEnum enumType) throws CException;

    CClassifier addAttribute(String name, Object defaultValue) throws CException;

    CClassifier setAttributeDefaultValue(String name, Object defaultValue) throws CException;

    CClassifier deleteAttribute(String name) throws CException;

    CMetaclass asMetaclass() throws CException;

    CStereotype asStereotype() throws CException;

    CClass asClass() throws CException;

    List<CClassifier> getSuperclasses();

    List<CClassifier> getSubclasses();

    List<CClassifier> getAllSuperclasses();

    List<CClassifier> getAllSubclasses();

    CClassifier addSuperclass(String name) throws CException;

    CClassifier addSuperclass(CClassifier superclass) throws CException;

    CClassifier deleteSuperclass(CClassifier superclass) throws CException;

    CClassifier deleteSuperclass(String name) throws CException;

    boolean hasSuperclass(CClassifier cl);

    boolean hasSubclass(CClassifier cl);

    boolean hasSuperclass(String clName);

    boolean hasSubclass(String clName);
}