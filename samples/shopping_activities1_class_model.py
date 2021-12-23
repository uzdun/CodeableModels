"""
*File Name:* samples/shopping_activities1_class_model.py

This is a Codeable Models example realizing a sample shopping activity model
as a class diagram.
It is used to explain meta-modelling by using meta-classes and their relations
from the :ref:`activity_metamodel`.

It is inspired by the model at:
`<https://www.uml-diagrams.org/online-shopping-uml-activity-diagram-example.html>`_

The example is explained in :ref:`meta_modelling`.

"""

from codeable_models import CBundle, CClass, add_links
from metamodels.activity_metamodel import activity_node, initial_node, decision_node, merge_node, final_node, \
    accept_event_action, edge_relation
from plant_uml_renderer import PlantUMLGenerator

initial_node_shopping_cart = CClass(initial_node, "[Initial]")
decision_node_search_browse = CClass(decision_node, "Search or Browse?")
merge_node_search = CClass(merge_node, "[Merge]")
search_item = CClass(activity_node, "Search Items")
merge_node_browse = CClass(merge_node, "[Merge]")
browse_item = CClass(activity_node, "Browse Items")
decision_node_found = CClass(decision_node, "Item Found?", values={"decision": "Item found?"})
merge_node_view_item = CClass(merge_node, "[Merge]")
view_item = CClass(activity_node, "View Item")
decision_node_decision_made = CClass(decision_node, "Decision Made?", values={"decision": "Decision made?"})
add_to_shopping_cart = CClass(activity_node, "Add to Shopping Cart")
decision_node_proceed = CClass(decision_node, "Proceed?")
merge_node_view_shopping_cart = CClass(merge_node, "[Merge]")
view_shopping_cart = CClass(activity_node, "View Shopping Cart")
decision_node_done = CClass(decision_node, "Done?")
update_shopping_cart = CClass(activity_node, "Update Shopping Cart")
checkout = CClass(activity_node, "Checkout")
final_node_shopping_cart = CClass(final_node, "[Final]")
checkout_merge_node = CClass(merge_node, "[Merge]")
check_shopping_cart = CClass(accept_event_action, "Check Shopping Cart")
proceed_to_checkout = CClass(accept_event_action, "Proceed to Checkout")

for source, targets in {initial_node_shopping_cart: [decision_node_search_browse],
                        merge_node_search: [search_item],
                        merge_node_browse: [browse_item],
                        search_item: [decision_node_found],
                        browse_item: [merge_node_view_item],
                        merge_node_view_item: [decision_node_search_browse, view_item],
                        view_item: [decision_node_decision_made],
                        decision_node_decision_made: [merge_node_search, merge_node_browse],
                        add_to_shopping_cart: [decision_node_proceed],
                        update_shopping_cart: [decision_node_proceed],
                        merge_node_view_shopping_cart: [view_shopping_cart],
                        view_shopping_cart: [decision_node_done],
                        check_shopping_cart: [merge_node_view_shopping_cart],
                        proceed_to_checkout: [checkout_merge_node],
                        checkout_merge_node: [checkout],
                        checkout: [final_node_shopping_cart]}.items():
    for target in targets:
        source.association(target, source_multiplicity="1", multiplicity="1", derived_from=edge_relation)

decision_node_search_browse.association(merge_node_search, name="[search]", source_multiplicity="1", multiplicity="1",
                                        derived_from=edge_relation)
decision_node_search_browse.association(merge_node_browse, name="[browse]", source_multiplicity="1", multiplicity="1",
                                        derived_from=edge_relation)
decision_node_found.association(merge_node_view_item, name="[found]", source_multiplicity="1", multiplicity="1",
                                derived_from=edge_relation)
decision_node_found.association(decision_node_search_browse, name="[not found]", source_multiplicity="1",
                                multiplicity="1", derived_from=edge_relation)
decision_node_decision_made.association(add_to_shopping_cart, name="[made decision]", source_multiplicity="1",
                                        multiplicity="1", derived_from=edge_relation)
decision_node_proceed.association(merge_node_view_shopping_cart, name="[view cart]", source_multiplicity="1",
                                  multiplicity="1", derived_from=edge_relation)
decision_node_proceed.association(decision_node_search_browse, name="[proceed]", source_multiplicity="1",
                                  multiplicity="1", derived_from=edge_relation)
decision_node_done.association(decision_node_search_browse, name="[more shopping]", source_multiplicity="1",
                               multiplicity="1", derived_from=edge_relation)
decision_node_done.association(update_shopping_cart, name="[update needed]", source_multiplicity="1", multiplicity="1",
                               derived_from=edge_relation)
decision_node_done.association(checkout_merge_node, name="[done with shopping]", source_multiplicity="1",
                               multiplicity="1", derived_from=edge_relation)

shopping_activity_class_model = CBundle("shopping_activity_class_model",
                                        elements=initial_node_shopping_cart.get_connected_elements())


# Classes Introspection
def print_classes_introspection_examples():
    print(f"Activity node classes: {activity_node.classes!s}")
    print(f"Activity node all classes: {activity_node.all_classes!s}")


# Classes Introspection
def run():
    print("***************** Shopping Activity Model 2: Meta-modelling example (class-level) *****************")

    print("*** Classes introspection")
    print_classes_introspection_examples()

    print('*** Plant UML Generation')
    generator = PlantUMLGenerator()
    generator.class_model_renderer.left_to_right = True
    generator.generate_class_models(shopping_activity_class_model.name,
                                    [shopping_activity_class_model, {"render_metaclass_as_stereotype": True}])
    print(f"... Generated models in {generator.directory!s}/{shopping_activity_class_model.name!s}")


if __name__ == "__main__":
    run()
