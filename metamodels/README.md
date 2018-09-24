# Metamodels

This folder contains metamodels we use in our work as samples.

## Getting Started

TBD

### Prerequisites / Installing

[Codeable Models](https://github.com/uzdun/CodeableModels/) 
is required and the PYTHONPATH must be correctly set to contain 
Codeable Models.

The PlantUMLGenerator has two instance variables that can be used to configure where to find
the plantuml.jar file and to which directory the generated output should be written. The
default values are:

```
self.directory = "../_generated"
self.plantUmlJarPath = "../../libs/plantuml.jar"
```

The directory containing `codeableModels` and `plantUMLRenderer` must be on the PYTHONPATH.

## Running the tests

TBD

## Deployment

TBD

## Built With

* [Codeable Models](https://github.com/uzdun/CodeableModels/) - Modelling platform
* [PlantUML](http://plantuml.com/download) - Generate figures



