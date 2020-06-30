"""
*File Name:* samples/shopping_instance1.py

This is a Codeable Models object model example based on the previous class model samples.
It uses the class model in  :ref:`shopping_model4`.

The example is explained in :ref:`first_object_model`.
"""

from codeable_models import CBundle, CObject, add_links, delete_links
from lib.standard_types import today
from plant_uml_renderer import PlantUMLGenerator
from samples.shopping_model4 import address, cart, customer, product, item, item_product_relation, \
    order_item_relation, order, customer_orders_relation, staff_member, staff_reports_to_relation

thomas_home_address = CObject(address, "Thomas Home Address", values={
    "street1": "Waehringer Strasse 29",
    "street2": "",
    "zip": "1090",
    "city": "Vienna",
    "state": "Vienna",
    "country": "Austria"
})

thomas_customer = CObject(customer, "Thomas Customer", values={
    "id": "C001",
    "first name": "Thomas",
    "last name": "Test",
    "address": thomas_home_address,
    "email": "thomas.test@thomastest.com",
    "phone": "+43111111222333",
    "shipping addresses": [thomas_home_address]
})

basic_pen = CObject(product, values={"id": "P001", "name": "Basic Pen", "price": 1.50})
premium_pen = CObject(product, values={"id": "P001", "name": "Premium Pen", "price": 2.50})
basic_paper = CObject(product, values={"id": "P001", "name": "Basic Paper", "price": 2.75})
premium_paper = CObject(product, values={"id": "P001", "name": "Premium Paper", "price": 5.50})

cart1 = CObject(cart, "Thomas Cart")
# add links can optionally specify the association.
# cart1.add_links(thomas_customer, association=customer_cart_relation)
cart1.add_links(thomas_customer)

item1 = CObject(item, "Premium Paper Item", values={
    "quantity": 2,
    "price": 11.00
})
item1.add_links(premium_paper, association=item_product_relation)
item2 = CObject(item, "Basic Pen Item", values={
    "quantity": 1,
    "price": 1.50
})
item2.add_links(basic_pen, role_name="product")

add_links({cart1: [item1, item2]}, role_name="item in cart")

order1 = CObject(order, values={
    "id": "O001",
    "ship to": thomas_home_address,
    "total": 12.50
})
order1.add_links(thomas_customer, association=customer_orders_relation)
order1.add_links([item1, item2], association=order_item_relation)

manager = CObject(staff_member, values={
    "id": "S001",
    "first name": "Marie",
    "last name": "Schneider",
    "role": "Management"
})
crm1 = CObject(staff_member, values={
    "id": "S002",
    "first name": "Joe",
    "last name": "Lang",
    "role": "Customer Support"
})
crm2 = CObject(staff_member, values={
    "id": "S003",
    "first name": "Fei",
    "last name": "Wong",
    "role": "Customer Support"
})

# wrong way to specify the association of the links using 'association'; the direction is unclear.
# this is used below in the "wrong" staff model
# add_links({manager: [crm1, crm2]}, association=staff_reports_to_relation)
add_links({manager: [crm1, crm2]}, role_name="managed")

shopping_instance1_order_model = CBundle("shopping_instance1_order_model",
                                         elements=(order1.get_connected_elements() +
                                                   [thomas_home_address, today]))
shopping_instance1_staff_model = CBundle("shopping_instance1_staff_model",
                                         elements=manager.get_connected_elements())


def print_attribute_getting_setting_examples():
    print(f"Values of basic pen: {basic_pen.values!s}")
    basic_pen.values = {'name': 'Basic Pen', 'price': 1.75, 'id': 'P015'}
    print(f"New values of basic pen: {basic_pen.values!s}")

    print(f"Old basic pen item price: {item2.get_value('price')!s}, old order total: {order1.get_value('total')!s}")
    item2.set_value("price", 1.75)
    order1.set_value("total", 12.75)
    print(f"New basic pen price: {item2.get_value('price')!s}, new order total: {order1.get_value('total')!s}")
    print()


def print_link_introspection_examples():
    print(f"object {order1!r}")

    print("\nItem 2 Links:")
    for link in item2.links:
        print(str(link))

    print("\nItem 2 Links:")
    for link in item2.links:
        print(repr(link))

    print("\nItem 2 Links:")

    for link in item2.links:
        source_str = str(link.source)
        if link.source.instance_of(order):
            source_str = "Order " + link.source.get_value("id")
        target_str = str(link.target)
        if link.target.instance_of(product):
            target_str = "Product " + link.target.get_value("name")
        print(f"Link: {source_str} -> {target_str}")

    print("\nOrder 1 - Item Links:")

    for link in order1.get_links_for_association(order_item_relation):
        print(f"Link: Order {link.source.get_value('id')} -> {link.target!s}")

    print("\nItem 2 Linked:")
    for linked in item2.linked:
        print(repr(linked))

    print("\nOrder 1 - Linked Item:")

    for linked in order1.get_linked(association=order_item_relation):
        print(f"Order Item: {linked!s}")


def run():
    print("***************** Shopping Model Instance Model 1 (Using Shopping Model 4) *****************")

    print("*** Attribute Getting / Setting")
    print_attribute_getting_setting_examples()

    print("*** Link Introspection")
    print_link_introspection_examples()

    print('*** Plant UML Generation')
    generator = PlantUMLGenerator()
    generator.generate_object_models("shopping_instance1",
                                     [shopping_instance1_order_model,
                                      {"render_association_names_when_no_label_is_given": True},
                                      shopping_instance1_staff_model,
                                      {"render_association_names_when_no_label_is_given": True}])

    # change links to generate the "wrong" staff model as well
    delete_links({manager: [crm1, crm2]})
    add_links({manager: [crm1, crm2]}, association=staff_reports_to_relation)

    shopping_instance1_staff_model.name = shopping_instance1_staff_model.name + "_wrong"
    generator.generate_object_models("shopping_instance1",
                                     [shopping_instance1_staff_model,
                                      {"render_association_names_when_no_label_is_given": True}])

    # correct the links again
    delete_links({manager: [crm1, crm2]})
    add_links({manager: [crm1, crm2]}, role_name="managed")

    print(f"... Generated models in {generator.directory!s}/shopping_instance1")


if __name__ == "__main__":
    run()
