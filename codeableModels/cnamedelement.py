from codeableModels.internal.commons import setKeywordArgs, checkNamedElementIsNotDeleted
from codeableModels.cexception import CException

class CNamedElement(object):
    def __init__(self, name, **kwargs):
        self.name = name
        super().__init__()
        self._isDeleted = False
        if name != None and not isinstance(name, str):
            raise CException(f"is not a name string: '{name!r}'")
        self._initKeywordArgs(**kwargs)

    def __str__(self):
        if (self.name == None):
            return ""
        return self.name
    def __repr__(self):
        result = super().__repr__()
        if (self.name != None):
            result = f"{result}: {self.name!s}"
        return result

    def _initKeywordArgs(self, legalKeywordArgs = None, **kwargs):
        if legalKeywordArgs == None:
            legalKeywordArgs = []
        setKeywordArgs(self, legalKeywordArgs, **kwargs)

    def delete(self):
        if self._isDeleted == True:
            return
        self.name = None
        self._isDeleted = True




