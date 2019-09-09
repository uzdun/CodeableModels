from codeableModels import CClass, CMetaclass, CBundle, CStereotype

# Component and component type
component = CMetaclass("Component")
componentType = CStereotype("Component Type", extended = component)

# connector relation and connector type
connectorsRelation = component.association(component, "connected to: [source] * -> [target] *")
# attribute description can be used for explaining e.g. how the type affects the connector or what parts are affected
connectorType = CStereotype("Connector Type", extended = connectorsRelation, 
    attributes = {"description": str})


_all = CBundle("_all", 
    elements = component.getConnectedElements(addStereotypes = True) + connectorType.getConnectedElements(addStereotypes = True))

componentMetamodelViews = [
    _all, {}]
