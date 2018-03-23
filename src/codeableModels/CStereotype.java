package codeableModels;

import java.util.*;

public interface CStereotype extends CClassifier {

    List<CStereotypedElement> getStereotypedElements();

    List<CStereotypedElementInstance> getStereotypedElementInstances();

    @Override
    CStereotype addSuperclass(CClassifier superclass) throws CException;

    @Override
    CStereotype addSuperclass(String superclassString) throws CException;

    @Override
    CStereotype deleteSuperclass(String name) throws CException;

    @Override
    CStereotype deleteSuperclass(CClassifier superclass) throws CException;

    @Override
    CStereotype addObjectAttribute(String name, CClassifier classifier) throws CException;

    @Override
    CStereotype addObjectAttribute(String name, String classifierName) throws CException;

    @Override
    CStereotype addStringAttribute(String name) throws CException;

    @Override
    CStereotype addIntAttribute(String name) throws CException;

    @Override
    CStereotype addBooleanAttribute(String name) throws CException;

    @Override
    CStereotype addFloatAttribute(String name) throws CException;

    @Override
    CStereotype addDoubleAttribute(String name) throws CException;

    @Override
    CStereotype addLongAttribute(String name) throws CException;

    @Override
    CStereotype addCharAttribute(String name) throws CException;

    @Override
    CStereotype addByteAttribute(String name) throws CException;

    @Override
    CStereotype addShortAttribute(String name) throws CException;

    @Override
    CStereotype addEnumAttribute(String name, CEnum enumType) throws CException;

    @Override
    CStereotype addAttribute(String name, Object defaultValue) throws CException;

    @Override
    CStereotype setAttributeDefaultValue(String name, Object defaultValue) throws CException;

    @Override
    CStereotype deleteAttribute(String name) throws CException;

}