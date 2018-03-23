package codeableModels.impl;

import codeableModels.*;

import java.util.*;

public class CObjectImpl extends CNamedElementImpl implements CObject {
    private final CAttributeValues attributeValues = new CAttributeValues();
    // instance used in association links is: for CObjects = this, for CClass = the class as a CObject
    private CObject thisInLinks;
    private CClassifier classifier;

    public CObjectImpl(String name) {
        super(name);
        setThisInLinks(this);
    }

    @Override
    public CClassifier getClassifier() {
        return classifier;
    }

    void setClassifier(CClassifier classifier) {
        this.classifier = classifier;
    }

    @Override
    public boolean instanceOf(CClassifier classifier) {
        return getClassifier() == classifier || getClassifier().getAllSuperclasses().contains(classifier);
    }

    @Override
    public boolean instanceOf(String classifierName) {
        return instanceOf(getModel().lookupClassifier(classifierName));
    }

    private CObject getThisInLinks() {
        return thisInLinks;
    }

    void setThisInLinks(CObject thisObject) {
        thisInLinks = thisObject;
    }

    private static String getRoleNameString(CAssociationEnd targetEnd) {
        String roleNameString = "";
        if (targetEnd.getRoleName() != null) {
            roleNameString = "with role name '" + targetEnd.getRoleName() + "' ";
        }
        return roleNameString;
    }

    private CAssociation getAssociationFromTargetEnd(CAssociationEnd targetEnd) throws CException {
        CAssociation association = getClassifier().getAssociationByEnd(targetEnd);
        if (association != null) {
            CAssociationEnd myEnd = association.getOtherEnd(targetEnd);
            if (thisInLinks.getClassifierPath().contains(myEnd.getClassifier())) {
                // this is my association and my end has my classifier
                return association;
            }
        }
        throw new CException("end " + getRoleNameString(targetEnd) + "is not an association target end of '" +
                thisInLinks.getName() + "'");
    }

    private void checkAssociationWithTargetEndExistsForClassifier(CAssociationEnd targetEnd) throws CException {
        // if we can get the association, it exists, else the get throws an exception
        getAssociationFromTargetEnd(targetEnd);
    }

    private void checkIsNavigable(CAssociationEnd targetEnd) throws CException {
        if (!targetEnd.isNavigable()) {
            throw new CException("end " + getRoleNameString(targetEnd) + "is not navigable and thus cannot be accessed from object '" +
                    thisInLinks.getName() + "'");
        }
    }


    private CLink addLinkToCObject(CAssociationEnd targetEnd, CObject linkObject) throws CException {
        CAssociation association = getAssociationFromTargetEnd(targetEnd);
        return association.addLink(targetEnd, getThisInLinks(), linkObject);
    }

    private List<CLink> addLinksToCObjects(CAssociationEnd targetEnd, List<CObject> linkObjects) throws CException {
        List<CLink> addedLinks = new ArrayList<>();
        for (CObject object : linkObjects) {
            addedLinks.add(addLinkToCObject(targetEnd, object));
        }
        return addedLinks;
    }

    private List<CObject> convertObjectListToCObjects(List<Object> links) throws CException {
        List<CObject> objectList = new ArrayList<>();
        for (Object link : links) {
            CObject object;
            if (link instanceof CObject) {
                object = (CObject) link;
            } else if (link instanceof String) {
                if (classifier instanceof CMetaclass) {
                    object = getModel().getClass((String) link);
                    if (object == null) {
                        throw new CException("class '" + link + "' unknown");
                    }
                } else {
                    object = getModel().getObject((String) link);
                    if (object == null) {
                        throw new CException("object '" + link + "' unknown");
                    }
                }
            } else {
                throw new CException("argument '" + link + "' is not of type String or CObject");
            }
            objectList.add(object);
        }
        return objectList;
    }

    @Override
    public List<CLink> addLinks(CAssociationEnd targetEnd, List<Object> links) throws CException {
        return addLinksToCObjects(targetEnd, convertObjectListToCObjects(links));
    }

    @Override
    public CLink addLink(CAssociationEnd targetEnd, CObject link) throws CException {
        if (link == null) {
            addLinks(targetEnd, new ArrayList<>(Collections.emptyList()));
            return null;
        }
        List<CLink> addedLinks = addLinks(targetEnd, new ArrayList<>(Collections.singletonList(link)));
        return addedLinks.get(0);
    }

    @Override
    public CLink addLink(CAssociationEnd targetEnd, String link) throws CException {
        if (link == null) {
            addLinks(targetEnd, new ArrayList<>(Collections.emptyList()));
            return null;
        }
        List<CLink> addedLinks = addLinks(targetEnd, new ArrayList<>(Collections.singletonList(link)));
        return addedLinks.get(0);
    }

    @Override
    public List<CLink> getLinkObjects(CAssociationEnd targetEnd) throws CException {
        CAssociation association = getAssociationFromTargetEnd(targetEnd);
        return association.getLinksByObject(targetEnd, thisInLinks);
    }

    @Override
    public List<CLink> getLinkObjects(CAssociation association) throws CException {
        CAssociationEnd myEnd = association.getEndByClassifier(getClassifier());
        if (myEnd == null) {
            throw new CException("end for classifier '" + getClassifier().getName() + "' unknown in association");
        }
        CAssociationEnd targetEnd = association.getOtherEnd(myEnd);
        List<CLink> links = new ArrayList<>(association.getLinksByObject(targetEnd, thisInLinks));
        // if the target end also matches the classifier, this is a link from a class to itself -> consider also
        // the link objects stored in the other direction.
        if (CAssociationImpl.checkClassifierMatches(getClassifier(), targetEnd.getClassifier())) {
            links.addAll(association.getLinksByObject(myEnd, thisInLinks));
        }
        return links;
    }

    @Override
    public List<CObject> getLinks(CAssociationEnd targetEnd) throws CException {
        checkIsNavigable(targetEnd);
        List<CObject> results = new ArrayList<>();
        List<CLink> links = getLinkObjects(targetEnd);
        for (CLink link : links) {
            CObject object = link.getLinkedObjectAtTargetEnd(targetEnd);
            if (object != thisInLinks) {
                results.add(object);
            }
        }
        return results;
    }

    @Override
    public void removeLink(CAssociationEnd targetEnd, CObject target) throws CException {
        CAssociation association = getAssociationFromTargetEnd(targetEnd);
        checkIsNavigable(targetEnd);
        association.removeLink(targetEnd, thisInLinks, target);
    }

    @Override
    public void removeLink(CAssociationEnd targetEnd, String targetString) throws CException {
        removeLinks(targetEnd, new ArrayList<>(Collections.singletonList(targetString)));
    }

    @Override
    public void removeLinks(CAssociationEnd targetEnd, List<Object> targets) throws CException {
        List<CObject> targetObjects = convertObjectListToCObjects(targets);
        for (CObject target : targetObjects) {
            removeLink(targetEnd, target);
        }
    }

    @Override
    public void removeAllLinks(CAssociationEnd targetEnd) throws CException {
        CAssociation association = getAssociationFromTargetEnd(targetEnd);
        checkIsNavigable(targetEnd);
        List<CLink> linksOfThisObject = new ArrayList<>(association.getLinksByObject(targetEnd, thisInLinks));
        for (CLink targetLink : linksOfThisObject) {
            association.removeLink(targetLink);
        }
    }

    @Override
    public List<CLink> setLinks(CAssociationEnd targetEnd, List<Object> links) throws CException {
        checkAssociationWithTargetEndExistsForClassifier(targetEnd);
        checkIsNavigable(targetEnd);
        if (links.isEmpty()) {
            // if this sets the links to 0, addLinks is not triggered and will not check that
            // the multiplicity 0 is acceptable, so we check here, before performing the removal
            CAssociationImpl.checkAssociationMultiplicityRange(targetEnd, 0);
        }
        removeAllLinks(targetEnd);
        return addLinks(targetEnd, links);
    }

    @Override
    public CLink setLink(CAssociationEnd targetEnd, CObject link) throws CException {
        if (link == null) {
            setLinks(targetEnd, new ArrayList<>(Collections.emptyList()));
            return null;
        }
        List<CLink> links = setLinks(targetEnd, new ArrayList<>(Collections.singletonList(link)));
        return links.get(0);
    }

    @Override
    public CLink setLink(CAssociationEnd targetEnd, String link) throws CException {
        if (link == null) {
            setLinks(targetEnd, new ArrayList<>(Collections.emptyList()));
            return null;
        }
        List<CLink> links = setLinks(targetEnd, new ArrayList<>(Collections.singletonList(link)));
        return links.get(0);
    }

    @Override
    public Object getAttributeValue(CClassifier classifier, String attributeName) throws CException {
        CAttribute attribute = classifier.getAttribute(attributeName);
        if (attribute == null) {
            throw new CException("attribute '" + attributeName + "' unknown for classifier '" + classifier.getName()
                    + "' on object '" + getName() + "'");
        }
        return attributeValues.get(classifier, attributeName);
    }

    @Override
    public void setAttributeValue(CClassifier classifier, String attributeName, Object value) throws CException {
        CAttribute attribute = classifier.getAttribute(attributeName);
        if (attribute == null) {
            throw new CException("attribute '" + attributeName + "' unknown for classifier '" + classifier.getName()
                    + "' on object '" + getName() + "'");
        }
        CAttributeImpl.checkAttributeValueType(attributeName, ((CAttributeImpl) attribute), value);
        attributeValues.add(classifier, attributeName, value);
    }

    @Override
    public Object getAttributeValue(String attributeName) throws CException {
        for (CClassifier classifier : getClassifierPath()) {
            if (classifier.getAttribute(attributeName) != null) {
                return getAttributeValue(classifier, attributeName);
            }
        }
        throw new CException("attribute '" + attributeName + "' unknown for object '" + getName() + "'");
    }

    @Override
    public void setAttributeValue(String attributeName, Object value) throws CException {
        for (CClassifier classifier : getClassifierPath()) {
            if (classifier.getAttribute(attributeName) != null) {
                setAttributeValue(classifier, attributeName, value);
                return;
            }
        }
        throw new CException("attribute '" + attributeName + "' unknown for object '" + getName() + "'");
    }

    private List<CClassifier> getClassifierPathSuperclasses(CClassifier classifier) {
        List<CClassifier> classifierPath = new ArrayList<>();
        classifierPath.add(classifier);
        for (CClassifier superclass : classifier.getSuperclasses()) {
            for (CClassifier cl : getClassifierPathSuperclasses(superclass)) {
                if (!classifierPath.contains(cl)) {
                    classifierPath.add(cl);
                }
            }
        }
        return classifierPath;
    }

    @Override
    public List<CClassifier> getClassifierPath() {
        return getClassifierPathSuperclasses(getClassifier());
    }

}
