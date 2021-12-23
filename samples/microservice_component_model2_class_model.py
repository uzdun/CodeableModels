"""
*File Name:* samples/microservice_component_model2_class_model.py

This is a Codeable Models example realizing a sample component model, shown as a class model
(class diagram).
It is used to explain meta-modelling with stereotypes. It uses meta-classes from the :ref:`component_metamodel`.

The example is explained in :ref:`meta_model_stereotypes`.

"""

from codeable_models import CClass, CBundle, add_links, CStereotype
from metamodels.component_metamodel import component, connectors_relation
from plant_uml_renderer import PlantUMLGenerator

# meta-model extensions
service = CStereotype("Service", extended=component)
database = CStereotype("Database", extended=component)

facade = CStereotype("Facade", extended=component)
web_ui = CStereotype("Web UI", superclasses=facade)
gateway = CStereotype("Gateway", extended=component)

jdbc = CStereotype("JDBC", extended=connectors_relation)
restful_http = CStereotype("RESTful HTTP", extended=connectors_relation)

# class model
api_gateway = CClass(component, "API Gateway", stereotype_instances=[gateway, facade])
zip_code_service = CClass(component, "Zip Code Service", stereotype_instances=service)
inventory_service = CClass(component, "Inventory Service", stereotype_instances=service)
shipping_service = CClass(component, "Shipping Service", stereotype_instances=service)
web_frontend = CClass(component, "Web Frontend", stereotype_instances=web_ui)
inventory_db = CClass(component, "Inventory DB", stereotype_instances=database)
shipping_db = CClass(component, "Shipping DB", stereotype_instances=database)

shipping_service_zip_code_association = \
    shipping_service.association(zip_code_service, "1 -> 1", derived_from=connectors_relation,
                                 stereotype_instances=restful_http)
for target in [inventory_service, shipping_service, zip_code_service]:
    api_gateway.association(target, "* -> *", derived_from=connectors_relation, stereotype_instances=restful_http)
for target in [inventory_service, shipping_service]:
    web_frontend.association(target, "1 -> *", derived_from=connectors_relation, stereotype_instances=restful_http)
for source, target in {inventory_service: inventory_db, shipping_service: shipping_db}.items():
    source.association(target, "1 -> *", derived_from=connectors_relation, stereotype_instances=jdbc)

microservice_component_model2_class_model = CBundle("microservice_component_model2_class_model",
                                                    elements=api_gateway.get_connected_elements())

component_meta_model = CBundle("component_meta_model",
                               elements=(component.get_connected_elements(add_stereotypes=True) +
                                         [jdbc, restful_http]))


def run():
    print("***************** Microservice Component Model 2: Meta-modelling example (Class Model) *****************")
    print('*** Plant UML Generation')
    generator = PlantUMLGenerator()
    generator.class_model_renderer.left_to_right = True
    generator.generate_class_models("microservice_component_model2", [microservice_component_model2_class_model, {}])
    generator.class_model_renderer.left_to_right = False
    generator.generate_class_models("microservice_component_model2", [component_meta_model, {}])
    print(f"... Generated models in {generator.directory!s}/microservice_component_model2")


if __name__ == "__main__":
    run()
