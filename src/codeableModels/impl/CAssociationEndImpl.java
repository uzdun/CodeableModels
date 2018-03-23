package codeableModels.impl;

import codeableModels.*;

public class CAssociationEndImpl implements CAssociationEnd {
    private String roleName;
    private CMultiplicity multiplicity;
    private boolean isNavigable = true;
    private CClassifier classifier;

    CAssociationEndImpl(CClassifier classifier, String roleName, String multiplicity) throws CException {
        setRoleName(roleName);
        setMultiplicity(multiplicity);
        setClassifier(classifier);
    }

    @Override
    public CClassifier getClassifier() {
        return classifier;
    }

    private void setClassifier(CClassifier classifier) {
        this.classifier = classifier;
    }

    @Override
    public String getRoleName() {
        return roleName;
    }

    private void setRoleName(String roleName) {
        this.roleName = roleName;
    }

    @Override
    public boolean isNavigable() {
        return isNavigable;
    }

    @Override
    public void setNavigable(boolean isNavigable) {
        this.isNavigable = isNavigable;
    }

    @Override
    public CMultiplicity getMultiplicity() {
        return multiplicity;
    }

    @Override
    public String getMultiplicityString() {
        return multiplicity.getMultiplicity();
    }

    private void setMultiplicity(String multiplicityString) throws CException {
        multiplicity = new CMultiplicityImpl(multiplicityString);
    }
}
