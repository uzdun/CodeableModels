Getting started
***************

Installing codeable models
==========================

Codeable Models - by purpose - only uses plain Python. So there are no requirements to get the project up and running.

Get the latest release or development version from `<https://github.com/uzdun/CodeableModels>`_.

Running the tests
=================

Nosetest is required for executing the test cases. Find installation instructions under:
`Nosetest <https://nose.readthedocs.io/en/latest/>`_.

Execute ``nosetests`` either in the main directory of the project or in ``./tests``. The test files contained in
this directory comprise the test suite.

On Unix, please be aware that nosetests does not consider executable files. If running the tests fails, make
sure that the scripts in ``tests`` are not executable, e.g., run: ``chmod -x $(find . -name '*.py')`` in ``tests``.

Deployment
==========

Simply import from the ``codeable_models`` module like this::

    from codeable_models import CMetaclass, CClass, CObject, CAttribute, CException, CEnum, CStereotype


Installing and rendering with Plant UML
=======================================

Codeable Models provides a few Plant UML renderers. If you want to use them, the `PlantUML <http://plantuml.com/download>`_ jar file is required. In addition, Codeable Models must be on the ``PYTHONPATH``.

The ``PlantUMLGenerator`` (used in examples below) has two instance variables that can be used to configure where to find
the ``plantuml.jar`` file and to which directory the generated output should be written. The
default values are::

    self.directory = "../_generated"
    self.plant_uml_jar_path = "../../libs/plantuml.jar"

For example, you can specify::

    generator = PlantUMLGenerator()
    generator.plant_uml_jar_path = "./libs/plantuml.jar"
    generator.directory = "."


The directory containing ``codeable_models`` and ``plant_uml_renderer`` must be on the ``PYTHONPATH``.


