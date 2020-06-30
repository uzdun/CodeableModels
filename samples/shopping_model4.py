"""
*File Name:* samples/shopping_model4.py

This is a Codeable Models example realizing a simple sample shopping domain model.
This is a cleaned-up version of the previous class models :ref:`shopping_model1`, :ref:`shopping_model2`,
and :ref:`shopping_model3` which uses coded model features. Those parts are explained in :ref:`coded_model`.

The model is inspired by the model at:
`<https://www.uml-diagrams.org/examples/online-shopping-domain-uml-diagram-example.html>`_

"""

from codeable_models import CClass, CEnum, CObject, CAttribute, CAssociation, add_links
from lib.standard_types import today, date
from metamodels.domain_metamodel import domain_metaclass

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
item_product_relation = item.association(product, "product: [cart item] * -> [product] 1")

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
    "selected shipping address": 0
})

customer_cart_relation = customer.association(cart, "shops with: [customer] 1 <*>- [cart] 1")
customer_orders_relation = customer.association(order, "orders: [customer] 1 <*>- [order] *")

staff_role = CEnum("Staff Role", values=["Customer Support", "Management", "IT Support", "Payment Processing"])

staff_member = CClass(domain_metaclass, "Staff Member", superclasses=person, attributes={
    "id": str,
    "role": staff_role,
})
staff_reports_to_relation = staff_member.association(staff_member, "reports to: [managed] * -> [manager] *")

staff_customer = CClass(domain_metaclass, "Staff Customer", superclasses=[staff_member, customer])


def add_items_to_cart(a_cart, items_list):
    items = []
    for element in items_list:
        item_product = element[0]
        item_quantity = element[1]
        price = item_product.get_value("price") * item_quantity
        new_item = CObject(item, values={
            "quantity": item_quantity,
            "price": price
        })
        new_item.add_links(item_product, role_name="product")
        items.append(new_item)
        a_cart.add_links(new_item, role_name="item in cart")
    return items


_order_id_counter = 0


def get_order_id():
    global _order_id_counter
    _order_id_counter += 1
    return "O" + "{:07d}".format(_order_id_counter)


_customer_id_counter = 0


def get_customer_id():
    global _customer_id_counter
    _customer_id_counter += 1
    return "C" + "{:07d}".format(_customer_id_counter)


_staff_id_counter = 0


def get_staff_id():
    global _staff_id_counter
    _staff_id_counter += 1
    return "S" + "{:07d}".format(_staff_id_counter)


_product_id_counter = 0


def get_product_id():
    global _product_id_counter
    _product_id_counter += 1
    return "P" + "{:07d}".format(_product_id_counter)


def calc_cart_total(a_cart):
    total = 0
    items = a_cart.get_linked(role_name="item in cart")
    for item_in_cart in items:
        total += item_in_cart.get_value("price")
    return total


def get_shipping_address(a_customer):
    shipping_addresses = a_customer.get_value("shipping addresses")
    return shipping_addresses[a_customer.get_value("selected shipping address")]


def place_order(a_cart):
    a_customer = a_cart.get_linked(role_name="customer")[0]

    # this assumes "today" is set to the current date and thus we
    # can just use the default value for those values.
    new_order = CObject(order, values={
        "id": get_order_id(),
        "ship to": get_shipping_address(a_customer),
        "total": calc_cart_total(a_cart)
    })

    items = a_cart.get_linked(role_name="item in cart")
    add_links({new_order: items}, role_name="item in order")
    add_links({a_customer: new_order}, role_name="order")

    return new_order


def ship_order(an_order):
    an_order.set_value("shipped", today)
    an_order.set_value("status", "Shipped")


def new_product(name=None, **kwargs):
    a_product = CObject(product, name, **kwargs)
    a_product.set_value("id", get_product_id())
    return a_product


def new_customer(name=None, **kwargs):
    a_customer = CObject(customer, name, **kwargs)
    a_customer.set_value("id", get_customer_id())
    return a_customer
