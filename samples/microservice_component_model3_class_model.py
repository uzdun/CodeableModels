"""
*File Name:* samples/microservice_component_model3_class_model.py

This is a Codeable Models example realizing a sample component model at the
class model level.
It is used to explain meta-modelling with stereotypes. In particular, tagged values, introspection options,
and default values features are used in the example.
It uses meta-classes from the :ref:`component_metamodel`.

The example is explained in :ref:`meta_model_stereotypes`.

"""

from codeable_models import CClass, CBundle, CStereotype, CMetaclass, CEnum, CAttribute
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

shipping_service_zip_code_association = \
    shipping_service.association(zip_code_service, "1 -> 1", derived_from=connectors_relation,
                                 stereotype_instances=restful_http)
for target in [inventory_service, shipping_service, zip_code_service]:
    api_gateway.association(target, "* -> *", derived_from=connectors_relation,
                            stereotype_instances=restful_http)
for target in [inventory_service, shipping_service]:
    web_frontend.association(target, "1 -> *", derived_from=connectors_relation,
                             stereotype_instances=restful_http)

for source, target in {inventory_service: inventory_db, shipping_service: shipping_db}.items():
    source.association(target, "1 -> *", derived_from=connectors_relation,
                       stereotype_instances=jdbc)

microservice_component_model3 = CBundle("microservice_component_model3_class_model",
                                        elements=api_gateway.get_connected_elements())

microservice_component_model3_no_tagged_values = CBundle("microservice_component_model3_class_model_no_tagged_values",
                                                         elements=api_gateway.get_connected_elements())

component_meta_model2 = CBundle("component_meta_model2",
                                elements=(component.get_connected_elements(add_stereotypes=True) +
                                          [jdbc, restful_http]))


def print_instances_introspection():
    print(f"Shipping DB stereotype instances: {shipping_db.stereotype_instances!s}")
    print(f"Shipping service to zip code association stereotype instances: " +
          f"{shipping_service_zip_code_association.stereotype_instances!s}")

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
          f"{shipping_service_zip_code_association.get_tagged_value('protocol')}")
    shipping_service_zip_code_association.set_tagged_value('protocol', "HTTP")
    print(f"new protocol shipping service to zip code: " +
          f"{shipping_service_zip_code_association.get_tagged_value('protocol')}")
    print()


def print_default_values():
    print(f"inventory service values = {inventory_service.values!s}")
    print(f"zip code service values = {zip_code_service.values!s}")
    print()


def run():
    print("***************** Microservice Component Model 3: Meta-modelling example (class model) *****************")
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
    generator.class_model_renderer.left_to_right = True
    generator.generate_class_models("microservice_component_model3", [microservice_component_model3, {},
                                                                      microservice_component_model3_no_tagged_values,
                                                                      {"render_tagged_values": False}])
    generator.class_model_renderer.left_to_right = False
    generator.generate_class_models("microservice_component_model3", [component_meta_model2, {}])
    print(f"... Generated models in {generator.directory!s}/microservice_component_model3")


if __name__ == "__main__":
    run()
