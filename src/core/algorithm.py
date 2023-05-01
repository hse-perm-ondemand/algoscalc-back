import signal
import logging.config
from logging import Logger
from typing import Callable, Optional, Any


from src.core.data_element import DataElement
from src.core.constants import PARAM_NOT_DATAELEMENT_MSG, PARAM_EXISTS_TMPL, \
    OUTPUT_NOT_DATAELEMENT_MSG, OUTPUT_EXISTS_TMPL, METHOD_NOT_CALL_MSG,\
    ADDING_METHOD_FAILED_TEMPL, UNEXPECTED_OUTPUT_TEMPL, TIME_OVER_TEMPL,\
    UNEXPECTED_PARAM_MSG, EXECUTION_FAILED_TEMPL, UNSET_PARAMS_MSG,\
    UNSET_OUTPUTS_MSG, NOT_DICT_PARAMS_MSG, REDUNDANT_PARAMETER_TEMPL, \
    MISSED_PARAMETER_TEMPL, NOT_DICT_OUTPUTS_MSG, REDUNDANT_OUTPUT_TEMPL, \
    MISSED_OUTPUT_TEMPL, NON_STRING_PARAM_TEMPL, EMPTY_STRING_PARAM_TEMPL, \
    NON_INT_TIMEOUT_MSG, NEG_INT_TIMEOUT_MSG, DEFAULT_TIMEOUT


class Algorithm(object):
    """Класс представляет описание алгоритма, структуры входных и
    выходных данных, предоставляет возможность выполнения алгоритма согласно
    заданным параметрам.
    """
    def __init__(self, name: str, title: str, description: str,
                 log_config: dict[str, Any],
                 execute_timeout: int = DEFAULT_TIMEOUT):
        """Конструктор класса

        :param name: уникальное имя алгоритма;
        :type name: str
        :param title: название алгоритма;
        :type title: str
        :param description: описание алгоритма;
        :type description: str
        :param log_config: конфигурация логирования;
        :type log_config: dict[str, Any]
        :param execute_timeout: время отведенное для выполнения алгоритма;
        :type execute_timeout: int
        :raises ValueError: при несоответствии типов данных для параметров,
            при отрицательных значениях параметра execute_timeout.
        """
        self.__name: str = ''
        param_errors = Algorithm.__check_params(name, title, description,
                                                execute_timeout)
        self.__log_config: dict[str: Any] = log_config
        logging.config.dictConfig(log_config)
        self.__logger: Logger = logging.getLogger(__name__)
        self.__logger.debug(f'name: {name}, title: {title}, '
                            f'description: {description}, '
                            f'execute_timeout: {execute_timeout}')

        if param_errors is not None:
            self.__log_and_raise_error(param_errors, ValueError)
        self.__name: str = name
        self.__title: str = title
        self.__description: str = description
        self.__execute_timeout: int = execute_timeout
        self.__parameters: dict[str, DataElement] = {}
        self.__outputs: dict[str, DataElement] = {}
        self.__execute_method: Optional[Callable] = None

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра класса."""
        return f'Algorithm: {self.__name}, title: {self.__title}'

    @property
    def name(self) -> str:
        """Возвращает уникальное имя алгоритма.

        :return: уникальное имя алгоритма.
        :rtype: str
        """
        return self.__name

    @property
    def title(self) -> str:
        """Возвращает название алгоритма.

        :return: название алгоритма.
        :rtype: str
        """
        return self.__title

    @property
    def description(self) -> str:
        """Возвращает описание алгоритма.

        :return: описание алгоритма.
        :rtype: str
        """
        return self.__description

    @property
    def parameters(self) -> tuple[DataElement]:
        """Возвращает описание входных данных алгоритма.

        :return: описание входных данных алгоритма.
        :rtype: tuple[DataElement]
        """
        return tuple(param for param in self.__parameters.values())

    @property
    def outputs(self) -> tuple[DataElement]:
        """Возвращает описание выходных данных алгоритма.

        :return: описание выходных данных алгоритма.
        :rtype: tuple[DataElement]
        """
        return tuple(output for output in self.__outputs.values())

    @property
    def execute_timeout(self) -> int:
        """Возвращает время отведенное для выполнения алгоритма.

        :return: время отведенное для выполнения алгоритма.
        :rtype: int
        """
        return self.__execute_timeout

    def add_parameter(self, parameter: DataElement) -> None:
        """Добавляет в описание входных данных алгоритма, элемент
        переданный в параметре parameter

        :param parameter: элемент входных данных.
        :type parameter: DataElement
        :return: None
        :raises TypeError: если параметр не является экземпляром DataElement;
        :raises ValueError: если элемент входных данных с указанным именем
            уже имеется в описании структуры входных данных.
        """
        if not isinstance(parameter, DataElement):
            self.__log_and_raise_error(PARAM_NOT_DATAELEMENT_MSG, TypeError)
        if parameter.name in self.__parameters.keys():
            self.__log_and_raise_error(PARAM_EXISTS_TMPL.format(parameter.name),
                                       ValueError)
        self.__parameters[parameter.name] = parameter

    def add_output(self, output: DataElement) -> None:
        """Добавляет в описание выходных данных алгоритма,  элемент
        переданный в параметре output

        :param output: элемент выходных данных.
        :type output: DataElement
        :return: None
        :raises TypeError: если параметр не является экземпляром DataElement;
        :raises ValueError: если элемент выходных данных с указанным именем
            уже имеется в описании структуры выходных данных.
        """
        if not isinstance(output, DataElement):
            self.__log_and_raise_error(OUTPUT_NOT_DATAELEMENT_MSG, TypeError)
        if output.name in self.__outputs.keys():
            self.__log_and_raise_error(OUTPUT_EXISTS_TMPL.format(output.name),
                                       ValueError)
        self.__outputs[output.name] = output

    def add_execute_method(self, method: Callable) -> None:
        """Добавляет метод, реализующий выполнение алгоритма.

        :param method: метод, реализующий выполнение алгоритма;
        :type method: Callable
        :return: None
        :raises TypeError: если параметр не является методом;
        :raises RuntimeError: если тестовое выполнение алгоритма
            завершилось с ошибкой.
        """
        if not callable(method):
            self.__log_and_raise_error(METHOD_NOT_CALL_MSG, TypeError)
        self.__execute_method = method
        errors = self.get_test_errors()
        if errors is not None:
            self.__execute_method = None
            self.__log_and_raise_error(
                ADDING_METHOD_FAILED_TEMPL.format(errors), RuntimeError)

    def get_test_errors(self) -> Optional[str]:
        """Выполняет тестовое выполнение алгоритма, с параметрами заданными
        по умолчанию.

        :return: текст сообщения об ошибке выполнения алгоритма.
        :rtype: str or None
        """
        try:
            params = self.__get_default_parameters()
            outputs = self.execute(params)
            for key, value in self.__outputs.items():
                if outputs[key] != value.default_value:
                    raise ValueError(
                        UNEXPECTED_OUTPUT_TEMPL.format(key, outputs[key],
                                                       value.default_value))
            return None
        except Exception as ex:
            self.__logger.error(ex)
            return str(ex).strip("'")

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
        :raises KeyError: если во входных или выходных данных отсутствует
            необходимый или имеется лишний элемент;
        :raises TimeoutError: если закончилось время, отведенное для
            выполнения алгоритма;
        :raises RuntimeError: при возникновении ошибки при выполнении.
        """
        self.__check_method_raises_ex()
        self.__check_parameters_raises_ex(params)

        def timeout_handler(signum, frame):
            raise TimeoutError()
        if self.__execute_timeout > 0:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.__execute_timeout)
        method_outputs = None
        try:
            method_outputs = self.__execute_method(**params)
            if self.__execute_timeout > 0:
                signal.alarm(0)
        except TimeoutError:
            msg = TIME_OVER_TEMPL.format(self.__execute_timeout, params)
            self.__log_and_raise_error(msg, TimeoutError)
        except TypeError:
            msg = EXECUTION_FAILED_TEMPL.format(UNEXPECTED_PARAM_MSG, params)
            self.__log_and_raise_error(msg, RuntimeError)
        except Exception as ex:
            self.__log_and_raise_error(
                EXECUTION_FAILED_TEMPL.format(ex, params), RuntimeError)
        self.__check_outputs_raises_ex(method_outputs)
        return method_outputs

    def __get_default_parameters(self) -> dict[str, Any]:
        """Возвращает значения по умолчанию для входных данных алгоритма."""
        return {key: value.default_value
                for key, value in self.__parameters.items()}

    def __check_method_raises_ex(self) -> None:
        """Проверяет возможность выполнения метода. При наличии ошибок
        вызывает исключения TypeError, AttributeError."""
        if not callable(self.__execute_method):
            self.__log_and_raise_error(METHOD_NOT_CALL_MSG, TypeError)
        if not self.__parameters:
            self.__log_and_raise_error(UNSET_PARAMS_MSG, AttributeError)
        if not self.__outputs:
            self.__log_and_raise_error(UNSET_OUTPUTS_MSG, AttributeError)

    def __check_parameters_raises_ex(self, fact_params: dict[str, Any]) -> None:
        """"Проверяет входные данные для выполнения алгоритма. При наличии
        ошибок вызывает исключения TypeError, KeyError."""
        if type(fact_params) != dict:
            self.__log_and_raise_error(NOT_DICT_PARAMS_MSG, TypeError)
        for key in fact_params.keys():
            if key not in self.__parameters.keys():
                self.__log_and_raise_error(
                    REDUNDANT_PARAMETER_TEMPL.format(key), KeyError)
        for key in self.__parameters.keys():
            if key not in fact_params.keys():
                self.__log_and_raise_error(
                    MISSED_PARAMETER_TEMPL.format(key), KeyError)
            errors = self.__parameters[key].get_check_value_errors(
                fact_params[key])
            if errors is not None:
                self.__log_and_raise_error(errors, TypeError)

    def __check_outputs_raises_ex(self, method_outputs: dict[str, Any]) -> None:
        """"Проверяет выходные данные для выполнения алгоритма. При наличии
        ошибок вызывает исключения TypeError, KeyError."""
        if type(method_outputs) != dict:
            self.__log_and_raise_error(NOT_DICT_OUTPUTS_MSG, TypeError)
        for key in method_outputs.keys():
            if key not in self.__outputs.keys():
                self.__log_and_raise_error(REDUNDANT_OUTPUT_TEMPL.format(key),
                                           KeyError)
        for key in self.__outputs.keys():
            if key not in method_outputs.keys():
                self.__log_and_raise_error(MISSED_OUTPUT_TEMPL.format(key),
                                           KeyError)
            errors = self.__outputs[key].get_check_value_errors(
                method_outputs[key])
            if errors is not None:
                self.__log_and_raise_error(errors, TypeError)

    @staticmethod
    def __check_params(name: str, title: str, description: str,
                       execute_timeout: int) -> Optional[str]:
        """Проверяет параметры для конструктора класса. Возвращает сообщение
        об ошибке"""
        str_params = [['name', name], ['title', title],
                      ['description', description]]
        for name, value in str_params:
            if type(value) != str:
                return NON_STRING_PARAM_TEMPL.format(name)
            if not value:
                return EMPTY_STRING_PARAM_TEMPL.format(name)
        if type(execute_timeout) != int:
            return NON_INT_TIMEOUT_MSG
        if execute_timeout < 0:
            return NEG_INT_TIMEOUT_MSG
        return None

    def __log_and_raise_error(self, msg: str, error_type: Callable) -> None:
        """Логирует сообщение об ошибке и вызывает требуемое исключение."""
        self.__logger.error(f'{self.__name}. {msg}')
        raise error_type(msg)
