
import unittest

from campusflow.tickets import calculate_priority


class TestPriority(unittest.TestCase):

    def test_critical_priority(self):
        result = calculate_priority("high", 12)
        self.assertEqual(result, "critical")

    def test_high_priority(self):
        result = calculate_priority("high", 2)
        self.assertEqual(result, "high")

    def test_medium_priority(self):
        result = calculate_priority("low", 4)
        self.assertEqual(result, "medium")

    def test_low_priority(self):
        result = calculate_priority("low", 1)
        self.assertEqual(result, "low")

    def test_invalid_affected_users(self):
        with self.assertRaises(ValueError):
            calculate_priority("high", 0)


if __name__ == "__main__":
    unittest.main()
