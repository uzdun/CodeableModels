package codeableModels;

public interface CAttribute {

    String getName();

    void setName(String name);

    String getType() throws CException;

    CClassifier getTypeClassifier();

    CEnum getEnumType();

    Object getDefaultValue();

    void setDefaultValue(Object defaultValue) throws CException;

}