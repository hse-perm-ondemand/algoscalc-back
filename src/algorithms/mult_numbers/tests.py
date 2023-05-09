import unittest


from src.algorithms.mult_numbers.function import mult_numbers


class TestCase(unittest.TestCase):
    def test_string_type_of_numbers(self):
        self.assertRaisesRegex(TypeError, 'Перемножать можно только числа',
                               mult_numbers, 'qwe', 'rty')

    def test_correct_mult_1(self):
        self.assertEqual(mult_numbers(1.1, 5.1), 5.61)

    def test_correct_mult_2(self):
        self.assertEqual(mult_numbers(-1.4, -100.0), 140.0)

    def test_correct_mult_3(self):
        self.assertEqual(mult_numbers(-8.0, 3.8742), -30.9936)

    def test_correct_mult_4(self):
        self.assertEqual(mult_numbers(2, 3), 6)

    def test_correct_mult_5(self):
        self.assertEqual(mult_numbers(0, 6), 0)

    def test_correct_mult_6(self):
        self.assertEqual(mult_numbers(39726.475, 3745.295), 148787368.185125)


if __name__ == '__main__':
    unittest.main()
