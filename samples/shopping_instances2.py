"""
*File Name:* samples/shopping_instance2.py

This is a Codeable Models object model example based on the previous class model samples.
It uses the class model in  :ref:`shopping_model4`. Compared to the previous sample
:ref:`shopping_instances1` it improve the model building through code.

The example is explained in :ref:`coded_model`.
"""

from codeable_models import CBundle, CObject
from lib.standard_types import today
from plant_uml_renderer import PlantUMLGenerator
from samples.shopping_model4 import address, cart, add_items_to_cart, place_order, \
    customer_cart_relation, new_product, new_customer, ship_order

thomas_home_address = CObject(address, "Thomas Home Address", values={
    "street1": "Waehringer Strasse 29",
    "street2": "",
    "zip": "1090",
    "city": "Vienna",
    "state": "Vienna",
    "country": "Austria"
})

thomas_customer = new_customer("Thomas Customer", values={
    "first name": "Thomas",
    "last name": "Test",
    "address": thomas_home_address,
    "email": "thomas.test@thomastest.com",
    "phone": "+43111111222333",
    "shipping addresses": [thomas_home_address]
})

basic_pen = new_product(values={"name": "Basic Pen", "price": 1.50})
premium_pen = new_product(values={"name": "Premium Pen", "price": 2.50})
basic_paper = new_product(values={"name": "Basic Paper", "price": 2.75})
premium_paper = new_product(values={"name": "Premium Paper", "price": 5.50})

cart1 = CObject(cart)
add_items_to_cart(cart1, [[premium_paper, 2], [basic_paper, 1], [premium_pen, 3]])
cart1.add_links(thomas_customer, association=customer_cart_relation)

order1 = place_order(cart1)
ship_order(order1)

shopping_instance2_all = CBundle("shopping_instance2_all", elements=(order1.get_connected_elements() +
                                                                     [thomas_home_address, today]))


def run():
    print("***************** Shopping Model Instance Model 1 (Using Shopping Model 4) *****************")
    print('*** Plant UML Generation')
    generator = PlantUMLGenerator()
    generator.generate_object_models("shopping_instance2", [shopping_instance2_all, {}])
    print(f"... Generated models in {generator.directory!s}/shopping_instance2")


if __name__ == "__main__":
    run()
