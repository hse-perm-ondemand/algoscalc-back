import signal
import logging.config
from logging import Logger
from typing import Callable, Optional, Any


from src.core.data_element import DataElement


DEFAULT_TIMEOUT = 5
PARAM_NOT_DATAELEMENT_MSG = 'Parameter is not an DataElement instance'
PARAM_EXISTS_TMPL = 'Parameter "{0}" already exists'
OUTPUT_NOT_DATAELEMENT_MSG = 'Output is not an DataElement instance'
OUTPUT_EXISTS_TMPL = 'Output "{0}" already exists'
METHOD_NOT_CALL_MSG = 'Method object is not callable'
ADDING_METHOD_FAILED_TEMPL = 'Adding the method failed. Error: {0}'
UNEXPECTED_OUTPUT_TEMPL = 'Fact output "{0}" value "{1}" is not ' \
                                     'equal to expected value "{2}"'
TIME_OVER_TEMPL = 'The time for execution ({0} s) is over. Parameters: {1}'
UNEXPECTED_PARAM_MSG = 'The method got an unexpected parameter'
EXECUTION_FAILED_TEMPL = 'Method execution is failed! Error: {0}. ' \
                         'Parameters: {1}'
UNSET_PARAMS_MSG = 'Parameters for the algorithm are not set'
UNSET_OUTPUTS_MSG = 'Outputs for the algorithm are not set'
NOT_DICT_PARAMS_MSG = 'Specified parameters is not a dictionary'
REDUNDANT_PARAMETER_TEMPL = 'The specified parameter "{0}" is missing ' \
                            'in the algorithms parameters'
MISSED_PARAMETER_TEMPL = 'The defined parameter "{0}" is missing ' \
                         'in the specified parameters'
NOT_DICT_OUTPUTS_MSG = 'The outputs returned is not a dictionary'
REDUNDANT_OUTPUT_TEMPL = 'The returned output key "{0}" is missing ' \
                         'in the algorithms outputs'
MISSED_OUTPUT_TEMPL = 'The defined output key "{0}" is missing ' \
                      'in the method outputs'
NON_STRING_PARAM_TEMPL = 'The "{0}" parameter is not a string'
EMPTY_STRING_PARAM_TEMPL = 'The "{0}" parameter is empty'
NON_INT_TIMEOUT_MSG = 'The execute_timeout parameter is not an integer'
NEG_INT_TIMEOUT_MSG = 'The execute_timeout parameter is less than 0'


class Algorithm(object):
    def __init__(self, name: str, title: str, description: str,
                 log_config: dict[str, Any],
                 execute_timeout: int = DEFAULT_TIMEOUT):
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
        return f'Algorithm: {self.__name}, title: {self.__title}'

    @property
    def name(self) -> str:
        return self.__name

    @property
    def title(self) -> str:
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def parameters(self) -> tuple[DataElement]:
        return tuple(param for param in self.__parameters.values())

    @property
    def outputs(self) -> tuple[DataElement]:
        return tuple(output for output in self.__outputs.values())

    @property
    def execute_timeout(self) -> int:
        return self.__execute_timeout

    def add_parameter(self, parameter: DataElement) -> None:
        if not isinstance(parameter, DataElement):
            self.__log_and_raise_error(PARAM_NOT_DATAELEMENT_MSG, TypeError)
        if parameter.name in self.__parameters.keys():
            self.__log_and_raise_error(PARAM_EXISTS_TMPL.format(parameter.name),
                                       ValueError)
        self.__parameters[parameter.name] = parameter

    def add_output(self, output: DataElement) -> None:
        if not isinstance(output, DataElement):
            self.__log_and_raise_error(OUTPUT_NOT_DATAELEMENT_MSG, TypeError)
        if output.name in self.__outputs.keys():
            self.__log_and_raise_error(OUTPUT_EXISTS_TMPL.format(output.name),
                                       ValueError)
        self.__outputs[output.name] = output

    def add_execute_method(self, method: Callable) -> None:
        if not callable(method):
            self.__log_and_raise_error(METHOD_NOT_CALL_MSG, TypeError)
        self.__execute_method = method
        errors = self.get_test_errors()
        if errors is not None:
            self.__execute_method = None
            self.__log_and_raise_error(
                ADDING_METHOD_FAILED_TEMPL.format(errors), RuntimeError)

    def get_test_errors(self) -> Optional[str]:
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
        return {key: value.default_value
                for key, value in self.__parameters.items()}

    def __check_method_raises_ex(self) -> None:
        if not callable(self.__execute_method):
            self.__log_and_raise_error(METHOD_NOT_CALL_MSG, TypeError)
        if not self.__parameters:
            self.__log_and_raise_error(UNSET_PARAMS_MSG, AttributeError)
        if not self.__outputs:
            self.__log_and_raise_error(UNSET_OUTPUTS_MSG, AttributeError)

    def __check_parameters_raises_ex(self, fact_params: dict[str, Any]) -> None:
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
        self.__logger.error(f'{self.__name}. {msg}')
        raise error_type(msg)
