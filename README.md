# Badminton Match Planner (Idea 2)

Professional, lightweight planner for generating weekly badminton match schedules and exporting them as Excel and PNG.

This repository contains a Streamlit-based UI plus small, well-scoped modules to:
- manage weekly player entries and locking (JSON storage),
- generate match schedules (heuristic to minimize repeat teammates), and
- export schedules to Excel and a simple PNG table.

## Key features
- Web UI using Streamlit (`app.py`) for easy player entry and schedule generation.
- Deterministic storage of weekly state in `JSON/` files (one JSON file per ISO week).
- Schedule generation in `planner.py` (12 players, 3 courts, 6 matches by default).
- Export helpers in `export_utils.py` producing `.xlsx` and `.png` artifacts in `schedule/`.

## Requirements
- Python 3.11+ recommended.
- See `requirements.txt` (pinned versions included).

Recommended core dependencies (already detected and pinned):
- streamlit==1.17.0
- pandas==2.3.3
- matplotlib==3.10.7
- openpyxl==3.1.5

## Quickstart — run locally (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

2. Install pinned dependencies:

```powershell
pip install -r requirements.txt
```

3. Start the Streamlit UI (preferred):

```powershell
streamlit run app.py
```

Alternatively, you can run `python app.py` but `app.py` uses Streamlit APIs, so `streamlit run` provides the proper environment and auto-reload.

## Project layout

- `app.py` — Streamlit web app (entry point).
- `planner.py` — schedule generation logic.
- `storage.py` — read/write weekly JSON state in `JSON/`.
- `export_utils.py` — save schedule to Excel (`.xlsx`) and PNG (`schedule/`).
- `JSON/` — week JSON files (created automatically).
- `schedule/` — generated outputs (Excel/PNG).
- `requirements.txt` — pinned dependencies for reproducible installs.

## Data and configuration
- Time zone: the app uses `Europe/Tallinn` by default (`storage.TIMEZONE`). Change `TIMEZONE` in `storage.py` if needed.
- Week filename format: `<YEAR> - WK <WEEKNUMBER>.json` (e.g. `2025 - WK 44.json`).

Example week JSON (trimmed):

```json
{
  "week": "2025 - WK 44",
  "created_at": "2025-10-27T10:00:00+02:00",
  "locked": false,
  "players": ["Alice", "Bob", "Carol", "Dave", ...],
  "matches": []
}
```

When a week is locked and `matches` is empty the app will auto-generate a schedule and export it.

## Exported outputs
- Excel: `<WEEK NAME> - schedule.xlsx` (written with pandas + openpyxl).
- PNG: `<WEEK NAME> - schedule.png` (simple table rendered via matplotlib) saved in `schedule/`.

## Development notes
- The schedule generator expects exactly 12 players. `planner.generate_full_schedule` will raise on different sizes.
- Add tests: recommended places are unit tests for `planner.py` (pairing/coverage heuristics) and `storage.py` (week name/path logic).

## Troubleshooting
- If you see import errors, ensure the virtual environment is activated and dependencies are installed from `requirements.txt`.
- If Excel export fails, confirm `openpyxl` is installed (it is pinned in `requirements.txt`).
- If Streamlit does not start, run `streamlit --version` to confirm the executable is available in the venv.

## Contributing
- Small changes: open a PR with a clear description and a short test/example when appropriate.
- Larger features: open an issue first describing the goal and migration/compatibility concerns.

## Next improvements (suggested)
- Add a lightweight test suite (pytest) and CI to run tests and linting on PRs.
- Add example week JSON files or an onboarding flow to seed sample players.
- Improve the export layout (colours/formatting) for the PNG and Excel files.

