from codeable_models.cbundlable import CBundlable
from codeable_models.cexception import CException


class CEnum(CBundlable):
    def __init__(self, name=None, **kwargs):
        """``CEnum`` is used for defining enumerations.

        **Superclasses:**  :py:class:`.CBundlable`

        Args:
           name (str): An optional name.
           **kwargs: Pass in any kwargs acceptable to superclasses. In addition, ``CEnum`` accepts:
                ``values``.

                - The ``values`` kwarg accepts a list of string enumeration values in the form acceptable
                  to the ``attributes`` property.

        **Example:** The following defines an enumeration with 4 values and then prints all the values
        with the ``values`` getter::

            player_state = CEnum("Player State", values=["Walk", "Run", "Attack", "Roll"])

            print(f"player states: {player_state.values!s}")

        Another example is provided in the document :ref:`class_attributes`.

        """
        self.values_ = []
        super().__init__(name, **kwargs)

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = []
        legal_keyword_args.append("values")
        super()._init_keyword_args(legal_keyword_args, **kwargs)

    @property
    def values(self):
        """list[str]: Gets or sets the enumeration values.
        """
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
        """Deletes the enumeration. Calls ``delete()`` on superclass.

        Returns:
            None
        """
        if self.is_deleted:
            return
        self.values_ = []
        super().delete()
