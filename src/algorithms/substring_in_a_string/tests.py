import unittest

from src.algorithms.substring_in_a_string.function import main


class TestCase(unittest.TestCase):
    def test_check_value(self):
        self.assertRaisesRegex(ValueError, "Значения не строковые", main, "one", 0)

    def test_long_text(self):
        self.assertEqual(
            main("Hello world world hello hello hello world", "hello world"),
            {"num_count": 2},
        )

    def test_short_findtext(self):
        self.assertEqual(main("it is very long text", "i"), {"num_count": 2})

    def test_short_them_text(self):
        self.assertEqual(main("text is ", "text is very long"), {"num_count": 0})

    def test_equal_texts(self):
        self.assertEqual(main("texts", "texts"), {"num_count": 1})


if __name__ == "__main__":
    unittest.main()
