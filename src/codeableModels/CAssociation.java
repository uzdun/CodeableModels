package codeableModels;

import java.util.*;

public interface CAssociation extends CNamedElement, CStereotypedElement {

    // for Aggregation/Composition we assume end1 is the aggregating end
    boolean isAggregation();

    void setAggregation(boolean isAggregation);

    boolean isComposition();

    void setComposition(boolean isComposition);

    List<CAssociationEnd> getEnds();

    boolean hasEndType(CClassifier type);

    CAssociationEnd getEndByRoleName(String roleName);

    CAssociationEnd getEndByClassifier(CClassifier classifier);

    CAssociationEnd getOtherEnd(CAssociationEnd end) throws CException;

    CLink addLink(CAssociationEnd targetEnd, CObject object1, CObject object2) throws CException;

    List<CLink> getLinksByObject(CAssociationEnd targetEnd, CObject object);

    void removeLink(CAssociationEnd targetEnd, CObject object1, CObject object2) throws CException;

    void removeLink(CLink linkToBeRemoved);

    List<CLink> getLinks();

}