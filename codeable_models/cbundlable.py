from codeable_models.cexception import CException
from codeable_models.cnamedelement import CNamedElement
from codeable_models.internal.commons import set_keyword_args, check_named_element_is_not_deleted, is_cbundle, \
    is_cmetaclass, is_cstereotype, is_cbundlable, is_cassociation, is_cclass, is_cobject, is_clink


class CBundlable(CNamedElement):
    def __init__(self, name, **kwargs):
        self.bundles_ = []
        super().__init__(name, **kwargs)

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.append("bundles")
        super()._init_keyword_args(legal_keyword_args, **kwargs)

    @property
    def bundles(self):
        return list(self.bundles_)

    @bundles.setter
    def bundles(self, bundles):
        if bundles is None:
            bundles = []
        for b in self.bundles_:
            b.remove(self)
        self.bundles_ = []
        if is_cbundle(bundles):
            bundles = [bundles]
        elif not isinstance(bundles, list):
            raise CException(f"bundles requires a list of bundles or a bundle as input")
        for b in bundles:
            if not is_cbundle(b):
                raise CException(f"bundles requires a list of bundles or a bundle as input")
            check_named_element_is_not_deleted(b)
            if b in self.bundles_:
                raise CException(f"'{b.name!s}' is already a bundle of '{self.name!s}'")
            self.bundles_.append(b)
            b.elements_.append(self)

    def delete(self):
        if self.is_deleted:
            return
        bundles_to_delete = list(self.bundles_)
        for b in bundles_to_delete:
            b.remove(self)
        self.bundles_ = []
        super().delete()

    def get_connected_elements(self, **kwargs):
        context = ConnectedElementsContext()

        allowed_keyword_args = ["add_bundles", "process_bundles", "stop_elements_inclusive",
                                "stop_elements_exclusive"]
        if is_cmetaclass(self) or is_cbundle(self) or is_cstereotype(self):
            allowed_keyword_args = ["add_stereotypes", "process_stereotypes"] + allowed_keyword_args
        if is_cmetaclass(self) or is_cclass(self) or is_cassociation(self):
            allowed_keyword_args = ["add_associations"] + allowed_keyword_args
        if is_cobject(self) or is_clink(self):
            allowed_keyword_args = ["add_links"] + allowed_keyword_args

        set_keyword_args(context, allowed_keyword_args, **kwargs)

        if self in context.stop_elements_exclusive:
            return []
        context.elements.append(self)
        self.compute_connected_(context)
        if not context.add_bundles:
            context.elements = [elt for elt in context.elements if not is_cbundle(elt)]
        if not context.add_stereotypes:
            context.elements = [elt for elt in context.elements if not is_cstereotype(elt)]
        if not context.add_associations:
            context.elements = [elt for elt in context.elements if not is_cassociation(elt)]
        if not context.add_links:
            context.elements = [elt for elt in context.elements if not is_clink(elt)]
        return context.elements

    @staticmethod
    def append_connected_(context, connected):
        for c in connected:
            if c not in context.elements:
                context.elements.append(c)
                if c not in context.all_stop_elements:
                    c.compute_connected_(context)

    def compute_connected_(self, context):
        connected = []
        for bundle in self.bundles_:
            if bundle not in context.stop_elements_exclusive:
                connected.append(bundle)
        self.append_connected_(context, connected)


class ConnectedElementsContext(object):
    def __init__(self):
        self.elements = []
        self.add_bundles = False
        self.add_associations = False
        self.add_links = False
        self.add_stereotypes = False
        self.process_bundles = False
        self.process_stereotypes = False
        self._stop_elements_inclusive = []
        self._stop_elements_exclusive = []
        self.all_stop_elements = []

    @property
    def stop_elements_inclusive(self):
        return list(self._stop_elements_inclusive)

    @stop_elements_inclusive.setter
    def stop_elements_inclusive(self, stop_elements_inclusive):
        if is_cbundlable(stop_elements_inclusive):
            stop_elements_inclusive = [stop_elements_inclusive]
        if not isinstance(stop_elements_inclusive, list):
            raise CException(f"expected one element or a list of stop elements, but got: '{stop_elements_inclusive!s}'")
        for e in stop_elements_inclusive:
            if not is_cbundlable(e):
                raise CException(f"expected one element or a list of stop elements, but got: " +
                                 f"'{stop_elements_inclusive!s}' with element of wrong type: '{e!s}'")
        self._stop_elements_inclusive = stop_elements_inclusive
        self.all_stop_elements = self._stop_elements_inclusive + self._stop_elements_exclusive

    @property
    def stop_elements_exclusive(self):
        return list(self._stop_elements_exclusive)

    @stop_elements_exclusive.setter
    def stop_elements_exclusive(self, stop_elements_exclusive):
        if is_cbundlable(stop_elements_exclusive):
            stop_elements_exclusive = [stop_elements_exclusive]
        if not isinstance(stop_elements_exclusive, list):
            raise CException(f"expected a list of stop elements, but got: '{stop_elements_exclusive!s}'")
        for e in stop_elements_exclusive:
            if not is_cbundlable(e):
                raise CException(f"expected a list of stop elements, but got: '{stop_elements_exclusive!s}'" +
                                 f" with element of wrong type: '{e!s}'")
        self._stop_elements_exclusive = stop_elements_exclusive
        self.all_stop_elements = self._stop_elements_inclusive + self._stop_elements_exclusive
