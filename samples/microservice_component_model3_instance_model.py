"""
*File Name:* samples/microservice_component_model3_instance_model.py

This is a Codeable Models example realizing a sample component model at the
instance model level (i.e. instances of meta-classes are depicted in an object diagram).
It is used to explain meta-modelling with stereotypes. In particular, tagged values, introspection options,
and default values features are used in the example.
It uses meta-classes from the :ref:`component_metamodel`.

The example is explained in :ref:`meta_model_stereotypes`.

"""

from codeable_models import CClass, CBundle, add_links, CStereotype, CMetaclass, CEnum, CAttribute
from metamodels.component_metamodel import component, connectors_relation
from plant_uml_renderer import PlantUMLGenerator

distributed_component = CMetaclass("Distributed Component", superclasses=component,
                                   attributes={
                                       "stateless": False,
                                       "mock": False
                                   })

# meta-model extensions
service = CStereotype("Service", extended=component, attributes={
    "host_name": str,
    "port": int
})
stateless_service = CStereotype("Stateless Service", extended=distributed_component, superclasses=service,
                                default_values={"stateless": True})

# service = CStereotype("Service", extended=distributed_component, attributes={
#     "host_name": str,
#     "port": int
# })
# stateless_service = CStereotype("Service", superclasses=service,
#                                 default_values={"stateless": True})
database = CStereotype("Database", extended=component)

facade = CStereotype("Facade", extended=component)
web_ui = CStereotype("Web UI", superclasses=facade)
gateway = CStereotype("Gateway", extended=component)

jdbc = CStereotype("JDBC", extended=connectors_relation)

http_protocol = CEnum("HTTP Protocol", values=["HTTP", "HTTPS"])
restful_http = CStereotype("RESTful HTTP", extended=connectors_relation, attributes={
    "protocol": CAttribute(type=http_protocol, default="HTTPS"),
})


def print_stereotypes_and_extended_introspection():
    print(f"component stereotypes = {component.stereotypes!s}")
    print(f"connector stereotypes = {connectors_relation.stereotypes!s}")
    print(f"facade extended = {facade.extended!s}")
    print(f"restful_http extended = {restful_http.extended!s}")
    print()


# class model
api_gateway = CClass(distributed_component, "API Gateway", stereotype_instances=[gateway, facade])
zip_code_service = CClass(distributed_component, "Zip Code Service", stereotype_instances=stateless_service)
inventory_service = CClass(distributed_component, "Inventory Service", stereotype_instances=service)
shipping_service = CClass(distributed_component, "Shipping Service", stereotype_instances=service)
web_frontend = CClass(distributed_component, "Web Frontend", stereotype_instances=web_ui)
inventory_db = CClass(distributed_component, "Inventory DB", stereotype_instances=database)
shipping_db = CClass(distributed_component, "Shipping DB", stereotype_instances=database)

restful_links = add_links({shipping_service: zip_code_service,
                           api_gateway: [inventory_service, shipping_service, zip_code_service],
                           web_frontend: [inventory_service, shipping_service]},
                          role_name="target", stereotype_instances=restful_http)

shipping_service_zip_code_service_link = restful_links[0]

add_links({inventory_service: inventory_db, shipping_service: shipping_db},
          role_name="target", stereotype_instances=jdbc)

microservice_component_model3 = CBundle("microservice_component_model3_instance_model",
                                        elements=api_gateway.class_object.get_connected_elements())

microservice_component_model3_instance_model_no_attribute_or_tag_values = CBundle(
    "microservice_component_model3_instance_model_no_attribute_or_tag_values",
    elements=api_gateway.class_object.get_connected_elements())


# component_meta_model3 = CBundle("component_meta_model",
#                                 elements=(component.get_connected_elements(add_stereotypes=True) +
#                                           [jdbc, restful_http]))


def print_instances_introspection():
    print(f"Shipping DB stereotype instances: {shipping_db.stereotype_instances!s}")
    print(f"Shipping service to zip code link stereotype instances: " +
          f"{shipping_service_zip_code_service_link.stereotype_instances!s}")

    print(f"extended instances of database: {database.extended_instances!s}")
    print(f"all extended instances of component: {service.extended_instances!s}")
    print(f"extended instances of restful_http: {restful_http.extended_instances!s}")
    print()


def print_tagged_values():
    shipping_service.set_tagged_value("host_name", "www.example.com")
    shipping_service.set_tagged_value("port", 80)

    print(f'shipping service is running on {shipping_service.get_tagged_value("host_name")!s} ' +
          f'and port {shipping_service.get_tagged_value("port")!s}')

    print(f"old protocol shipping service to zip code: " +
          f"{shipping_service_zip_code_service_link.get_tagged_value('protocol')}")
    shipping_service_zip_code_service_link.set_tagged_value('protocol', "HTTP")
    print(f"new protocol shipping service to zip code: " +
          f"{shipping_service_zip_code_service_link.get_tagged_value('protocol')}")
    print()


def print_default_values():
    print(f"inventory service values = {inventory_service.values!s}")
    print(f"zip code service values = {zip_code_service.values!s}")
    print()


def run():
    print("***************** Microservice Component Model 3: Meta-modelling example (instance model) *****************")
    print("*** Stereotypes and Extended Introspection")
    print_stereotypes_and_extended_introspection()
    print("*** Instances Introspection")
    print_instances_introspection()
    print("*** Tagged Values")
    print_tagged_values()
    print("*** Default Values")
    print_default_values()
    print('*** Plant UML Generation')
    generator = PlantUMLGenerator()
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models("microservice_component_model3",
                                     [microservice_component_model3, {},
                                      microservice_component_model3_instance_model_no_attribute_or_tag_values,
                                      {"render_attribute_values": False, "render_tagged_values": False}])
    # avoid doing this step twice, it is also called in ..._class_model.py
    # generator.generate_class_models("microservice_component_model3", [component_meta_model3, {}])
    print(f"... Generated models in {generator.directory!s}/microservice_component_model3")


if __name__ == "__main__":
    run()
