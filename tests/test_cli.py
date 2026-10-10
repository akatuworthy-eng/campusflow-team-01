"""CLI safety regression tests for CampusFlow."""

import json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from main import run_cli


class CLISafetyTestCase(unittest.TestCase):
    def test_malformed_json_prevents_start_and_preserves_original_file(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            original = "{broken json"
            path.write_text(original, encoding="utf-8")
            output = StringIO()

            with redirect_stdout(output), patch(
                "builtins.input",
                side_effect=AssertionError("The CLI must not prompt when loading fails"),
            ):
                exit_code = run_cli(path)

            self.assertEqual(exit_code, 1)
            self.assertEqual(path.read_text(encoding="utf-8"), original)
            self.assertIn("Could not load tickets", output.getvalue())
            self.assertNotIn("Choose an option", output.getvalue())

    def test_invalid_ticket_data_prevents_start_and_preserves_original_file(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            original = '{"unexpected": "object instead of a ticket list"}'
            path.write_text(original, encoding="utf-8")

            with redirect_stdout(StringIO()), patch(
                "builtins.input",
                side_effect=AssertionError("The CLI must not prompt when validation fails"),
            ):
                exit_code = run_cli(path)

            self.assertEqual(exit_code, 1)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_fresh_start_can_exit_and_save_empty_list(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "data" / "tickets.json"
            with redirect_stdout(StringIO()), patch("builtins.input", return_value="9"):
                exit_code = run_cli(path)

            self.assertEqual(exit_code, 0)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), [])


if __name__ == "__main__":
    unittest.main()
