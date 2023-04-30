import unittest
import time


from src.core.data_element import DataType, DataShape, DataElement
from src.core_tests.constants import LOG_CONFIG_STUB, NAME, TITLE, DESCRIPTION,\
    PARAM_NAME, PARAM_LIST_NAME, PARAM_TITLE, PARAM_DESCRIPTION,\
    PARAM_INT_DEFAULT, PARAM_LIST_DEFAULT, OUTPUT_NAME, OUTPUT_MATRIX_NAME,\
    OUTPUT_TITLE, OUTPUT_DESCRIPTION
from src.core.algorithm import Algorithm, \
    NON_STRING_PARAM_TEMPL, EMPTY_STRING_PARAM_TEMPL, NON_INT_TIMEOUT_MSG, \
    NEG_INT_TIMEOUT_MSG, PARAM_NOT_DATAELEMENT_MSG, PARAM_EXISTS_TMPL, \
    OUTPUT_NOT_DATAELEMENT_MSG, OUTPUT_EXISTS_TMPL, METHOD_NOT_CALL_MSG, \
    ADDING_METHOD_FAILED_TEMPL, UNEXPECTED_OUTPUT_TEMPL, TIME_OVER_TEMPL, \
    EXECUTION_FAILED_TEMPL, UNSET_PARAMS_MSG, UNSET_OUTPUTS_MSG, \
    NOT_DICT_PARAMS_MSG, REDUNDANT_PARAMETER_TEMPL, MISSED_PARAMETER_TEMPL, \
    NOT_DICT_OUTPUTS_MSG, REDUNDANT_OUTPUT_TEMPL, MISSED_OUTPUT_TEMPL,\
    UNEXPECTED_PARAM_MSG


class AlgorithmTests(unittest.TestCase):
    STR_TEMPL = 'Algorithm: {0}, title: {1}'
    alg = Algorithm(NAME, TITLE, DESCRIPTION, LOG_CONFIG_STUB)
    param = DataElement(PARAM_NAME, PARAM_TITLE, PARAM_DESCRIPTION,
                        DataType.INT, DataShape.SCALAR, PARAM_INT_DEFAULT)
    param_list = DataElement(PARAM_LIST_NAME, PARAM_TITLE, PARAM_DESCRIPTION,
                             DataType.STRING, DataShape.LIST,
                             PARAM_LIST_DEFAULT)
    output = DataElement(OUTPUT_NAME, OUTPUT_TITLE, OUTPUT_DESCRIPTION,
                         DataType.INT, DataShape.SCALAR, 0)
    output_matrix = DataElement(OUTPUT_MATRIX_NAME, OUTPUT_TITLE,
                                OUTPUT_DESCRIPTION, DataType.INT,
                                DataShape.MATRIX, [[0]])

    def setUp(self) -> None:
        self.alg = Algorithm(NAME, TITLE, DESCRIPTION, LOG_CONFIG_STUB)
        self.param = DataElement(PARAM_NAME, PARAM_TITLE, PARAM_DESCRIPTION,
                                 DataType.INT, DataShape.SCALAR,
                                 PARAM_INT_DEFAULT)
        self.param_list = DataElement(PARAM_LIST_NAME, PARAM_TITLE,
                                      PARAM_DESCRIPTION, DataType.STRING,
                                      DataShape.LIST, PARAM_LIST_DEFAULT)
        self.output = DataElement(OUTPUT_NAME, OUTPUT_TITLE, OUTPUT_DESCRIPTION,
                                  DataType.INT, DataShape.SCALAR, 0)
        self.output_matrix = DataElement(OUTPUT_MATRIX_NAME, OUTPUT_TITLE,
                                         OUTPUT_DESCRIPTION, DataType.INT,
                                         DataShape.MATRIX, [[0]])

    def test_non_string_name(self):
        with self.assertRaises(ValueError) as error:
            Algorithm(100500, 'title', 'description', LOG_CONFIG_STUB)
        self.assertEqual(NON_STRING_PARAM_TEMPL.format(NAME),
                         str(error.exception))

    def test_none_string_name(self):
        with self.assertRaises(ValueError) as error:
            Algorithm(None, 'title', 'description', LOG_CONFIG_STUB)
        self.assertEqual(NON_STRING_PARAM_TEMPL.format(NAME),
                         str(error.exception))

    def test_empty_string_name(self):
        with self.assertRaises(ValueError) as error:
            Algorithm('', 'title', 'description', LOG_CONFIG_STUB)
        self.assertEqual(EMPTY_STRING_PARAM_TEMPL.format(NAME),
                         str(error.exception))

    def test_non_string_title(self):
        with self.assertRaises(ValueError) as error:
            Algorithm(NAME, 1.1, 'description', LOG_CONFIG_STUB)
        self.assertEqual(NON_STRING_PARAM_TEMPL.format('title'),
                         str(error.exception))

    def test_none_string_title(self):
        with self.assertRaises(ValueError) as error:
            Algorithm(NAME, None, 'description', LOG_CONFIG_STUB)
        self.assertEqual(NON_STRING_PARAM_TEMPL.format('title'),
                         str(error.exception))

    def test_empty_string_title(self):
        with self.assertRaises(ValueError) as error:
            Algorithm(NAME, '', 'description', LOG_CONFIG_STUB)
        self.assertEqual(EMPTY_STRING_PARAM_TEMPL.format('title'),
                         str(error.exception))

    def test_non_string_description(self):
        with self.assertRaises(ValueError) as error:
            Algorithm(NAME, 'title', 1, LOG_CONFIG_STUB)
        self.assertEqual(NON_STRING_PARAM_TEMPL.format('description'),
                         str(error.exception))

    def test_none_string_description(self):
        with self.assertRaises(ValueError) as error:
            Algorithm(NAME, 'title', None, LOG_CONFIG_STUB)
        self.assertEqual(NON_STRING_PARAM_TEMPL.format('description'),
                         str(error.exception))

    def test_empty_string_description(self):
        with self.assertRaises(ValueError) as error:
            Algorithm(NAME, 'title', '', LOG_CONFIG_STUB)
        self.assertEqual(EMPTY_STRING_PARAM_TEMPL.format('description'),
                         str(error.exception))

    def test_non_int_execute_timeout(self):
        with self.assertRaises(ValueError) as error:
            Algorithm(NAME, 'title', 'description', LOG_CONFIG_STUB, 'str')
        self.assertEqual(NON_INT_TIMEOUT_MSG, str(error.exception))

    def test_negative_execute_timeout(self):
        with self.assertRaises(ValueError) as error:
            Algorithm(NAME, 'title', 'description', LOG_CONFIG_STUB, -1)
        self.assertEqual(NEG_INT_TIMEOUT_MSG, str(error.exception))

    def test_init(self):
        self.assertEqual(self.alg.name, NAME)
        self.assertEqual(self.alg.title, TITLE)
        self.assertEqual(self.alg.description, DESCRIPTION)
        self.assertEqual(self.alg.parameters, ())
        self.assertEqual(self.alg.outputs, ())
        self.assertEqual(str(self.alg), self.STR_TEMPL.format(NAME, TITLE))

    def test_add_parameter(self):
        self.alg.add_parameter(self.param)
        self.assertEqual(self.alg.parameters, (self.param,))

    def test_add_parameters(self):
        self.alg.add_parameter(self.param)
        self.alg.add_parameter(self.param_list)
        self.assertEqual(self.alg.parameters, (self.param, self.param_list))

    def test_add_non_data_element_parameter(self):
        self.assertRaisesRegex(TypeError, PARAM_NOT_DATAELEMENT_MSG,
                               self.alg.add_parameter, 'param')

    def test_add_duplicate_parameter(self):
        self.alg.add_parameter(self.param)
        self.assertRaisesRegex(ValueError, PARAM_EXISTS_TMPL.format(PARAM_NAME),
                               self.alg.add_parameter, self.param)

    def test_add_output(self):
        self.alg.add_output(self.output)
        self.assertEqual(self.alg.outputs, (self.output,))

    def test_add_outputs(self):
        self.alg.add_output(self.output)
        self.alg.add_output(self.output_matrix)
        self.assertEqual(self.alg.outputs, (self.output, self.output_matrix))

    def test_add_non_data_element_output(self):
        self.assertRaisesRegex(TypeError, OUTPUT_NOT_DATAELEMENT_MSG,
                               self.alg.add_output, 'output')

    def test_add_duplicate_output(self):
        self.alg.add_output(self.output)
        self.assertRaisesRegex(ValueError,
                               OUTPUT_EXISTS_TMPL.format(OUTPUT_NAME),
                               self.alg.add_output, self.output)

    def test_add_execute_method_non_callable(self):
        self.assertRaisesRegex(TypeError, METHOD_NOT_CALL_MSG,
                               self.alg.add_execute_method, 'method')

    def test_add_execute_method_timeout(self):
        timeout = 1
        alg = Algorithm(NAME, TITLE, DESCRIPTION, LOG_CONFIG_STUB, timeout)
        param_name = 'parameter'
        param_default = 0
        param = DataElement(param_name, 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 0)
        alg.add_parameter(param)
        alg.add_output(self.output)

        def method(parameter):
            time.sleep(timeout + 1)
            return {OUTPUT_NAME: parameter}
        timeout_msg = TIME_OVER_TEMPL.format(timeout,
                                             {param_name: param_default})
        err_msg = ADDING_METHOD_FAILED_TEMPL.format(timeout_msg)
        with self.assertRaises(Exception) as error:
            alg.add_execute_method(method)
        self.assertEqual(str(error.exception), err_msg)

    def test_zero_execute_timeout(self):
        timeout = 0
        alg = Algorithm(NAME, TITLE, DESCRIPTION, LOG_CONFIG_STUB, timeout)
        param = DataElement('param_val', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 0)
        alg.add_parameter(param)
        alg.add_output(self.output)

        def method(param_val):
            time.sleep(1)
            return {OUTPUT_NAME: param_val}

        alg.add_execute_method(method)
        self.assertIsNone(alg.get_test_errors())

    def test_add_execute_method_without_parameters(self):
        self.alg.add_output(self.output)
        with self.assertRaises(Exception) as error:
            self.alg.add_execute_method(lambda param: {OUTPUT_NAME: param})
        self.assertEqual(str(error.exception),
                         ADDING_METHOD_FAILED_TEMPL.format(UNSET_PARAMS_MSG))

    def test_add_execute_method_without_outputs(self):
        self.alg.add_parameter(self.param)
        with self.assertRaises(Exception) as error:
            self.alg.add_execute_method(lambda param: {OUTPUT_NAME: param})
        self.assertEqual(str(error.exception),
                         ADDING_METHOD_FAILED_TEMPL.format(UNSET_OUTPUTS_MSG))

    def test_add_execute_method_wrong_param(self):
        self.alg.add_parameter(self.param)
        self.alg.add_output(self.output)
        err = ADDING_METHOD_FAILED_TEMPL.format(
            EXECUTION_FAILED_TEMPL.format(UNEXPECTED_PARAM_MSG,
                                          {PARAM_NAME: PARAM_INT_DEFAULT}))
        with self.assertRaises(RuntimeError) as error:
            self.alg.add_execute_method(
                lambda wrong_name: {'output': wrong_name})
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method_missing_param(self):
        self.alg.add_parameter(self.param)
        self.alg.add_parameter(self.param_list)
        self.alg.add_output(self.output)
        params = {PARAM_NAME: PARAM_INT_DEFAULT,
                  PARAM_LIST_NAME: PARAM_LIST_DEFAULT}
        err = ADDING_METHOD_FAILED_TEMPL.format(
            EXECUTION_FAILED_TEMPL.format(UNEXPECTED_PARAM_MSG, params))
        with self.assertRaises(Exception) as error:
            self.alg.add_execute_method(
                lambda param_name: {OUTPUT_NAME: param_name})
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method_missing_output(self):
        self.alg.add_parameter(self.param)
        self.alg.add_output(self.output)
        self.alg.add_output(self.output_matrix)
        err = ADDING_METHOD_FAILED_TEMPL.format(
            MISSED_OUTPUT_TEMPL.format(OUTPUT_MATRIX_NAME))
        with self.assertRaises(Exception) as error:
            self.alg.add_execute_method(
                lambda param_name: {OUTPUT_NAME: param_name})
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method_wrong_output(self):
        self.alg.add_parameter(self.param)
        self.alg.add_output(self.output)
        wrong_name = 'wrong_name'
        err = ADDING_METHOD_FAILED_TEMPL.format(
            REDUNDANT_OUTPUT_TEMPL.format(wrong_name))
        with self.assertRaises(Exception) as error:
            self.alg.add_execute_method(
                lambda param_name: {wrong_name: param_name})
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method_wrong_output_value(self):
        self.alg.add_parameter(self.param)
        self.alg.add_output(self.output)
        wrong_value = -1
        err = ADDING_METHOD_FAILED_TEMPL.format(
            UNEXPECTED_OUTPUT_TEMPL.format(OUTPUT_NAME, wrong_value,
                                           PARAM_INT_DEFAULT))
        with self.assertRaises(Exception) as error:
            self.alg.add_execute_method(
                lambda param_name: {OUTPUT_NAME: wrong_value})
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method(self):
        self.alg.add_parameter(self.param)
        self.alg.add_output(self.output)
        self.alg.add_execute_method(
            lambda param_name: {OUTPUT_NAME: param_name})
        self.assertIsNone(self.alg.get_test_errors())

    def test_execute_non_dict_params(self):
        self.alg.add_parameter(self.param)
        self.alg.add_output(self.output)
        self.alg.add_execute_method(
            lambda param_name: {OUTPUT_NAME: param_name})
        with self.assertRaises(TypeError) as error:
            self.alg.execute('params')
        self.assertEqual(str(error.exception), NOT_DICT_PARAMS_MSG)

    def test_execute_redundant_param(self):
        self.alg.add_parameter(self.param)
        self.alg.add_output(self.output)
        self.alg.add_execute_method(
            lambda param_name: {OUTPUT_NAME: param_name})
        redundant_param = 'redundant_param'
        with self.assertRaises(KeyError) as error:
            self.alg.execute({PARAM_NAME: PARAM_INT_DEFAULT,
                              redundant_param: PARAM_INT_DEFAULT})
        self.assertEqual(str(error.exception).strip("'"),
                         REDUNDANT_PARAMETER_TEMPL.format(redundant_param))

    def test_execute_missed_param(self):
        self.alg.add_parameter(self.param)
        self.alg.add_parameter(self.param_list)
        self.alg.add_output(self.output)
        self.alg.add_execute_method(
            lambda param_name, param_list_name: {OUTPUT_NAME: param_name})
        with self.assertRaises(KeyError) as error:
            self.alg.execute({PARAM_NAME: PARAM_INT_DEFAULT})
        self.assertEqual(str(error.exception).strip("'"),
                         MISSED_PARAMETER_TEMPL.format(PARAM_LIST_NAME))

    def test_execute_non_dict_output(self):
        self.alg.add_parameter(self.param)
        self.alg.add_output(self.output)
        self.alg.add_execute_method(
            lambda param_name: {OUTPUT_NAME: param_name}
            if param_name == PARAM_INT_DEFAULT else param_name)
        with self.assertRaises(TypeError) as error:
            self.alg.execute({PARAM_NAME: -1})
        self.assertEqual(str(error.exception).strip("'"),
                         NOT_DICT_OUTPUTS_MSG)

    def test_execute_timeout(self):
        timeout = 1
        alg = Algorithm(NAME, TITLE, DESCRIPTION, LOG_CONFIG_STUB, timeout)
        alg.add_parameter(self.param)
        alg.add_output(self.output)

        def method(param_name):
            time.sleep(param_name)
            return {OUTPUT_NAME: param_name}
        alg.add_execute_method(method)
        params = {PARAM_NAME: timeout + 1}
        timeout_msg = TIME_OVER_TEMPL.format(timeout, params)
        with self.assertRaises(TimeoutError) as error:
            alg.execute(params)
        self.assertEqual(str(error.exception), timeout_msg)

    def test_execute_runtime_error(self):
        param = DataElement('param_val', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 1)
        self.alg.add_parameter(param)
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.FLOAT, DataShape.SCALAR, 1.)
        self.alg.add_output(output)
        self.alg.add_execute_method(lambda param_val: {'output': 1/param_val})
        params = {'param_val': 0}
        err = EXECUTION_FAILED_TEMPL.format('division by zero', params)
        with self.assertRaises(RuntimeError) as error:
            self.alg.execute(params)
        self.assertEqual(str(error.exception), err)

    def test_execute(self):
        alg = Algorithm('sum', 'sum', 'returns the sum of two numbers',
                        LOG_CONFIG_STUB)
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
        self.assertEqual(alg.execute({'a': 10, 'b': 20}), {'sum': 30})


if __name__ == '__main__':
    unittest.main()
