from codeable_models import CClass, CMetaclass, CBundle, CStereotype

# Technology and technology type
technology = CMetaclass("Technology")
technologyType = CStereotype("Technology Type", extended = technology)

programmingLanguageTechType = CStereotype("Programming Language", superclasses = technologyType)
pythonTechType = CStereotype("Python", superclasses = programmingLanguageTechType)
javascriptTechType = CStereotype("Javascript", superclasses = programmingLanguageTechType)
javaTechType = CStereotype("Java", superclasses = programmingLanguageTechType)
goTechType = CStereotype("Go", superclasses = programmingLanguageTechType)

webFrameworkTechType = CStereotype("Web Framework", superclasses = technologyType)
expressTechType = CStereotype("Express", superclasses = technologyType)

messagingMiddlewareTechType = CStereotype("Messaging Middleware", superclasses = technologyType)
amqpTechType = CStereotype("AMQP", superclasses = messagingMiddlewareTechType)

_all = CBundle("_all",
               elements = technology.get_connected_elements(add_stereotypes = True))
technologyMetamodelViews = [
    _all, {}]
