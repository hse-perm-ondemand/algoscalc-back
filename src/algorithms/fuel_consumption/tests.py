import unittest

from src.algorithms.fuel_consumption.function import (
    COST,
    DISTANCE_NAME,
    MEAN_NAME,
    NEG_VALUE_PARAM_TEMPL,
    NON_FLOAT_PARAM_TEMPL,
    PRICE_NAME,
    VOLUME,
    main,
)


class TestCase(unittest.TestCase):
    def test_distance_not_float(self):
        self.assertRaisesRegex(
            TypeError,
            NON_FLOAT_PARAM_TEMPL.format(DISTANCE_NAME),
            main,
            "str",
            0.0,
            0.0,
            True,
        )

    def test_distance_neg(self):
        self.assertRaisesRegex(
            ValueError,
            NEG_VALUE_PARAM_TEMPL.format(DISTANCE_NAME),
            main,
            -1.0,
            0.0,
            0.0,
            True,
        )

    def test_mean_not_float(self):
        self.assertRaisesRegex(
            TypeError, NON_FLOAT_PARAM_TEMPL.format(MEAN_NAME), main, 0.0, [], 0.0, True
        )

    def test_mean_neg(self):
        self.assertRaisesRegex(
            ValueError,
            NEG_VALUE_PARAM_TEMPL.format(MEAN_NAME),
            main,
            0.0,
            -1.0,
            0.0,
            True,
        )

    def test_price_not_float(self):
        self.assertRaisesRegex(
            TypeError,
            NON_FLOAT_PARAM_TEMPL.format(PRICE_NAME),
            main,
            0.0,
            0.0,
            None,
            True,
        )

    def test_price_neg(self):
        self.assertRaisesRegex(
            ValueError,
            NEG_VALUE_PARAM_TEMPL.format(PRICE_NAME),
            main,
            0.0,
            0.0,
            -1.0,
            True,
        )

    def test_zero(self):
        self.assertEqual({VOLUME: 0.0, COST: 0.0}, main(0.0, 0.0, 0.0, True))

    def test_round(self):
        self.assertEqual({VOLUME: 8.0, COST: 338.0}, main(100.0, 7.5, 45.0, True))

    def test_not_round(self):
        self.assertEqual({VOLUME: 7.5, COST: 337.5}, main(100.0, 7.5, 45.0, False))


if __name__ == "__main__":
    unittest.main()
