# Plant UML Renderer

This folder contains early generators for generating class and object model visualizations
with Plant UML.

## Getting Started

Here is an example script importing a number of models and views and generating object models
and class models from lists of the form `[<view-1>, <config-option-1>, ... <view-n>, <config-options-n>]`. 
The views are CBundles of model elements:

```
from plantUMLGenerator import PlantUMLGenerator
from domainMetaModel import domainMetaModel
from guidanceMetaModel import guidanceMetaModelHierarchy, guidanceMetaModelDetails
from webAPIDomainModel import webAPIDomainModelViews
from webAPIQuality import webAPIQualityViews
from webAPIStructure import webAPIStructureViews

generator = PlantUMLGenerator()

generator.generateObjectModels("webAPIStructure", webAPIStructureViews)
generator.generateObjectModels("webAPIQuality", webAPIQualityViews)

generator.generateClassModels("webAPIDomainModel", webAPIDomainModelViews)
generator.generateClassModels("guidanceMetaModel", [
    domainMetaModel, {},
    guidanceMetaModelHierarchy, {"renderAssociations": False},
    guidanceMetaModelDetails, {}
])
```

### Prerequisites / Installing

[PlantUML](http://plantuml.com/download)'s jar file and  
[Codeable Models](https://github.com/uzdun/CodeableModels/) 
are required and the sys path in the files must be correctly set. 

The PlantUMLGenerator has two instance variables that can be used to configure where to find
the plantuml.jar file and to which directory the generated output should be written. The
default values are:

```
self.directory = "../_generated"
self.plantUmlJarPath = "../../libs/plantuml.jar"
```


## Running the tests

TBD

## Deployment

TBD

## Built With

* [Codeable Models](https://github.com/uzdun/CodeableModels/) - Modelling platform
* [PlantUML](http://plantuml.com/download) - Generate figures



