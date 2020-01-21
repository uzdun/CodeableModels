import nose
from nose.tools import ok_, eq_

from codeable_models import CBundle, CMetaclass, CClass, CException, CLayer, CPackage
from tests.testing_commons import exception_expected_


class TestBundles:
    def setup(self):
        self.mcl = CMetaclass("MCL")
        self.b1 = CBundle("B1")

    def test_bundle_name_fail(self):
        try:
            CBundle(self.mcl)
            exception_expected_()
        except CException as e:
            ok_(e.value.startswith("is not a name string: '"))
            ok_(e.value.endswith(" MCL'"))

    def test_get_elements_wrong_kw_arg(self):
        try:
            self.b1.get_elements(x=CBundle)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown argument to getElements: 'x'")

    def test_get_element_wrong_kw_arg(self):
        try:
            self.b1.get_element(x=CBundle)
            exception_expected_()
        except CException as e:
            eq_(e.value, "unknown argument to getElements: 'x'")

    def test_package_and_layer_subclasses(self):
        layer1 = CLayer("L1")
        layer2 = CLayer("L2", sub_layer=layer1)
        package1 = CPackage("P1")
        c1 = CClass(self.mcl, "C1")
        c2 = CClass(self.mcl, "C2")
        c3 = CClass(self.mcl, "C3")
        layer1.elements = [c1, c2]
        layer2.elements = [c3]
        package1.elements = [layer1, layer2] + layer1.elements + layer2.elements
        eq_(set(package1.elements), {layer1, layer2, c1, c2, c3})
        eq_(set(layer1.elements), {c1, c2})
        eq_(set(layer2.elements), {c3})
        eq_(set(c1.bundles), {layer1, package1})
        eq_(set(c2.bundles), {layer1, package1})
        eq_(set(c3.bundles), {layer2, package1})

    def test_layer_sub_layers(self):
        layer1 = CLayer("L1")
        eq_(layer1.super_layer, None)
        eq_(layer1.sub_layer, None)

        layer1 = CLayer("L1", sub_layer=None)
        eq_(layer1.super_layer, None)
        eq_(layer1.sub_layer, None)

        layer2 = CLayer("L2", sub_layer=layer1)
        eq_(layer1.super_layer, layer2)
        eq_(layer1.sub_layer, None)
        eq_(layer2.super_layer, None)
        eq_(layer2.sub_layer, layer1)

        layer3 = CLayer("L3", sub_layer=layer1)
        eq_(layer1.super_layer, layer3)
        eq_(layer1.sub_layer, None)
        eq_(layer2.super_layer, None)
        eq_(layer2.sub_layer, None)
        eq_(layer3.super_layer, None)
        eq_(layer3.sub_layer, layer1)

        layer3.sub_layer = layer2
        eq_(layer1.super_layer, None)
        eq_(layer1.sub_layer, None)
        eq_(layer2.super_layer, layer3)
        eq_(layer2.sub_layer, None)
        eq_(layer3.super_layer, None)
        eq_(layer3.sub_layer, layer2)

        layer2.sub_layer = layer1
        eq_(layer1.super_layer, layer2)
        eq_(layer1.sub_layer, None)
        eq_(layer2.super_layer, layer3)
        eq_(layer2.sub_layer, layer1)
        eq_(layer3.super_layer, None)
        eq_(layer3.sub_layer, layer2)

    def test_layer_super_layers(self):
        layer1 = CLayer("L1")
        eq_(layer1.super_layer, None)
        eq_(layer1.sub_layer, None)

        layer1 = CLayer("L1", super_layer=None)
        eq_(layer1.super_layer, None)
        eq_(layer1.sub_layer, None)

        layer2 = CLayer("L2", super_layer=layer1)
        eq_(layer1.super_layer, None)
        eq_(layer1.sub_layer, layer2)
        eq_(layer2.super_layer, layer1)
        eq_(layer2.sub_layer, None)

        layer3 = CLayer("L3", super_layer=layer1)
        eq_(layer1.super_layer, None)
        eq_(layer1.sub_layer, layer3)
        eq_(layer2.super_layer, None)
        eq_(layer2.sub_layer, None)
        eq_(layer3.super_layer, layer1)
        eq_(layer3.sub_layer, None)

        layer3.super_layer = layer2
        eq_(layer1.super_layer, None)
        eq_(layer1.sub_layer, None)
        eq_(layer2.super_layer, None)
        eq_(layer2.sub_layer, layer3)
        eq_(layer3.super_layer, layer2)
        eq_(layer3.sub_layer, None)

        layer2.super_layer = layer1
        eq_(layer1.super_layer, None)
        eq_(layer1.sub_layer, layer2)
        eq_(layer2.super_layer, layer1)
        eq_(layer2.sub_layer, layer3)
        eq_(layer3.super_layer, layer2)
        eq_(layer3.sub_layer, None)


if __name__ == "__main__":
    nose.main()
