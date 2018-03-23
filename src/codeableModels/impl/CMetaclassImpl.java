package codeableModels.impl;

import codeableModels.*;

import java.util.*;

public class CMetaclassImpl extends CClassifierImpl implements CMetaclass {
    private final List<CClass> classInstances = new ArrayList<>();
    private final CStereotypeList stereotypeList = new CStereotypeList(this);

    public CMetaclassImpl(String name) {
        super(name);
    }

    void addClassInstance(CClass cl) {
        classInstances.add(cl);
    }

    @Override
    public List<CClass> getClassInstances() {
        return classInstances;
    }

    @Override
    public List<CClass> getAllClassInstances() {
        List<CClass> result = new ArrayList<>(classInstances);
        for (CClassifier cl : getAllSubclasses()) {
            result.addAll(((CMetaclass) cl).getClassInstances());
        }
        return result;
    }

    void removeClassInstance(CClass cl) throws CException {
        boolean success = classInstances.remove(cl);
        if (!success) {
            throw new CException("can't remove class instance '" + cl.getName() + "' from metaclass '" + this.getName()
                    + "': is not a class instance");
        }
    }

    @Override
    public List<CStereotype> getStereotypes() {
        return stereotypeList.getStereotypes();
    }

    @Override
    public void addStereotype(CStereotype stereotype) throws CException {
        stereotypeList.addStereotype(stereotype);
        ((CStereotypeImpl)stereotype).addStereotypedElement(this);
    }

    @Override
    public void addStereotype(String stereotypeString) throws CException {
        CStereotype stereotype = getModel().lookupStereotype(stereotypeString);
        if (stereotype == null) {
            throw new CException("stereotype '" + stereotypeString + "' does not exist");
        }
        addStereotype(stereotype);
    }

    @Override
    public void removeStereotype(CStereotype stereotype) throws CException {
        stereotypeList.removeStereotype(stereotype);
        ((CStereotypeImpl)stereotype).removeStereotypedElement(this);
    }

    @Override
    public void removeStereotype(String stereotypeString) throws CException {
        CStereotype stereotype = getModel().lookupStereotype(stereotypeString);
        if (stereotype == null) {
            throw new CException("stereotype '" + stereotypeString + "' does not exist");
        }
        removeStereotype(stereotype);
    }

    @Override
    protected void cleanupClassifier() throws CException {
        super.cleanupClassifier();
        ArrayList<CClass> delClasses = new ArrayList<>(getClassInstances());
        for (CClass cl : delClasses) {
            getModel().deleteClassifier(cl);
        }
        List<CStereotype> stereotypesCopy = new ArrayList<>(stereotypeList.getStereotypes());
        for (CStereotype stereotype : stereotypesCopy) {
            removeStereotype(stereotype);
        }
        stereotypeList.resetStereotypes();
    }

    @Override
    public CMetaclass addSuperclass(CClassifier superclass) throws CException {
        if (!(superclass instanceof CMetaclass)) {
            throw new CException(
                    "cannot add superclass '" + superclass.getName() + "' to '" + getName() + "': not a metaclass");
        }
        return super.addSuperclass(superclass).asMetaclass();
    }

    @Override
    public CMetaclass addSuperclass(String superclassString) throws CException {
        return super.addSuperclass(superclassString).asMetaclass();
    }

    @Override
    public CMetaclass deleteSuperclass(String name) throws CException {
        return super.deleteSuperclass(name).asMetaclass();
    }

    @Override
    public CMetaclass deleteSuperclass(CClassifier superclass) throws CException {
        return super.deleteSuperclass(superclass).asMetaclass();
    }

    @Override
    public CMetaclass addObjectAttribute(String name, CClassifier classifier) throws CException {
        return super.addObjectAttribute(name, classifier).asMetaclass();
    }

    @Override
    public CMetaclass addObjectAttribute(String name, String classifierName) throws CException {
        return super.addObjectAttribute(name, classifierName).asMetaclass();
    }

    @Override
    public CMetaclass addStringAttribute(String name) throws CException {
        return super.addStringAttribute(name).asMetaclass();
    }

    @Override
    public CMetaclass addIntAttribute(String name) throws CException {
        return super.addIntAttribute(name).asMetaclass();
    }

    @Override
    public CMetaclass addBooleanAttribute(String name) throws CException {
        return super.addBooleanAttribute(name).asMetaclass();
    }

    @Override
    public CMetaclass addFloatAttribute(String name) throws CException {
        return super.addFloatAttribute(name).asMetaclass();
    }

    @Override
    public CMetaclass addDoubleAttribute(String name) throws CException {
        return super.addDoubleAttribute(name).asMetaclass();
    }

    @Override
    public CMetaclass addLongAttribute(String name) throws CException {
        return super.addLongAttribute(name).asMetaclass();
    }

    @Override
    public CMetaclass addCharAttribute(String name) throws CException {
        return super.addCharAttribute(name).asMetaclass();
    }

    @Override
    public CMetaclass addByteAttribute(String name) throws CException {
        return super.addByteAttribute(name).asMetaclass();
    }

    @Override
    public CMetaclass addShortAttribute(String name) throws CException {
        return super.addShortAttribute(name).asMetaclass();
    }

    @Override
    public CMetaclass addEnumAttribute(String name, CEnum enumType) throws CException {
        return super.addEnumAttribute(name, enumType).asMetaclass();
    }

    @Override
    public CMetaclass setAttributeDefaultValue(String name, Object defaultValue) throws CException {
        return super.setAttributeDefaultValue(name, defaultValue).asMetaclass();
    }

    @Override
    public CMetaclass addAttribute(String name, Object defaultValue) throws CException {
        return super.addAttribute(name, defaultValue).asMetaclass();
    }

    @Override
    public CMetaclass deleteAttribute(String name) throws CException {
        return super.deleteAttribute(name).asMetaclass();
    }
}
