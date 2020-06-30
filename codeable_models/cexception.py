class CException(Exception):
    def __init__(self, value):
        """
        ``CException`` is a Python ``Exception`` that signals that an Exception is raised in Codeable Models.
        This type of exception is raised in all Codeable Models classes whenever an exception occurs.

        Args:
           value (str): An optional name.
        """
        self.value = value

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return repr(self.value)
