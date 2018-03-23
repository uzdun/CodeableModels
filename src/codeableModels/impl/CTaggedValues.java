package codeableModels.impl;

import codeableModels.*;

import java.util.*;

class CTaggedValues {
    private final CAttributeValues taggedValues = new CAttributeValues();

    public Object getTaggedValue(List<CStereotype> legalStereotypes, CStereotype stereotype, String taggedValueName) throws CException {
        if (!legalStereotypes.contains(stereotype)) {
            throw new CException("stereotype '" + stereotype.getName() + "' is not a stereotype of element");
        }
        return getTaggedValue(stereotype, taggedValueName);
    }

    private Object getTaggedValue(CStereotype stereotype, String taggedValueName) throws CException {
        CAttribute attribute = stereotype.getAttribute(taggedValueName);
        if (attribute == null) {
            throw new CException("tagged value '" + taggedValueName + "' unknown for stereotype '" + stereotype.getName() + "'");
        }
        return taggedValues.get(stereotype, taggedValueName);
    }

    public void setTaggedValue(List<CStereotype> legalStereotypes, CStereotype stereotype, String taggedValueName, Object value) throws CException {
        if (!legalStereotypes.contains(stereotype)) {
            throw new CException("stereotype '" + stereotype.getName() + "' is not a stereotype of element");
        }
        setTaggedValue(stereotype, taggedValueName, value);
    }

    private void setTaggedValue(CStereotype stereotype, String taggedValueName, Object value) throws CException {
        CAttribute attribute = stereotype.getAttribute(taggedValueName);
        if (attribute == null) {
            throw new CException("tagged value '" + taggedValueName + "' unknown for stereotype '" + stereotype.getName() + "'");
        }
        CAttributeImpl.checkAttributeValueType(taggedValueName, ((CAttributeImpl) attribute), value);
        taggedValues.add(stereotype, taggedValueName, value);
    }

    // uses the first stereotype in the list that has the tagged value defined
    public Object getTaggedValue(List<CStereotype> legalStereotypes, String taggedValueName) throws CException {
        for (CStereotype stereotype : legalStereotypes) {
            if (stereotype.getAttribute(taggedValueName) != null) {
                return getTaggedValue(stereotype, taggedValueName);
            }
        }
        throw new CException("tagged value '" + taggedValueName + "' unknown");
    }

    // uses the first stereotype in the list that has the tagged value defined
    public void setTaggedValue(List<CStereotype> legalStereotypes, String taggedValueName, Object value) throws CException {
        for (CStereotype stereotype : legalStereotypes) {
            if (stereotype.getAttribute(taggedValueName) != null) {
                setTaggedValue(stereotype, taggedValueName, value);
                return;
            }
        }
        throw new CException("tagged value '" + taggedValueName + "' unknown");
    }
}
