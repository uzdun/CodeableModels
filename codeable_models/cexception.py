class CException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return repr(self.value)
