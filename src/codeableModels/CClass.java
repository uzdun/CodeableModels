package codeableModels;

import java.util.*;

public interface CClass extends CClassifier, CObject, CStereotypedElementInstance {

    List<CObject> getInstances();

    List<CObject> getAllInstances();

    CMetaclass getMetaclass();

    @Override
    CClass addSuperclass(CClassifier superclass) throws CException;

    @Override
    CClass addSuperclass(String superclassString) throws CException;

    @Override
    CClass deleteSuperclass(String name) throws CException;

    @Override
    CClass deleteSuperclass(CClassifier superclass) throws CException;

    CClass addObjectAttribute(String name, CClass classifier) throws CException;

    @Override
    CClass addObjectAttribute(String name, String classifierName) throws CException;

    @Override
    CClass addStringAttribute(String name) throws CException;

    @Override
    CClass addIntAttribute(String name) throws CException;

    @Override
    CClass addBooleanAttribute(String name) throws CException;

    @Override
    CClass addFloatAttribute(String name) throws CException;

    @Override
    CClass addDoubleAttribute(String name) throws CException;

    @Override
    CClass addLongAttribute(String name) throws CException;

    @Override
    CClass addCharAttribute(String name) throws CException;

    @Override
    CClass addByteAttribute(String name) throws CException;

    @Override
    CClass addShortAttribute(String name) throws CException;

    @Override
    CClass addEnumAttribute(String name, CEnum enumType) throws CException;

    @Override
    CClass addAttribute(String name, Object defaultValue) throws CException;

    @Override
    CClass setAttributeDefaultValue(String name, Object defaultValue) throws CException;

    @Override
    CClass deleteAttribute(String name) throws CException;
}