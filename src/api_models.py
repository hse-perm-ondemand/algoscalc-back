"""Классы модуля реализуют структуры данных для API онлайн-калькулятора

"""

from typing import Union, Optional, Any
from pydantic import BaseModel


class AlgorithmTitle(BaseModel):
    """Класс представляет краткую информацию об алгоритме.

    :param name: уникальное имя алгоритма;
    :type name: str
    :param title: название алгоритма.
    :type title: str
    """
    name: str
    title: str


class Algorithms(BaseModel):
    """Класс представляет список имеющихся алгоритмов.

    :param algorithms: список имеющихся алгоритмов.
    :type algorithms: list[AlgorithmTitle]

    """
    algorithms: Optional[list[AlgorithmTitle]]


class DataDefinition(BaseModel):
    """Класс представляет описание элемента входных/выходных данных.

    :param name: уникальное имя элемента входных/выходных данных;
    :type name: str
    :param title: название элемента входных/выходных данных;
    :type title: str
    :param description: описание элемента входных/выходных данных;
    :type description: str
    :param data_type: тип данных;
    :type data_type: str
    :param data_shape: размерность данных;
    :type data_shape: str
    :param default_value: значение по умолчанию.
    :type default_value: int, float, str, bool либо список или двумерная
        матрица с элементами указанных типов.

    """
    name: str
    title: str
    description: str
    data_type: str
    data_shape: str
    default_value: Union[int, float, str, bool,
                         Optional[list[Union[int, float, str, bool,
                                             Optional[list[
                                                 Union[int, float,
                                                       str, bool]]]]]]]

    class Config:
        smart_union = True


class AlgorithmDefinition(BaseModel):
    """Класс представляет описание алгоритма.

    :param name: уникальное имя алгоритма;
    :type name: str
    :param title: название алгоритма;
    :type title: str
    :param description: описание алгоритма;
    :type description: str
    :param parameters: список описаний входных данных алгоритма;
    :type parameters: list[DataDefinition]
    :param outputs: список описаний выходных данных алгоритма.
    :type outputs: list[DataDefinition]
    """
    name: str
    title: str
    description: str
    parameters: list[DataDefinition]
    outputs: list[DataDefinition]


class Data(BaseModel):
    """Класс представляет фактическое значение элемента входных/выходных данных.

    :param name: уникальное имя элемента входных/выходных данных;
    :type name: str
    :param value: фактическое значение.
    :type value: int, float, str, bool либо список или двумерная
        матрица с элементами указанных типов.
    """
    name: str
    value: Union[int, float, str, bool,
                 Optional[list[Union[int, float, str, bool,
                                     Optional[list[
                                         Union[int, float, str, bool]]]]]]]

    class Config:
        smart_union = True


class Parameters(BaseModel):
    """Класс представляет список фактических значений входных данных
    для алгоритма.

    :param parameters: список фактических значений входных данных алгоритма;
    :type parameters: list[Data]
    """
    parameters: list[Data]

    def get_params_to_execute(self) -> dict[str, Any]:
        """Возвращает значения входных данных для выполнения алгоритма в
        виде словаря, где ключи - имена входных данных, значения - фактические
        значения входных данных.

        :return: словарь с именами и значениями входных данных.
        :rtype: dict[str, Any]
        """
        return {param.name: param.value for param in self.parameters}


class Outputs(BaseModel):
    """Класс представляет список фактических значений выходных данных
    для алгоритма.

    :param outputs: список фактических значений выходных данных алгоритма;
    :type outputs: list[Data]
    """
    outputs: list[Data]


class Answer(BaseModel):
    """Базовый класс для ответа, включающего результат выполнения запроса или
    текст ошибки выполнения запроса.

    :param result: результат выполнения запроса;
    :type result: Any or None
    :param errors: текст ошибки выполнения запроса;
    :type errors: str or None
    """
    result: Optional[Any]
    errors: Optional[str]

    class Config:
        @staticmethod
        def schema_extra(schema, model):
            """Корректирует JSON Schema класса для корректной валидации
            nullable значений."""
            for prop, value in schema.get('properties', {}).items():
                field = [x for x in model.__fields__.values()
                         if x.alias == prop][0]
                if field.allow_none:
                    if 'type' in value:
                        value['anyOf'] = [{'type': value.pop('type')}]
                    elif '$ref' in value:
                        if issubclass(field.type_, BaseModel):
                            value['title'] = field.type_.__config__.title \
                                             or field.type_.__name__
                        value['anyOf'] = [{'$ref': value.pop('$ref')}]
                    value['anyOf'].append({'type': 'null'})


class AnswerAlgorithmDefinition(Answer):
    """Класс ответа, включающего результат выполнения запроса описания
    алгоритма или текст ошибки выполнения запроса. Наследует от класса Answer.

    :param result: описание алгоритма;
    :type result: AlgorithmDefinition or None
    """
    result: Optional[AlgorithmDefinition]


class AnswerOutputs(Answer):
    """Класс ответа, включающего результат выполнения алгоритма или
    текст ошибки выполнения алгоритма. Наследует от класса Answer.

    :param result: список фактических значений выходных данных алгоритма;
    :type result: Outputs or None
    """
    result: Optional[Outputs]
