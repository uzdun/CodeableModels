package codeableModels;

import codeableModels.impl.*;

public class CodeableModels {
    public static CModel createModel() {
        return new CModelImpl();
    }
}
