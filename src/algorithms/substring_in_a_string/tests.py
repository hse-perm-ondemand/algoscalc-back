import unittest


from src.algorithms.substring_in_a_string.function import findcountstring


class TestCase(unittest.TestCase):
    def test_type_of_coefficient(self):
        self.assertRaisesRegex(ValueError,
                               "Значения не строковые",
                               findcountstring,"one",0)

    def test_zero_a_coefficient(self):
        self.assertRaisesRegex(ValueError,
                               "Значения не строковые",
                               findcountstring,0,0)

    def test_zero_b_coefficient(self):
        self.assertRaisesRegex(ValueError,
                               "Значения не строковые",
                               findcountstring,0,"ищу")

    def test_zero_c_coefficient(self):
        self.assertEqual(findcountstring("Hello world world hello hello hello world","hello world"),
                             {"num_count": 3})

    def test_negative_discriminant(self):
        self.assertEqual(findcountstring("it is very long text","i"),
                              {"num_count": 2})

    def test_zero_discriminant(self):
        self.assertEqual(findcountstring("text is very long","text is very longe"),
                          {"num_count": 0})

    def test_periodic_fraction_coefficient(self):
        self.assertEqual(findcountstring("text is very long","text is very long"),
                          {"num_count": 1})

if __name__ == '__main__':
    unittest.main()
