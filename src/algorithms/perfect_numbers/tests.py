import unittest


from src.algorithms.perfect_numbers.function import main, HAS_PERFECT,\
    PERFECT_NUMBERS


class TestCase(unittest.TestCase):
    def test_not_list(self):
        self.assertRaisesRegex(TypeError, 'Параметр не является списком',
                               main, 'str')

    def test_none(self):
        self.assertRaisesRegex(TypeError, 'Параметр не является списком',
                               main, None)

    def test_empty(self):
        self.assertRaisesRegex(ValueError, 'Список чисел пуст', main, [])

    def test_not_int(self):
        self.assertRaisesRegex(ValueError,
                               'Список чисел содержит нечисловое значение',
                               main, [1, 'str'])


    def test_neg(self):
        self.assertRaisesRegex(ValueError,
                               'Список чисел содержит отрицательное значение',
                               main, [1, 2, -1])


    def test_single_true(self):
        self.assertEqual({HAS_PERFECT: True, PERFECT_NUMBERS: [6]},
                         main([6]))


    def test_single_false(self):
        self.assertEqual({HAS_PERFECT: False, PERFECT_NUMBERS: []},
                         main([5]))


    def test_multi_true(self):
        self.assertEqual({HAS_PERFECT: True, PERFECT_NUMBERS: [6]},
                         main([0, 1, 6]))


    def test_multi_perfect_only(self):
        self.assertEqual({HAS_PERFECT: True,
                          PERFECT_NUMBERS: [6, 28, 496, 8128]},
                         main([6, 28, 496, 8128]))


    def test_multi(self):
        self.assertEqual({HAS_PERFECT: True,
                          PERFECT_NUMBERS: [6, 28, 496, 8128]},
                         main([6, 0, 10, 28, 100, 496, 532, 8128]))

if __name__ == '__main__':
    unittest.main()
