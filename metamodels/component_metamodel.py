"""
*File Name:* metamodels/component.py

This is a simple component metamodel. As it is used for explaining meta-modelling with stereotypes, it is
described in :ref:`meta_model_stereotypes`.

It provides a ``component`` meta-class with a generic ``component_type`` stereotype for extensions
with component types, as well as a ``connectors_relation`` meta-class association with a generic ``connector_type``
stereotype for extensions with connector types.

"""

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
_all = CBundle("component_model_all", elements=_all_elements)

componentMetamodelViews = [
    _all, {}]


