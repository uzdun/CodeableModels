# Plant UML Renderer

This folder contains early generators for generating class and object model visualizations
with Plant UML.

## Getting Started

Here is an example script importing a number of models and views and generating object models
and class models from lists of the form `[<view-1>, <config-option-1>, ... <view-n>, <config-options-n>]`. 
The views are CBundles of model elements:

```
from plant_uml_renderer import PlantUMLGenerator
from metamodels.componentMetamodel import componentMetamodelViews
from microserviceModels.ecommerceMicroservices import ecommerceMicroservicesViews
from microserviceModels.ecommerceMicroservicesDetailed import ecommerceMicroservicesDetailedViews
from microserviceModels.ecommerceMicroservicesEventSourcing import ecommerceMicroservicesEventSourcingViews
from microserviceModels.ecommerceMicroservicesSharedDB import ecommerceMicroservicesSharedDBViews

generator = PlantUMLGenerator()
generator.generateObjectModels("microserviceModels", ecommerceMicroservicesViews)
generator.generateClassModels("componentMetamodel", componentMetamodelViews)
```

For instance, in this case `ecommerceMicroservicesViews` is defined as follows with `mobileApp` being a
class connected to all other classes that should be rendered: 

```
ecommerceMicroservices = CBundle("ecommerceMicroservices", elements = mobileApp.class_object.getConnectedElements())

ecommerceMicroservicesViews = [
    ecommerceMicroservices, {}]
```

### Prerequisites / Installing

[PlantUML](http://plantuml.com/download)'s jar file and  
[Codeable Models](https://github.com/uzdun/CodeableModels/) 
are required and the PYTHONPATH must be correctly set to contain 
Codeable Models.

The PlantUMLGenerator has two instance variables that can be used to configure where to find
the plantuml.jar file and to which directory the generated output should be written. The
default values are:

```
self.directory = "../_generated"
self.plant_uml_jar_path = "../../libs/plantuml.jar"
```

The directory containing `codeable_models` and `plant_uml_renderer` must be on the PYTHONPATH.

## Running the tests

TBD

## Deployment

TBD

## Built With

* [Codeable Models](https://github.com/uzdun/CodeableModels/) - Modelling platform
* [PlantUML](http://plantuml.com/download) - Generate figures



