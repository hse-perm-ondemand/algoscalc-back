import unittest
import time


from core.algorithm import Algorithm, DEFAULT_TIMEOUT
from core.data_element import DataType, DataShape, DataElement


class AlgorithmTests(unittest.TestCase):
    STR_TEMPL = 'Algorithm: {0}, title: {1}'

    def test_non_string_name(self):
        self.assertRaisesRegex(ValueError, 'The name parameter is not a string',
                               Algorithm.__init__, None, 100500, 'title',
                               'description')

    def test_none_string_name(self):
        self.assertRaisesRegex(ValueError, 'The name parameter is empty',
                               Algorithm.__init__, None, '', 'title',
                               'description')

    def test_non_string_title(self):
        self.assertRaisesRegex(ValueError,
                               'The title parameter is not a string',
                               Algorithm.__init__, None, 'name', 1.1,
                               'description')

    def test_none_string_title(self):
        self.assertRaisesRegex(ValueError, 'The title parameter is empty',
                               Algorithm.__init__, None, 'name', '',
                               'description')

    def test_non_string_description(self):
        self.assertRaisesRegex(ValueError,
                               'The description parameter is not a string',
                               Algorithm.__init__, None, 'name', 'title', [])

    def test_none_string_description(self):
        self.assertRaisesRegex(ValueError, 'The description parameter is empty',
                               Algorithm.__init__, None, 'name', 'title', '')

    def test_non_int_execute_timeout(self):
        self.assertRaisesRegex(ValueError,
                               'The execute_timeout parameter '
                               'is not an integer',
                               Algorithm.__init__, None, 'name', 'title',
                               'description', 'str')

    def test_zero_execute_timeout(self):
        self.assertRaisesRegex(ValueError, 'The execute_timeout parameter '
                                           'is equal or less than 0',
                               Algorithm.__init__, None, 'name', 'title',
                               'description', 0)

    def test_negative_execute_timeout(self):
        self.assertRaisesRegex(ValueError, 'The execute_timeout parameter '
                                           'is equal or less than 0',
                               Algorithm.__init__, None, 'name', 'title',
                               'description', -1)

    def test_init(self):
        name = 'name'
        title = 'title'
        description = 'description'
        alg = Algorithm(name, title, description)
        self.assertEqual(alg.name, name)
        self.assertEqual(alg.title, title)
        self.assertEqual(alg.description, description)
        self.assertEqual(alg.parameters, ())
        self.assertEqual(alg.outputs, ())
        self.assertEqual(str(alg), self.STR_TEMPL.format(name, title))

    def test_add_parameter(self):
        alg = Algorithm('name', 'title', 'description')
        param = DataElement('param', 'param_title', 'param_descr', DataType.INT,
                            DataShape.SCALAR, 0)
        alg.add_parameter(param)
        self.assertEqual(alg.parameters, (param,))
        param_list = DataElement('list', 'list_title', 'list_descr',
                                 DataType.STRING, DataShape.LIST, ['0'])
        alg.add_parameter(param_list)
        self.assertEqual(alg.parameters, (param, param_list))

    def test_add_non_data_element_parameter(self):
        alg = Algorithm('name', 'title', 'description')
        param = 'param'
        self.assertRaisesRegex(TypeError,
                               'Parameter is not an DataElement instance',
                               alg.add_parameter, param)

    def test_add_duplicate_parameter(self):
        alg = Algorithm('name', 'title', 'description')
        param = DataElement('param', 'param_title', 'param_descr', DataType.INT,
                            DataShape.SCALAR, 0)
        alg.add_parameter(param)
        self.assertRaisesRegex(ValueError, 'Parameter "param" already exists',
                               alg.add_parameter, param)

    def test_add_output(self):
        alg = Algorithm('name', 'title', 'description')
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.INT, DataShape.SCALAR, 0)
        alg.add_output(output)
        self.assertEqual(alg.outputs, (output,))
        output_matrix = DataElement('matrix', 'matrix_title', 'matrix_descr',
                                    DataType.BOOL, DataShape.MATRIX, [[True]])
        alg.add_output(output_matrix)
        self.assertEqual(alg.outputs, (output, output_matrix))

    def test_add_non_data_element_output(self):
        alg = Algorithm('name', 'title', 'description')
        output = 'output'
        self.assertRaisesRegex(TypeError,
                               'Output is not an DataElement instance',
                               alg.add_output, output)

    def test_add_duplicate_output(self):
        alg = Algorithm('name', 'title', 'description')
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.INT, DataShape.SCALAR, 0)
        alg.add_output(output)
        self.assertRaisesRegex(ValueError, 'Output "output" already exists',
                               alg.add_output, output)

    def test_add_execute_method_non_callable(self):
        alg = Algorithm('name', 'title', 'description')
        self.assertRaisesRegex(TypeError, 'Method object is not callable',
                               alg.add_execute_method, 'method')

    def test_add_execute_method_timeout(self):
        alg = Algorithm('name', 'title', 'description')
        param = DataElement('param_val', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 0)
        alg.add_parameter(param)
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.INT, DataShape.SCALAR, 0)
        alg.add_output(output)

        def method(param_val):
            time.sleep(DEFAULT_TIMEOUT + 1)
            return {'output': param_val}
        err = 'Adding the method failed. Error: The time for execution ' \
              f'({DEFAULT_TIMEOUT} s) is over'\
              " Parameters: {'param_val': 0}"
        with self.assertRaises(Exception) as error:
            alg.add_execute_method(method)
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method_without_parameters(self):
        alg = Algorithm('name', 'title', 'description')
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.INT, DataShape.SCALAR, 0)
        alg.add_output(output)
        err = 'Adding the method failed. Error: Parameters for the algorithm ' \
              'are not set'
        with self.assertRaises(Exception) as error:
            alg.add_execute_method(lambda param_val: {'output': param_val})
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method_without_outputs(self):
        alg = Algorithm('name', 'title', 'description')
        param = DataElement('param_val', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 0)
        alg.add_parameter(param)
        err = 'Adding the method failed. Error: Outputs for the algorithm ' \
              'are not set'
        with self.assertRaises(Exception) as error:
            alg.add_execute_method(lambda param_val: {'output': param_val})
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method_wrong_param(self):
        alg = Algorithm('name', 'title', 'description')
        param = DataElement('param_val', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 0)
        alg.add_parameter(param)
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.INT, DataShape.SCALAR, 0)
        alg.add_output(output)
        err = 'Adding the method failed. Error: Method execution is failed! ' \
              'Error: <lambda>() got an unexpected keyword argument ' \
              "'param_val'. Parameters: {'param_val': 0}"
        with self.assertRaises(Exception) as error:
            alg.add_execute_method(lambda wrong_name: {'output': wrong_name})
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method_missing_param(self):
        alg = Algorithm('name', 'title', 'description')
        param = DataElement('param_val', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 0)
        alg.add_parameter(param)
        param2 = DataElement('missing_param', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 0)
        alg.add_parameter(param2)
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.INT, DataShape.SCALAR, 0)
        alg.add_output(output)
        err = 'Adding the method failed. Error: Method execution is failed! ' \
              'Error: <lambda>() got an unexpected keyword argument ' \
              "'missing_param'. " \
              "Parameters: {'param_val': 0, 'missing_param': 0}"
        with self.assertRaises(Exception) as error:
            alg.add_execute_method(lambda param_val: {'output': param_val})
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method_missing_output(self):
        alg = Algorithm('name', 'title', 'description')
        param = DataElement('param_val', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 0)
        alg.add_parameter(param)
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.INT, DataShape.SCALAR, 0)
        alg.add_output(output)
        output2 = DataElement('missing_output', 'output_title', 'output_descr',
                             DataType.INT, DataShape.SCALAR, 0)
        alg.add_output(output2)
        err = "Adding the method failed. Error: 'The defined output key " \
              "\"missing_output\" is missing in the method outputs'"
        with self.assertRaises(Exception) as error:
            alg.add_execute_method(lambda param_val: {'output': param_val})
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method_wrong_output(self):
        alg = Algorithm('name', 'title', 'description')
        param = DataElement('param_val', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 0)
        alg.add_parameter(param)
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.INT, DataShape.SCALAR, 0)
        alg.add_output(output)
        err = "Adding the method failed. Error: 'The returned output key " \
              "\"wrong_name\" is missing in the algorithms outputs'"
        with self.assertRaises(Exception) as error:
            alg.add_execute_method(lambda param_val: {'wrong_name': param_val})
        self.assertEqual(str(error.exception), err)

    def test_add_execute_method(self):
        alg = Algorithm('name', 'title', 'description')
        param = DataElement('param_val', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 0)
        alg.add_parameter(param)
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.INT, DataShape.SCALAR, 0)
        alg.add_output(output)
        alg.add_execute_method(lambda param_val: {'output': param_val})
        self.assertIsNone(alg.get_test_errors())

    def test_execute_timeout(self):
        alg = Algorithm('name', 'title', 'description')
        param = DataElement('param_val', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 0)
        alg.add_parameter(param)
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.INT, DataShape.SCALAR, 0)
        alg.add_output(output)

        def method(param_val):
            time.sleep(param_val)
            return {'output': param_val}
        alg.add_execute_method(method)
        err = (f'The time for execution ({DEFAULT_TIMEOUT} s) is over'
              " Parameters: {'param_val': ") + \
              (str(DEFAULT_TIMEOUT + 1) + '}')
        with self.assertRaises(TimeoutError) as error:
            alg.execute({'param_val': DEFAULT_TIMEOUT + 1})
        self.assertEqual(str(error.exception), err)

    def test_execute_runtime_error(self):
        alg = Algorithm('name', 'title', 'description')
        param = DataElement('param_val', 'param_title', 'param_descr',
                            DataType.INT, DataShape.SCALAR, 1)
        alg.add_parameter(param)
        output = DataElement('output', 'output_title', 'output_descr',
                             DataType.FLOAT, DataShape.SCALAR, 1.)
        alg.add_output(output)
        alg.add_execute_method(lambda param_val: {'output': 1/param_val})
        err = "Method execution is failed! Error: division by zero. " \
              "Parameters: {'param_val': 0}"
        with self.assertRaises(RuntimeError) as error:
            alg.execute({'param_val': 0})
        self.assertEqual(str(error.exception), err)

    def test_execute(self):
        alg = Algorithm('sum', 'sum', 'returns the sum of two numbers')
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
