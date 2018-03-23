package codeableModels;

import java.util.*;

public interface CEnum extends CNamedElement {

    List<String> getValues();

    boolean isLegalValue(String value);

}