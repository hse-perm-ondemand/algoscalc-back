import unittest


from src.algorithms.quadratic_equation.function import quadratic_equation


class TestCase(unittest.TestCase):
    def test_type_of_coefficient(self):
        self.assertRaisesRegex(TypeError, 'Коэффициенты должны быть числами',
                               quadratic_equation, 'one', 1, 1)

    def test_zero_a_coefficient(self):
        with self.assertRaises(ValueError) as error:
            quadratic_equation(0, 1, 1)
        self.assertEqual('Коэффициент при х^2 в квадратном уравнении не может '
                         'быть равен 0!',
                         str(error.exception))

    def test_zero_b_coefficient(self):
        self.assertEqual(quadratic_equation(1/3, 0, -3), 'x1 = 3.0, x2 = -3.0')

    def test_zero_c_coefficient(self):
        self.assertEqual(quadratic_equation(3.2, 6.5, 0),
                         'x1 = 0.0, x2 = -2.03125')

    def test_negative_discriminant(self):
        self.assertEqual(quadratic_equation(1, 2, 3),
                         'Действительных корней нет, т. к. D < 0')

    def test_zero_discriminant(self):
        self.assertEqual(quadratic_equation(1, 10, 25),
                         'Корень только один: x = -5.0')

    def test_periodic_fraction_coefficient(self):
        self.assertEqual(quadratic_equation(1/3, 5/7, -3),
                         'x1 = 2.11415759, x2 = -4.25701473')


if __name__ == '__main__':
    unittest.main()
