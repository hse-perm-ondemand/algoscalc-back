import unittest


from algorithms.fibonacci_list.function import fibonacci


class TestCase(unittest.TestCase):
    numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    def test_fibonacci(self):
        for i in range(len(self.numbers)):
            self.assertEqual(fibonacci(i + 1), self.numbers[:i + 1])


if __name__ == '__main__':
    unittest.main()
