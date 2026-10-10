import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket


class StorageTestCase(unittest.TestCase):
    def make_tickets(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi outage", "Network", "high", 20)
        create_ticket(tickets, "Broken laptop", "Hardware", "low", 1)
        return tickets

    def test_saving_and_loading_preserves_all_ticket_fields(self):
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "nested" / "tickets.json"
            tickets = self.make_tickets()

            save_tickets(tickets, path)
            loaded_tickets = load_tickets(path)

            self.assertEqual(loaded_tickets, tickets)
            self.assertIn("\n  {", path.read_text(encoding="utf-8"))

    def test_missing_storage_file_returns_empty_list(self):
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "missing.json"
            self.assertEqual(load_tickets(path), [])

    def test_malformed_json_raises_without_changing_file(self):
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "tickets.json"
            malformed_content = "{not valid json"
            path.write_text(malformed_content, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "malformed JSON"):
                load_tickets(path)

            self.assertEqual(path.read_text(encoding="utf-8"), malformed_content)

    def test_duplicate_ids_in_loaded_data_are_rejected(self):
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "tickets.json"
            tickets = self.make_tickets()
            tickets[1]["id"] = "T001"
            path.write_text(json.dumps(tickets), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Duplicate ticket ID"):
                load_tickets(path)

    def test_new_ticket_after_reload_uses_next_available_id(self):
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "tickets.json"
            tickets = self.make_tickets()
            save_tickets(tickets, path)

            loaded_tickets = load_tickets(path)
            new_ticket = create_ticket(
                loaded_tickets, "Printer issue", "Hardware", "medium", 2
            )

            self.assertEqual(new_ticket["id"], "T003")


if __name__ == "__main__":
    unittest.main()
