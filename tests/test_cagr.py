import unittest

from src.analytics.cagr import calculate_cagr


class TestCAGR(unittest.TestCase):

    def test_normal(self):
        cagr, flag = calculate_cagr(100, 200, 5)
        self.assertEqual(flag, "NORMAL")

    def test_zero_base(self):
        cagr, flag = calculate_cagr(0, 200, 5)
        self.assertEqual(flag, "ZERO_BASE")

    def test_turnaround(self):
        cagr, flag = calculate_cagr(-100, 200, 5)
        self.assertEqual(flag, "TURNAROUND")

    def test_decline(self):
        cagr, flag = calculate_cagr(100, -200, 5)
        self.assertEqual(flag, "DECLINE_TO_LOSS")

    def test_both_negative(self):
        cagr, flag = calculate_cagr(-100, -200, 5)
        self.assertEqual(flag, "BOTH_NEGATIVE")

    def test_insufficient_start(self):
        cagr, flag = calculate_cagr(None, 100, 5)
        self.assertEqual(flag, "INSUFFICIENT")

    def test_insufficient_end(self):
        cagr, flag = calculate_cagr(100, None, 5)
        self.assertEqual(flag, "INSUFFICIENT")

    def test_positive_growth(self):
        cagr, flag = calculate_cagr(100, 300, 3)
        self.assertTrue(cagr > 0)

    def test_negative_growth(self):
        cagr, flag = calculate_cagr(300, 100, 3)
        self.assertTrue(cagr < 0)

    def test_same_value(self):
        cagr, flag = calculate_cagr(100, 100, 5)
        self.assertEqual(cagr, 0.0)


if __name__ == "__main__":
    unittest.main()