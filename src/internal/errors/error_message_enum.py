from strenum import StrEnum


class ErrorMessageEnum(StrEnum):
    """Перечисление сообщений об ошибках приложения."""

    EMPTY_STRING = "Значение параметра не может быть пустой строкой"
    NOT_DATA_TYPE = "Параметр data_type не является экземпляром DataTypeEnum"
    NOT_DATA_SHAPE = "Параметр data_shape не является экземпляром DataShapeEnum"
    NONE_VALUE = "Значение отсутствует (тип None)"
    NOT_SCALAR_VALUE = "Значение не является скалярным"
    NOT_MATRIX_VALUE = "Значение не является матрицей"
    NOT_LIST_VALUE = "Значение не является списком"
    PARAM_NOT_DATAELEMENT = (
        "Элемент входных данных не является экземпляром класса DataElement"
    )
    OUTPUT_NOT_DATAELEMENT = (
        "Элемент выходных данных не является экземпляром класса DataElement"
    )
    PARAMS_HAS_DUPLICATE = "Описания входных данных содержат дубликаты"
    OUTPUTS_HAS_DUPLICATE = "Описания выходных данных содержат дубликаты"
    METHOD_NOT_CALL = "Объект, переданный в качестве метода, не является вызываемым"
    UNEXPECTED_PARAM = "В метод передан недопустимый параметр"
    UNSET_PARAMS = "Для алгоритма не заданы входные данные"
    UNSET_OUTPUTS = "Для алгоритма не заданы выходные данные"
    INCORRECT_PARAMS = "Входные данные переданы в некорректном формате"
    NOT_DICT_OUTPUTS = "Выходные данные алгоритма не формате словаря"
    NON_INT_TIMEOUT = "Параметр execute_timeout не является целым числом"
    NEG_INT_TIMEOUT = "Значение параметра execute_timeout меньше нуля"
    UNIT_TEST_FAILED = "Модульные тесты для алгоритма завершились с ошибкой"
    NO_ALGORITHMS = "Алгоритмов не найдено"
    TIME_OVER = "Время для выполнения алгоритма истекло"
    UNEXPECTED_ERROR = "Что-то пошло не так..."
