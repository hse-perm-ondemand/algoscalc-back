"""В пакете представлены классы для обработки ошибок."""

from .error_message_enum import ErrorMessageEnum
from .error_message_template_enum import ErrorMessageTemplateEnum
from .exceptions import (
    AlgorithmError,
    AlgorithmNotFoundError,
    AlgorithmRuntimeError,
    AlgorithmTimeoutError,
    AlgorithmTypeError,
    AlgorithmUnexpectedError,
    AlgorithmValueError,
)

__all__ = [
    "ErrorMessageEnum",
    "ErrorMessageTemplateEnum",
    "AlgorithmError",
    "AlgorithmValueError",
    "AlgorithmTypeError",
    "AlgorithmTimeoutError",
    "AlgorithmRuntimeError",
    "AlgorithmNotFoundError",
    "AlgorithmUnexpectedError",
]
