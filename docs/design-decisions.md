# CampusFlow — Proposed design decisions

**Status:** Proposed by Engineer A; Engineer B must review and agree before integration.

## Ownership
- Engineer A (Issue #1): `campusflow/tickets.py`, `tests/test_tickets.py` — ticket creation, validation, priority.
- Engineer B: `campusflow/workflow.py`, `campusflow/reports.py` and matching tests — assignment, lifecycle, queue, reports.
- Shared: `campusflow/storage.py`, `main.py`, integration tests, documentation. Each fellow must contribute code and tests.

## Data model
Use a mutable `list[dict]` of tickets. Required fields: `id` (T001, T002...), `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, `assigned_to`.
Statuses: `open`, `in_progress`, `resolved`. Categories: Network, Hardware, Software, Other. Urgency: low, medium, high.

## Existing Engineer A interface
```python
calculate_priority(urgency: str, affected_users: int) -> str
create_ticket(tickets: list, title: str, category: str, urgency: str, affected_users: int) -> dict
```
`calculate_priority` validates urgency and affected users; `create_ticket` validates/normalizes, allocates a new sequential ID from the highest existing valid ID, appends the ticket only after validations, and returns it. Invalid inputs raise `ValueError`. Ticket IDs must be unique; stored records should be validated by the storage layer on load. The CLI catches and displays validation errors.

## Proposed Engineer B interfaces — confirm together
```python
assign_ticket(tickets: list, ticket_id: str, staff_name: str) -> dict
update_status(tickets: list, ticket_id: str, new_status: str) -> dict
reopen_ticket(tickets: list, ticket_id: str) -> dict
get_work_queue(tickets: list) -> list
generate_report(tickets: list) -> dict
```
`get_work_queue` should return only `open` tickets, sorted critical/high/medium/low and numeric ID ascending. Reject unknown ticket IDs. No `in_progress` without assignment. Only `open -> in_progress -> resolved` in normal flow. A resolved ticket must be explicitly reopened (to `open`) before modification.

## Proposed shared persistence
Use Python's standard `json` module and `data/tickets.json`. A missing file starts with `[]`; malformed JSON raises an understandable error, never overwriting the file silently. Loading must preserve existing IDs and validate enough structure to avoid silent corruption. Agree on `load_tickets(path)` / `save_tickets(tickets, path)` return and error contracts before coding.

## Test command
```bash
python3 -m unittest discover -s tests -v
```
Verify on latest integrated `main` after the review process, not just on the feature branch.
