from codeableModels.cbundlable import CBundlable
from codeableModels.internal.commons import setKeywordArgs
from codeableModels.cexception import CException

class CEnum(CBundlable):
    def __init__(self, name = None, **kwargs):
        self._values = []
        super().__init__(name, **kwargs)

    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = [] 
        legalKeywordArgs.append("values")
        super()._initKeywordArgs(legalKeywordArgs, **kwargs)

    @property
    def values(self):
        return list(self._values)
    
    @values.setter
    def values(self, values):
        if values == None:
            values = []
        if not isinstance(values, list):
            raise CException(f"an enum needs to be initialized with a list of values, but got: '{values!s}'")
        self._values = values

    def isLegalValue(self, value):
        if value in self._values:
            return True
        return False

    def delete(self):
        if self._isDeleted == True:
            return
        self._values = []
        super().delete()