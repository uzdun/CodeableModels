package codeableModels.impl;

import codeableModels.*;

public abstract class CElementImpl implements CElement {
    private CModel model;

    @Override
    public CModel getModel() {
        return model;
    }

    @Override
    public void setModel(CModel model) {
        this.model = model;
    }

}
