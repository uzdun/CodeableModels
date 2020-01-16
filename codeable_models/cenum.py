from codeable_models.cbundlable import CBundlable
from codeable_models.cexception import CException


class CEnum(CBundlable):
    def __init__(self, name=None, **kwargs):
        self.values_ = []
        super().__init__(name, **kwargs)

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.append("values")
        super()._init_keyword_args(legal_keyword_args, **kwargs)

    @property
    def values(self):
        return list(self.values_)

    @values.setter
    def values(self, values):
        if values is None:
            values = []
        if not isinstance(values, list):
            raise CException(f"an enum needs to be initialized with a list of values, but got: '{values!s}'")
        self.values_ = values

    def is_legal_value(self, value):
        if value in self.values_:
            return True
        return False

    def delete(self):
        if self.is_deleted:
            return
        self.values_ = []
        super().delete()
