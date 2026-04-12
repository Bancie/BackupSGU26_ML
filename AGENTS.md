# AGENTS.md

## Cursor Cloud specific instructions

This is an empty Python/ML repository (`BackupSGU26_ML`). The `.gitignore` is pre-configured for Python projects.

### Environment

- **Python 3.12** is the system Python. A virtualenv at `.venv` is created by the update script.
- Activate with: `source /workspace/.venv/bin/activate`
- `ruff` (linter) and `pytest` (test runner) are pre-installed in the venv.

### Common commands

| Task | Command |
|------|---------|
| Activate venv | `source .venv/bin/activate` |
| Lint | `ruff check .` |
| Run tests | `pytest` |
| Install deps | `pip install -r requirements.txt` (once a requirements file exists) |

### Notes

- `python3.12-venv` system package is required to create the virtualenv; it is installed as part of the VM setup.
- No source code, services, or dependency manifests exist yet. Once code is added, update this file with service-specific instructions.
