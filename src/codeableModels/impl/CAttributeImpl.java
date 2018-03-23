package codeableModels.impl;

import codeableModels.*;

public class CAttributeImpl implements CAttribute {

    // for isLegalAttributeTypeCode() to work, OBJECT should stay the first element and
    // ENUM the last, and every constant in between should be incremented by 1
    static final int OBJECT = 0;
    static final int STRING = 1;
    static final int INT = 2;
    static final int BOOLEAN = 3;
    static final int FLOAT = 4;
    static final int DOUBLE = 5;
    static final int LONG = 6;
    static final int CHAR = 7;
    static final int BYTE = 8;
    static final int SHORT = 9;
    static final int ENUM = 10;
    static final int UNKNOWN_TYPE = -1;

    private String name;
    private int typeCode;
    private Object defaultValue;
    private CClassifier typeClassifier = null;
    private CEnum enumType = null;

    public static boolean isLegalAttributeTypeCode(int type) {
        return type >= OBJECT && type <= ENUM;
    }

    public static int getAttributeTypeCodeOfObject(Object object) {
        if (object instanceof CObject)
            return OBJECT;
        if (object instanceof String)
            return STRING;
        if (object instanceof Integer)
            return INT;
        if (object instanceof Boolean)
            return BOOLEAN;
        if (object instanceof Float)
            return FLOAT;
        if (object instanceof Double)
            return DOUBLE;
        if (object instanceof Long)
            return LONG;
        if (object instanceof Byte)
            return BYTE;
        if (object instanceof Short)
            return SHORT;
        if (object instanceof Character)
            return CHAR;
        // ENUM cannot be guessed by default value, but requires explicit creation, as its value is also a string.

        return UNKNOWN_TYPE;
    }

    public static void checkAttributeValueType(String name, CAttributeImpl attribute, Object value) throws CException {
        int actualAttributeTypeCode = getAttributeTypeCodeOfObject(value);
        if (actualAttributeTypeCode == CAttributeImpl.UNKNOWN_TYPE)
            throw new CException("value for attribute '" + name + "' is not a known attribute type");
        if (actualAttributeTypeCode != attribute.typeCode) {
            // an enum requires a string to be provided as a value
            if (!(attribute.typeCode == ENUM && actualAttributeTypeCode == STRING)) {
                throw new CException("value type for attribute '" + name + "' does not match attribute type");
            }
        }
        if (actualAttributeTypeCode == OBJECT) {
            CObject object = (CObject) value;
            if (object.getClassifier() != attribute.getTypeClassifier()) {
                throw new CException("type classifier of object '" + object.getName() + "' is not matching attribute " +
                        "type of attribute '" + name + "'");
            }
        }
        if (attribute.typeCode == ENUM && actualAttributeTypeCode == STRING) {
            String stringValue = (String) value;
            if (!attribute.getEnumType().isLegalValue(stringValue)) {
                throw new CException("value '" + stringValue + "' not element of enumeration");
            }
        }

    }

    public CClassifier getTypeClassifier() {
        return typeClassifier;
    }

    void setTypeClassifier(CClassifier classifier) {
        this.typeClassifier = classifier;
    }

    @Override
    public CEnum getEnumType() {
        return enumType;
    }

    void setEnumType(CEnum enumType) {
        this.enumType = enumType;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String getType() throws CException {
        switch (typeCode) {
            case OBJECT:
                return "Object";
            case STRING:
                return "String";
            case INT:
                return "Int";
            case BOOLEAN:
                return "Boolean";
            case FLOAT:
                return "Float";
            case DOUBLE:
                return "Double";
            case LONG:
                return "Long";
            case CHAR:
                return "Char";
            case BYTE:
                return "Byte";
            case SHORT:
                return "Short";
            case ENUM:
                return "Enum";
        }
        throw new CException("type string unknown");
    }


    void setTypeCode(int typeCode) {
        this.typeCode = typeCode;
    }

    @Override
    public Object getDefaultValue() {
        return defaultValue;
    }

    @Override
    public void setDefaultValue(Object defaultValue) throws CException {
        checkAttributeValueType(this.name, this, defaultValue);
        this.defaultValue = defaultValue;
    }
}
