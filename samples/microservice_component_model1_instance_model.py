"""
*File Name:* samples/microservice_component_model1_instance_model.py

This is a Codeable Models example realizing a sample component model, shown as an instance
model (object diagram).
It is used to explain meta-modelling. It uses meta-classes from the :ref:`component_metamodel`.

The example is explained in :ref:`meta_model_stereotypes`.

"""

from codeable_models import CClass, CBundle, add_links
from metamodels.component_metamodel import component
from plant_uml_renderer import PlantUMLGenerator

api_gateway = CClass(component, "API Gateway")
inventory_service = CClass(component, "Inventory Service")
shipping_service = CClass(component, "Shipping Service")
web_frontend = CClass(component, "Web Frontend")
inventory_db = CClass(component, "Inventory DB")
shipping_db = CClass(component, "Shipping DB")

add_links({api_gateway: [inventory_service, shipping_service],
           web_frontend: [inventory_service, shipping_service],
           inventory_service: inventory_db,
           shipping_service: shipping_db},
          role_name="target")

microservice_component_model1_instance_model = CBundle("microservice_component_model1_instance_model",
                                                       elements=api_gateway.class_object.get_connected_elements())


def run():
    print("***************** Microservice Component Model 1: Meta-modelling example (instance model) *****************")
    print('*** Plant UML Generation')
    generator = PlantUMLGenerator()
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models("microservice_component_model1",
                                     [microservice_component_model1_instance_model, {}])
    print(f"... Generated models in {generator.directory!s}/microservice_component_model1")


if __name__ == "__main__":
    run()
