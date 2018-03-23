package codeableModels.impl;

import codeableModels.*;

public abstract class CNamedElementImpl extends CElementImpl implements CNamedElement {
    final private String name;

    CNamedElementImpl(String name) {
        super();
        this.name = name;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public String toString() {
        String n = "";
        if (name != null) {
            n = name;
        }
        return n + "<" + super.toString() + ">";
    }
}
