from codeable_models import CMetaclass, CBundle, CStereotype

# Component and component type
component = CMetaclass("Component")
component_type = CStereotype("Component Type", extended=component)

# connector relation and connector type
connectors_relation = component.association(component, "connected to: [source] * -> [target] *")
# attribute description can be used for explaining e.g. how the type affects the connector or what parts are affected
connector_type = CStereotype("Connector Type", extended=connectors_relation,
                             attributes={"description": str})

_all_elements = component.get_connected_elements(add_stereotypes=True) + \
                connector_type.get_connected_elements(add_stereotypes=True) + \
                component_type.get_connected_elements(add_stereotypes=True)
_all = CBundle("_all", elements=_all_elements)

componentMetamodelViews = [
    _all, {}]


