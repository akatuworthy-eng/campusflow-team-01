"""JSON persistence helpers for CampusFlow tickets."""

import json
from pathlib import Path

from campusflow.tickets import calculate_priority
from campusflow.workflow import VALID_STATUSES


_CATEGORIES = ("Network", "Hardware", "Software", "Other")
_URGENCY_LEVELS = ("low", "medium", "high")
_REQUIRED_FIELDS = {
    "id",
    "title",
    "category",
    "urgency",
    "affected_users",
    "priority",
    "status",
    "assigned_to",
}


def validate_tickets(tickets):
    """Raise ValueError when ticket data is not safe for the application to use."""
    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a list")

    seen_ids = set()
    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Each ticket must be an object")

        missing_fields = _REQUIRED_FIELDS - ticket.keys()
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Ticket is missing required fields: {missing}")

        ticket_id = ticket["id"]
        if (
            not isinstance(ticket_id, str)
            or not ticket_id.startswith("T")
            or not ticket_id[1:].isdigit()
            or int(ticket_id[1:]) < 1
            or ticket_id != f"T{int(ticket_id[1:]):03d}"
        ):
            raise ValueError("Ticket ID must use the format T001")
        if ticket_id in seen_ids:
            raise ValueError(f"Duplicate ticket ID: {ticket_id}")
        seen_ids.add(ticket_id)

        if not isinstance(ticket["title"], str) or not ticket["title"].strip():
            raise ValueError(f"Ticket {ticket_id} has a blank title")
        if ticket["category"] not in _CATEGORIES:
            raise ValueError(f"Ticket {ticket_id} has an invalid category")
        if ticket["urgency"] not in _URGENCY_LEVELS:
            raise ValueError(f"Ticket {ticket_id} has an invalid urgency")

        affected_users = ticket["affected_users"]
        if type(affected_users) is not int or affected_users <= 0:
            raise ValueError(f"Ticket {ticket_id} has invalid affected_users")

        expected_priority = calculate_priority(ticket["urgency"], affected_users)
        if ticket["priority"] != expected_priority:
            raise ValueError(f"Ticket {ticket_id} has an invalid priority")
        if ticket["status"] not in VALID_STATUSES:
            raise ValueError(f"Ticket {ticket_id} has an invalid status")
        if ticket["assigned_to"] is not None and (
            not isinstance(ticket["assigned_to"], str)
            or not ticket["assigned_to"].strip()
        ):
            raise ValueError(f"Ticket {ticket_id} has an invalid assignee")


def load_tickets(path):
    """Load and validate tickets from *path*, or return an empty list if missing."""
    file_path = Path(path)
    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Ticket storage contains malformed JSON: {error.msg}") from error
    except OSError as error:
        raise ValueError(f"Could not read ticket storage: {error}") from error

    validate_tickets(tickets)
    return tickets


def save_tickets(tickets, path):
    """Validate and save tickets as readable JSON, creating parent directories."""
    validate_tickets(tickets)
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=2)
            file.write("\n")
    except OSError as error:
        raise ValueError(f"Could not save ticket storage: {error}") from error
