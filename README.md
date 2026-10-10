# CampusFlow

CampusFlow is a beginner-friendly Python command-line helpdesk ticket manager.
It uses only the Python standard library and stores tickets in JSON.

## Run the project

No package installation is required. From the repository root on Windows:

```powershell
py main.py
```

The CLI loads `data/tickets.json` when it starts. If that file does not exist,
CampusFlow starts with no tickets. Saving creates the `data` directory when
needed. If the file contains malformed JSON or invalid ticket records, startup
stops without changing the file. Correct or recover the stored data before
starting again.

## Run tests

```powershell
py -m unittest discover -s tests -v
```

## CLI menu

1. Create ticket
2. List tickets
3. View ticket
4. Assign ticket
5. Change status (enter `reopen` to explicitly reopen a resolved ticket)
6. Show work queue
7. Show reports
8. Save tickets
9. Exit (saves tickets first)

## Rules

Ticket categories are Network, Hardware, Software, and Other. Urgency is low,
medium, or high. Priority is calculated in this exact order:

1. High urgency and at least 10 affected users: `critical`
2. High urgency or at least 10 affected users: `high`
3. Medium urgency or at least 3 affected users: `medium`
4. Otherwise: `low`

The normal status workflow is `open -> in_progress -> resolved`. A ticket must
be assigned before it starts work. Resolved tickets can only return to `open`
through the explicit reopen action; they cannot be reassigned until reopened.

The work queue contains open tickets, ordered by priority (critical through
low) and then the numeric portion of the ticket ID.

## Current status and limitations

Ticket creation, workflow, reports, JSON persistence, and the text CLI are
implemented with automated unit tests. The application stores all data in one
local JSON file; it does not support user authentication, concurrent editing,
search, or a graphical/web interface.
