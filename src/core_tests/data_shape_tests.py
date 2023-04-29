import unittest


from src.core.data_element import DataShape


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
        self.assertEqual(ds.get_shape_errors(None), 'The value is None!')
        self.assertEqual(ds.get_shape_errors([]), 'The value is not a scalar!')

    def test_list_errors(self):
        ds = DataShape.LIST
        self.assertIsNone(ds.get_shape_errors([]))
        self.assertIsNone(ds.get_shape_errors(['1']))
        self.assertIsNone(ds.get_shape_errors([1., 2.]))
        self.assertEqual(ds.get_shape_errors(None), 'The value is None!')
        self.assertEqual(ds.get_shape_errors(1), 'The value is not a list!')

    def test_matrix_errors(self):
        ds = DataShape.MATRIX
        self.assertIsNone(ds.get_shape_errors([[]]))
        self.assertIsNone(ds.get_shape_errors([['1']]))
        self.assertIsNone(ds.get_shape_errors([[1., 2.], [1., 2.]]))
        self.assertEqual(ds.get_shape_errors(None), 'The value is None!')
        self.assertEqual(ds.get_shape_errors(1), 'The value is not a matrix!')
        self.assertEqual(ds.get_shape_errors([[1., 2.], [1., 2.], 'row']),
                         'The type of 2 row in the matrix is not a list')


if __name__ == '__main__':
    unittest.main()
