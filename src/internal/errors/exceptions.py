from src.internal.errors import ErrorMessageTemplateEnum as ErrMsgTmpl
from src.internal.errors import ErrorMessageEnum as ErrMsg


class AlgorithmError(Exception):
    """Базовый класс ошибок выполнения алгоритмов."""

    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class AlgorithmValueError(AlgorithmError):
    """Ошибка некорректного значения параметра при выполнении алгоритма."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class AlgorithmTypeError(AlgorithmError):
    """Ошибка некорректного типа данных параметра при выполнении алгоритма."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class AlgorithmTimeoutError(AlgorithmError):
    """Ошибка истечения времени выполнения алгоритма."""

    def __init__(self, timeout: int):
        super().__init__(ErrMsgTmpl.TIME_OVER.format(timeout))


class AlgorithmRuntimeError(AlgorithmError):
    """Ошибка выполнения алгоритма."""

    def __init__(self, message: str):
        super().__init__(ErrMsgTmpl.EXECUTION_FAILED.format(message))


class AlgorithmUnexpectedError(AlgorithmError):
    """Непредвиденная ошибка выполнения алгоритма."""

    def __init__(self):
        super().__init__(ErrMsg.UNEXPECTED_ERROR)


class AlgorithmNotFoundError(AlgorithmError):
    """Ошибка отсутствия алгоритма."""

    def __init__(self, algorithm_name: str):
        super().__init__(ErrMsgTmpl.ALGORITHM_NOT_EXISTS.format(algorithm_name))
