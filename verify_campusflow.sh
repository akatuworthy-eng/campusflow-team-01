#!/usr/bin/env bash
# Run from inside the campusflow-team-01 Git repository.
set -euo pipefail

if [[ ! -d .git ]]; then
  echo 'ERROR: Run this script from the campusflow-team-01 repository root.' >&2
  exit 2
fi

echo '=== 1. Updating main safely ==='
git fetch origin
git switch main
git pull --ff-only origin main
printf 'HEAD: '
git rev-parse --short HEAD

echo '=== 2. Running the complete unittest suite ==='
python3 -m unittest discover -s tests -v

echo '=== 3. Running an isolated CLI persistence smoke test ==='
python3 - <<'PY'
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from main import run_cli
from campusflow.storage import load_tickets

with TemporaryDirectory(prefix='campusflow-check-') as directory:
    path = Path(directory) / 'tickets.json'
    commands = [
        '1', 'Campus Wi-Fi is down', 'Network', 'high', '15',
        '2',
        '4', 'T001', 'Ada',
        '5', 'T001', 'in_progress',
        '5', 'T001', 'resolved',
        '7', '8', '9',
    ]
    transcript = StringIO()
    with patch('builtins.input', side_effect=commands), redirect_stdout(transcript):
        result = run_cli(path)
    assert result == 0, f'Expected normal CLI exit, got {result}'
    tickets = load_tickets(path)
    assert len(tickets) == 1, f'Expected one saved ticket, got {len(tickets)}'
    ticket = tickets[0]
    assert ticket['id'] == 'T001', ticket
    assert ticket['priority'] == 'critical', ticket
    assert ticket['status'] == 'resolved', ticket
    assert ticket['assigned_to'] == 'Ada', ticket
    assert 'Total tickets: 1' in transcript.getvalue()
    with patch('builtins.input', return_value='9'), redirect_stdout(StringIO()):
        assert run_cli(path) == 0
    assert load_tickets(path) == tickets, 'Ticket changed after restart'
    print('PASS: create -> assign -> resolve -> report -> save -> restart')

    original = '{broken json'
    path.write_text(original, encoding='utf-8')
    with patch('builtins.input', side_effect=AssertionError('CLI must not start')), redirect_stdout(StringIO()):
        assert run_cli(path) == 1
    assert path.read_text(encoding='utf-8') == original
    print('PASS: malformed JSON prevents startup without losing original content')
PY

echo '=== All local verification steps passed ==='
