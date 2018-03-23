package codeableModels.impl;

import codeableModels.*;

import java.util.*;

class CStereotypeList {
    List<CStereotype> stereotypes = new ArrayList<>();
    final CNamedElement element;

    public CStereotypeList(CNamedElement element) {
        this.element = element;
    }

    public List<CStereotype> getStereotypes() {
        return stereotypes;
    }

    private String getNameString() {
        String nameString = "";
        if (element.getName() != null) {
            nameString = " on '" + element.getName() + "'";
        }
        return nameString;
    }

    void addStereotype(CStereotype stereotype) throws CException {
        if (stereotypes.contains(stereotype)) {
            throw new CException("stereotype '" + stereotype.getName() +
                    "' already exists" + getNameString());
        }
        stereotypes.add(stereotype);
    }

    void removeStereotype(CStereotype stereotype) throws CException {
        boolean success = stereotypes.remove(stereotype);
        if (!success) {
            throw new CException("can't remove stereotype '" + stereotype.getName() + "'" +
                    getNameString() + ": does not exist");
        }
    }

    void resetStereotypes() {
        stereotypes = new ArrayList<>();
    }

}
