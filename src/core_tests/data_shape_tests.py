import unittest


from src.core.data_element import DataShape, NONE_VALUE_MSG,\
    NOT_MATRIX_VALUE_MSG, NOT_LIST_VALUE_MSG, NOT_SCALAR_VALUE_MSG, \
    NOT_LIST_ROW_TEMPL


class DataShapeTests(unittest.TestCase):
    def test_scalar(self):
        ds = DataShape.SCALAR
        self.assertEqual(ds.name, 'SCALAR')
        self.assertEqual(ds.value, 'SCALAR')

    def test_list(self):
        ds = DataShape.LIST
        self.assertEqual(ds.name, 'LIST')
        self.assertEqual(ds.value, 'LIST')

    def test_matrix(self):
        ds = DataShape.MATRIX
        self.assertEqual(ds.name, 'MATRIX')
        self.assertEqual(ds.value, 'MATRIX')

    def test_scalar_errors(self):
        ds = DataShape.SCALAR
        self.assertIsNone(ds.get_shape_errors(1))
        self.assertIsNone(ds.get_shape_errors('1'))
        self.assertIsNone(ds.get_shape_errors(1.))
        self.assertIsNone(ds.get_shape_errors(True))
        self.assertEqual(ds.get_shape_errors(None), NONE_VALUE_MSG)
        self.assertEqual(ds.get_shape_errors([]), NOT_SCALAR_VALUE_MSG)

    def test_list_errors(self):
        ds = DataShape.LIST
        self.assertIsNone(ds.get_shape_errors([]))
        self.assertIsNone(ds.get_shape_errors(['1']))
        self.assertIsNone(ds.get_shape_errors([1., 2.]))
        self.assertEqual(ds.get_shape_errors(None), NONE_VALUE_MSG)
        self.assertEqual(ds.get_shape_errors(1), NOT_LIST_VALUE_MSG)

    def test_matrix_errors(self):
        ds = DataShape.MATRIX
        self.assertIsNone(ds.get_shape_errors([[]]))
        self.assertIsNone(ds.get_shape_errors([['1']]))
        self.assertIsNone(ds.get_shape_errors([[1., 2.], [1., 2.]]))
        self.assertEqual(ds.get_shape_errors(None), NONE_VALUE_MSG)
        self.assertEqual(ds.get_shape_errors(1), NOT_MATRIX_VALUE_MSG)
        self.assertEqual(ds.get_shape_errors([[1., 2.], [1., 2.], 'row']),
                         NOT_LIST_ROW_TEMPL.format(2))


if __name__ == '__main__':
    unittest.main()
