"""
*File Name:* samples/codeable_models_class_relations.py

This is a Codeable Models example modelling the Codeable Models classes, their attributes, and
relations as a class model. The resulting views generated from this model are used throughout
the API documentation to illustrate the relations of the various classes. Please
use the API description in :ref:`api` as a documentation of the meaning of the elements
of this model.

"""
from codeable_models import CClass, CBundle
from lib.standard_types import dictionary, exception
from metamodels.domain_metamodel import domain_metaclass
from plant_uml_renderer import PlantUMLGenerator

# required additional types
supported_type = CClass(domain_metaclass, "Supported Type")
supported_type_value = CClass(domain_metaclass, "Supported Type Value")

cnamed_element = CClass(domain_metaclass, "CNamedElement", attributes={
    "name": str
})
cbundlable = CClass(domain_metaclass, "CBundlable", superclasses=cnamed_element)
cclassifier = CClass(domain_metaclass, "CClassifier", superclasses=cbundlable)
cattribute = CClass(domain_metaclass, "CAttribute", attributes={
    "name": str,
    "type": supported_type,
    "default": supported_type_value
})
cclass = CClass(domain_metaclass, "CClass", superclasses=cclassifier, attributes={
    "tagged_values": dictionary
})
cassociation = CClass(domain_metaclass, "CAssociation", superclasses=cclassifier, attributes={
    "multiplicity": str,
    "role_name": str,
    "source_multiplicity": str,
    "source_role_name": str,
    "aggregation": bool,
    "composition": bool,
})
cbundle = CClass(domain_metaclass, "CBundle", superclasses=cbundlable)
clayer = CClass(domain_metaclass, "CLayer", superclasses=cbundle)
cpackage = CClass(domain_metaclass, "CPackage", superclasses=cbundle)

cenum = CClass(domain_metaclass, "CEnum", superclasses=cbundlable, attributes={
    "values": list
})
cexception = CClass(domain_metaclass, "CException", superclasses=exception, attributes={
    "value": str
})
cobject = CClass(domain_metaclass, "CObject", superclasses=cbundlable, attributes={
    "values": dictionary
})
clink = CClass(domain_metaclass, "CLink", superclasses=cobject, attributes={
    "label": str,
    "tagged_values": dictionary

})
cmetaclass = CClass(domain_metaclass, "CMetaclass", superclasses=cclassifier)
cstereotype = CClass(domain_metaclass, "CStereotype", superclasses=cclassifier, attributes={
    "default_values": dictionary
})

bundle_elements_relation = cbundle.association(cbundlable, "elements: [bundles] * -> [elements] *")

classifier_association_relation = \
    cclassifier.association(cassociation, "associations: 0..1 <>- [associations] *")
classifier_attribute_relation = \
    cclassifier.association(cattribute, "attributes: [classifier] 0..1 <>- [attributes] *")
inheritance_relation = \
    cclassifier.association(cclassifier, "inheritance hierarchy: [subclasses] * -> [superclasses] *")

class_metaclass_relation = cclass.association(cmetaclass, "metaclass: [classes] * -> [metaclass] 1")
cclass.association(cobject, "objects: [classifier] 1 -> [objects] *")
cclass.association(cobject, "class object: [class_object_class] 1 <*>- [class_object] 1")
class_stereotype_instances = \
    cclass.association(cstereotype, "stereotype instances: [extended_instances] * -> [stereotype_instances] *")

association_source_relation = \
    cassociation.association(cclassifier, "source: [associations] * -> [source] 1")
association_target_relation = \
    cassociation.association(cclassifier, "target: [associations] * -> [target] 1")
association_stereotypes_relation = \
    cassociation.association(cstereotype, "stereotypes: [extended] * -> [stereotypes] *")

clink.association(cobject, "source: [links] * -> [source] 1")
clink.association(cobject, "target: [links] * -> [target] 1")
link_stereotype_instances = \
    clink.association(cstereotype, "stereotype instances: [extended_instances] * -> [stereotype_instances] *")
clink.association(cassociation, "association: * -> [association] 1")

metaclass_stereotypes_relation = \
    cmetaclass.association(cstereotype, "stereotypes: [extended] * -> [stereotypes] *")

codeable_models_all = CBundle("codeable_models_model_all",
                              elements=cnamed_element.get_connected_elements() + [cexception, exception])
codeable_models_hierarchy = CBundle("codeable_models_model_hierarchy",
                                    elements=cnamed_element.get_connected_elements(
                                        stop_elements_exclusive=[cattribute]) + [cexception, exception])
bundles_model = CBundle("bundles_model",
                        elements=[cbundlable, cbundle, cenum, cobject, cclassifier, cclass, cmetaclass, cstereotype,
                                  cassociation, clink, cpackage, clayer])
classifier_model = CBundle("classifier_model",
                           elements=[cclassifier, cclass, cmetaclass, cstereotype,
                                     cassociation, cattribute])
metaclass_model = CBundle("metaclass_model",
                          elements=[cmetaclass, cclassifier, cclass, cstereotype])
stereotype_model = CBundle("stereotype_model",
                           elements=[cstereotype, cclassifier, cclass, cmetaclass, cassociation, clink])
class_model = CBundle("class_model",
                      elements=[cclassifier, cclass, cmetaclass, cstereotype, cobject])
object_model = CBundle("object_model",
                       elements=[cobject, cclass, clink, cbundlable])
link_model = CBundle("link_model",
                     elements=[clink, cobject, cassociation, cstereotype])
association_model = CBundle("association_model",
                            elements=[cclassifier, cassociation, clink, cstereotype])

clayer.association(clayer, "layer order: [super_layer] 1 -> [sub_layer] 1")


def run():
    print("***************** Codeable Models Class Relations *****************")
    generator = PlantUMLGenerator()
    generator.generate_class_models(
        "codeable_models_model", [
            codeable_models_all, {},
            codeable_models_hierarchy, {"render_associations": False, "render_attributes": False},
            bundles_model, {"render_attributes": False, "included_associations": [bundle_elements_relation]},
            classifier_model, {"included_associations": [inheritance_relation, classifier_association_relation,
                                                         classifier_attribute_relation]},
            metaclass_model, {"excluded_associations": [inheritance_relation]},
            stereotype_model, {"excluded_associations": [inheritance_relation, classifier_association_relation,
                                                         association_source_relation, association_target_relation]},
            class_model, {},
            object_model, {},
            association_model, {"excluded_associations": [inheritance_relation]},
            link_model, {}
        ])
    print(f"... Generated models in {generator.directory!s}/codeable_models_model")


if __name__ == "__main__":
    run()
