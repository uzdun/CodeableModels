package codeableModels;

import java.util.*;

public interface CStereotypedElementInstance extends CNamedElement {

    Object getTaggedValue(CStereotype stereotype, String taggedValueName) throws CException;

    void setTaggedValue(CStereotype stereotype, String taggedValueName, Object value) throws CException;

    Object getTaggedValue(String taggedValueName) throws CException;

    void setTaggedValue(String taggedValueName, Object value) throws CException;

    CStereotypedElement getStereotypedElement();

    void addStereotypeInstance(String name) throws CException;

    void addStereotypeInstance(CStereotype stereotype) throws CException;

    void deleteStereotypeInstance(String name) throws CException;

    void deleteStereotypeInstance(CStereotype stereotype) throws CException;

    List<CStereotype> getStereotypeInstances();
}