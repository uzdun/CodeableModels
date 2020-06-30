"""
*File Name:* samples/shopping_model3.py

This is a Codeable Models example realizing a simple sample shopping domain model focusing on
class relationships.
It is inspired by the model at:
`<https://www.uml-diagrams.org/examples/online-shopping-domain-uml-diagram-example.html>`_

The example is explained in :ref:`class_relationships`.
"""

from codeable_models import CClass, CBundle, CEnum, CObject, CAttribute, CAssociation
from plant_uml_renderer import PlantUMLGenerator
from metamodels.domain_metamodel import domain_metaclass

date = CClass(domain_metaclass, "Date", attributes={
    "day": int,
    "month": int,
    "year": int
})
today = CObject(date, "today", values={
    "day": 1,
    "month": 5,
    "year": 20
})

address = CClass(domain_metaclass, "Address", attributes={
    "street1": str,
    "street2": str,
    "zip": str,
    "city": str,
    "state": str,
    "country": str
})

cart = CClass(domain_metaclass, "Cart")

item = CClass(domain_metaclass, "Item", attributes={
    "quantity": int,
    "price": float
})

product = CClass(domain_metaclass, "Product", attributes={
    "id": str,
    "name": "",
    "price": 0.0
})

cart_item_relation = cart.association(item, "in cart: [cart] 1 -> [item in cart] *")
item_product_relation = item.association(product, "product definition: [cart item] * -> [product] 1")

order_status = CEnum("Order Status", values=["New", "Hold", "Shipped", "Delivered"])

order = CClass(domain_metaclass, "Order", attributes={
    "id": str,
    "ordered": today,
    "shipped": date,
    "ship to": address,
    "status": CAttribute(type=order_status, default="New"),
    "total": float
})

order_item_relation = CAssociation(order, item, "in order: [order] 1 -> [item in order] *")

person = CClass(domain_metaclass, "Person", attributes={
    "first name": str,
    "last name": str,
    "address": address,
    "email": str,
    "phone": str
})

customer = CClass(domain_metaclass, "Customer", superclasses=person, attributes={
    "id": str,
    "shipping addresses": [],
})

customer_cart_relation = customer.association(cart, "shops with: [customer] 1 <*>- [cart] 1")
customer_orders_relation = customer.association(order, "orders: [customer] 1 <*>- [orders] *")

staff_role = CEnum("Staff Role", values=["Customer Support", "Management", "IT Support", "Payment Processing"])

staff_member = CClass(domain_metaclass, "Staff Member", superclasses=person, attributes={
    "id": str,
    "role": staff_role,
})
staff_reports_to_relation = staff_member.association(staff_member, "reports to: [managed] * -> [manager] *")

staff_customer = CClass(domain_metaclass, "Staff Customer", superclasses=[staff_member, customer])

shopping_model_all = CBundle("shopping_model3_all", elements=cart.get_connected_elements() + [order_status, staff_role])
shopping_model_persons = CBundle("shopping_model3_persons",
                                 elements=[person, customer, staff_member, staff_customer, staff_role])
shopping_model_orders = CBundle("shopping_model3_orders",
                                elements=(order.get_connected_elements(stop_elements_inclusive=[customer]) +
                                          [order_status]))


# Association Introspection
def print_association_introspection_examples():
    print("Order associations")
    for association in order.associations:
        print(f"SOURCE = {association.source!s} -> TARGET = {association.target!s}")
    print()

    print("Classes associated to order:")
    for association in order.associations:
        print(f"- {association.get_opposite_classifier(order)!s}")
    print()


# Class Introspection
def print_class_introspection_examples():
    print("Direct superclasses of Staff Customer? " +
          f"{[c.name for c in staff_customer.superclasses]!s}")
    print("All superclasses of Staff Customer? " +
          f"{[c.name for c in staff_customer.all_superclasses]!s}")
    print("Is Staff Customer of type Person? " +
          f"{staff_customer.is_classifier_of_type(person)!s}")
    print("Is Staff Customer of type Staff Customer? " +
          f"{staff_customer.is_classifier_of_type(staff_customer)!s}")
    print("Has Staff Customer superclass Person? " +
          f"{staff_customer.has_superclass(person)!s}")
    print("Has Staff Customer superclass Staff Customer? " +
          f"{staff_customer.has_superclass(staff_customer)!s}")
    print("What is the class path of Staff Customer? " +
          f"{[c.name for c in staff_customer.class_path]!s}")
    print()


def run():
    print("***************** Shopping Model Example 3 *****************")

    print("*** Association introspection")
    print_association_introspection_examples()

    print("*** Class introspection\n")
    print_class_introspection_examples()

    print('*** Plant UML Generation')
    generator = PlantUMLGenerator()
    generator.generate_class_models("shopping_model3", [shopping_model_all, {},
                                                        shopping_model_persons, {},
                                                        shopping_model_orders, {}])
    print(f"... Generated models in {generator.directory!s}/shopping_model3")


if __name__ == "__main__":
    run()
