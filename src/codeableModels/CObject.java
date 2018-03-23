package codeableModels;

import java.util.*;

public interface CObject extends CNamedElement {

    CClassifier getClassifier();

    boolean instanceOf(CClassifier classifier);

    boolean instanceOf(String classifierName);

    // Terminology as in UML: Associations represent relationships between classes; links represent relationships between objects.

    List<CLink> addLinks(CAssociationEnd targetEnd, List<Object> links) throws CException;

    CLink addLink(CAssociationEnd targetEnd, CObject link) throws CException;

    CLink addLink(CAssociationEnd targetEnd, String link) throws CException;

    List<CLink> getLinkObjects(CAssociationEnd targetEnd) throws CException;

    List<CLink> getLinkObjects(CAssociation association) throws CException;

    List<CObject> getLinks(CAssociationEnd targetEnd) throws CException;

    void removeLink(CAssociationEnd targetEnd, CObject target) throws CException;

    void removeLink(CAssociationEnd targetEnd, String targetString) throws CException;

    void removeLinks(CAssociationEnd targetEnd, List<Object> targets) throws CException;

    void removeAllLinks(CAssociationEnd targetEnd) throws CException;

    List<CLink> setLinks(CAssociationEnd targetEnd, List<Object> links) throws CException;

    CLink setLink(CAssociationEnd targetEnd, CObject link) throws CException;

    CLink setLink(CAssociationEnd targetEnd, String link) throws CException;

    Object getAttributeValue(CClassifier classifier, String attributeName) throws CException;

    void setAttributeValue(CClassifier classifier, String attributeName, Object value) throws CException;

    // uses the first classifier on the classifier path of the object that defines an attribute with the name
    Object getAttributeValue(String attributeName) throws CException;

    // uses the first classifier on the classifier path of the object that defines an attribute with the name
    void setAttributeValue(String attributeName, Object value) throws CException;

    List<CClassifier> getClassifierPath();

}