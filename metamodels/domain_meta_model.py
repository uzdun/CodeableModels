from codeable_models import CMetaclass, CBundle

domain_metaclass = CMetaclass("Domain Class")
domain_metaclass_group = CMetaclass("Domain Class Group", superclasses=domain_metaclass)
and_combined_group = CMetaclass("And-Combined Group", superclasses=domain_metaclass_group)
or_combined_group = CMetaclass("Or-Combined Group", superclasses=domain_metaclass_group)
domain_metaclass_group.association(domain_metaclass, "[collection] * <>- [class] *")

domain_meta_model = CBundle("Domain Meta Model", elements=domain_metaclass.get_connected_elements())
