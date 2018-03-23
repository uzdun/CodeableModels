package codeableModels.impl;

import codeableModels.*;

import java.util.*;

public class CLinkImpl extends CNamedElementImpl implements CLink {
    private final CObject object1;
    private final CObject object2;
    private final CAssociation association;
    private final CTaggedValues taggedValues = new CTaggedValues();
    private final CStereotypeInstanceList stereotypeInstances = new CStereotypeInstanceList(this);

    @Override
    public CAssociation getAssociation() {
        return association;
    }

    @SuppressWarnings("RedundantThrows")
    public CLinkImpl(CModel model, CAssociation association, CObject object1, CObject object2) throws CException {
        super("[" + object1.getName() + " -> " + object2.getName() + "]");
        setModel(model);
        this.association = association;
        this.object1 = object1;
        this.object2 = object2;

    }

    @Override
    public List<CObject> getLinkedObjects() {
        return Arrays.asList(object1, object2);
    }

    @Override
    public CObject getLinkedObjectByName(String objectName) {
        if (object1.getName().equals(objectName)) {
            return object1;
        } else if (object2.getName().equals(objectName)) {
            return object2;
        }
        return null;
    }

    @Override
    public CObject getLinkedObjectByClassifier(CClassifier classifier) {
        if (object1.getClassifier() == classifier) {
            return object1;
        } else if (object2.getClassifier() == classifier) {
            return object2;
        }
        return null;
    }

    @Override
    public CObject getLinkedObjectAtTargetEnd(CAssociationEnd targetEnd) throws CException {
        if (targetEnd == association.getEnds().get(0)) {
            return object1;
        } else if (targetEnd == association.getEnds().get(1)) {
            return object2;
        }
        throw new CException("target end unknown in link");
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
    public CStereotypedElement getStereotypedElement() {
        return association;
    }

    @Override
    public String toString() {
        return getName() + "<" + super.toString() + ">";
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
}
