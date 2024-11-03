import unittest

from src.algorithms.matrix_sub.function import main
from src.internal.errors import AlgorithmValueError


class TestCase(unittest.TestCase):

    def test_dlina(self):
        n = [[0.0], [1.0]]
        m = [[0.0], [0.0], [0.0]]
        self.assertRaisesRegex(
            AlgorithmValueError, "Длины матриц не совпадают!", main, n, m
        )

    def test_row(self):
        n = [[None], [1.0]]
        m = [[0.0], [0.0]]
        self.assertRaisesRegex(
            AlgorithmValueError, "Не введено значение в матрице n", main, n, m
        )

    def test_rows(self):
        n = [[2.0], [1.0]]
        m = [[None], [1.0]]
        self.assertRaisesRegex(
            AlgorithmValueError, "Не введено значение в матрице m", main, n, m
        )

    def test_sub(self):
        n = [[1.0, 2.0, 3.0], [2.0, 3.0, 4.0]]
        m = [[0.0, 2.0, 2.0], [2.0, 1.0, 4.0]]
        self.assertEqual(main(n, m), {"result": [[1.0, 0.0, 1.0], [0.0, 2.0, 0.0]]})

    def test_subtr(self):
        n = [[1.0, 2.0, 3.0], [2.0, 3.0, 4.0]]
        m = [[1.0, 2.0, 3.0], [2.0, 3.0, 4.0]]
        self.assertEqual(main(n, m), {"result": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]})


if __name__ == "__main__":
    unittest.main()
