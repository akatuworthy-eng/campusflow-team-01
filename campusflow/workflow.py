"""Ticket assignment and lifecycle operations for CampusFlow."""


VALID_STATUSES = ("open", "in_progress", "resolved")
_PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _find_ticket(tickets, ticket_id):
    """Return a ticket by ID or raise a useful validation error."""
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be stored in a list")
    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID cannot be blank")

    normalized_id = ticket_id.strip().upper()
    for ticket in tickets:
        if isinstance(ticket, dict) and ticket.get("id") == normalized_id:
            return ticket
    raise ValueError(f"Unknown ticket ID: {normalized_id}")


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign a ticket to a non-empty staff member name."""
    ticket = _find_ticket(tickets, ticket_id)
    if ticket.get("status") == "resolved":
        raise ValueError("Resolved tickets must be explicitly reopened before reassignment")
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be blank")
    ticket["assigned_to"] = staff_name.strip()
    return ticket


def update_status(tickets, ticket_id, new_status):
    """Move a ticket through the normal open/in-progress/resolved workflow."""
    ticket = _find_ticket(tickets, ticket_id)
    if not isinstance(new_status, str):
        raise ValueError("Invalid status")

    normalized_status = new_status.strip().lower()
    if normalized_status not in VALID_STATUSES:
        raise ValueError("Invalid status")

    current_status = ticket.get("status")
    allowed_transition = {
        "open": {"in_progress"},
        "in_progress": {"resolved"},
        "resolved": set(),
    }
    if normalized_status not in allowed_transition.get(current_status, set()):
        if current_status == "resolved" and normalized_status == "open":
            raise ValueError("Resolved tickets must be explicitly reopened")
        raise ValueError(
            f"Invalid status transition: {current_status} -> {normalized_status}"
        )
    if normalized_status == "in_progress" and not ticket.get("assigned_to"):
        raise ValueError("A ticket must be assigned before it can be in progress")

    ticket["status"] = normalized_status
    return ticket


def reopen_ticket(tickets, ticket_id):
    """Explicitly reopen a resolved ticket by setting its status to open."""
    ticket = _find_ticket(tickets, ticket_id)
    if ticket.get("status") != "resolved":
        raise ValueError("Only resolved tickets can be reopened")
    ticket["status"] = "open"
    return ticket


def get_work_queue(tickets):
    """Return open tickets ordered by priority and numeric ticket ID."""
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be stored in a list")

    queue = [ticket for ticket in tickets if ticket.get("status") == "open"]

    def sort_key(ticket):
        priority_key = _PRIORITY_ORDER.get(ticket.get("priority"), len(_PRIORITY_ORDER))
        ticket_id = ticket.get("id", "")
        try:
            numeric_id = int(ticket_id[1:])
        except (TypeError, ValueError, IndexError):
            numeric_id = float("inf")
        return priority_key, numeric_id

    return sorted(queue, key=sort_key)
