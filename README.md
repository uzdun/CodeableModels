# Codeable Models

Codeable Models aims to provide an easy-to-use API for coding software design models
akin to UML models, but radically simplified compared to the UML2 meta-model. That is,
the API allows you to create metaclasses, classes, objects, stereotypes and their
dependencies. The main envisaged use case is at the moment to create domain models in
your code at runtime and generate visual representations of those models for human users.
We use PlantUML and Graphviz in our projects for such visual representations; but no
generation code is yet included in the Codeable Models project.

## Getting Started

As the project introduces fairly standard modeling abstractions, it should be possible
to get started based on the samples. Detailed examples will be added as the project
matures. For the time being, search the test cases for use of API elements that are not
clear from the interfaces.

### Prerequisites / Installing

The project - by purpose - only uses plain old Java objects. So there are no requirements
to get the project up and running, other than placing it in your classpath.

JUnit is required in the classpath for executing the test cases.

## Running the tests

```
codedableModels/tests/AllTests.java
```

contains the test suite. Run it as a JUnit test suite. All other files in the tests
directory contain individual JUnit tests.

## Deployment

No specific instructions so far; simply build

## Built With

* [JUnit](https://junit.org) - The test framework used

## Contributing

Please read [CONTRIBUTING.md] for details on our code of conduct, and the process for
submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see
the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Uwe Zdun** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who
participated in this project.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE)
file for details

## Acknowledgments

*

