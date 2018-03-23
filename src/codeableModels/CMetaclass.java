package codeableModels;

import java.util.*;

public interface CMetaclass extends CClassifier, CStereotypedElement {

    List<CClass> getClassInstances();

    List<CClass> getAllClassInstances();

    @Override
    CMetaclass addSuperclass(CClassifier superclass) throws CException;

    @Override
    CMetaclass addSuperclass(String superclassString) throws CException;

    @Override
    CMetaclass deleteSuperclass(String name) throws CException;

    @Override
    CMetaclass deleteSuperclass(CClassifier superclass) throws CException;

    @Override
    CMetaclass addObjectAttribute(String name, CClassifier classifier) throws CException;

    @Override
    CMetaclass addObjectAttribute(String name, String classifierName) throws CException;

    @Override
    CMetaclass addStringAttribute(String name) throws CException;

    @Override
    CMetaclass addIntAttribute(String name) throws CException;

    @Override
    CMetaclass addBooleanAttribute(String name) throws CException;

    @Override
    CMetaclass addFloatAttribute(String name) throws CException;

    @Override
    CMetaclass addDoubleAttribute(String name) throws CException;

    @Override
    CMetaclass addLongAttribute(String name) throws CException;

    @Override
    CMetaclass addCharAttribute(String name) throws CException;

    @Override
    CMetaclass addByteAttribute(String name) throws CException;

    @Override
    CMetaclass addShortAttribute(String name) throws CException;

    @Override
    CMetaclass addEnumAttribute(String name, CEnum enumType) throws CException;

    @Override
    CMetaclass addAttribute(String name, Object defaultValue) throws CException;

    @Override
    CMetaclass setAttributeDefaultValue(String name, Object defaultValue) throws CException;

    @Override
    CMetaclass deleteAttribute(String name) throws CException;

}