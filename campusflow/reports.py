"""Reporting helpers for CampusFlow tickets."""


STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")


def generate_report(tickets):
    """Return totals and stable status/priority breakdown dictionaries."""
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be stored in a list")

    by_status = {status: 0 for status in STATUSES}
    by_priority = {priority: 0 for priority in PRIORITIES}

    for ticket in tickets:
        status = ticket.get("status")
        priority = ticket.get("priority")
        if status in by_status:
            by_status[status] += 1
        if priority in by_priority:
            by_priority[priority] += 1

    return {
        "total": len(tickets),
        "by_status": by_status,
        "by_priority": by_priority,
    }
