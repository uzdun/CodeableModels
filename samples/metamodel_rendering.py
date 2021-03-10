"""
*File Name:* samples/metamodel_rendering.py

This is a Codeable Models example realizing the Plant UML rendering of
predefined meta-del such as :ref:`activity_metamodel`,
:ref:`component_metamodel`, and :ref:`microservice_components_metamodel` used in
the documentation.

"""

from plant_uml_renderer import PlantUMLGenerator
from metamodels.component_metamodel import componentMetamodelViews
from metamodels.microservice_components_metamodel import microservice_metamodel_views
from metamodels.activity_metamodel import activity_metamodel_views


def run():
    print("***************** Rendering Predefined Meta-Models *****************")
    generator = PlantUMLGenerator()
    generator.generate_class_models("component_metamodel", componentMetamodelViews)
    print(f"... Generated models in {generator.directory!s}/component_metamodel")
    generator.generate_class_models("microservices_metamodel", microservice_metamodel_views)
    print(f"... Generated models in {generator.directory!s}/microservices_metamodel")
    generator.generate_class_models("activity_metamodel", activity_metamodel_views)
    print(f"... Generated models in {generator.directory!s}/activity_metamodel")


if __name__ == "__main__":
    run()
