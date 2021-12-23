# Codeable Models

Codeable Models aims to provide an easy-to-use API for coding software design models
akin to UML models, but radically simplified compared to the UML2 meta-model. That is,
the API allows you to create metaclasses, classes, objects, stereotypes and their
dependencies. The main envisaged use case is at the moment to create domain models in
your code at runtime and generate visual representations of those models for human users.

We use PlantUML and Graphviz in our projects for such visual representations; see folder 
plant_uml_renderer for simple class and object model renderers. 

The folder metamodels contains a couple of example metamodels.

## Getting Started

As the project introduces fairly standard modeling abstractions, it should be possible
to get started based on the samples. Detailed examples will be added as the project
matures. For the time being, search the test cases for use of API elements that are not
clear from the interfaces.

### Prerequisites / Installing

The project - by purpose - only uses plain Python. So there are no requirements
to get the project up and running.

Nosetest is required for executing the test cases. Find installation instructions under:
[Nosetest](https://nose.readthedocs.io/en/latest/) 

## Running the tests

Execute `nosetests` either in the main directory of the project or in `./tests`. The test files contained in 
this directory comprise the test suite. 

On Unix, please be aware that nosetests does not consider executable files. If running the tests fails, make 
sure that the scripts in `tests` are not executable, e.g., run: `chmod -x $(find . -name '*.py')` in `tests`.

## Building the documentation

To build the documentation Sphinx and the extensions configured in `docsrc/source/conf.py`
need to be installed first, e.g. using `pip`.

The documentation is built in the folder `docsrc`. Use `make html` to build the `html` 
pages into the subfolder `build`, and `make docs` to copy the build into the `docs` folder.
The distribution contains the latest built of the documentation in the `docs` folder.

The documentation can also be found at:
[Github Pages Documentation](https://uzdun.github.io/CodeableModels/)

## Deployment

No specific instructions so far; simply import from the `codeable_models` module like:

```
from codeable_models import CMetaclass, CClass, CObject, CAttribute, CException, CEnum, CStereotype
``` 

## Built With

* [Nosetest](https://nose.readthedocs.io/en/latest/) - The test framework used

## Contributing

Please read [CONTRIBUTING.md] for details on our code of conduct, and the process for
submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see
the [tags on this repository](https://github.com/uzdun/CodeableModels/tags).

## Authors

* **Uwe Zdun** - *Initial work* - [https://github.com/uzdun/](https://github.com/uzdun/)

See also the list of [contributors](https://github.com/uzdun/CodeableModels/contributors) who
participated in this project.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE)
file for details

## Acknowledgments

*

