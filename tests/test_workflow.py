import unittest

from campusflow.reports import generate_report
from campusflow.tickets import create_ticket
from campusflow.workflow import (
    assign_ticket,
    get_work_queue,
    reopen_ticket,
    update_status,
)


class WorkflowTestCase(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        create_ticket(self.tickets, "Wi-Fi outage", "Network", "high", 20)
        create_ticket(self.tickets, "Broken laptop", "Hardware", "low", 1)

    def test_assign_ticket_to_existing_ticket(self):
        ticket = assign_ticket(self.tickets, "T001", "Ada Lovelace")
        self.assertEqual(ticket["assigned_to"], "Ada Lovelace")

    def test_assign_rejects_unknown_id_and_blank_name(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Ada Lovelace")
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "  ")
        self.assertIsNone(self.tickets[0]["assigned_to"])

    def test_unassigned_ticket_cannot_start_work(self):
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "in_progress")
        self.assertEqual(self.tickets[0]["status"], "open")

    def test_assigned_ticket_follows_lifecycle(self):
        assign_ticket(self.tickets, "T001", "Ada Lovelace")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")
        self.assertEqual(self.tickets[0]["status"], "resolved")

    def test_invalid_transition_does_not_change_status(self):
        assign_ticket(self.tickets, "T001", "Ada Lovelace")
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "resolved")
        self.assertEqual(self.tickets[0]["status"], "open")

    def test_resolved_ticket_requires_explicit_reopen(self):
        assign_ticket(self.tickets, "T001", "Ada Lovelace")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "open")
        reopened = reopen_ticket(self.tickets, "T001")
        self.assertEqual(reopened["status"], "open")

    def test_queue_sorts_by_priority_then_numeric_id(self):
        create_ticket(self.tickets, "Medium issue", "Software", "low", 3)
        create_ticket(self.tickets, "Another critical", "Network", "high", 10)
        queue = get_work_queue(self.tickets)
        self.assertEqual([ticket["id"] for ticket in queue], ["T001", "T004", "T003", "T002"])

    def test_queue_excludes_resolved_tickets(self):
        assign_ticket(self.tickets, "T001", "Ada Lovelace")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")
        self.assertEqual([ticket["id"] for ticket in get_work_queue(self.tickets)], ["T002"])


class ReportTestCase(unittest.TestCase):
    def test_empty_report_has_zero_counts(self):
        report = generate_report([])
        self.assertEqual(report["total"], 0)
        self.assertTrue(all(value == 0 for value in report["by_status"].values()))
        self.assertTrue(all(value == 0 for value in report["by_priority"].values()))

    def test_report_counts_statuses_and_priorities(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi outage", "Network", "high", 20)
        create_ticket(tickets, "Printer issue", "Hardware", "low", 1)
        assign_ticket(tickets, "T001", "Ada Lovelace")
        update_status(tickets, "T001", "in_progress")
        report = generate_report(tickets)
        self.assertEqual(report["total"], 2)
        self.assertEqual(report["by_status"], {"open": 1, "in_progress": 1, "resolved": 0})
        self.assertEqual(report["by_priority"], {"critical": 1, "high": 0, "medium": 0, "low": 1})


if __name__ == "__main__":
    unittest.main()
