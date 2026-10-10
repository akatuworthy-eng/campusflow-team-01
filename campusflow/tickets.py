
def calculate_priority(urgency: str, affected_users: int) -> str:
    if not isinstance(urgency, str):
        raise ValueError("Invalid urgency")

    urgency = urgency.strip().lower()

    if urgency not in ("low", "medium", "high"):
        raise ValueError("Invalid urgency")

    if type(affected_users) is not int or affected_users <= 0:
        raise ValueError("Affected users must be a positive integer")

    if urgency == "high" and affected_users >= 10:
        return "critical"

    elif urgency == "high" or affected_users >= 10:
        return "high"

    elif urgency == "medium" or affected_users >= 3:
        return "medium"

    else:
        return "low"


def create_ticket(tickets, title, category, urgency, affected_users):
    # Validate the ticket collection
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be stored in a list")

    # Validate the title
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title cannot be blank")

    # Validate and normalize the category
    categories = {
        name.lower(): name
        for name in ("Network", "Hardware", "Software", "Other")
    }

    if not isinstance(category, str) or category.strip().lower() not in categories:
        raise ValueError("Invalid ticket category")

    # Validate urgency and affected users using the existing function
    priority = calculate_priority(urgency, affected_users)

    normalized_category = categories[category.strip().lower()]
    normalized_urgency = urgency.strip().lower()

    # Generate a unique ID
    next_number = max(
        (int(ticket["id"][1:]) for ticket in tickets),
        default=0
    ) + 1

    ticket = {
        "id": f"T{next_number:03d}",
        "title": title.strip(),
        "category": normalized_category,
        "urgency": normalized_urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }

    tickets.append(ticket)
    return ticket
