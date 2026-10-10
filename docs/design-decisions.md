# CampusFlow — Design decisions

**Status:** Implemented on the Engineer B feature branch where noted below.

## Ownership
- Engineer A (Issue #1): `campusflow/tickets.py`, `tests/test_tickets.py` — ticket creation, validation, priority.
- Engineer B: `campusflow/workflow.py`, `campusflow/reports.py`, `campusflow/storage.py`, `main.py`, and matching tests — assignment, lifecycle, reopening, queue, reports, JSON persistence, and CLI integration.
- Engineer A owns `campusflow/tickets.py` and its priority/creation behavior; Engineer B reuses that public interface rather than duplicating it.

## Data model
Use a mutable `list[dict]` of tickets. Required fields: `id` (T001, T002...), `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, `assigned_to`.
Statuses: `open`, `in_progress`, `resolved`. Categories: Network, Hardware, Software, Other. Urgency: low, medium, high.

## Existing Engineer A interface
```python
calculate_priority(urgency: str, affected_users: int) -> str
create_ticket(tickets: list, title: str, category: str, urgency: str, affected_users: int) -> dict
```
`calculate_priority` validates urgency and affected users; `create_ticket` validates/normalizes, allocates a new sequential ID from the highest existing valid ID, appends the ticket only after validations, and returns it. Invalid inputs raise `ValueError`. Ticket IDs must be unique; stored records should be validated by the storage layer on load. The CLI catches and displays validation errors.

## Engineer B function contracts
```python
assign_ticket(tickets: list, ticket_id: str, staff_name: str) -> dict
update_status(tickets: list, ticket_id: str, new_status: str) -> dict
reopen_ticket(tickets: list, ticket_id: str) -> dict
get_work_queue(tickets: list) -> list
generate_report(tickets: list) -> dict
```
`assign_ticket` strips a non-empty staff name and returns the modified ticket. All ID-based operations reject unknown IDs. `update_status` allows only `open -> in_progress -> resolved`; starting work requires an assignee, skipped/invalid transitions leave the ticket unchanged, and resolved tickets must use `reopen_ticket`. `reopen_ticket` changes only a resolved ticket back to `open`. `get_work_queue` returns a new list of open tickets sorted critical/high/medium/low and then by numeric ID ascending.

## Persistence and error handling

`load_tickets(path)` returns `[]` for a missing file. Otherwise it parses standard-library JSON and validates each ticket's required fields, ID format/uniqueness, category, urgency, positive affected-user count, calculated priority, status, and assignee. Malformed or invalid data raises `ValueError` and is never overwritten as part of loading. `save_tickets(tickets, path)` validates before opening the file, creates parent directories as needed, and writes readable indented JSON. This protects against saving already-corrupted in-memory ticket data.

## CLI separation

`main.py` owns prompts, printed output, and the persistent `data/tickets.json` path. It delegates creation, workflow, reports, and persistence to `campusflow` modules, catches input/validation errors, and keeps the menu running. Business logic remains callable without interactive input and is unit tested independently.

## Test command
```bash
python3 -m unittest discover -s tests -v
```
Run the platform-appropriate command before integration. On Windows this project uses `py -m unittest discover -s tests -v`. The AI-learning log is intentionally not expanded with unperformed experiments.
