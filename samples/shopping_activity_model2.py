"""
*File Name:* samples/shopping_activity_model2.py

This is a Codeable Models example realizing a sample shopping activity model and a
workflow trace model derived from it.

It is used to explain meta-modelling by using meta-classes and their relations from the :ref:`activity_metamodel`.

In particular, it looks into how to combine object, class, and meta-class del. That is, an activity class
model is derived from an activity meta-model. The activity class model is used to define an object model
for workflow traces. The trace objects are linked to domain model elements from :ref:`shopping_instances2`
(derived themselves from the class model in  :ref:`shopping_model4`).

The example is explained in :ref:`combining_object_class_and_meta_class_modelling`.

The activity model is inspired by the model at:
`<https://www.uml-diagrams.org/online-shopping-uml-activity-diagram-example.html>`_

"""

from codeable_models import CBundle, CClass, add_links, CObject, set_links
from metamodels.activity_metamodel import activity_node, initial_node, decision_node, merge_node, final_node, \
    accept_event_action
from plant_uml_renderer import PlantUMLGenerator
from samples.shopping_instances2 import premium_pen, thomas_customer, cart1, order1
from samples.shopping_model4 import product, cart, add_items_to_cart, customer_cart_relation, \
    place_order, order, item

workflow_node = CClass(activity_node, "Workflow Node")
workflow_trace = workflow_node.association(workflow_node, "next: 1 [from] -> 1 [to]")
view_product_node = CClass(activity_node, "View Product", superclasses=workflow_node)
view_product_node.association(product, "product: * -> [product] 1")
view_cart_node = CClass(activity_node, "View Cart", superclasses=workflow_node)
view_product_node.association(cart, "cart: * -> [cart] 1", superclasses=workflow_node)
access_order_node = CClass(activity_node, "Access Order", superclasses=workflow_node)
access_order_node.association(order, "order: * -> [order] 1", superclasses=workflow_node)
create_item_node = CClass(activity_node, "Create Item", superclasses=workflow_node)
create_item_node.association(item, "item: * -> [item] 1", superclasses=workflow_node)

initial_node_shopping_cart = CClass(initial_node, superclasses=workflow_node)
decision_node_search_browse = CClass(decision_node, superclasses=workflow_node)
merge_node_search = CClass(merge_node, superclasses=workflow_node)
search_item = CClass(activity_node, "Search Items", superclasses=workflow_node, attributes={
    "search string": str
})
merge_node_browse = CClass(merge_node, superclasses=workflow_node)
browse_item = CClass(activity_node, "Browse Items", superclasses=workflow_node)
decision_node_found = CClass(decision_node, values={"decision": "Item found?"}, superclasses=workflow_node)
merge_node_view_item = CClass(merge_node, superclasses=workflow_node)
view_item = CClass(activity_node, "View Item", superclasses=view_product_node)
decision_node_decision_made = CClass(decision_node, values={"decision": "Decision made?"}, superclasses=workflow_node)
add_to_shopping_cart = CClass(activity_node, "Add to Shopping Cart", superclasses=create_item_node)
decision_node_proceed = CClass(decision_node, superclasses=workflow_node)
merge_node_view_shopping_cart = CClass(merge_node, superclasses=workflow_node)
view_shopping_cart = CClass(activity_node, "View Shopping Cart", superclasses=view_product_node)
decision_node_done = CClass(decision_node, superclasses=workflow_node)
update_shopping_cart = CClass(activity_node, "Update Shopping Cart", superclasses=workflow_node)
checkout = CClass(activity_node, "Checkout", superclasses=access_order_node)
final_node_shopping_cart = CClass(final_node, superclasses=workflow_node)
checkout_merge_node = CClass(merge_node, superclasses=workflow_node)
check_shopping_cart = CClass(accept_event_action, "Check Shopping Cart", superclasses=workflow_node)
proceed_to_checkout = CClass(accept_event_action, "Proceed to Checkout", superclasses=workflow_node)

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


def create_trace(node_list):
    trace = []
    for node in node_list:
        if node.classifier.name is not None:
            trace.append(node)
    for i in range(0, len(trace) - 1):
        trace[i].add_links(trace[i + 1], role_name="to")
    return trace


# get rid of the objects, we don't need from the imported shopping model
cart1.delete()
order1.delete()
for item_object in item.objects:
    item_object.delete()

# define a new cart and order, as they would be created in the shopping session
cart1 = CObject(cart)
cart1_items = add_items_to_cart(cart1, [[premium_pen, 3]])
set_links({cart1: thomas_customer}, association=customer_cart_relation)
order1 = place_order(cart1)

# create and link the objects which have attributes or links
search_obj = CObject(search_item)
search_obj.set_value("search string", "pens")
view_shopping_cart_obj = CObject(view_shopping_cart)
view_shopping_cart_obj.add_links(cart1, role_name="cart")
add_to_shopping_cart_obj = CObject(add_to_shopping_cart)
add_to_shopping_cart_obj.add_links(cart1_items, role_name="item")
checkout_obj = CObject(checkout)
checkout_obj.add_links(order1, role_name="order")
view_item_obj = CObject(view_item)
view_item_obj.add_links(premium_pen, role_name="product")

# pass the full trace to create_trace to filter out the meaningful objects in the trace and link them
a_trace = create_trace([CObject(initial_node_shopping_cart),
                        CObject(decision_node_search_browse),
                        CObject(merge_node_search),
                        search_obj,
                        CObject(decision_node_found),
                        CObject(merge_node_view_item),
                        view_item_obj,
                        CObject(decision_node_decision_made),
                        add_to_shopping_cart_obj,
                        CObject(decision_node_proceed),
                        CObject(merge_node_view_shopping_cart),
                        view_shopping_cart_obj,
                        CObject(decision_node_done),
                        CObject(checkout_merge_node),
                        checkout_obj,
                        CObject(final_node_shopping_cart)])

named_classes_in_workflow_class_model = [c for c in workflow_node.get_connected_elements() if c.name is not None]
workflow_class_model = CBundle("workflow_class_model",
                               elements=named_classes_in_workflow_class_model)

shopping_trace_object_model = CBundle("shopping_trace_object_model",
                                      elements=a_trace)
shopping_trace_object_model_with_objects = CBundle("shopping_trace_object_model_with_objects",
                                                   elements=a_trace[0].get_connected_elements())


def run():
    print("***************** Shopping Activity Model 2: " +
          "Example combining object, class, and meta-del *****************")

    print('*** Plant UML Generation')
    generator = PlantUMLGenerator()
    generator.generate_class_models("workflow_class_model", [workflow_class_model, {}])
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models("shopping_trace_object_model", [shopping_trace_object_model, {},
                                                                     shopping_trace_object_model_with_objects, {}])


if __name__ == "__main__":
    run()
