package codeableModels.tests;

import org.junit.runner.*;
import org.junit.runners.*;
import org.junit.runners.Suite.*;

@RunWith(Suite.class)
@SuiteClasses({TestsAssociationsInModel.class, TestsAttributes.class, TestsAttributesMetaclass.class,
        TestsAttributesStereotype.class, TestsClass.class, TestsClassifier.class,
        TestsImportModel.class, TestsInheritanceClass.class, TestsInheritanceMetaclass.class,
        TestsInheritanceStereotype.class, TestsMetaclass.class, TestsObject.class, TestsStereotypesOnClasses.class,
        TestsObjectLinks.class, TestsClassLinks.class, TestsAttributeValues.class, TestsTaggedValuesOnClasses.class,
        TestsStereotypesOnAssociations.class, TestsTaggedValuesOnLinks.class,
        TestsStereotypeInstancesOnClasses.class,
        TestsStereotypeInstancesOnAssociations.class})
public class AllTests {

}
