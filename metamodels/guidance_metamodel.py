"""
*File Name:* metamodels/guidance_metamodel.py

This is a meta-model for modelling architectural guidance del, aka reusable architectural decision del.

"""

from codeable_models import CMetaclass, CBundle, CStereotype
from metamodels.domain_metamodel import domain_metaclass, domain_metamodel

model_element = CMetaclass("Model Element", attributes={"aka": str, "description": str})
category = CMetaclass("Category", superclasses=model_element)

design_solution = CMetaclass("Design Solution", superclasses=model_element,
                             attributes={"background reading": str})

design_solution_domain_metaclass = CMetaclass("Design Solution / Domain Class",
                                              superclasses=[design_solution, domain_metaclass])

practice = CMetaclass("Practice", superclasses=design_solution)
pattern = CMetaclass("Pattern", superclasses=practice)

known_use = CMetaclass("Known Use", superclasses=model_element,
                       attributes={"reference": str})
solutions_known_uses_relation = design_solution.association(known_use, "used in: [solutions] * -> [knownUses] *")

decision = CMetaclass("Decision", superclasses=design_solution, attributes={"recommendation": str})
category_decisions_relation = category.association(decision, "[category] 1 <>- [decisions] *")

decision_type = CStereotype("Decision Type", extended=decision)
single_answer = CStereotype("Single Answers", superclasses=decision_type)
multiple_answers = CStereotype("Multiple Answers", superclasses=decision_type)

force = CMetaclass("Force", superclasses=model_element)
force_impact_relation = design_solution.association(force, "has force: [solutions] * -> [forces] *")

force_impact_type = CStereotype("Force Impact Type", extended=force_impact_relation)
very_positive = CStereotype("++", superclasses=force_impact_type)
positive = CStereotype("+", superclasses=force_impact_type)
neutral = CStereotype("o", superclasses=force_impact_type)
negative = CStereotype("-", superclasses=force_impact_type)
very_negative = CStereotype("--", superclasses=force_impact_type)
positive_and_negative = CStereotype("+/-", superclasses=force_impact_type)

category_hierarchy_relation = category.association(category,
                                                   "has sub-category: [parent category] 1 <*>- [sub category] *")

design_solution_dependencies = design_solution.association(design_solution, "is dependent on: [from] * -> [to] *")
design_solution_dependency_type = CStereotype("Design Solution Dependency Type", extended=design_solution_dependencies,
                                              attributes={"how": str, "role": str})
requires = CStereotype("Requires", superclasses=design_solution_dependency_type)
uses = CStereotype("Uses", superclasses=design_solution_dependency_type)
can_use = CStereotype("Can Use", superclasses=design_solution_dependency_type)
can_be_combined_with = CStereotype("Can Be Combined With", superclasses=design_solution_dependency_type)
can_be_realized_by = CStereotype("Can be Realized By", superclasses=design_solution_dependency_type)
has_variant = CStereotype("Has Variant", superclasses=design_solution_dependency_type)
extension = CStereotype("Extension", superclasses=design_solution_dependency_type)
is_a = CStereotype("Is-a", superclasses=design_solution_dependency_type)
realizes = CStereotype("Realizes", superclasses=design_solution_dependency_type)
includes = CStereotype("Includes", superclasses=design_solution_dependency_type)
can_include = CStereotype("Can Include", superclasses=design_solution_dependency_type)
alternative_to = CStereotype("Alternative To", superclasses=design_solution_dependency_type)
rules_out = CStereotype("Rules Out", superclasses=design_solution_dependency_type)
influences = CStereotype("Influences", superclasses=design_solution_dependency_type)
leads_to = CStereotype("Leads To", superclasses=design_solution_dependency_type)
enables = CStereotype("Enables", superclasses=design_solution_dependency_type)

solutions_to_next_decisions_relation = design_solution.association(decision,
                                                                   "is next: [prior solution] * -> [next decision] *")

solutions_to_next_decisions_relation_type = CStereotype("Solutions To Decisions Relation Type",
                                                        extended=solutions_to_next_decisions_relation)
mandatory_next = CStereotype("Mandatory Next", superclasses=solutions_to_next_decisions_relation_type)
optional_next = CStereotype("Optional Next", superclasses=solutions_to_next_decisions_relation_type)
# unspecified if the next decision is mandatory or optional
next_decision = CStereotype("Next", superclasses=solutions_to_next_decisions_relation_type)
consider_if_not_decided_yet = CStereotype("Consider If Not Decided Yet",
                                          superclasses=solutions_to_next_decisions_relation_type)

decision_solution_relation = decision.association(design_solution, "has: *->*")
option = CStereotype("Option", extended=decision_solution_relation,
                     attributes={"name": str})

decision_category_to_contexts_relation = category.association(domain_metaclass,
                                                              "has context: [category] * -> [context] *")

decision_to_contexts_relation = decision.association(domain_metaclass, "has context: [decision] * -> [context] *")

context_relations_type = CStereotype("Decision Category To Contexts Relation Type",
                                     extended=[decision_category_to_contexts_relation, decision_to_contexts_relation])
decide_for_all_instances_of = CStereotype("decide for all instances of", superclasses=context_relations_type)
decide_for_some_instances_of = CStereotype("decide for some instances of", superclasses=context_relations_type)

do_nothing_design_solution = CMetaclass("Do Nothing", superclasses=design_solution)

# bundles

_all = CBundle("Guidance Meta Model", elements=model_element.get_connected_elements())

guidance_metamodel_hierarchy = CBundle("Guidance Meta Model Hierarchy", elements=model_element.get_connected_elements(
    stop_elements_exclusive=domain_metaclass))

guidance_metamodel_details = CBundle("Guidance Meta Model Details",
                                     elements=design_solution.get_connected_elements(
                                         stop_elements_inclusive=domain_metaclass,
                                         stop_elements_exclusive=[model_element, do_nothing_design_solution, practice,
                                                                  pattern]))

force_impact_metaclasses = [force_impact_relation.source, force_impact_relation.target]
force_impact_type_bundle = CBundle("Force Impact Types",
                                   elements=force_impact_metaclasses + force_impact_type.get_connected_elements(
                                       add_stereotypes=True,
                                       stop_elements_inclusive=force_impact_metaclasses))

design_solution_dependencies_metaclasses = [design_solution_dependencies.source, design_solution_dependencies.target]
_bundle_elements = design_solution_dependencies_metaclasses + design_solution_dependency_type.get_connected_elements(
    add_stereotypes=True, stop_elements_inclusive=design_solution_dependencies_metaclasses)
design_solution_dependency_type_bundle = CBundle("Design Solution Dependency Types", elements=_bundle_elements)

solutions_to_next_decisions_relation_metaclasses = [solutions_to_next_decisions_relation.source,
                                                    solutions_to_next_decisions_relation.target]
_bundle_elements = solutions_to_next_decisions_relation_metaclasses + \
                   solutions_to_next_decisions_relation_type.get_connected_elements(
                       add_stereotypes=True, stop_elements_inclusive=solutions_to_next_decisions_relation_metaclasses)
solution_to_next_decisions_relation_type_bundle = CBundle("Solutions To Next Decisions Relation Types",
                                                          elements=_bundle_elements)

decision_category_to_contexts_relation_metaclasses = [decision_category_to_contexts_relation.source,
                                                      decision_category_to_contexts_relation.target]
_bundle_elements = decision_category_to_contexts_relation_metaclasses + context_relations_type.get_connected_elements(
    add_stereotypes=True, stop_elements_inclusive=decision_category_to_contexts_relation_metaclasses)
context_relations_type_bundle = CBundle("Decision Category To Contexts Relation Types",
                                        elements=_bundle_elements)

guidance_metamodel_views = [_all, {},
                            guidance_metamodel_hierarchy, {"render_associations": False},
                            guidance_metamodel_details, {},
                            domain_metamodel, {},
                            force_impact_type_bundle, {},
                            design_solution_dependency_type_bundle, {},
                            solution_to_next_decisions_relation_type_bundle, {},
                            context_relations_type_bundle, {}]


# helper functions
def add_stereotyped_link_with_how_tagged_value(link_from, link_to, stereotype_instance, tag_value):
    links = link_from.add_links(link_to, role_name="to")[0]
    links.stereotype_instances = [stereotype_instance]
    links.set_tagged_value("how", tag_value)
    return links


def add_stereotyped_link_with_role_tagged_value(link_from, link_to, stereotype_instance, tag_value):
    links = link_from.add_links(link_to, role_name="to")[0]
    links.stereotype_instances = [stereotype_instance]
    links.set_tagged_value("role", tag_value)
    return links


def add_decision_option_link(decision_, design_solution_, option_name=None):
    links = decision_.add_links(design_solution_, association=decision_solution_relation)[0]
    links.stereotype_instances = [option]
    if option_name is not None:
        links.set_tagged_value("name", option_name)
    return links


def add_stereotyped_design_solution_link(from_design_solution, to_design_solution, stereotype_instance):
    from_design_solution.add_links(to_design_solution, role_name="to")[0].stereotype_instances = [stereotype_instance]


def add_decision_option_association(decision_, design_solution_, option_name=None):
    association = decision_.association(design_solution_, multiplicity="*", source_multiplicity="1",
                                        derived_from=decision_solution_relation)
    association.stereotype_instances = [option]
    if option_name is not None:
        association.set_tagged_value("name", option_name)
    return association
