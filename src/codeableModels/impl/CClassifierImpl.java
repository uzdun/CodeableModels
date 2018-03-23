package codeableModels.impl;

import codeableModels.*;

import java.util.*;

public abstract class CClassifierImpl extends CNamedElementImpl implements CClassifier {
    private final List<CAssociation> associations = new ArrayList<>();
    private final Map<String, CAttribute> attributes = new LinkedHashMap<>();
    private List<CClassifier> superclasses = new ArrayList<>();
    private List<CClassifier> subclasses = new ArrayList<>();

    CClassifierImpl(String name) {
        super(name);
    }

    @Override
    public CAssociationEnd createEnd(String multiplicity) throws CException {
        // guess the role name from the classifier name
        String roleName = this.getName().toLowerCase();
        return new CAssociationEndImpl(this, roleName, multiplicity);
    }

    @Override
    public CAssociationEnd createEnd(String roleName, String multiplicity) throws CException {
        return new CAssociationEndImpl(this, roleName, multiplicity);
    }

    @Override
    public CAssociationEnd createEnd(String roleName, String multiplicity, boolean isNavigable) throws CException {
        CAssociationEnd ae = createEnd(roleName, multiplicity);
        ae.setNavigable(isNavigable);
        return ae;
    }

    @Override
    public List<CAssociation> getAssociations() {
        return associations;
    }

    @Override
    public CAssociation getAssociationByRoleName(String roleName) {
        List<CAssociation> objAssociations = getModel().getAssociationsForType(this);
        for (CAssociation a : objAssociations) {
            CAssociationEnd end = a.getEndByRoleName(roleName);
            if (end != null && end.getClassifier() != this &&
                    !this.getAllSuperclasses().contains(end.getClassifier())) {
                return a;
            }
        }
        return null;
    }

    @Override
    public CAssociation getAssociationByEnd(CAssociationEnd associationEnd) {
        List<CAssociation> objAssociations = getModel().getAssociationsForType(this);
        for (CAssociation a : objAssociations) {
            if (a.getEnds().get(0) == associationEnd || a.getEnds().get(1) == associationEnd) {
                return a;
            }
        }
        return null;
    }


    @Override
    public CAssociation getAssociationByName(String name) {
        List<CAssociation> objAssociations = getModel().getAssociationsForType(this);
        for (CAssociation a : objAssociations) {
            if (a.getName() != null && a.getName().equals(name)) {
                return a;
            }
        }
        return null;
    }

    void addAssociation(CAssociation assoc) {
        associations.add(assoc);
    }

    void removeAssociation(CAssociation assoc) throws CException {
        boolean success = associations.remove(assoc);
        if (!success) {
            throw new CException("can't remove association '" + assoc.getName() + "' from classifier '" + this.getName()
                    + "': is not an association");
        }
    }

    private void removeAllAssociations() throws CException {
        List<CAssociation> associations = new ArrayList<>();

        // make a copy of associations as elements get deleted below.
        // make it unique, as not to double trigger deletion of a self-reference, which
        // is twice listed in the list of associations
        for (CAssociation assoc : this.associations) {
            if (!associations.contains(assoc)) {
                associations.add(assoc);
            }
        }

        for (CAssociation assoc : associations) {
            getModel().deleteAssociation(assoc);
        }
    }

    @Override
    public List<CAttribute> getAttributes() {
        return new ArrayList<>(attributes.values());
    }

    @Override
    public List<String> getAttributeNames() {
        return new ArrayList<>(attributes.keySet());
    }

    private CAttribute createAttribute(int typeCode, String name) throws CException {
        if (!CAttributeImpl.isLegalAttributeTypeCode(typeCode)) {
            throw new CException("attribute type for attribute '" + name + "' unknown");
        }
        if (getAttribute(name) != null) {
            throw new CException("attribute '" + name + "' cannot be created, attribute name already exists");
        }

        CAttribute attr = new CAttributeImpl();
        ((CAttributeImpl) attr).setTypeCode(typeCode);
        attr.setName(name);
        attributes.put(name, attr);
        return attr;
    }

    @Override
    public CAttribute getAttribute(String name) {
        return attributes.get(name);
    }

    private CClassifier addAttribute(int type, String name) throws CException {
        createAttribute(type, name);
        return this;
    }

    @Override
    public CClassifier addObjectAttribute(String name, CClassifier classifier) throws CException {
        CAttributeImpl attribute = (CAttributeImpl) createAttribute(CAttributeImpl.OBJECT, name);
        attribute.setTypeClassifier(classifier);
        return this;
    }

    @Override
    public CClassifier addObjectAttribute(String name, String classifierName) throws CException {
        CClassifier classifier = getModel().getClassifier(classifierName);
        return addObjectAttribute(name, classifier);
    }

    @Override
    public CClassifier addStringAttribute(String name) throws CException {
        return addAttribute(CAttributeImpl.STRING, name);
    }

    @Override
    public CClassifier addIntAttribute(String name) throws CException {
        return addAttribute(CAttributeImpl.INT, name);
    }

    @Override
    public CClassifier addBooleanAttribute(String name) throws CException {
        return addAttribute(CAttributeImpl.BOOLEAN, name);
    }

    @Override
    public CClassifier addFloatAttribute(String name) throws CException {
        return addAttribute(CAttributeImpl.FLOAT, name);
    }

    @Override
    public CClassifier addDoubleAttribute(String name) throws CException {
        return addAttribute(CAttributeImpl.DOUBLE, name);
    }

    @Override
    public CClassifier addLongAttribute(String name) throws CException {
        return addAttribute(CAttributeImpl.LONG, name);
    }

    @Override
    public CClassifier addCharAttribute(String name) throws CException {
        return addAttribute(CAttributeImpl.CHAR, name);
    }

    @Override
    public CClassifier addByteAttribute(String name) throws CException {
        return addAttribute(CAttributeImpl.BYTE, name);
    }

    @Override
    public CClassifier addShortAttribute(String name) throws CException {
        return addAttribute(CAttributeImpl.SHORT, name);
    }

    @Override
    public CClassifier addEnumAttribute(String name, CEnum enumType) throws CException {
        CAttributeImpl attribute = (CAttributeImpl) createAttribute(CAttributeImpl.ENUM, name);
        attribute.setEnumType(enumType);
        return this;
    }

    @Override
    public CClassifier setAttributeDefaultValue(String name, Object defaultValue) throws CException {
        CAttribute attribute = attributes.get(name);
        if (attribute == null) {
            throw new CException("unknown attribute name '" + name +"' on classifier '" + getName() + "'");
        }
        attribute.setDefaultValue(defaultValue);
        return this;
    }

    @Override
    public CClassifier addAttribute(String name, Object defaultValue) throws CException {
        int attributeType = CAttributeImpl.getAttributeTypeCodeOfObject(defaultValue);
        if (attributeType == CAttributeImpl.UNKNOWN_TYPE)
            throw new CException("value for attribute '" + name + "' is not a known attribute type");
        CAttribute attr = createAttribute(attributeType, name);
        if (attributeType == CAttributeImpl.OBJECT) {
            ((CAttributeImpl) attr).setTypeClassifier(((CObject) defaultValue).getClassifier());
        }
        attr.setDefaultValue(defaultValue);
        return this;
    }

    @Override
    public CClassifier deleteAttribute(String name) throws CException {
        if (attributes.containsKey(name)) {
            attributes.remove(name);
            return this;
        }
        throw new CException(
                "attribute '" + name + "' to be deleted not defined on classifier '" + this.getName() + "'");
    }

    @Override
    public CMetaclass asMetaclass() throws CException {
        if (this instanceof CMetaclass) {
            return (CMetaclass) this;
        }
        throw new CException("'" + getName() + "' is not a metaclass");
    }

    @Override
    public CStereotype asStereotype() throws CException {
        if (this instanceof CStereotype) {
            return (CStereotype) this;
        }
        throw new CException("'" + getName() + "' is not a stereotype");
    }

    @Override
    public CClass asClass() throws CException {
        if (this instanceof CClass) {
            return (CClass) this;
        }
        throw new CException("'" + getName() + "' is not a class");
    }

    @Override
    public List<CClassifier> getSuperclasses() {
        return superclasses;
    }

    @Override
    public List<CClassifier> getSubclasses() {
        return subclasses;
    }

    private Set<CClassifier> getAllSuperclasses(Set<CClassifier> iteratedClasses) {
        if (superclasses == null) {
            return null;
        }
        Set<CClassifier> orderedResultSet = new LinkedHashSet<>();

        for (CClassifier c : superclasses) {
            CClassifierImpl cImpl = (CClassifierImpl) c;
            if (!iteratedClasses.contains(cImpl)) {
                iteratedClasses.add(cImpl);
                orderedResultSet.add(cImpl);
                Set<CClassifier> sc = cImpl.getAllSuperclasses(iteratedClasses);
                if (sc != null) {
                    orderedResultSet.addAll(sc);
                }
            }
        }
        return orderedResultSet;
    }

    @Override
    public List<CClassifier> getAllSuperclasses() {
        Set<CClassifier> orderedResultSet = getAllSuperclasses(new LinkedHashSet<>());
        if (orderedResultSet == null) {
            return new ArrayList<>();
        }
        return new ArrayList<>(orderedResultSet);
    }

    private Set<CClassifier> getAllSubclasses(Set<CClassifier> iteratedClasses) {
        if (subclasses == null) {
            return null;
        }
        Set<CClassifier> orderedResultSet = new LinkedHashSet<>();

        for (CClassifier c : subclasses) {
            CClassifierImpl cImpl = (CClassifierImpl) c;
            if (!iteratedClasses.contains(cImpl)) {
                iteratedClasses.add(cImpl);
                orderedResultSet.add(cImpl);
                Set<CClassifier> sc = cImpl.getAllSubclasses(iteratedClasses);
                if (sc != null) {
                    orderedResultSet.addAll(sc);
                }
            }
        }
        return orderedResultSet;
    }

    @Override
    public List<CClassifier> getAllSubclasses() {
        Set<CClassifier> orderedResultSet = getAllSubclasses(new LinkedHashSet<>());
        if (orderedResultSet == null) {
            return new ArrayList<>();
        }
        return new ArrayList<>(orderedResultSet);
    }

    private void resetSuperclasses() {
        superclasses = new ArrayList<>();
    }

    private void resetSubclasses() {
        subclasses = new ArrayList<>();
    }

    private void removeSubclass(CClassifier subclass) throws CException {
        boolean success = subclasses.remove(subclass);
        if (!success) {
            throw new CException("can't remove subclass '" + subclass.getName() + "' from classifier '" + this.getName()
                    + "': is not a subclass");
        }
    }

    private void removeSuperclass(CClassifier superclass) throws CException {
        boolean success = superclasses.remove(superclass);
        if (!success) {
            throw new CException("can't remove subclass '" + superclass.getName() + "' from classifier '"
                    + this.getName() + "': is not a subclass");
        }
    }

    @Override
    public CClassifier addSuperclass(String name) throws CException {
        CModel model = getModel();
        CClassifier superclass = model.lookupClassifier(name);
        if (superclass == null) {
            throw new CException("can't find superclass '" + name + "'");
        }
        return addSuperclass(superclass);
    }

    @Override
    public CClassifier addSuperclass(CClassifier superclass) throws CException {
        CClassifierImpl superclassImpl = (CClassifierImpl) superclass;
        if (superclasses.contains(superclassImpl)) {
            throw new CException(
                    "'" + superclassImpl.getName() + "' is already a superclass of '" + this.getName() + "'");
        }
        if (superclassImpl.subclasses.contains(this)) {
            throw new CException(
                    "'" + this.getName() + "' is already a subclass of '" + superclassImpl.getName() + "'");
        }
        this.superclasses.add(superclassImpl);
        superclassImpl.subclasses.add(this);
        return this;
    }

    @Override
    public CClassifier deleteSuperclass(CClassifier superclass) throws CException {
        CClassifierImpl superclassImpl = (CClassifierImpl) superclass;
        superclassImpl.removeSubclass(this);
        this.removeSuperclass(superclassImpl);
        return this;
    }

    @Override
    public CClassifier deleteSuperclass(String name) throws CException {
        CClassifier superclass = getModel().getClassifier(name);
        return deleteSuperclass(superclass);
    }

    void cleanupClassifier() throws CException {
        for (CClassifier superclass : getSuperclasses()) {
            ((CClassifierImpl) superclass).removeSubclass(this);
        }
        resetSuperclasses();
        for (CClassifier subclass : getSubclasses()) {
            ((CClassifierImpl) subclass).removeSuperclass(this);
        }
        resetSubclasses();
        removeAllAssociations();
    }

    @Override
    public boolean hasSuperclass(CClassifier cl) {
        return getAllSuperclasses().contains(cl);
    }

    @Override
    public boolean hasSuperclass(String clName) {
        return hasSuperclass(getModel().getClassifier(clName));
    }

    @Override
    public boolean hasSubclass(CClassifier cl) {
        return getAllSubclasses().contains(cl);
    }

    @Override
    public boolean hasSubclass(String clName) {
        return hasSubclass(getModel().getClassifier(clName));
    }

}
