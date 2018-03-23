package codeableModels;

public interface CMultiplicity {

    int STAR_MULTIPLICITY = -1;

    String getMultiplicity();

    int getUpperMultiplicity();

    int getLowerMultiplicity();

}