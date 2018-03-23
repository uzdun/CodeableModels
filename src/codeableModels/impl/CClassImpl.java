package codeableModels.impl;

import codeableModels.*;

import java.util.*;

public class CClassImpl extends CClassifierImpl implements CClass, CObject, CStereotypedElementInstance {
    private final List<CObject> instances = new ArrayList<>();
    private final CStereotypeInstanceList stereotypeInstances = new CStereotypeInstanceList(this);
    private final CObject classObject;
    private final CTaggedValues taggedValues = new CTaggedValues();

    @SuppressWarnings("RedundantThrows")
    public CClassImpl(String name) throws CException {
        super(name);
        classObject = new CObjectImpl(name);
        ((CObjectImpl) classObject).setThisInLinks(this);
    }

    void addInstance(CObject obj) {
        instances.add(obj);
    }

    @Override
    public void setModel(CModel model) {
        super.setModel(model);
        classObject.setModel(model);
    }

    CObjectImpl getClassObjectImpl() {
        return (CObjectImpl) classObject;
    }

    @Override
    public List<CObject> getInstances() {
        return instances;
    }

    @Override
    public List<CObject> getAllInstances() {
        List<CObject> result = new ArrayList<>(instances);
        for (CClassifier cl : getAllSubclasses()) {
            result.addAll(((CClass) cl).getInstances());
        }
        return result;
    }

    void removeInstance(CObject delObj) throws CException {
        boolean success = instances.remove(delObj);
        if (!success) {
            throw new CException("can't remove instance '" + delObj.getName() + "' from class '" + this.getName()
                    + "': is not an instance of this class");
        }
    }

    @Override
    protected void cleanupClassifier() throws CException {
        super.cleanupClassifier();
        ArrayList<CObject> objectsToDelete = new ArrayList<>(getInstances());
        for (CObject obj : objectsToDelete) {
            getModel().deleteObject(obj);
        }
        if (getMetaclass() != null) {
            ((CMetaclassImpl) getMetaclass()).removeClassInstance(this);
            setMetaclass(null);
        }
    }

    @Override
    public CMetaclass getMetaclass() {
        return (CMetaclass) classObject.getClassifier();
    }

    void setMetaclass(CMetaclass metaclass) {
        ((CObjectImpl) classObject).setClassifier(metaclass);
        if (metaclass != null)
            ((CMetaclassImpl) metaclass).addClassInstance(this);
    }

    @Override
    public CClass addSuperclass(CClassifier superclass) throws CException {
        if (!(superclass instanceof CClass)) {
            throw new CException(
                    "cannot add superclass '" + superclass.getName() + "' to '" + getName() + "': not a class");
        }
        return super.addSuperclass(superclass).asClass();
    }

    @Override
    public CClass addSuperclass(String superclassString) throws CException {
        return super.addSuperclass(superclassString).asClass();
    }

    @Override
    public CClass deleteSuperclass(String name) throws CException {
        return super.deleteSuperclass(name).asClass();
    }

    @Override
    public CClass deleteSuperclass(CClassifier superclass) throws CException {
        return super.deleteSuperclass(superclass).asClass();
    }


    @Override
    public CClass addObjectAttribute(String name, CClass classifier) throws CException {
        return super.addObjectAttribute(name, classifier).asClass();
    }

    @Override
    public CClass addObjectAttribute(String name, String classifierName) throws CException {
        return super.addObjectAttribute(name, classifierName).asClass();
    }

    @Override
    public CClass addStringAttribute(String name) throws CException {
        return super.addStringAttribute(name).asClass();
    }

    @Override
    public CClass addIntAttribute(String name) throws CException {
        return super.addIntAttribute(name).asClass();
    }

    @Override
    public CClass addBooleanAttribute(String name) throws CException {
        return super.addBooleanAttribute(name).asClass();
    }

    @Override
    public CClass addFloatAttribute(String name) throws CException {
        return super.addFloatAttribute(name).asClass();
    }

    @Override
    public CClass addDoubleAttribute(String name) throws CException {
        return super.addDoubleAttribute(name).asClass();
    }

    @Override
    public CClass addLongAttribute(String name) throws CException {
        return super.addLongAttribute(name).asClass();
    }

    @Override
    public CClass addCharAttribute(String name) throws CException {
        return super.addCharAttribute(name).asClass();
    }

    @Override
    public CClass addByteAttribute(String name) throws CException {
        return super.addByteAttribute(name).asClass();
    }

    @Override
    public CClass addShortAttribute(String name) throws CException {
        return super.addShortAttribute(name).asClass();
    }

    @Override
    public CClass addEnumAttribute(String name, CEnum enumType) throws CException {
        return super.addEnumAttribute(name, enumType).asClass();
    }

    @Override
    public CClass addAttribute(String name, Object defaultValue) throws CException {
        return super.addAttribute(name, defaultValue).asClass();
    }

    @Override
    public CClass setAttributeDefaultValue(String name, Object defaultValue) throws CException {
        return super.setAttributeDefaultValue(name, defaultValue).asClass();
    }

    @Override
    public CClass deleteAttribute(String name) throws CException {
        return super.deleteAttribute(name).asClass();
    }

    @Override
    public CStereotypedElement getStereotypedElement() {
        return getMetaclass();
    }

    @Override
    public void addStereotypeInstance(String name) throws CException {
        CStereotype stereotype = getModel().lookupStereotype(name);
        if (stereotype == null) {
            throw new CException("stereotype '" + name + "' does not exist");
        }
        addStereotypeInstance(stereotype);
    }

    @Override
    public void addStereotypeInstance(CStereotype stereotype) throws CException {
        stereotypeInstances.addStereotype(stereotype);
    }

    @Override
    public void deleteStereotypeInstance(String name) throws CException {
        CStereotype stereotype = getModel().getStereotype(name);
        if (stereotype == null) {
            throw new CException("stereotype '" + name + "' does not exist");
        }
        deleteStereotypeInstance(stereotype);
    }

    @Override
    public void deleteStereotypeInstance(CStereotype stereotype) throws CException {
        stereotypeInstances.removeStereotype(stereotype);
    }

    @Override
    public List<CStereotype> getStereotypeInstances() {
        return stereotypeInstances.getStereotypes();
    }

    @Override
    public CClassifier getClassifier() {
        return classObject.getClassifier();
    }

    @Override
    public boolean instanceOf(CClassifier classifier) {
        return classObject.instanceOf(classifier);
    }

    @Override
    public boolean instanceOf(String classifierName) {
        return classObject.instanceOf(classifierName);
    }

    @Override
    public List<CLink> addLinks(CAssociationEnd targetEnd, List<Object> links) throws CException {
        return classObject.addLinks(targetEnd, links);
    }

    @Override
    public CLink addLink(CAssociationEnd targetEnd, CObject link) throws CException {
        return classObject.addLink(targetEnd, link);
    }

    @Override
    public CLink addLink(CAssociationEnd targetEnd, String link) throws CException {
        List<CLink> links = addLinks(targetEnd, new ArrayList<>(Collections.singletonList(link)));
        return links.get(0);
    }

    @Override
    public List<CLink> setLinks(CAssociationEnd targetEnd, List<Object> links) throws CException {
        return classObject.setLinks(targetEnd, links);
    }

    @Override
    public CLink setLink(CAssociationEnd targetEnd, CObject link) throws CException {
        return classObject.setLink(targetEnd, link);
    }

    @Override
    public CLink setLink(CAssociationEnd targetEnd, String link) throws CException {
        List<CLink> links = setLinks(targetEnd, new ArrayList<>(Collections.singletonList(link)));
        return links.get(0);
    }

    @Override
    public List<CLink> getLinkObjects(CAssociationEnd targetEnd) throws CException {
        return classObject.getLinkObjects(targetEnd);
    }

    @Override
    public List<CLink> getLinkObjects(CAssociation association) throws CException {
        return classObject.getLinkObjects(association);
    }

    @Override
    public List<CObject> getLinks(CAssociationEnd targetEnd) throws CException {
        return classObject.getLinks(targetEnd);
    }

    @Override
    public void removeLink(CAssociationEnd targetEnd, CObject target) throws CException {
        classObject.removeLink(targetEnd, target);
    }

    @Override
    public void removeLink(CAssociationEnd targetEnd, String targetString) throws CException {
        classObject.removeLink(targetEnd, targetString);
    }

    @Override
    public void removeLinks(CAssociationEnd targetEnd, List<Object> targets) throws CException {
        classObject.removeLinks(targetEnd, targets);
    }

    @Override
    public void removeAllLinks(CAssociationEnd targetEnd) throws CException {
        classObject.removeAllLinks(targetEnd);
    }

    @Override
    public Object getAttributeValue(CClassifier classifier, String attributeName) throws CException {
        return classObject.getAttributeValue(classifier, attributeName);
    }

    @Override
    public void setAttributeValue(CClassifier classifier, String attributeName, Object value) throws CException {
        classObject.setAttributeValue(classifier, attributeName, value);
    }

    @Override
    public Object getAttributeValue(String attributeName) throws CException {
        return classObject.getAttributeValue(attributeName);
    }

    @Override
    public void setAttributeValue(String attributeName, Object value) throws CException {
        classObject.setAttributeValue(attributeName, value);
    }

    @Override
    public Object getTaggedValue(CStereotype stereotype, String taggedValueName) throws CException {
        return taggedValues.getTaggedValue(stereotypeInstances.getStereotypeInstancePath(), stereotype, taggedValueName);
    }

    @Override
    public void setTaggedValue(CStereotype stereotype, String taggedValueName, Object value) throws CException {
        taggedValues.setTaggedValue(stereotypeInstances.getStereotypeInstancePath(), stereotype, taggedValueName, value);
    }

    @Override
    public Object getTaggedValue(String taggedValueName) throws CException {
        return taggedValues.getTaggedValue(stereotypeInstances.getStereotypeInstancePath(), taggedValueName);
    }

    @Override
    public void setTaggedValue(String taggedValueName, Object value) throws CException {
        taggedValues.setTaggedValue(stereotypeInstances.getStereotypeInstancePath(), taggedValueName, value);
    }

    @Override
    public List<CClassifier> getClassifierPath() {
        return classObject.getClassifierPath();
    }

}
