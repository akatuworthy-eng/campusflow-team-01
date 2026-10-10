
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


def test_priority_boundaries(self):
    cases = [
        ("high", 9, "high"),
        ("high", 10, "critical"),
        ("low", 10, "high"),
        ("low", 3, "medium"),
        ("medium", 1, "medium"),
    ]

    for urgency, users, expected in cases:
        with self.subTest(urgency=urgency, users=users):
            result = calculate_priority(urgency, users)
            self.assertEqual(result, expected)


def test_invalid_affected_user_values(self):
    invalid_values = [0, -3, 1.5, "5", True, None]

    for value in invalid_values:
        with self.subTest(value=value):
            with self.assertRaises(ValueError):
                calculate_priority("low", value)


def test_invalid_urgency_values(self):
    for urgency in ["urgent", "", "extreme", None]:
        with self.subTest(urgency=urgency):
            with self.assertRaises(ValueError):
                calculate_priority(urgency, 5)



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


def test_invalid_creation_preserves_tickets(self):
    create_ticket(
        self.tickets, "Wi-Fi down", "Network", "high", 12
    )

    original = self.tickets.copy()

    with self.assertRaises(ValueError):
        create_ticket(
            self.tickets, "Broken laptop", "Invalid", "low", 2
        )

    self.assertEqual(self.tickets, original)


def test_continue_existing_id_sequence(self):
    first = create_ticket(
        self.tickets, "Wi-Fi down", "Network", "low", 1
    )

    # Simulate an existing ticket restored from storage
    first["id"] = "T007"

    second = create_ticket(
        self.tickets, "Laptop broken", "Hardware", "high", 2
    )

    self.assertEqual(second["id"], "T008")


def test_reject_malformed_existing_id(self):
    self.tickets.append({"id": "X001"})

    with self.assertRaises(ValueError):
        create_ticket(
            self.tickets, "Wi-Fi down", "Network", "low", 1
        )


if __name__ == "__main__":
    unittest.main()

    