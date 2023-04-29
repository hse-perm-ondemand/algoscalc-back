from typing import Callable, Optional, Any
import signal

from src.core.data_element import DataElement, DataType, DataShape


DEFAULT_TIMEOUT = 5


class Algorithm(object):
    def __init__(self, name: str, title: str, description: str,
                 execute_timeout: int = DEFAULT_TIMEOUT):
        param_errors = Algorithm.__check_params(name, title, description,
                                                execute_timeout)
        if param_errors is not None:
            raise ValueError(param_errors)
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
            raise TypeError('Parameter is not an DataElement instance')
        if parameter.name in self.__parameters.keys():
            raise ValueError(f'Parameter "{parameter.name}" already exists')
        self.__parameters[parameter.name] = parameter

    def add_output(self, output: DataElement) -> None:
        if not isinstance(output, DataElement):
            raise TypeError('Output is not an DataElement instance')
        if output.name in self.__outputs.keys():
            raise ValueError(f'Output "{output.name}" already exists')
        self.__outputs[output.name] = output

    def add_execute_method(self, method: Callable) -> None:
        if not callable(method):
            raise TypeError('Method object is not callable')
        self.__execute_method = method
        errors = self.get_test_errors()
        if errors is not None:
            self.__execute_method = None
            raise RuntimeError(f'Adding the method failed. Error: {errors}')

    def get_test_errors(self) -> Optional[str]:
        try:
            params = self.__get_default_parameters()
            outputs = self.execute(params)
            for key, value in self.__outputs.items():
                if outputs[key] != value.default_value:
                    raise ValueError(f'Fact output "{key}" '
                                     f'value "{outputs[key]}" '
                                     f'is not equal to expected '
                                     f'value "{value.default_value}"')
            return None
        except Exception as ex:
            return str(ex)

    def execute(self, params: dict[str, Any]) -> dict[str, Any]:
        self.__check_method_raises_ex()
        self.__check_parameters_raises_ex(params)

        def timeout_handler(signum, frame):
            raise TimeoutError('The time for execution '
                               f'({self.__execute_timeout} s) is over')
        if self.__execute_timeout > 0:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.__execute_timeout)
        try:
            method_outputs = self.__execute_method(**params)
            if self.__execute_timeout > 0:
                signal.alarm(0)
        except TimeoutError as ex:
            raise TimeoutError(str(ex) + f' Parameters: {params}')
        except Exception as ex:
            raise RuntimeError(f'Method execution is failed! Error: {ex}. '
                               f'Parameters: {params}')
        self.__check_outputs_raises_ex(method_outputs)
        return method_outputs

    def __get_default_parameters(self) -> dict[str, Any]:
        return {key: value.default_value
                for key, value in self.__parameters.items()}

    def __check_method_raises_ex(self) -> None:
        if not callable(self.__execute_method):
            raise TypeError('Execute method object is not callable')
        if not self.__parameters:
            raise AttributeError('Parameters for the algorithm are not set')
        if not self.__outputs:
            raise AttributeError('Outputs for the algorithm are not set')

    def __check_parameters_raises_ex(self, fact_params: dict[str, Any]) -> None:
        if type(fact_params) != dict:
            raise TypeError('Specified parameters is not a dictionary')
        for key in fact_params.keys():
            if key not in self.__parameters.keys():
                raise KeyError(f'The specified parameter "{key}" is missing in '
                               f'the algorithms parameters')
        for key in self.__parameters.keys():
            if key not in fact_params.keys():
                raise KeyError(f'The defined parameter "{key}" is missing in '
                               f'the specified parameters')
            errors = self.__parameters[key].get_check_value_errors(
                fact_params[key])
            if errors is not None:
                raise TypeError(errors)

    def __check_outputs_raises_ex(self, method_outputs: dict[str, Any]) -> None:
        if type(method_outputs) != dict:
            raise TypeError('The outputs returned is not a dictionary')
        for key in method_outputs.keys():
            if key not in self.__outputs.keys():
                raise KeyError(f'The returned output key "{key}" is missing in '
                               f'the algorithms outputs')
        for key in self.__outputs.keys():
            if key not in method_outputs.keys():
                raise KeyError(f'The defined output key "{key}" is missing in '
                               f'the method outputs')
            errors = self.__outputs[key].get_check_value_errors(
                method_outputs[key])
            if errors is not None:
                raise TypeError(errors)

    @staticmethod
    def __check_params(name: str, title: str, description: str,
                       execute_timeout: int) -> Optional[str]:
        if type(name) != str:
            return 'The name parameter is not a string'
        if not name:
            return 'The name parameter is empty'
        if type(title) != str:
            return 'The title parameter is not a string'
        if not title:
            return 'The title parameter is empty'
        if type(description) != str:
            return 'The description parameter is not a string'
        if not description:
            return 'The description parameter is empty'
        if type(execute_timeout) != int:
            return 'The execute_timeout parameter is not an integer'
        if execute_timeout < 0:
            return 'The execute_timeout parameter is less than 0'
        return None


if __name__ == '__main__':
    alg = Algorithm('sum', 'sum', 'returns the sum of two numbers', 5)
    param_a = DataElement('a', 'a number', 'just an integer', DataType.INT,
                          DataShape.SCALAR, 1)
    param_b = DataElement('b', 'b number', 'just an integer', DataType.INT,
                          DataShape.SCALAR, 2)
    alg.add_parameter(param_a)
    alg.add_parameter(param_b)
    output = DataElement('sum', 'sum', 'the sum of two numbers',
                         DataType.INT, DataShape.SCALAR, 3)
    alg.add_output(output)
    alg.add_execute_method(lambda a, b: {'sum': a + b})
    print(alg.execute({'a': 10, 'b': 20}))
