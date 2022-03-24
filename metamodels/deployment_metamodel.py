from codeable_models import CMetaclass, CStereotype, CBundle
from metamodels.component_metamodel import component

deployment_node = CMetaclass("Deployment Node")
deployment_node_relation = deployment_node.association(deployment_node, "connected to: [from] * -> [to] *")
deployment_relation = component.association(deployment_node,
                                            "deployed on: [components] * -> [deployment_nodes] *")

device = CMetaclass("Device", superclasses=deployment_node)
execution_environment = CMetaclass("Execution Environment", superclasses=deployment_node)

#
# device types
#
device_type = CStereotype("Device Type", extended=device)

server_device_type = CStereotype("Server", superclasses=device_type)
web_server_device_type = CStereotype("Web Server", superclasses=server_device_type)
application_server_device_type = CStereotype("Application Server", superclasses=server_device_type)
client_workstation_device_type = CStereotype("Client Workstation", superclasses=device_type)
mobile_device_type = CStereotype("Mobile Device", superclasses=device_type)
embedded_device_type = CStereotype("Embedded Device", superclasses=device_type)
iot_device_type = CStereotype("IoT Device", superclasses=device_type)
cloud_devices_type = CStereotype("Cloud", superclasses=device_type)
paas_cloud_devices_type = CStereotype("PaaS Cloud", superclasses=cloud_devices_type)
cloud_server_device_type = CStereotype("Cloud Server", superclasses=[cloud_devices_type, server_device_type])
virtual_machine_device_type = CStereotype("Virtual Machine Device", superclasses=device_type)
cloud_vm_device_type = CStereotype("Cloud VM", superclasses=[cloud_devices_type, virtual_machine_device_type])

#
# execution environment types
#
execution_environment_type = CStereotype("Execution Environment Type", extended=execution_environment)

# environment types, intended to be combined like <<Cloud, Cluster>>
# note that there are server environment types such as a JSP server, but also server
# devices such as the application server devices on which the JSP server runs, same for
# cloud devices and software environments running on them
cloud_env_type = CStereotype("Cloud Environment", superclasses=execution_environment_type)
public_cloud_env_type = CStereotype("Public Cloud", superclasses=cloud_env_type)
private_cloud_env_type = CStereotype("Private Cloud", superclasses=cloud_env_type)
virtual_private_cloud_env_type = CStereotype("Virtual Private Cloud", superclasses=cloud_env_type)
server_env_type = CStereotype("Server", superclasses=execution_environment_type)
web_server_env_type = CStereotype("Web Server", superclasses=server_env_type)
virtual_machine_env_type = CStereotype("Virtual Machine", superclasses=execution_environment_type)
container_env_type = CStereotype("Container", superclasses=execution_environment_type)
cluster_env_type = CStereotype("Cluster", superclasses=execution_environment_type)
on_premise_env_type = CStereotype("On-Premises", superclasses=execution_environment_type)
datacenter_env_type = CStereotype("Datacenter", superclasses=execution_environment_type)
local_workstation_env_type = CStereotype("Local Workstation", superclasses=execution_environment_type)

#
# deployment relation types
# 
deployment_relation_type = CStereotype("Deployment Relation Type", extended=deployment_relation)
deployed_on_type = CStereotype("deployed on", superclasses=deployment_relation_type)
uses_deployment_node_type = CStereotype("uses", superclasses=deployment_relation_type)
launches_deployment_node_type = CStereotype("launches", superclasses=deployment_relation_type)
provides_deployment_artifacts_type = CStereotype("provides deployment artifacts", superclasses=deployment_relation_type)
deployed_in_container_type = CStereotype("deployed in container", superclasses=deployed_on_type)

#
# deployment node relations
# 
deployment_node_relation_type = CStereotype("Deployment Node Relation Type", extended=deployment_node_relation)
part_of_deployment_node_relation_type = CStereotype("part of", superclasses=deployment_node_relation_type)
runs_on_deployment_node_relation_type = CStereotype("runs on", superclasses=deployment_node_relation_type)
connects_to_deployment_node_relation_type = CStereotype("connects to", superclasses=deployment_node_relation_type)

_all = CBundle("_all",
               elements=deployment_node.get_connected_elements(add_stereotypes=True,
                                                               stop_elements_inclusive=[component]) +
                        deployment_relation_type.get_connected_elements(add_stereotypes=True) +
                        deployment_node_relation_type.get_connected_elements(add_stereotypes=True))

deployment_metamodel_views = [
    _all, {}]
