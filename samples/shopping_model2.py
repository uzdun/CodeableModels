"""
*File Name:* samples/shopping_model2.py

This is a Codeable Models example realizing a simple sample shopping domain model focusing on
class attributes.
It is inspired by the model at:
`<https://www.uml-diagrams.org/examples/online-shopping-domain-uml-diagram-example.html>`_

The example is explained in :ref:`class_attributes`.
"""

from codeable_models import CClass, CBundle, CEnum, CObject, CAttribute
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

#
# Option to define Order->status with the type, not a default value, as done below
#
# order = CClass(domain_metaclass, "Order", attributes={
#     "id": str,
#     "ordered": date,
#     "shipped": date,
#     "ship to": address,
#     "status": order_status,
#     "total": float
# })
order = CClass(domain_metaclass, "Order", attributes={
    "id": str,
    "ordered": today,
    "shipped": date,
    "ship to": address,
    "status": CAttribute(type=order_status, default="New"),
    "total": float
})

order_item_relation = order.association(item, "in order: [order] 1 -> [item in order] *")

shopping_model = CBundle("shopping_model2", elements=cart.get_connected_elements() + [order_status])


# Attribute Introspection
def print_attribute_introspection_examples():
    print('Product Attributes:')
    for attribute in product.attributes:
        print(
            '- "%s": type "%s", classifier "%s", default "%s"' % (attribute.name, attribute.type, attribute.classifier,
                                                                  attribute.default))

    print('Product Attributes: %s' % product.attribute_names)
    print('Default for price attribute = %s' % product.get_attribute("price").default)

    print('Order Attributes:')
    for attribute in order.attributes:
        print(
            '- "%s": type "%s", classifier "%s", default "%s"' % (attribute.name, attribute.type, attribute.classifier,
                                                                  attribute.default))
    print()


def run():
    print("***************** Shopping Model Example 2 *****************")
    print('*** Attribute introspection examples')
    print_attribute_introspection_examples()

    print('*** Plant UML Generation')
    generator = PlantUMLGenerator()
    generator.generate_class_models(shopping_model.name, [shopping_model, {}])
    print(f"... Generated models in {generator.directory!s}/{shopping_model.name!s}")


if __name__ == "__main__":
    run()
