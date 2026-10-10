
import unittest

from campusflow.tickets import calculate_priority, create_ticket


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


class TestTicketCreation(unittest.TestCase):

    def setUp(self):
        self.tickets = []

    def test_create_ticket(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi down", "Network", "high", 15
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(len(self.tickets), 1)

    def test_unique_ids(self):
        first = create_ticket(
            self.tickets, "Wi-Fi down", "Network", "high", 15
        )

        second = create_ticket(
            self.tickets, "Laptop broken", "Hardware", "low", 1
        )

        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")

    def test_reject_blank_title(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets, "  ", "Network", "high", 10
            )

        self.assertEqual(self.tickets, [])

    def test_reject_invalid_category(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets, "Error", "Transport", "low", 2
            )

    def test_case_normalization(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi", "nEtWoRk", "HIGH", 12
        )

        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")


if __name__ == "__main__":
    unittest.main()

    