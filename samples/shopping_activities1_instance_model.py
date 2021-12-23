"""
*File Name:* samples/shopping_activity_model1.py

This is a Codeable Models example realizing a sample shopping activity model.
It is used to explain meta-modelling by using meta-classes and their relations
from the :ref:`activity_metamodel`.

It is inspired by the model at:
`<https://www.uml-diagrams.org/online-shopping-uml-activity-diagram-example.html>`_

The example is explained in :ref:`meta_modelling`.

"""

from codeable_models import CBundle, CClass, add_links
from metamodels.activity_metamodel import activity_node, initial_node, decision_node, merge_node, final_node, \
    accept_event_action
from plant_uml_renderer import PlantUMLGenerator

initial_node_shopping_cart = CClass(initial_node)
decision_node_search_browse = CClass(decision_node)
merge_node_search = CClass(merge_node)
search_item = CClass(activity_node, "Search Items")
merge_node_browse = CClass(merge_node)
browse_item = CClass(activity_node, "Browse Items")
decision_node_found = CClass(decision_node, values={"decision": "Item found?"})
merge_node_view_item = CClass(merge_node)
view_item = CClass(activity_node, "View Item")
decision_node_decision_made = CClass(decision_node, values={"decision": "Decision made?"})
add_to_shopping_cart = CClass(activity_node, "Add to Shopping Cart")
decision_node_proceed = CClass(decision_node)
merge_node_view_shopping_cart = CClass(merge_node)
view_shopping_cart = CClass(activity_node, "View Shopping Cart")
decision_node_done = CClass(decision_node)
update_shopping_cart = CClass(activity_node, "Update Shopping Cart")
checkout = CClass(activity_node, "Checkout")
final_node_shopping_cart = CClass(final_node)
checkout_merge_node = CClass(merge_node)
check_shopping_cart = CClass(accept_event_action, "Check Shopping Cart")
proceed_to_checkout = CClass(accept_event_action, "Proceed to Checkout")

add_links({
    initial_node_shopping_cart: decision_node_search_browse,
    merge_node_search: search_item,
    merge_node_browse: browse_item,
    search_item: decision_node_found,
    browse_item: merge_node_view_item,
    merge_node_view_item: [decision_node_search_browse, view_item],
    view_item: decision_node_decision_made,
    decision_node_decision_made: [merge_node_search, merge_node_browse],
    add_to_shopping_cart: decision_node_proceed,
    update_shopping_cart: decision_node_proceed,
    merge_node_view_shopping_cart: view_shopping_cart,
    view_shopping_cart: decision_node_done,
    check_shopping_cart: merge_node_view_shopping_cart,
    proceed_to_checkout: checkout_merge_node,
    checkout_merge_node: checkout,
    checkout: final_node_shopping_cart,
}, role_name="target")

decision_node_search_browse.add_links(merge_node_search, label="[search]", role_name="target")
decision_node_search_browse.add_links(merge_node_browse, label="[browse]", role_name="target")
decision_node_found.add_links(merge_node_view_item, label="[found]", role_name="target")
decision_node_found.add_links(decision_node_search_browse, label="[not found]", role_name="target")
decision_node_decision_made.add_links(add_to_shopping_cart, label="[made decision]", role_name="target")
decision_node_proceed.add_links(merge_node_view_shopping_cart, label="[view cart]", role_name="target")
decision_node_proceed.add_links(decision_node_search_browse, label="[proceed]", role_name="target")
decision_node_done.add_links(decision_node_search_browse, label="[more shopping]", role_name="target")
decision_node_done.add_links(update_shopping_cart, label="[update needed]", role_name="target")
decision_node_done.add_links(checkout_merge_node, label="[done with shopping]", role_name="target")

shopping_activity_model = CBundle("shopping_activity_model",
                                  elements=initial_node_shopping_cart.class_object.get_connected_elements())


# Classes Introspection
def print_classes_introspection_examples():
    print(f"Activity node classes: {activity_node.classes!s}")
    print(f"Activity node all classes: {activity_node.all_classes!s}")


def run():
    print("***************** Shopping Activity Model 1: Meta-modelling example *****************")

    print("*** Classes introspection")
    print_classes_introspection_examples()

    print('*** Plant UML Generation')
    generator = PlantUMLGenerator()
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models(shopping_activity_model.name, [shopping_activity_model, {}])
    print(f"... Generated models in {generator.directory!s}/{shopping_activity_model.name!s}")


if __name__ == "__main__":
    run()
