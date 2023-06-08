import unittest


from src.core.data_element import DataType, DataShape, DataElement, \
    NON_STRING_PARAM_TEMPL, EMPTY_STRING_PARAM_TEMPL, NOT_DATA_TYPE_MSG, \
    NOT_DATA_SHAPE_MSG, NONE_VALUE_MSG, NOT_MATRIX_VALUE_MSG,\
    NOT_LIST_VALUE_MSG, NOT_SCALAR_VALUE_MSG, NOT_LIST_ROW_TEMPL,\
    MISMATCH_VALUE_TYPE_TEMPL, MISMATCH_LIST_VALUE_TYPE_TEMPL, \
    MISMATCH_MATRIX_VALUE_TYPE_TEMPL
from src.core_tests import NAME, TITLE, DESCRIPTION


class DataElementTests(unittest.TestCase):
    STR_TEMPL = 'DataElement: {0}, "{1}", value: {2}'

    def test_non_string_name(self):
        self.assertRaisesRegex(ValueError, NON_STRING_PARAM_TEMPL.format(NAME),
                               DataElement.__init__, None, 100500, TITLE,
                               DESCRIPTION, DataType.INT, DataShape.SCALAR, 0)

    def test_none_string_name(self):
        self.assertRaisesRegex(ValueError,
                               EMPTY_STRING_PARAM_TEMPL.format(NAME),
                               DataElement.__init__, None, '', TITLE,
                               DESCRIPTION, DataType.INT, DataShape.SCALAR, 0)

    def test_non_string_title(self):
        self.assertRaisesRegex(ValueError, NON_STRING_PARAM_TEMPL.format(TITLE),
                               DataElement.__init__, None, NAME, 1.1,
                               DESCRIPTION, DataType.INT, DataShape.SCALAR, 0)

    def test_none_string_title(self):
        self.assertRaisesRegex(ValueError,
                               EMPTY_STRING_PARAM_TEMPL.format(TITLE),
                               DataElement.__init__, None, NAME, '',
                               DESCRIPTION, DataType.INT, DataShape.SCALAR, 0)

    def test_non_string_description(self):
        self.assertRaisesRegex(ValueError,
                               NON_STRING_PARAM_TEMPL.format(DESCRIPTION),
                               DataElement.__init__, None, NAME, TITLE,
                               [], DataType.INT, DataShape.SCALAR, 0)

    def test_none_string_description(self):
        self.assertRaisesRegex(ValueError,
                               EMPTY_STRING_PARAM_TEMPL.format(DESCRIPTION),
                               DataElement.__init__, None, NAME, TITLE,
                               '', DataType.INT, DataShape.SCALAR, 0)

    def test_non_data_type(self):
        self.assertRaisesRegex(ValueError, NOT_DATA_TYPE_MSG,
                               DataElement.__init__, None, NAME, TITLE,
                               DESCRIPTION, int, DataShape.SCALAR, 0)

    def test_non_data_shape(self):
        self.assertRaisesRegex(ValueError, NOT_DATA_SHAPE_MSG,
                               DataElement.__init__, None, NAME, TITLE,
                               DESCRIPTION, DataType.INT, 100500, 0)

    def test_default_value_shape_scalar_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                        DataShape.SCALAR, None)
        self.assertEqual(str(error.exception), NONE_VALUE_MSG)
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                        DataShape.SCALAR, {})
        self.assertEqual(str(error.exception), NOT_SCALAR_VALUE_MSG)

    def test_default_value_shape_list_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                        DataShape.LIST, None)
        self.assertEqual(str(error.exception), NONE_VALUE_MSG)
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                        DataShape.LIST, 'str')
        self.assertEqual(str(error.exception), NOT_LIST_VALUE_MSG)

    def test_default_value_shape_matrix_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                        DataShape.MATRIX, None)
        self.assertEqual(str(error.exception), NONE_VALUE_MSG)
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                        DataShape.MATRIX, 'str')
        self.assertEqual(str(error.exception), NOT_MATRIX_VALUE_MSG)
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                        DataShape.MATRIX, [])
        self.assertEqual(str(error.exception), NOT_MATRIX_VALUE_MSG)
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                        DataShape.MATRIX, [[1., 2.], [1., 2.], 'row'])
        self.assertEqual(str(error.exception), NOT_LIST_ROW_TEMPL.format(2))

    def test_default_value_type_scalar_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                        DataShape.SCALAR, '1')
        self.assertEqual(str(error.exception),
                         MISMATCH_VALUE_TYPE_TEMPL.format('int'))
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.FLOAT,
                        DataShape.SCALAR, '1.1')
        self.assertEqual(str(error.exception),
                         MISMATCH_VALUE_TYPE_TEMPL.format('float'))
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.STRING,
                        DataShape.SCALAR, 1)
        self.assertEqual(str(error.exception),
                         MISMATCH_VALUE_TYPE_TEMPL.format('string'))
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.BOOL,
                        DataShape.SCALAR, 123)
        self.assertEqual(str(error.exception),
                         MISMATCH_VALUE_TYPE_TEMPL.format('bool'))

    def test_default_value_type_list_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                        DataShape.LIST, [1, '1'])
        self.assertEqual(str(error.exception),
                         MISMATCH_LIST_VALUE_TYPE_TEMPL.format(1, 'int'))
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.FLOAT,
                        DataShape.LIST, [1, 1.])
        self.assertEqual(str(error.exception),
                         MISMATCH_LIST_VALUE_TYPE_TEMPL.format(0, 'float'))
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.STRING,
                        DataShape.LIST, ['a', 'b', 1])
        self.assertEqual(str(error.exception),
                         MISMATCH_LIST_VALUE_TYPE_TEMPL.format(2, 'string'))
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.BOOL,
                        DataShape.LIST, [True, 123, True])
        self.assertEqual(str(error.exception),
                         MISMATCH_LIST_VALUE_TYPE_TEMPL.format(1, 'bool'))

    def test_default_value_type_matrix_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                        DataShape.MATRIX, [[1, '1']])
        self.assertEqual(str(error.exception),
                         MISMATCH_MATRIX_VALUE_TYPE_TEMPL.format(1, 0, 'int'))
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.FLOAT,
                        DataShape.MATRIX, [[0., 0.], [1, 1.]])
        self.assertEqual(str(error.exception),
                         MISMATCH_MATRIX_VALUE_TYPE_TEMPL.format(0, 1, 'float'))
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.STRING,
                        DataShape.MATRIX, [['a', 'b', 'c'],
                                           ['a', 'b', 1],
                                           ['a', 'b', 'c']])
        self.assertEqual(str(error.exception),
                         MISMATCH_MATRIX_VALUE_TYPE_TEMPL.format(2, 1,
                                                                 'string'))
        with self.assertRaises(ValueError) as error:
            DataElement(NAME, TITLE, DESCRIPTION, DataType.BOOL,
                        DataShape.MATRIX, [[True, 123, True]])
        self.assertEqual(str(error.exception),
                         MISMATCH_MATRIX_VALUE_TYPE_TEMPL.format(1, 0, 'bool'))

    def test_init_scalar(self):
        default_value = 0
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                         DataShape.SCALAR, default_value)
        self.assertEqual(de.name, NAME)
        self.assertEqual(de.title, TITLE)
        self.assertEqual(de.description, DESCRIPTION)
        self.assertEqual(de.data_type, DataType.INT)
        self.assertEqual(de.data_shape, DataShape.SCALAR)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

        default_value = 0.
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.FLOAT,
                         DataShape.SCALAR, default_value)
        self.assertEqual(de.data_type, DataType.FLOAT)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

        default_value = 'string'
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.STRING,
                         DataShape.SCALAR, default_value)
        self.assertEqual(de.data_type, DataType.STRING)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

        default_value = False
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.BOOL,
                         DataShape.SCALAR, default_value)
        self.assertEqual(de.data_type, DataType.BOOL)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

    def test_init_list(self):
        default_value = [0]
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                         DataShape.LIST, default_value)
        self.assertEqual(de.name, NAME)
        self.assertEqual(de.title, TITLE)
        self.assertEqual(de.description, DESCRIPTION)
        self.assertEqual(de.data_type, DataType.INT)
        self.assertEqual(de.data_shape, DataShape.LIST)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

        default_value = [0., 1.]
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.FLOAT,
                         DataShape.LIST, default_value)
        self.assertEqual(de.data_type, DataType.FLOAT)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

        default_value = ['string', 'string', 'string']
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.STRING,
                         DataShape.LIST, default_value)
        self.assertEqual(de.data_type, DataType.STRING)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

        default_value = [False, True, False]
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.BOOL,
                         DataShape.LIST, default_value)
        self.assertEqual(de.data_type, DataType.BOOL)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

    def test_init_matrix(self):
        default_value = [[0]]
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                         DataShape.MATRIX, default_value)
        self.assertEqual(de.name, NAME)
        self.assertEqual(de.title, TITLE)
        self.assertEqual(de.description, DESCRIPTION)
        self.assertEqual(de.data_type, DataType.INT)
        self.assertEqual(de.data_shape, DataShape.MATRIX)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

        default_value = [[0.], [1.]]
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.FLOAT,
                         DataShape.MATRIX, default_value)
        self.assertEqual(de.data_type, DataType.FLOAT)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

        default_value = [['string', 'string', 'string'],
                         ['string', 'string', 'string']]
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.STRING,
                         DataShape.MATRIX, default_value)
        self.assertEqual(de.data_type, DataType.STRING)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

        default_value = [[False, True, False],
                         [False, True, False],
                         [False, True, False]]
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.BOOL,
                         DataShape.MATRIX, default_value)
        self.assertEqual(de.data_type, DataType.BOOL)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(NAME, TITLE,
                                                        default_value))

    def test_check_value_shape_scalar_errors(self):
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                         DataShape.SCALAR, 1)
        self.assertEqual(de.get_check_value_errors(None), NONE_VALUE_MSG)
        self.assertEqual(de.get_check_value_errors([1]), NOT_SCALAR_VALUE_MSG)
        self.assertIsNone(de.get_check_value_errors(1))

    def test_check_value_shape_list_errors(self):
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                         DataShape.LIST, [1])
        self.assertEqual(de.get_check_value_errors(None), NONE_VALUE_MSG)
        self.assertEqual(de.get_check_value_errors(1), NOT_LIST_VALUE_MSG)
        self.assertIsNone(de.get_check_value_errors([1, 2, 3]))

    def test_check_value_list_has_none(self):
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                         DataShape.LIST, [1])
        self.assertIsNone(de.get_check_value_errors([1, None, 3]))

    def test_check_value_shape_matrix_errors(self):
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                         DataShape.MATRIX, [[1]])
        self.assertEqual(de.get_check_value_errors(None), NONE_VALUE_MSG)
        self.assertEqual(de.get_check_value_errors(1), NOT_MATRIX_VALUE_MSG)
        self.assertEqual(de.get_check_value_errors([]), NOT_MATRIX_VALUE_MSG)
        self.assertEqual(de.get_check_value_errors([[1., 2.], [1., 2.], 'row']),
                         NOT_LIST_ROW_TEMPL.format(2))
        self.assertIsNone(de.get_check_value_errors([[1, 2, 3], [1, 2, 3]]))

    def test_check_value_matrix_has_none(self):
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                         DataShape.MATRIX, [[1]])
        self.assertIsNone(de.get_check_value_errors([[1, 2, 3],
                                                     [1, None, 3]]))

    def test_check_value_type_scalar_errors(self):
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                         DataShape.SCALAR, 1)
        self.assertEqual(de.get_check_value_errors('1'),
                         MISMATCH_VALUE_TYPE_TEMPL.format('int'))
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.FLOAT,
                         DataShape.SCALAR, 1.)
        self.assertEqual(de.get_check_value_errors('str'),
                         MISMATCH_VALUE_TYPE_TEMPL.format('float'))
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.FLOAT,
                         DataShape.SCALAR, 1)
        self.assertIsNone(de.get_check_value_errors(1))
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.STRING,
                         DataShape.SCALAR, 'str')
        self.assertEqual(de.get_check_value_errors(1),
                         MISMATCH_VALUE_TYPE_TEMPL.format('string'))
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.BOOL,
                         DataShape.SCALAR, True)
        self.assertEqual(de.get_check_value_errors(1),
                         MISMATCH_VALUE_TYPE_TEMPL.format('bool'))

    def test_check_value_type_list_errors(self):
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                         DataShape.LIST, [1])
        self.assertEqual(de.get_check_value_errors([1, '1']),
                         MISMATCH_LIST_VALUE_TYPE_TEMPL.format(1, 'int'))
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.FLOAT,
                         DataShape.LIST, [1.])
        self.assertEqual(de.get_check_value_errors([1, 1.]),
                         MISMATCH_LIST_VALUE_TYPE_TEMPL.format(0, 'float'))
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.STRING,
                         DataShape.LIST, ['str'])
        self.assertEqual(de.get_check_value_errors(['a', 'b', 1]),
                         MISMATCH_LIST_VALUE_TYPE_TEMPL.format(2, 'string'))
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.BOOL,
                         DataShape.LIST, [True])
        self.assertEqual(de.get_check_value_errors([True, 123, True]),
                         MISMATCH_LIST_VALUE_TYPE_TEMPL.format(1, 'bool'))

    def test_check_value_type_matrix_errors(self):
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.INT,
                         DataShape.MATRIX, [[1]])
        self.assertEqual(de.get_check_value_errors([[1, '1']]),
                         MISMATCH_MATRIX_VALUE_TYPE_TEMPL.format(1, 0, 'int'))
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.FLOAT,
                         DataShape.MATRIX, [[1.]])
        self.assertEqual(de.get_check_value_errors([[0., 0.], [1, 1.]]),
                         MISMATCH_MATRIX_VALUE_TYPE_TEMPL.format(0, 1, 'float'))
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.STRING,
                         DataShape.MATRIX, [['str']])
        self.assertEqual(de.get_check_value_errors([['a', 'b', 'c'],
                                                    ['a', 'b', 1],
                                                    ['a', 'b', 'c']]),
                         MISMATCH_MATRIX_VALUE_TYPE_TEMPL.format(2, 1,
                                                                 'string'))
        de = DataElement(NAME, TITLE, DESCRIPTION, DataType.BOOL,
                         DataShape.MATRIX, [[True]])
        self.assertEqual(de.get_check_value_errors([[True, 123, True]]),
                         MISMATCH_MATRIX_VALUE_TYPE_TEMPL.format(1, 0, 'bool'))


if __name__ == '__main__':
    unittest.main()
