"""
*File Name:* samples/shopping_model1.py

This is a Codeable Models example realizing a simple sample shopping domain model.
It is inspired by the model at:
`<https://www.uml-diagrams.org/examples/online-shopping-domain-uml-diagram-example.html>`_

The example is explained in :ref:`first_class_model`.

"""
from codeable_models import CClass, CBundle
from plant_uml_renderer import PlantUMLGenerator
from metamodels.domain_metamodel import domain_metaclass

cart = CClass(domain_metaclass, "Cart")

item = CClass(domain_metaclass, "Item", attributes={
    "quantity": int,
    "price": float
})

product = CClass(domain_metaclass, "Product", attributes={
    "id": str,
    "name": str,
    "price": float
})

cart_item_relation = cart.association(item, "in cart: [cart] 0..1 -> [item in cart] *")
#
# Alternative way to write the cart-item association
# cart.association(item, name="in cart", role_name="item in cart", multiplicity="*",
#                  source_role_name="cart", source_multiplicity="0..1")

item_product_relation = item.association(product, "product definition: [cart item] * -> [product] 1")

shopping_model = CBundle("shopping_model1", elements=cart.get_connected_elements())


def run():
    print("***************** Shopping Model Example 1 *****************")
    print('*** Plant UML Generation')
    generator = PlantUMLGenerator()
    generator.generate_class_models(shopping_model.name, [shopping_model, {}])
    print(f"... Generated models in {generator.directory!s}/{shopping_model.name!s}")


if __name__ == "__main__":
    run()
