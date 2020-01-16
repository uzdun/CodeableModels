from codeable_models.cexception import CException
from codeable_models.internal.commons import set_keyword_args


class CNamedElement(object):
    def __init__(self, name, **kwargs):
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
        if self.is_deleted:
            return
        self.name = None
        self.is_deleted = True
