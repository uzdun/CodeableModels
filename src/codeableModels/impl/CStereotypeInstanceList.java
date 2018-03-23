package codeableModels.impl;

import codeableModels.*;

import java.util.*;

class CStereotypeInstanceList extends CStereotypeList {
    private CStereotypedElementInstance stereotypedElementInstance;

    public CStereotypeInstanceList(CNamedElement element) throws CException {
        super(element);
        if (element instanceof CStereotypedElementInstance) {
            stereotypedElementInstance = (CStereotypedElementInstance) element;
        } else {
            throw new CException("element " + element.getName() +
                    " is not of type CStereotypedElementInstance");
        }
    }

    private void setAllDefaultTaggedValuesOfStereotype(CStereotype stereotype) throws CException {
        for (CAttribute attribute : stereotype.getAttributes()) {
            if (attribute.getDefaultValue() != null) {
                stereotypedElementInstance.setTaggedValue(stereotype,
                        attribute.getName(), attribute.getDefaultValue());
            }
        }
    }

    public void addStereotype(CStereotype stereotype) throws CException {
        if (stereotypes.contains(stereotype)) {
            throw new CException("stereotype '" + stereotype.getName() + "' cannot be added: it is already a " +
                    "stereotype of '" + element.getName() + "'");
        }
        if (!((CStereotypeImpl) stereotype).isElementExtendedByStereotype(stereotypedElementInstance.getStereotypedElement())) {
            throw new CException("stereotype '" + stereotype.getName() + "' cannot be added to '" + element
                    .getName() + "': no extension by this stereotype found");
        }
        stereotypes.add(stereotype);
        ((CStereotypeImpl) stereotype).addStereotypedElementInstance(stereotypedElementInstance);

        setAllDefaultTaggedValuesOfStereotype(stereotype);
        for (CClassifier sc : stereotype.getAllSuperclasses()) {
            setAllDefaultTaggedValuesOfStereotype((CStereotypeImpl) sc);
        }
    }

    public void removeStereotype(CStereotype stereotype) throws CException {
        super.removeStereotype(stereotype);
        ((CStereotypeImpl) stereotype).removeStereotypedElementInstance(stereotypedElementInstance);
    }


    private List<CStereotype> getStereotypeInstancePathSuperclasses(CStereotype stereotype) {
        List<CStereotype> stereotypePath = new ArrayList<>();
        stereotypePath.add(stereotype);
        for (CClassifier superclass : stereotype.getSuperclasses()) {
            for (CStereotype superclassStereotype : getStereotypeInstancePathSuperclasses((CStereotype) superclass)) {
                if (!stereotypePath.contains(superclassStereotype)) {
                    stereotypePath.add(superclassStereotype);
                }
            }
        }
        return stereotypePath;
    }

    public List<CStereotype> getStereotypeInstancePath() {
        List<CStereotype> stereotypePath = new ArrayList<>();
        for (CStereotype stereotypeOfThisClass : getStereotypes()) {
            for (CStereotype stereotype : getStereotypeInstancePathSuperclasses(stereotypeOfThisClass)) {
                if (!stereotypePath.contains(stereotype)) {
                    stereotypePath.add(stereotype);
                }
            }
        }
        return stereotypePath;
    }


}
