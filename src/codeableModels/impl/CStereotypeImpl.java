package codeableModels.impl;

import codeableModels.*;

import java.util.*;

public class CStereotypeImpl extends CClassifierImpl implements CStereotype {
    private final List<CStereotypedElement> stereotypedElements = new ArrayList<>();
    private final List<CStereotypedElementInstance> stereotypedElementInstances = new ArrayList<>();

    public CStereotypeImpl(String name) {
        super(name);
    }

    @Override
    public List<CStereotypedElement> getStereotypedElements() {
        return stereotypedElements;
    }

    void addStereotypedElement(CStereotypedElement element) {
        stereotypedElements.add(element);
    }

    void removeStereotypedElement(CStereotypedElement element) {
        stereotypedElements.remove(element);
    }

    /*
    @Override
    public CStereotype setStereotypedElement(CStereotypedElement newStereotypedElement) throws CException {
        if (stereotypedElement != null) {
            stereotypedElement.removeStereotype(this);
        }
        stereotypedElement = newStereotypedElement;
        if (newStereotypedElement != null) {
            if (newStereotypedElement instanceof CAssociation) {
                CAssociation association = (CAssociation) newStereotypedElement;
                CClassifier cl1 = association.getEnds().get(0).getClassifier(),
                        cl2 = association.getEnds().get(1).getClassifier();
                if (!(cl1 instanceof CMetaclass && cl2 instanceof CMetaclass)) {
                    throw new CException("association classifiers '" + cl1.getName() +
                            "' and/or '" + cl2.getName() + "' are not metaclasses");
                }
            }
            newStereotypedElement.addStereotype(this);
        }
        return this;
    }
    */


    private boolean isMetaclassExtendedByThisStereotype(CMetaclass metaclass) {
        if (stereotypedElements.contains(metaclass)) {
            return true;
        }
        for (CClassifier superclass : metaclass.getAllSuperclasses()) {
            CMetaclass scMetaclass = (CMetaclass) superclass;
            if (stereotypedElements.contains(scMetaclass)) {
                return true;
            }
        }
        return false;
    }

    boolean isElementExtendedByStereotype(CStereotypedElement element) throws CException {
        if (element instanceof CMetaclass) {
            CMetaclass metaclass = (CMetaclass) element;
            if (isMetaclassExtendedByThisStereotype(metaclass)) {
                return true;
            }
            for (CClassifier superclass : getAllSuperclasses()) {
                if (((CStereotypeImpl) superclass).isMetaclassExtendedByThisStereotype(metaclass)) {
                    return true;
                }
            }
            return false;
        } else if (element instanceof CAssociation) {
            CAssociation association = (CAssociation) element;
            if (stereotypedElements.contains(association)) {
                return true;
            }
            for (CClassifier superclass : getAllSuperclasses()) {
                if (((CStereotypeImpl) superclass).stereotypedElements.contains(association)) {
                    return true;
                }
            }
            return false;
        }
        String nameString = "";
        if (element.getName() != null) {
            nameString =  element.getName() + " ";
        }
        throw new CException("element " + nameString + "is neither a metaclass nor an association");
    }

    @Override
    public List<CStereotypedElementInstance> getStereotypedElementInstances() {
        return stereotypedElementInstances;
    }

    void addStereotypedElementInstance(CStereotypedElementInstance stereotypedElementInstance) {
        this.stereotypedElementInstances.add(stereotypedElementInstance);
    }

    void removeStereotypedElementInstance(CStereotypedElementInstance stereotypedElementInstance) throws CException {
        boolean success = stereotypedElementInstances.remove(stereotypedElementInstance);
        if (!success) {
            throw new CException("can't remove stereotyped element instance from stereotype" +
                    " '" + this.getName() + "'");
        }
    }

    @Override
    protected void cleanupClassifier() throws CException {
        super.cleanupClassifier();
        List<CStereotypedElement> stereotypedElementsCopy = new ArrayList<>(stereotypedElements);
        for (CStereotypedElement stereotypedElement : stereotypedElementsCopy) {
            stereotypedElement.removeStereotype(this);
        }
    }

    @Override
    public CStereotype addSuperclass(CClassifier superclass) throws CException {
        if (!(superclass instanceof CStereotype)) {
            throw new CException("cannot add superclass '" + superclass.getName() + "' to '"
                    + getName() + "': not a stereotype");
        }
        return super.addSuperclass(superclass).asStereotype();
    }

    @Override
    public CStereotype addSuperclass(String superclassString) throws CException {
        return super.addSuperclass(superclassString).asStereotype();
    }

    @Override
    public CStereotype deleteSuperclass(String name) throws CException {
        return super.deleteSuperclass(name).asStereotype();
    }

    @Override
    public CStereotype deleteSuperclass(CClassifier superclass) throws CException {
        return super.deleteSuperclass(superclass).asStereotype();
    }

    @Override
    public CStereotype addObjectAttribute(String name, CClassifier classifier) throws CException {
        return super.addObjectAttribute(name, classifier).asStereotype();
    }

    @Override
    public CStereotype addObjectAttribute(String name, String classifierName) throws CException {
        return super.addObjectAttribute(name, classifierName).asStereotype();
    }

    @Override
    public CStereotype addStringAttribute(String name) throws CException {
        return super.addStringAttribute(name).asStereotype();
    }

    @Override
    public CStereotype addIntAttribute(String name) throws CException {
        return super.addIntAttribute(name).asStereotype();
    }

    @Override
    public CStereotype addBooleanAttribute(String name) throws CException {
        return super.addBooleanAttribute(name).asStereotype();
    }

    @Override
    public CStereotype addFloatAttribute(String name) throws CException {
        return super.addFloatAttribute(name).asStereotype();
    }

    @Override
    public CStereotype addDoubleAttribute(String name) throws CException {
        return super.addDoubleAttribute(name).asStereotype();
    }

    @Override
    public CStereotype addLongAttribute(String name) throws CException {
        return super.addLongAttribute(name).asStereotype();
    }

    @Override
    public CStereotype addCharAttribute(String name) throws CException {
        return super.addCharAttribute(name).asStereotype();
    }

    @Override
    public CStereotype addByteAttribute(String name) throws CException {
        return super.addByteAttribute(name).asStereotype();
    }

    @Override
    public CStereotype addShortAttribute(String name) throws CException {
        return super.addShortAttribute(name).asStereotype();
    }

    @Override
    public CStereotype addEnumAttribute(String name, CEnum enumType) throws CException {
        return super.addEnumAttribute(name, enumType).asStereotype();
    }

    private void setTaggedValueOnStereotypedElementInstances(List<CStereotypedElementInstance> instances,
                                                             CStereotype stereotype, String name, Object value)
            throws CException {
        for (CStereotypedElementInstance instance : instances) {
            instance.setTaggedValue(stereotype, name, value);
        }
    }

    private void setStereotypeDefaultValuesForOneAttribute(CStereotype stereotype, String name, Object defaultValue) throws CException {
        setTaggedValueOnStereotypedElementInstances(stereotypedElementInstances, stereotype, name, defaultValue);
        for (CClassifier sc : stereotype.getAllSubclasses()) {
            setTaggedValueOnStereotypedElementInstances(((CStereotypeImpl) sc).stereotypedElementInstances, stereotype, name, defaultValue);
        }
    }

    @Override
    public CStereotype addAttribute(String name, Object defaultValue) throws CException {
        CStereotype stereotype = super.addAttribute(name, defaultValue).asStereotype();
        setStereotypeDefaultValuesForOneAttribute(stereotype, name, defaultValue);
        return stereotype;
    }

    @Override
    public CStereotype setAttributeDefaultValue(String name, Object defaultValue) throws CException {
        CStereotype stereotype = super.setAttributeDefaultValue(name, defaultValue).asStereotype();
        setStereotypeDefaultValuesForOneAttribute(stereotype, name, defaultValue);
        return stereotype;
    }

    @Override
    public CStereotype deleteAttribute(String name) throws CException {
        return super.deleteAttribute(name).asStereotype();
    }

}
