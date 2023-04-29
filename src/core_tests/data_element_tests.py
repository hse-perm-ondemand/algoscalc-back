import unittest


from src.core.data_element import DataType, DataShape, DataElement


class DataElementTests(unittest.TestCase):
    STR_TEMPL = 'DataElement: {0}, "{1}", value: {2}'

    def test_non_string_name(self):
        self.assertRaisesRegex(ValueError, 'The name parameter is not a string',
                               DataElement.__init__, None, 100500, 'title',
                               'description', DataType.INT, DataShape.SCALAR, 0)

    def test_none_string_name(self):
        self.assertRaisesRegex(ValueError, 'The name parameter is empty',
                               DataElement.__init__, None, '', 'title',
                               'description', DataType.INT, DataShape.SCALAR, 0)

    def test_non_string_title(self):
        self.assertRaisesRegex(ValueError,
                               'The title parameter is not a string',
                               DataElement.__init__, None, 'name', 1.1,
                               'description', DataType.INT, DataShape.SCALAR, 0)

    def test_none_string_title(self):
        self.assertRaisesRegex(ValueError, 'The title parameter is empty',
                               DataElement.__init__, None, 'name', '',
                               'description', DataType.INT, DataShape.SCALAR, 0)

    def test_non_string_description(self):
        self.assertRaisesRegex(ValueError,
                               'The description parameter is not a string',
                               DataElement.__init__, None, 'name', 'title',
                               [], DataType.INT, DataShape.SCALAR, 0)

    def test_none_string_description(self):
        self.assertRaisesRegex(ValueError, 'The description parameter is empty',
                               DataElement.__init__, None, 'name', 'title',
                               '', DataType.INT, DataShape.SCALAR, 0)

    def test_non_data_type(self):
        self.assertRaisesRegex(ValueError, 'The data_type parameter is not '
                                           'a DataType instance',
                               DataElement.__init__, None, 'name', 'title',
                               'description', int, DataShape.SCALAR, 0)

    def test_non_data_shape(self):
        self.assertRaisesRegex(ValueError, 'The data_shape parameter is not '
                                           'a DataShape instance',
                               DataElement.__init__, None, 'name', 'title',
                               'description', DataType.INT, 100500, 0)

    def test_default_value_shape_scalar_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.INT,
                        DataShape.SCALAR, None)
        self.assertEqual(str(error.exception), 'The value is None!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.INT,
                        DataShape.SCALAR, {})
        self.assertEqual(str(error.exception), 'The value is not a scalar!')

    def test_default_value_shape_list_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.INT,
                        DataShape.LIST, None)
        self.assertEqual(str(error.exception), 'The value is None!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.INT,
                        DataShape.LIST, 'str')
        self.assertEqual(str(error.exception), 'The value is not a list!')

    def test_default_value_shape_matrix_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.INT,
                        DataShape.MATRIX, None)
        self.assertEqual(str(error.exception), 'The value is None!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.INT,
                        DataShape.MATRIX, 'str')
        self.assertEqual(str(error.exception), 'The value is not a matrix!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.INT,
                        DataShape.MATRIX, [])
        self.assertEqual(str(error.exception), 'The value is not a matrix!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.INT,
                        DataShape.MATRIX, [[1., 2.], [1., 2.], 'row'])
        self.assertEqual(str(error.exception),
                         'The type of 2 row in the matrix is not a list')

    def test_default_value_type_scalar_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.INT,
                        DataShape.SCALAR, '1')
        self.assertEqual(str(error.exception), 'The type of value is not int!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.FLOAT,
                        DataShape.SCALAR, 1)
        self.assertEqual(str(error.exception),
                         'The type of value is not float!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.STRING,
                        DataShape.SCALAR, 1)
        self.assertEqual(str(error.exception),
                         'The type of value is not string!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.BOOL,
                        DataShape.SCALAR, 123)
        self.assertEqual(str(error.exception), 'The type of value is not bool!')

    def test_default_value_type_list_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.INT,
                        DataShape.LIST, [1, '1'])
        self.assertEqual(str(error.exception),
                         'The type at 1 position in the list is not int!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.FLOAT,
                        DataShape.LIST, [1, 1.])
        self.assertEqual(str(error.exception),
                         'The type at 0 position in the list is not float!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.STRING,
                        DataShape.LIST, ['a', 'b', 1])
        self.assertEqual(str(error.exception),
                         'The type at 2 position in the list is not string!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.BOOL,
                        DataShape.LIST, [True, 123, True])
        self.assertEqual(str(error.exception),
                         'The type at 1 position in the list is not bool!')

    def test_default_value_type_matrix_errors(self):
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.INT,
                        DataShape.MATRIX, [[1, '1']])
        self.assertEqual(str(error.exception), 'The type at 1 position in 0 row'
                                               ' in the matrix is not int!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.FLOAT,
                        DataShape.MATRIX, [[0., 0.], [1, 1.]])
        self.assertEqual(str(error.exception), 'The type at 0 position in 1 row'
                                               ' in the matrix is not float!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.STRING,
                        DataShape.MATRIX, [['a', 'b', 'c'],
                                           ['a', 'b', 1],
                                           ['a', 'b', 'c']])
        self.assertEqual(str(error.exception), 'The type at 2 position in 1 row'
                                               ' in the matrix is not string!')
        with self.assertRaises(ValueError) as error:
            DataElement('name', 'title', 'description', DataType.BOOL,
                        DataShape.MATRIX, [[True, 123, True]])
        self.assertEqual(str(error.exception), 'The type at 1 position in 0 row'
                                               ' in the matrix is not bool!')

    def test_init_scalar(self):
        name = 'name'
        title = 'title'
        description = 'description'
        default_value = 0
        de = DataElement(name, title, description, DataType.INT,
                         DataShape.SCALAR, default_value)
        self.assertEqual(de.name, name)
        self.assertEqual(de.title, title)
        self.assertEqual(de.description, description)
        self.assertEqual(de.data_type, DataType.INT)
        self.assertEqual(de.data_shape, DataShape.SCALAR)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

        default_value = 0.
        de = DataElement(name, title, description, DataType.FLOAT,
                         DataShape.SCALAR, default_value)
        self.assertEqual(de.data_type, DataType.FLOAT)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

        default_value = 'string'
        de = DataElement(name, title, description, DataType.STRING,
                         DataShape.SCALAR, default_value)
        self.assertEqual(de.data_type, DataType.STRING)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

        default_value = False
        de = DataElement(name, title, description, DataType.BOOL,
                         DataShape.SCALAR, default_value)
        self.assertEqual(de.data_type, DataType.BOOL)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

    def test_init_list(self):
        name = 'list name'
        title = 'list title'
        description = 'list description'
        default_value = [0]
        de = DataElement(name, title, description, DataType.INT,
                         DataShape.LIST, default_value)
        self.assertEqual(de.name, name)
        self.assertEqual(de.title, title)
        self.assertEqual(de.description, description)
        self.assertEqual(de.data_type, DataType.INT)
        self.assertEqual(de.data_shape, DataShape.LIST)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

        default_value = [0., 1.]
        de = DataElement(name, title, description, DataType.FLOAT,
                         DataShape.LIST, default_value)
        self.assertEqual(de.data_type, DataType.FLOAT)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

        default_value = ['string', 'string', 'string']
        de = DataElement(name, title, description, DataType.STRING,
                         DataShape.LIST, default_value)
        self.assertEqual(de.data_type, DataType.STRING)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

        default_value = [False, True, False]
        de = DataElement(name, title, description, DataType.BOOL,
                         DataShape.LIST, default_value)
        self.assertEqual(de.data_type, DataType.BOOL)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

    def test_init_matrix(self):
        name = 'matrix'
        title = 'matrix title'
        description = 'matrix description'
        default_value = [[0]]
        de = DataElement(name, title, description, DataType.INT,
                         DataShape.MATRIX, default_value)
        self.assertEqual(de.name, name)
        self.assertEqual(de.title, title)
        self.assertEqual(de.description, description)
        self.assertEqual(de.data_type, DataType.INT)
        self.assertEqual(de.data_shape, DataShape.MATRIX)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

        default_value = [[0.], [1.]]
        de = DataElement(name, title, description, DataType.FLOAT,
                         DataShape.MATRIX, default_value)
        self.assertEqual(de.data_type, DataType.FLOAT)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

        default_value = [['string', 'string', 'string'],
                         ['string', 'string', 'string']]
        de = DataElement(name, title, description, DataType.STRING,
                         DataShape.MATRIX, default_value)
        self.assertEqual(de.data_type, DataType.STRING)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

        default_value = [[False, True, False],
                         [False, True, False],
                         [False, True, False]]
        de = DataElement(name, title, description, DataType.BOOL,
                         DataShape.MATRIX, default_value)
        self.assertEqual(de.data_type, DataType.BOOL)
        self.assertEqual(de.default_value, default_value)
        self.assertEqual(str(de), self.STR_TEMPL.format(name, title,
                                                        default_value))

    def test_check_value_shape_scalar_errors(self):
        de = DataElement('name', 'title', 'description', DataType.INT,
                         DataShape.SCALAR, 1)
        self.assertEqual(de.get_check_value_errors(None), 'The value is None!')
        self.assertEqual(de.get_check_value_errors([1]),
                         'The value is not a scalar!')
        self.assertIsNone(de.get_check_value_errors(1))

    def test_check_value_shape_list_errors(self):
        de = DataElement('name', 'title', 'description', DataType.INT,
                         DataShape.LIST, [1])
        self.assertEqual(de.get_check_value_errors(None), 'The value is None!')
        self.assertEqual(de.get_check_value_errors(1),
                         'The value is not a list!')
        self.assertIsNone(de.get_check_value_errors([1, 2, 3]))

    def test_check_value_list_has_none(self):
        de = DataElement('name', 'title', 'description', DataType.INT,
                         DataShape.LIST, [1])
        self.assertIsNone(de.get_check_value_errors([1, None, 3]))

    def test_check_value_shape_matrix_errors(self):
        de = DataElement('name', 'title', 'description', DataType.INT,
                         DataShape.MATRIX, [[1]])
        self.assertEqual(de.get_check_value_errors(None), 'The value is None!')
        self.assertEqual(de.get_check_value_errors(1),
                         'The value is not a matrix!')
        self.assertEqual(de.get_check_value_errors([]),
                         'The value is not a matrix!')
        self.assertEqual(de.get_check_value_errors([[1., 2.], [1., 2.], 'row']),
                         'The type of 2 row in the matrix is not a list')
        self.assertIsNone(de.get_check_value_errors([[1, 2, 3], [1, 2, 3]]))

    def test_check_value_matrix_has_none(self):
        de = DataElement('name', 'title', 'description', DataType.INT,
                         DataShape.MATRIX, [[1]])
        self.assertIsNone(de.get_check_value_errors([[1, 2, 3],
                                                     [1, None, 3]]))

    def test_check_value_type_scalar_errors(self):
        de = DataElement('name', 'title', 'description', DataType.INT,
                         DataShape.SCALAR, 1)
        self.assertEqual(de.get_check_value_errors('1'),
                         'The type of value is not int!')
        de = DataElement('name', 'title', 'description', DataType.FLOAT,
                         DataShape.SCALAR, 1.)
        self.assertEqual(de.get_check_value_errors(1),
                         'The type of value is not float!')
        de = DataElement('name', 'title', 'description', DataType.STRING,
                         DataShape.SCALAR, 'str')
        self.assertEqual(de.get_check_value_errors(1),
                         'The type of value is not string!')
        de = DataElement('name', 'title', 'description', DataType.BOOL,
                         DataShape.SCALAR, True)
        self.assertEqual(de.get_check_value_errors(1),
                         'The type of value is not bool!')

    def test_check_value_type_list_errors(self):
        de = DataElement('name', 'title', 'description', DataType.INT,
                         DataShape.LIST, [1])
        self.assertEqual(de.get_check_value_errors([1, '1']),
                         'The type at 1 position in the list is not int!')
        de = DataElement('name', 'title', 'description', DataType.FLOAT,
                         DataShape.LIST, [1.])
        self.assertEqual(de.get_check_value_errors([1, 1.]),
                         'The type at 0 position in the list is not float!')
        de = DataElement('name', 'title', 'description', DataType.STRING,
                         DataShape.LIST, ['str'])
        self.assertEqual(de.get_check_value_errors(['a', 'b', 1]),
                         'The type at 2 position in the list is not string!')
        de = DataElement('name', 'title', 'description', DataType.BOOL,
                         DataShape.LIST, [True])
        self.assertEqual(de.get_check_value_errors([True, 123, True]),
                         'The type at 1 position in the list is not bool!')

    def test_check_value_type_matrix_errors(self):
        de = DataElement('name', 'title', 'description', DataType.INT,
                         DataShape.MATRIX, [[1]])
        self.assertEqual(de.get_check_value_errors([[1, '1']]),
                         'The type at 1 position in 0 row'
                         ' in the matrix is not int!')
        de = DataElement('name', 'title', 'description', DataType.FLOAT,
                         DataShape.MATRIX, [[1.]])
        self.assertEqual(de.get_check_value_errors([[0., 0.], [1, 1.]]),
                         'The type at 0 position in 1 row'
                         ' in the matrix is not float!')
        de = DataElement('name', 'title', 'description', DataType.STRING,
                         DataShape.MATRIX, [['str']])
        self.assertEqual(de.get_check_value_errors([['a', 'b', 'c'],
                                                    ['a', 'b', 1],
                                                    ['a', 'b', 'c']]),
                         'The type at 2 position in 1 row'
                         ' in the matrix is not string!')
        de = DataElement('name', 'title', 'description', DataType.BOOL,
                         DataShape.MATRIX, [[True]])
        self.assertEqual(de.get_check_value_errors([[True, 123, True]]),
                         'The type at 1 position in 0 row'
                         ' in the matrix is not bool!')


if __name__ == '__main__':
    unittest.main()
