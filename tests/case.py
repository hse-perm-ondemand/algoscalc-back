class Case:
    """Класс для представления тестового случая со значением и необязательным описанием.

    Attributes:
    ----------
    value : any
        Значение тестового случая.
    description : str, optional
        Описание тестового случая. Если не указано, по умолчанию используется строковое
        представление значения.

    Methods:
    -------
    __repr__():
        Возвращает строковое представление экземпляра класса Case.
    """

    def __init__(self, value, description=None):
        self.value = value
        self.description = description if description is not None else str(value)

    def __repr__(self):
        return f"Case(value={self.value}, description='{self.description}')"


if __name__ == "__main__":
    print(Case(1))
    print(Case("1", "One"))
    print(Case([1, 2, 3], "List"))
    print(Case({"key": "value"}, "Dictionary"))
    print(Case((1, 2), "Tuple"))
    print(Case({1, 2, 3}, "Set"))
    print(Case([[1], [2]], "Matrix"))
