import signal
from typing import Any, Callable

from src.internal.constants import DEFAULT_TIMEOUT
from src.internal.data_dimension.data_dimension_checker import DataDimensionChecker
from src.internal.errors import ErrorMessageEnum as ErrMsg
from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl
from src.internal.schemas.algorithm_definition_schema import AlgorithmDefinitionSchema
from src.internal.schemas.data_definition_schema import DataDefinitionSchema


class AlgorithmExecutor(object):
    """Класс содержит описание алгоритма, структуры его входных и
    выходных данных, предоставляет возможность выполнения алгоритма согласно
    заданным параметрам.
    """

    def __init__(
        self,
        definition: AlgorithmDefinitionSchema,
        method: Callable,
        execute_timeout: int = DEFAULT_TIMEOUT,
    ):
        """Конструктор класса

        :param definition: описание алгоритма;
        :type definition: AlgorithmDefinitionSchema
        :param method: метод, обеспечивающий выполнение алгоритма;
        :type method: Callable
        :param execute_timeout: время отведенное для выполнения алгоритма;
        :type execute_timeout: int
        :raises ValueError: при несоответствии типов данных для параметров,
            при отрицательных значениях параметра execute_timeout.
        """
        self.__definition: AlgorithmDefinitionSchema = definition
        self.__execute_timeout: int = execute_timeout
        self.__execute_method: Callable = method
        self.__validate()

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра класса."""
        return f"Algorithm: {self.definition.name}, title: {self.definition.title}"

    @property
    def definition(self) -> AlgorithmDefinitionSchema:
        """Возвращает описание алгоритма.

        :return: описание алгоритма.
        :rtype: AlgorithmDefinitionSchema
        """
        return self.__definition

    @property
    def execute_timeout(self) -> int:
        """Возвращает время отведенное для выполнения алгоритма.

        :return: время отведенное для выполнения алгоритма.
        :rtype: int
        """
        return self.__execute_timeout

    @property
    def parameter_names(self):
        """Возвращает названия для входных данных алгоритма."""
        return [param.name for param in self.definition.parameters]

    @property
    def output_names(self):
        """Возвращает названия для выходных данных алгоритма."""
        return [output.name for output in self.definition.outputs]

    def get_parameter_by_name(self, name):
        """Возвращает описание элемента вхожных данных по его имени."""
        if name not in self.parameter_names:
            raise ValueError(ErrMsgTmpl.REDUNDANT_PARAMETER.format(name))
        return [param for param in self.definition.parameters if param.name == name][0]

    def get_output_by_name(self, name):
        """Возвращает описание элемента выхожных данных по его имени."""
        if name not in self.output_names:
            raise ValueError(ErrMsgTmpl.REDUNDANT_OUTPUT.format(name))
        return [output for output in self.definition.outputs if output.name == name][0]

    def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Выполняет алгоритм с заданными входными данными.

        :param params: значения входных данных для выполнения алгоритма.
            Словарь, где ключи - имена входных данных, значения - фактические
            значения входных данных.
        :type params: dict[str, Any]
        :return: результат выполнения алгоритма. Словарь, где ключи - имена
            выходных данных, значения - рассчитанные значения выходных данных.
        :rtype: dict[str, Any]
        :raises TypeError: если не установлен метод для выполнения, если
            параметры переданы не словарем, если метод вернул результаты
            не в виде словаря;
        :raises TimeoutError: если закончилось время, отведенное для
            выполнения алгоритма;
        :raises RuntimeError: при возникновении ошибки при выполнении.
        """
        self.validate_input_values(params)

        def timeout_handler(signum, frame):
            raise TimeoutError(
                ErrMsgTmpl.TIME_OVER.format(self.__execute_timeout, params)
            )

        if self.__execute_timeout > 0:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.__execute_timeout)

        method_outputs = None
        try:
            method_outputs = self.__execute_method(**params)
        except TimeoutError:
            raise
        except TypeError:
            raise RuntimeError(
                ErrMsgTmpl.EXECUTION_FAILED.format(ErrMsg.UNEXPECTED_PARAM, params)
            )
        except Exception as ex:
            raise RuntimeError(ErrMsgTmpl.EXECUTION_FAILED.format(ex, params))
        finally:
            if self.__execute_timeout > 0:
                signal.alarm(0)

        self.__validate_output_values(method_outputs)
        return method_outputs

    def validate_input_values(self, fact_params: dict[str, Any]) -> None:
        """ "Проверяет входные данные для выполнения алгоритма. При наличии
        ошибок вызывает исключения TypeError, ValueError."""
        if not isinstance(fact_params, dict):
            raise TypeError(ErrMsg.NOT_DICT_PARAMS)
        for key in fact_params.keys():
            if key not in self.parameter_names:
                raise ValueError(ErrMsgTmpl.REDUNDANT_PARAMETER.format(key))
        for key in self.parameter_names:
            if key not in fact_params.keys():
                raise ValueError(ErrMsgTmpl.MISSED_PARAMETER.format(key))
            errors = DataDimensionChecker.check_value(
                self.get_parameter_by_name(key), fact_params[key]
            )
            if errors is not None:
                raise TypeError(errors)

    def __validate_output_values(self, method_outputs: dict[str, Any]) -> None:
        """ "Проверяет выходные данные для выполнения алгоритма. При наличии
        ошибок вызывает исключения TypeError, ValueError."""
        if not isinstance(method_outputs, dict):
            raise TypeError(ErrMsg.NOT_DICT_OUTPUTS)
        for key in method_outputs.keys():
            if key not in self.output_names:
                raise ValueError(ErrMsgTmpl.REDUNDANT_OUTPUT.format(key))
        for key in self.output_names:
            if key not in method_outputs.keys():
                raise ValueError(ErrMsgTmpl.MISSED_OUTPUT.format(key))
            errors = DataDimensionChecker.check_value(
                self.get_output_by_name(key), method_outputs[key]
            )
            if errors is not None:
                raise TypeError(errors)

    def __get_test_errors(self) -> str | None:
        """Выполняет тестовое выполнение алгоритма, с параметрами заданными
        по умолчанию.

        :return: текст сообщения об ошибке выполнения алгоритма.
        :rtype: str or None
        """
        try:
            params = {
                param.name: param.default_value for param in self.definition.parameters
            }
            outputs = self.execute(params)
            for key, value in [
                (output.name, output.default_value)
                for output in self.definition.outputs
            ]:
                if outputs[key] != value:
                    raise ValueError(
                        ErrMsgTmpl.UNEXPECTED_OUTPUT.format(outputs[key], key, value)
                    )
        except Exception as ex:
            return str(ex).strip("'")

    def __validate(self) -> None:
        """Проверяет параметры для конструктора класса. Возвращает сообщение
        об ошибке"""
        if not isinstance(self.execute_timeout, int) or isinstance(
            self.execute_timeout, bool
        ):
            raise TypeError(ErrMsg.NON_INT_TIMEOUT)
        if self.execute_timeout < 0:
            raise ValueError(ErrMsg.NEG_INT_TIMEOUT)

        if not callable(self.__execute_method):
            raise TypeError(ErrMsg.METHOD_NOT_CALL)
        errors = self.__get_test_errors()
        if errors is not None:
            raise RuntimeError(ErrMsgTmpl.ADDING_METHOD_FAILED.format(errors))


if __name__ == "__main__":
    algorithm_definition = AlgorithmDefinitionSchema(
        name="alg",
        title="Algorithm",
        description="Some description",
        parameters=[
            DataDefinitionSchema(
                name="p",
                title="Param",
                description="Param description",
                data_type="INT",
                data_shape="SCALAR",
                default_value=1,
            )
        ],
        outputs=[
            DataDefinitionSchema(
                name="o",
                title="Output",
                description="Output description",
                data_type="INT",
                data_shape="SCALAR",
                default_value=2,
            )
        ],
    )
    algorithm_executor = AlgorithmExecutor(algorithm_definition, lambda p: {"o": p * 2})
    print(algorithm_executor)
    print(algorithm_executor.execute({"p": 10}))
