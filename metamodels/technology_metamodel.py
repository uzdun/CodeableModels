"""
*File Name:* metamodels/technology_metamodel.py

This is a simple meta-model for modelling technologies used in a system as stereotype extensions of a meta-class
``technology``. A few sample stereotypes are provided, too.

"""


from codeable_models import CMetaclass, CBundle, CStereotype

# Technology and technology type
technology = CMetaclass("Technology")
technology_type = CStereotype("Technology Type", extended=technology)

programming_language_tech_type = CStereotype("Programming Language", superclasses=technology_type)
python_tech_type = CStereotype("Python", superclasses=programming_language_tech_type)
javascript_tech_type = CStereotype("Javascript", superclasses=programming_language_tech_type)
java_tech_type = CStereotype("Java", superclasses=programming_language_tech_type)
go_tech_type = CStereotype("Go", superclasses=programming_language_tech_type)

web_framework_tech_type = CStereotype("Web Framework", superclasses=technology_type)
express_tech_type = CStereotype("Express", superclasses=technology_type)

messaging_middleware_tech_type = CStereotype("Messaging Middleware", superclasses=technology_type)
amqp_tech_type = CStereotype("AMQP", superclasses=messaging_middleware_tech_type)

_all = CBundle("_all",
               elements=technology.get_connected_elements(add_stereotypes=True))
technology_metamodel_views = [
    _all, {}]
