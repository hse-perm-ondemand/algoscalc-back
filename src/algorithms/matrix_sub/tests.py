import unittest


from src.algorithms.matrix_sub.function import main


class TestCase(unittest.TestCase):

    def test_dlina(self):
        n = [[0.0], [1.0]]
        m = [[0.0], [0.0], [0.0]]
        self.assertRaisesRegex(ValueError, 'Длины матриц не совпадают!',
                               main, n, m)

    def test_row(self):
        n = [[None], [1.0]]
        m = [[0.0], [0.0]]
        self.assertRaisesRegex(ValueError, 'Не введено значение в матрице n',
                               main, n, m)

    def test_rows(self):
        n = [[2.0], [1.0]]
        m = [[None], [1.0]]
        self.assertRaisesRegex(ValueError, 'Не введено значение в матрице m',
                               main, n, m)

    def test_sub(self):
        n = [[1., 2., 3.],
             [2., 3., 4.]]
        m = [[0., 2., 2.],
             [2., 1., 4.]]
        self.assertEqual(main(n, m), {'result': [[1.0, 0.0, 1.0],
                                                 [0.0, 2.0, 0.0]]})

    def test_subtr(self):
        n = [[1., 2., 3.],
             [2., 3., 4.]]
        m = [[1., 2., 3.],
             [2., 3., 4.]]
        self.assertEqual(main(n, m), {'result': [[0.0, 0.0, 0.0],
                                                 [0.0, 0.0, 0.0]]})

if __name__ == '__main__':
    unittest.main()
