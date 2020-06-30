from codeable_models.cexception import CException
from codeable_models.internal.commons import set_keyword_args


class CNamedElement(object):
    def __init__(self, name, **kwargs):
        """CNamedElement is the superclass for all named elements in Codeable Models, such as CClass, CObject, and
        so on. The class is usually not used directly.

        When it is reached in the inheritance hierarchy, it sets all keyword args contained in ``kwargs``.
        This is performed using the ``set_keyword_args()`` method, to be defined by subclasses.
        Calling it with keyword args that are not specified as legal keyword args (to be done in subclasses, in the
        ``legal_keyword_args`` list), causes an exception.

        For example, ``CClassifier`` adds ``superclasses`` and ``attributes`` to the legal keyword args, which
        can then be used on ``CClassifier`` and subclasses such as ``CClass``::

            CClass(domain_metaclass, "Item", attributes={
                "quantity": int,
                "price": float
            })

        Args:
           name (str): An optional name.
           **kwargs: Accepts keyword args defined as ``legal_keyword_args`` by subclasses.

        Attributes:
            name (str): The name of the entity. Can be ``None``.
        """
        self.name = name
        super().__init__()
        self.is_deleted = False
        if name is not None and not isinstance(name, str):
            raise CException(f"is not a name string: '{name!r}'")
        self._init_keyword_args(**kwargs)

    def __str__(self):
        if self.name is None:
            return ""
        return self.name

    def __repr__(self):
        result = super().__repr__()
        if self.name is not None:
            result = f"{result}: {self.name!s}"
        return result

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        set_keyword_args(self, legal_keyword_args, **kwargs)

    def delete(self):
        """Delete the named element.

        Returns:
            None
        """
        if self.is_deleted:
            return
        self.name = None
        self.is_deleted = True
