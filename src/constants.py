APP_CONFIG_FILE_PATH = 'config/app_config.json'
"""Путь к конфигурации приложения"""
LOG_CONFIG_FILE_PATH = 'config/log_config.json'
"""Путь к конфигурации логирования"""
PATH_CONFIG = 'path_config'
"""Ключ для раздела конфигурации, содержащего пути к файлам для алгоритмов"""
ALGORITHM_CONFIG = 'algorithm_config'
"""Ключ для раздела конфигурации с настройками для алгоритмов"""
IS_TEST_APP = 'IS_TEST_APP'
"""Переменная среды, свидетельствующая о проведении тестировании модуля main"""
EXECUTE_TIMEOUT = 'execute_timeout'
"""Ключ в конфигурации алгоритмов для задания времени выполнения алгоритма"""
ALGORITHMS_ENDPOINT = '/api/algorithms'
"""Конечная точка для API"""
TIME_OVER_MSG = 'Время для выполнения алгоритма истекло'
"""Сообщение об ошибке таймаута"""
