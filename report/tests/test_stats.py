import unittest

from hh_report.stats import median


class MedianTest(unittest.TestCase):
    def test_odd(self):
        self.assertEqual(median([3, 1, 2]), 2)

    def test_even(self):
        self.assertEqual(median([4, 1, 3, 2]), 2.5)

    def test_one(self):
        self.assertEqual(median([7]), 7)


if __name__ == "__main__":
    unittest.main()
