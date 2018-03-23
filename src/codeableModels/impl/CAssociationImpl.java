package codeableModels.impl;

import codeableModels.*;

import java.util.*;

public class CAssociationImpl extends CNamedElementImpl implements CAssociation {
    private CAssociationEnd end1, end2;
    private boolean isAggregation = false;
    private boolean isComposition = false;
    private final CStereotypeList stereotypeList = new CStereotypeList(this);
    private final List<CLink> links = new ArrayList<>();

    public CAssociationImpl(CModel model, String name) {
        // if an association should have no name, pass null as an argument
        super(name);
        setModel(model);
    }

    // for Aggregation/Composition we assume end1 is the aggregating end
    @Override
    public boolean isAggregation() {
        return isAggregation;
    }

    @Override
    public void setAggregation(boolean isAggregation) {
        if (isAggregation) {
            setComposition(false);
        }
        this.isAggregation = isAggregation;
    }

    @Override
    public boolean isComposition() {
        return isComposition;
    }

    @Override
    public void setComposition(boolean isComposition) {
        if (isComposition) {
            setAggregation(false);
        }
        this.isComposition = isComposition;
    }

    @Override
    public List<CAssociationEnd> getEnds() {
        return Arrays.asList(end1, end2);
    }

    void setEnd1(CAssociationEnd end1) {
        this.end1 = end1;
    }

    void setEnd2(CAssociationEnd end2) {
        this.end2 = end2;
    }

    @Override
    public boolean hasEndType(CClassifier type) {
        return end1.getClassifier() == type || end2.getClassifier() == type;
    }

    @Override
    public CAssociationEnd getEndByRoleName(String roleName) {
        if (end1.getRoleName().equals(roleName)) {
            return end1;
        } else if (end2.getRoleName().equals(roleName)) {
            return end2;
        }
        return null;
    }

    public static boolean checkClassifierMatches(CClassifier classifier, CClassifier endClassifier) {
        // a check identical to the one in  getEndByClassifier, but just for one classifier
        return endClassifier == classifier || endClassifier.getAllSuperclasses().contains(classifier) ||
                classifier.getAllSuperclasses().contains(endClassifier);
    }

    @Override
    public CAssociationEnd getEndByClassifier(CClassifier classifier) {
        // first check direct classifiers, then go up the hierarchy for the types of ends, if that also fails
        // check whether the provided classifier is of the type of one of the ends
        if (end1.getClassifier() == classifier) {
            return end1;
        } else if (end2.getClassifier() == classifier) {
            return end2;
        } else if (end1.getClassifier().getAllSuperclasses().contains(classifier)) {
            return end1;
        } else if (end2.getClassifier().getAllSuperclasses().contains(classifier)) {
            return end2;
        } else if (classifier.getAllSuperclasses().contains(end1.getClassifier())) {
            return end1;
        } else if (classifier.getAllSuperclasses().contains(end2.getClassifier())) {
            return end2;
        }

        return null;
    }

    @Override
    public CAssociationEnd getOtherEnd(CAssociationEnd end) throws CException {
        if (end1 == end) {
            return end2;
        } else if (end2 == end) {
            return end1;
        } else {
            String roleNameString = "";
            if (end.getRoleName() != null) {
                roleNameString = ": '" + end.getRoleName() + "'";
            }
            throw new CException("end unknown in association" + roleNameString);
        }
    }

    @Override
    public List<CStereotype> getStereotypes() {
        return stereotypeList.getStereotypes();
    }

    @Override
    public void addStereotype(CStereotype stereotype) throws CException {
        CClassifier cl1 = end1.getClassifier(), cl2 = end2.getClassifier();
        if (!(cl1 instanceof CMetaclass && cl2 instanceof CMetaclass)) {
            throw new CException("association classifiers '" + cl1.getName() +
                    "' and/or '" + cl2.getName() + "' are not metaclasses");
        }
        stereotypeList.addStereotype(stereotype);
        ((CStereotypeImpl)stereotype).addStereotypedElement(this);
    }

    @Override
    public void removeStereotype(CStereotype stereotype) throws CException {
        stereotypeList.removeStereotype(stereotype);
        ((CStereotypeImpl)stereotype).removeStereotypedElement(this);
    }

    @Override
    public void addStereotype(String stereotypeString) throws CException {
        CStereotype extension = getModel().lookupStereotype(stereotypeString);
        if (extension == null) {
            throw new CException("stereotype '" + stereotypeString + "' does not exist");
        }
        addStereotype(extension);
    }

    @Override
    public void removeStereotype(String stereotypeString) throws CException {
        CStereotype extension = getModel().lookupStereotype(stereotypeString);
        if (extension == null) {
            throw new CException("stereotype '" + stereotypeString + "' does not exist");
        }
        stereotypeList.removeStereotype(extension);
    }

    static void checkAssociationMultiplicityRange(CAssociationEnd end, int listSize) throws CException {
        CMultiplicity endMultiplicity = end.getMultiplicity();
        if ((endMultiplicity.getUpperMultiplicity() != CMultiplicityImpl.STAR_MULTIPLICITY && listSize >
                endMultiplicity.getUpperMultiplicity()) || listSize < endMultiplicity.getLowerMultiplicity()) {
            throw new CException("link has wrong multiplicity '" + listSize + "', but " +
                    "should be '" + endMultiplicity.toString() + "'");
        }
    }

    @Override
    public CLink addLink(CAssociationEnd targetEnd, CObject from, CObject to) throws CException {
        CObject object1 = from, object2 = to;

        if (end1 == targetEnd) {
            object1 = to;
            object2 = from;
        }

        if(!object1.getClassifierPath().contains(end1.getClassifier())) {
            throw new CException("link object '" + object1.getName() + "' not compatible with association classifier '" +
                    end1.getClassifier().getName() + "'");
        }
        if(!object2.getClassifierPath().contains(end2.getClassifier())) {
            throw new CException("link object '" + object2.getName() + "' not compatible with association classifier '" +
                    end2.getClassifier().getName() + "'");
        }

        int object1ToAnyCount = 1, object2ToAnyCount = 1;

        for (CLink link : links) {
            if (link.getLinkedObjects().get(0) == object1 && link.getLinkedObjects().get(1) == object2) {
                throw new CException("link between '" + object1.getName() + "' and '" + object2.getName() + "' already exists");
            }
            if (link.getLinkedObjects().get(0) == object1) {
                object1ToAnyCount++;
            }
            if (link.getLinkedObjects().get(1) == object2) {
                object2ToAnyCount++;
            }
        }

        checkAssociationMultiplicityRange(end2, object1ToAnyCount);
        checkAssociationMultiplicityRange(end1, object2ToAnyCount);

        CLink link = new CLinkImpl(object1.getModel(),this, object1, object2);
        links.add(link);
        return link;
    }

    @Override
    public List<CLink> getLinksByObject(CAssociationEnd targetEnd, CObject object) {
        List<CLink> results = new ArrayList<>();
        for (CLink link : links) {
            if (targetEnd == end1 && link.getLinkedObjects().get(1) == object) {
                results.add(link);
            }
            if (targetEnd == end2 && link.getLinkedObjects().get(0) == object) {
                results.add(link);
            }
        }
        return results;
    }

    @Override
    public void removeLink(CAssociationEnd targetEnd, CObject object1, CObject object2) throws CException {
        List<CLink> linksOfObject1 = getLinksByObject(targetEnd, object1);
        for (CLink link : linksOfObject1) {
            if (link.getLinkedObjects().contains(object2)) {
                links.remove(link);
                return;
            }
        }
        throw new CException("link between '" + object1.getName() + "' and '" + object2.getName() + "' can't be removed: it does not exist");
    }

    @Override
    public void removeLink(CLink linkToBeRemoved) {
        links.remove(linkToBeRemoved);
    }


    @Override
    public List<CLink> getLinks() {
        return links;
    }

}
