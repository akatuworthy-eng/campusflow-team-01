
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
