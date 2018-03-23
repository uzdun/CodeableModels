package codeableModels;

import java.util.*;

public interface CStereotypedElement extends CNamedElement {

    List<CStereotype> getStereotypes();

    void addStereotype(CStereotype stereotype) throws CException;

    void removeStereotype(CStereotype stereotype) throws CException;

    void addStereotype(String stereotypeString) throws CException;

    void removeStereotype(String stereotypeString) throws CException;

}