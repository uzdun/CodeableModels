package codeableModels.impl;

import codeableModels.*;

import java.util.*;

public class CEnumImpl extends CNamedElementImpl implements CEnum {
    private List<String> enumValues = new ArrayList<>();

    public CEnumImpl(String name, List<String> enumValueStrings) {
        super(name);
        enumValues = enumValueStrings;
    }

    @Override
    public List<String> getValues() {
        return enumValues;
    }

    @Override
    public boolean isLegalValue(String value) {
        return enumValues.contains(value);
    }


}
