package codeableModels;

public interface CAssociationEnd {

    CClassifier getClassifier();

    String getRoleName();

    boolean isNavigable();

    void setNavigable(boolean isNavigable);

    CMultiplicity getMultiplicity();

    String getMultiplicityString();
}