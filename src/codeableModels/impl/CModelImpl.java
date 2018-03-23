package codeableModels.impl;

import codeableModels.*;

import java.util.*;

public class CModelImpl implements CModel {
    private final Map<String, CClassifier> classifiers = new LinkedHashMap<>();
    private final Map<String, CObject> objects = new LinkedHashMap<>();
    private final List<CAssociation> associations = new ArrayList<>();
    private final List<CModel> importedModels = new ArrayList<>();
    private static long autoID = 0;

    private static List<String> classifiersAsStringList(List<? extends CClassifier> cls) {
        ArrayList<String> result = new ArrayList<>();
        for (CClassifier cl : cls) {
            result.add(cl.getName());
        }
        return result;
    }

    private String getAutoID() {
        return "##" + autoID++;
    }

    private CClassifier initClassifier(String name, CClassifier cl)
            throws CException {
        if (getClassifier(name) != null) {
            throw new CException("classifier '" + name + "' cannot be created, classifier name already exists");
        }
        classifiers.put(name, cl);
        cl.setModel(this);
        return cl;
    }

    @Override
    public CMetaclass createMetaclass(String name) throws CException {
        return (CMetaclass) initClassifier(name, new CMetaclassImpl(name));
    }

    @Override
    public CMetaclass createMetaclass() throws CException {
        return createMetaclass(getAutoID());
    }

    private void initObject(CObject obj) throws CException {
        obj.setModel(this);
        for (CClassifier classifier : obj.getClassifierPath()) {
            for (CAttribute attribute : classifier.getAttributes()) {
                if (attribute.getDefaultValue() != null) {
                    obj.setAttributeValue(classifier, attribute.getName(), attribute.getDefaultValue());
                }
            }
        }
    }

    @Override
    public CClass createClass(CMetaclass metaclass, String name) throws CException {
        CClass cl = (CClass) initClassifier(name, new CClassImpl(name));
        ((CClassImpl) cl).setMetaclass(metaclass);
        initObject(((CClassImpl) cl).getClassObjectImpl());
        return cl;
    }

    @Override
    public CClass createClass(CMetaclass metaclass) throws CException {
        return createClass(metaclass, getAutoID());
    }


    @Override
    public CClass createClass(String metaclassName, String name) throws CException {
        CMetaclass mcl = lookupMetaclass(metaclassName);
        if (mcl == null) {
            throw new CException("can't find metaclass: '" + metaclassName + "' to be instantiated");
        }
        return createClass(mcl, name);
    }

    @Override
    public CClass createClass(String metaclassName) throws CException {
        return createClass(metaclassName, getAutoID());
    }

    @Override
    public CObject createObject(CClass cl, String name) throws CException {
        if (getObject(name) != null) {
            throw new CException("object '" + name + "' cannot be created, object name already exists");
        }
        CObject obj = new CObjectImpl(name);
        ((CObjectImpl) obj).setClassifier(cl);
        ((CClassImpl) cl).addInstance(obj);
        objects.put(name, obj);
        initObject(obj);
        return obj;
    }

    @Override
    public CObject createObject(CClass cl) throws CException {
        return createObject(cl, getAutoID());
    }

    @Override
    public CObject createObject(String className, String name) throws CException {
        CClass cl = lookupClass(className);
        if (cl == null) {
            throw new CException("can't find class: '" + className + "' to be instantiated");
        }
        return createObject(cl, name);
    }

    @Override
    public CObject createObject(String className) throws CException {
        return createObject(className, getAutoID());
    }

    @Override
    public CStereotype createStereotype(String name) throws CException {
        return (CStereotype) initClassifier(name, new CStereotypeImpl(name));
    }

    @Override
    public CStereotype createStereotype() throws CException {
        return createStereotype(getAutoID());
    }

    @Override
    public CStereotype createStereotype(String name, CStereotypedElement stereotypedElement) throws CException {
        CStereotype stereotype = (CStereotype) initClassifier(name, new CStereotypeImpl(name));
        stereotypedElement.addStereotype(stereotype);
        return stereotype;
    }

    @Override
    public CStereotype createStereotype(String name, String stereotypedElementName) throws CException {
        CMetaclass metaclass = lookupMetaclass(stereotypedElementName);
        if (metaclass != null) {
            return createStereotype(name, metaclass);
        }
        List<CAssociation> associations = getAssociationsByName(stereotypedElementName);
        if (associations.size() == 0) {
            throw new CException("can't find association '" + stereotypedElementName + "' to be stereotyped");
        }
        if (associations.size() > 1) {
            throw new CException("found multiple associations with the name '" + stereotypedElementName +
                    "', use reference to select stereotype instead");
        }
        return createStereotype(name, associations.get(0));
    }

    @Override
    public CAssociation createAssociation(String name, CAssociationEnd end1, CAssociationEnd end2) throws CException {
        if ((end1.getClassifier() instanceof CClass && !(end2.getClassifier() instanceof CClass))) {
            throw new CException("association between model element and metamodel element not allowed: '"
                    + end1.getClassifier().getName() + ", " + end2.getClassifier().getName());
        }

        if ((end1.getClassifier() instanceof CMetaclass || end1.getClassifier() instanceof CStereotype)
                && !(end2.getClassifier() instanceof CMetaclass || end2.getClassifier() instanceof CStereotype)) {
            throw new CException("association between model element and metamodel element not allowed: '"
                    + end1.getClassifier().getName() + ", " + end2.getClassifier().getName());
        }

        CAssociation assoc = new CAssociationImpl(this, name);
        ((CAssociationImpl) assoc).setEnd1(end1);
        ((CAssociationImpl) assoc).setEnd2(end2);
        assoc.setModel(this);
        associations.add(assoc);
        ((CClassifierImpl) end1.getClassifier()).addAssociation(assoc);
        ((CClassifierImpl) end2.getClassifier()).addAssociation(assoc);
        return assoc;
    }

    @Override
    public CAssociation createComposition(String name, CAssociationEnd composingEnd, CAssociationEnd composedEnd)
            throws CException {
        CAssociation assoc = createAssociation(name, composingEnd, composedEnd);
        assoc.setComposition(true);
        return assoc;
    }

    @Override
    public CAssociation createAggregation(String name, CAssociationEnd aggregatingEnd, CAssociationEnd aggregatedEnd)
            throws CException {
        CAssociation assoc = createAssociation(name, aggregatingEnd, aggregatedEnd);
        assoc.setAggregation(true);
        return assoc;
    }

    @Override
    public CAssociation createAssociation(CAssociationEnd end1, CAssociationEnd end2) throws CException {
        return createAssociation(null, end1, end2);
    }

    @Override
    public CAssociation createComposition(CAssociationEnd end1, CAssociationEnd end2) throws CException {
        return createComposition(null, end1, end2);
    }

    @Override
    public CAssociation createAggregation(CAssociationEnd end1, CAssociationEnd end2) throws CException {
        return createAggregation(null, end1, end2);
    }

    @Override
    public CModel importModel(CModel model) {
        importedModels.add(model);
        return this;
    }

    @Override
    public CClassifier getClassifier(String name) {
        return classifiers.get(name);
    }

    @Override
    public CMetaclass getMetaclass(String name) throws CException {
        CClassifier cl = getClassifier(name);
        return cl == null ? null : cl.asMetaclass();
    }

    @Override
    public CStereotype getStereotype(String name) throws CException {
        CClassifier cl = getClassifier(name);
        return cl == null ? null : cl.asStereotype();
    }

    @Override
    public CClass getClass(String name) throws CException {
        CClassifier cl = getClassifier(name);
        return cl == null ? null : cl.asClass();
    }

    @Override
    public CObject getObject(String name) {
        return objects.get(name);
    }

    @Override
    public CClassifier lookupClassifier(String name) {
        CClassifier result = getClassifier(name);
        if (result != null) {
            return result;
        }
        for (CModel m : importedModels) {
            result = m.lookupClassifier(name);
            if (result != null) {
                return result;
            }
        }
        return null;
    }

    @Override
    public CMetaclass lookupMetaclass(String name) throws CException {
        CClassifier cl = lookupClassifier(name);
        return cl == null ? null : cl.asMetaclass();
    }

    @Override
    public CClass lookupClass(String name) throws CException {
        CClassifier cl = lookupClassifier(name);
        return cl == null ? null : cl.asClass();
    }

    @Override
    public CStereotype lookupStereotype(String name) throws CException {
        CClassifier cl = lookupClassifier(name);
        return cl == null ? null : cl.asStereotype();
    }

    @Override
    public List<String> getClassifierNames() {
        return new ArrayList<>(classifiers.keySet());
    }

    @Override
    public List<CClassifier> getClassifiers() {
        return new ArrayList<>(classifiers.values());
    }

    @Override
    public List<CMetaclass> getMetaclasses() {
        ArrayList<CMetaclass> result = new ArrayList<>();
        for (CClassifier cl : getClassifiers()) {
            if (cl instanceof CMetaclass) {
                result.add((CMetaclass) cl);
            }
        }
        return result;
    }

    @Override
    public List<CClass> getClasses() {
        ArrayList<CClass> result = new ArrayList<>();
        for (CClassifier cl : getClassifiers()) {
            if (cl instanceof CClass) {
                result.add((CClass) cl);
            }
        }
        return result;
    }

    @Override
    public List<CStereotype> getStereotypes() {
        ArrayList<CStereotype> result = new ArrayList<>();
        for (CClassifier cl : getClassifiers()) {
            if (cl instanceof CStereotype) {
                result.add((CStereotype) cl);
            }
        }
        return result;
    }

    @Override
    public List<String> getMetaclassNames() {
        return classifiersAsStringList(getMetaclasses());
    }

    @Override
    public List<String> getStereotypeNames() {
        return classifiersAsStringList(getStereotypes());
    }

    @Override
    public List<String> getClassNames() {
        return classifiersAsStringList(getClasses());
    }

    @Override
    public void deleteClassifier(CClassifier cl) throws CException {
        if (cl == null) {
            throw new CException("classifier '' to be deleted does not exist");
        }
        if (!classifiers.containsKey(cl.getName())) {
            throw new CException("classifier '" + cl.getName() + "' to be deleted does not exist");
        }

        ((CClassifierImpl) cl).cleanupClassifier();

        classifiers.remove(cl.getName());
        cl.setModel(null);
    }

    @Override
    public List<String> getObjectNames() {
        return new ArrayList<>(objects.keySet());
    }

    @Override
    public List<CObject> getObjects() {
        return new ArrayList<>(objects.values());
    }

    @Override
    public void deleteObject(CObject o) throws CException {
        if (o == null) {
            throw new CException("object '' to be deleted does not exist");
        }
        if (!objects.containsKey(o.getName())) {
            throw new CException("object '" + o.getName() + "' to be deleted does not exist");
        }
        if (o.getClassifier() == null) {
            throw new CException("trying to delete object '" + o.getName() + "' that has been deleted before");
        }
        ((CClassImpl) o.getClassifier()).removeInstance(o);
        ((CObjectImpl) o).setClassifier(null);
        objects.remove(o.getName());
        o.setModel(null);
    }

    @Override
    public List<CModel> getImportedModels() {
        return importedModels;
    }

    private void getFullModelList(List<CModel> models) {
        models.add(this);
        for (CModel importedModel : importedModels) {
            ((CModelImpl) importedModel).getFullModelList(models);
        }
    }

    @Override
    public List<CModel> getFullModelList() {
        List<CModel> models = new ArrayList<>();
        getFullModelList(models);
        return models;
    }

    @Override
    public List<CAssociation> getAssociations() {
        return associations;
    }

    private List<CAssociation> getAssociationsForTypeForThisModel(CClassifier type) {
        List<CAssociation> result = new ArrayList<>();
        for (CAssociation association : associations) {
            if (association.hasEndType(type)) {
                result.add(association);
            }
        }
        return result;
    }

    @Override
    public List<CAssociation> getAssociationsForType(CClassifier type) {
        List<CAssociation> result = new ArrayList<>();
        List<CClassifier> types = new ArrayList<>();
        types.add(type);
        types.addAll(type.getAllSuperclasses());
        for (CModel model : getFullModelList()) {
            for (CClassifier t : types) {
                result.addAll(((CModelImpl) model).getAssociationsForTypeForThisModel(t));
            }
        }
        return result;
    }

    @Override
    public void deleteAssociation(CAssociation assoc) throws CException {
        assoc.setModel(null);
        associations.remove(assoc);
        List<CAssociationEnd> ends = assoc.getEnds();
        ((CClassifierImpl) ends.get(0).getClassifier()).removeAssociation(assoc);
        ((CClassifierImpl) ends.get(1).getClassifier()).removeAssociation(assoc);
    }

    // returns an array list, as association names don't have to be unique,
    // including null == association with no name
    @Override
    public List<CAssociation> getAssociationsByName(String name) {
        List<CAssociation> result = new ArrayList<>();
        for (CAssociation a : associations) {
            if (a.getName() == null) {
                if (name == null) {
                    result.add(a);
                }
            } else {
                if (a.getName().equals(name)) {
                    result.add(a);
                }
            }
        }
        return result;
    }

    @Override
    public CEnum createEnum(String name, List<String> enumValues) {
        return new CEnumImpl(name, enumValues);
    }
}
