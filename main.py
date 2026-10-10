"""Interactive command-line interface for CampusFlow."""

from pathlib import Path

from campusflow.reports import generate_report
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, get_work_queue, reopen_ticket, update_status


DATA_PATH = Path("data") / "tickets.json"


def display_ticket(ticket):
    """Print one ticket in a consistent, readable format."""
    print(f"{ticket['id']}: {ticket['title']}")
    print(f"  Category: {ticket['category']}")
    print(f"  Urgency: {ticket['urgency']} | Priority: {ticket['priority']}")
    print(f"  Affected users: {ticket['affected_users']}")
    print(f"  Status: {ticket['status']} | Assigned to: {ticket['assigned_to']}")


def find_ticket(tickets, ticket_id):
    """Find a ticket for display without exposing workflow's private helper."""
    normalized_id = ticket_id.strip().upper()
    for ticket in tickets:
        if ticket["id"] == normalized_id:
            return ticket
    raise ValueError(f"Unknown ticket ID: {normalized_id}")


def prompt_create_ticket(tickets):
    """Collect ticket fields and delegate creation to the business logic."""
    title = input("Title: ")
    category = input("Category (Network/Hardware/Software/Other): ")
    urgency = input("Urgency (low/medium/high): ")
    affected_users = int(input("Affected users: "))
    ticket = create_ticket(tickets, title, category, urgency, affected_users)
    print(f"Created {ticket['id']}.")


def display_report(report):
    """Print a report returned by generate_report."""
    print(f"Total tickets: {report['total']}")
    print("By status:", report["by_status"])
    print("By priority:", report["by_priority"])


def run_cli(data_path=DATA_PATH):
    """Run the CampusFlow menu until the user chooses Exit."""
    try:
        tickets = load_tickets(data_path)
    except ValueError as error:
        print(f"Could not load tickets: {error}")
        tickets = []

    while True:
        print("\nCampusFlow")
        print("1. Create ticket\n2. List tickets\n3. View ticket\n4. Assign ticket")
        print("5. Change status\n6. Show work queue\n7. Show reports")
        print("8. Save tickets\n9. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                prompt_create_ticket(tickets)
            elif choice == "2":
                for ticket in tickets:
                    display_ticket(ticket)
            elif choice == "3":
                display_ticket(find_ticket(tickets, input("Ticket ID: ")))
            elif choice == "4":
                assign_ticket(tickets, input("Ticket ID: "), input("Staff name: "))
                print("Ticket assigned.")
            elif choice == "5":
                ticket_id = input("Ticket ID: ")
                new_status = input("New status (in_progress/resolved/reopen): ")
                if new_status.strip().lower() == "reopen":
                    reopen_ticket(tickets, ticket_id)
                else:
                    update_status(tickets, ticket_id, new_status)
                print("Status updated.")
            elif choice == "6":
                for ticket in get_work_queue(tickets):
                    display_ticket(ticket)
            elif choice == "7":
                display_report(generate_report(tickets))
            elif choice == "8":
                save_tickets(tickets, data_path)
                print("Tickets saved.")
            elif choice == "9":
                save_tickets(tickets, data_path)
                print("Tickets saved. Goodbye.")
                return
            else:
                print("Choose a number from 1 to 9.")
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    run_cli()
