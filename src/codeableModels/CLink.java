package codeableModels;

import java.util.*;

public interface CLink extends CStereotypedElementInstance {

    CAssociation getAssociation();

    List<CObject> getLinkedObjects();

    CObject getLinkedObjectByName(String objectName);

    CObject getLinkedObjectByClassifier(CClassifier classifier);

    CObject getLinkedObjectAtTargetEnd(CAssociationEnd targetEnd) throws CException;
}