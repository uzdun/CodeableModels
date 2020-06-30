.. _meta_modelling:

A first meta-model
******************

Defining a basic meta-model
===========================

Basic meta-modelling in Codeable Models is very similar to class modelling. Instead of :py:class:`.CClass`, used
to define classes, we use :py:class:`.CMetaclass` to define meta-classes.

As a first example of a meta-model, let us consider a simple meta-model for basic features of
activity meta-models defined in the folder ``metamodels`` of the Codeable Models distribution::

    activity_node = CMetaclass("Activity Node")
    control_node = CMetaclass("Control Node", superclasses=activity_node)
    initial_node = CMetaclass("Initial Node", superclasses=control_node)
    final_node = CMetaclass("Final Node", superclasses=control_node)
    activity_final_node = CMetaclass("Activity Final Node", superclasses=final_node)
    fork_node = CMetaclass("Fork Node", superclasses=control_node)
    join_node = CMetaclass("Join Node", superclasses=control_node)
    decision_node = CMetaclass("Decision Node", superclasses=control_node,
                               attributes={"decision": str})
    merge_node = CMetaclass("Merge Node", superclasses=control_node)
    action = CMetaclass("Action", superclasses=activity_node)
    accept_event_action = CMetaclass("Accept Event Action", superclasses=action)
    accept_time_event_action = CMetaclass("Accept Time Event Action",
                                          superclasses=accept_event_action,
                                          attributes={"description": str})
    send_signal_action = CMetaclass("Send Signal Action", superclasses=action)

    edge_relation = activity_node.association(activity_node, "next: [source] * -> [target] *")

Here, we first define a number of node types, which are needed to define an activity diagram. ``activity_node``
is the common superclass of all of them, and it has one association ``edge_relation`` to itself, defined
on the last line. ``edge_relation`` is used to define the directed links between nodes. Some of the nodes have
attributes, such as the ``decision_node``.

We can use the the Plant UML class model renderer to draw the resulting model. The result would be:

.. thumbnail:: images/activity_metamodel_all.png

This image has been rendered using the following code::

    activity_metamodel_all = CBundle("activity_metamodel_all",
                                     elements=activity_node.get_connected_elements(
                                     add_stereotypes=True))

    generator = PlantUMLGenerator()
    generator.generate_class_models("activityMetamodel", [activity_metamodel_all, {}])


Deriving a class model
======================

Next, let us create a class model with activities for filling a shopping cart based on the meta-model defined above.
Here are the classes needed for a model inspired by a model from
`uml-diagrams.org <https://www.uml-diagrams.org/online-shopping-uml-activity-diagram-example.html>`_. First we
define all required nodes::

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

Next we add all links that have no labels in one go::

    add_links({
        initial_node_shopping_cart: decision_node_search_browse,
        merge_node_search: search_item,
        merge_node_browse: browse_item,
        search_item: decision_node_found,
        browse_item: merge_node_view_item,
        merge_node_view_item: decision_node_search_browse,
        merge_node_view_item: view_item,
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

Finally, we add the links which have labels::

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

With this we have interconnected the class object with links based on the meta-class association. We thus can
use the object model renderer to create an object model with classes as instances and meta-classes as classifiers::

    shopping_activity_model = CBundle("shopping_activity_model",
                                      elements=initial_node_shopping_cart.class_object.get_connected_elements())
    generator = PlantUMLGenerator()
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models("shopping_activity_model", [shopping_activity_model, {}])

Please note that we need to compute the connected elements of the class object of one of the classes here,
not one of the classes, as we want to visualize the links of the class (object) not
its associations. That is, ``initial_node_shopping_cart.get_connected_elements()`` would
yield the class relations such as class associations, which we have not yet defined.

This creates the following model:

.. thumbnail:: images/shopping_activity_model.png


Introspecting the classes relations
===================================

A meta-class has various methods that can be used to introspect the ``classes`` relation that manages its instances.
First of all, the getter ``classes`` returns a list of all classes directly defined based on a meta-class.
``all_classes`` returns a list of all classes based on a meta-class, including those defined based on its
sub-classes::

    print(f"Activity node classes: {activity_node.classes!s}")
    print(f"Activity node all classes: {activity_node.all_classes!s}")

This would print something like:

.. code-block:: none

    Activity node classes: [<codeable_models.cclass.CClass object at 0x000001E3F490D148>: Search Items, <codeable_models.cclass.CClass object at 0x000001E3F490D948>: Browse Items, <codeable_models.cclass.CClass object at 0x000001E3F4910508>: View Item, <codeable_models.cclass.CClass object at 0x000001E3F4916848>: Add to Shopping Cart, <codeable_models.cclass.CClass object at 0x000001E3F4924048>: View Shopping Cart, <codeable_models.cclass.CClass object at 0x000001E3F4924648>: Update Shopping Cart, <codeable_models.cclass.CClass object at 0x000001E3F4924908>: Checkout]
    Activity node classes: [<codeable_models.cclass.CClass object at 0x000001E3F490D148>: Search Items, <codeable_models.cclass.CClass object at 0x000001E3F490D948>: Browse Items, <codeable_models.cclass.CClass object at 0x000001E3F4910508>: View Item, <codeable_models.cclass.CClass object at 0x000001E3F4916848>: Add to Shopping Cart, <codeable_models.cclass.CClass object at 0x000001E3F4924048>: View Shopping Cart, <codeable_models.cclass.CClass object at 0x000001E3F4924648>: Update Shopping Cart, <codeable_models.cclass.CClass object at 0x000001E3F4924908>: Checkout, <codeable_models.cclass.CClass object at 0x000001E3F490D308>, <codeable_models.cclass.CClass object at 0x000001E3F490D848>, <codeable_models.cclass.CClass object at 0x000001E3F490DDC8>, <codeable_models.cclass.CClass object at 0x000001E3F4916D48>, <codeable_models.cclass.CClass object at 0x000001E3F4924E88>, <codeable_models.cclass.CClass object at 0x000001E3F47DDB48>, <codeable_models.cclass.CClass object at 0x000001E3F4924BC8>, <codeable_models.cclass.CClass object at 0x000001E3F486BF08>, <codeable_models.cclass.CClass object at 0x000001E3F490DB88>, <codeable_models.cclass.CClass object at 0x000001E3F4910048>, <codeable_models.cclass.CClass object at 0x000001E3F4916A48>, <codeable_models.cclass.CClass object at 0x000001E3F4924348>, <codeable_models.cclass.CClass object at 0x000001E3F49271C8>: Check Shopping Cart, <codeable_models.cclass.CClass object at 0x000001E3F4927488>: Proceed to Checkout]

In addition, ``get_classes(name)`` gets all classes directly derived from this meta-class that have the specified name,
and ``get_class(name)`` gets a class directly derived from this meta-class that has the specified name.

Changing the classes relations
==============================

Classes can be added or removed from a meta-class. For example, with ``remove_class(class)`` we can remove one
class from the meta-class, and then we can add  a maybe different class with ``add_class(class)``.



The full code of the examples in this tutorial can be found in the sample :ref:`shopping_activity_model1`.