package codeableModels.impl;

import codeableModels.*;

import java.util.*;

class CAttributeValues {
    private final Map<CClassifier, Map<String, Object>> attributeValues = new HashMap<>();

    public Object get(CClassifier classifier, String attributeName) {
        Map<String, Object> attributeValuesClassifier = attributeValues.get(classifier);
        if (attributeValuesClassifier == null) {
            return null;
        }
        return attributeValuesClassifier.get(attributeName);
    }

    public void add(CClassifier classifier, String attributeName, Object value) {
        Map<String, Object> attributeValuesClassifier = attributeValues.get(classifier);
        if (attributeValuesClassifier == null) {
            attributeValuesClassifier = new HashMap<>();
            attributeValues.put(classifier, attributeValuesClassifier);
        }
        attributeValuesClassifier.put(attributeName, value);
    }
}

