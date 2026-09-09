# Life Dashboard V2

[![Tests](https://github.com/ryanthalis/life-dashboard/actions/workflows/tests.yml/badge.svg)](https://github.com/ryanthalis/life-dashboard/actions/workflows/tests.yml)

Life Dashboard V2 is a Python application for tracking workout and study sessions. Entries are stored in SQLite and can be managed through either an interactive command-line interface or a validated FastAPI REST API.

## Features

- Create, view, update, and delete workout and study entries
- Store entries in a constrained SQLite database
- Filter API results by workout or study category
- Validate API request and response data with Pydantic
- Migrate legacy database schemas automatically
- Test database, CLI, migration, and API behavior with `unittest`

## Setup

Python 3.13 or newer is recommended.

```powershell
git clone https://github.com/ryanthalis/life-dashboard.git
cd life-dashboard
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the CLI

```powershell
python life_tracker.py
```

The CLI initializes `life.db` automatically and presents a menu for managing entries and viewing summaries.

## Run the API

Initialize the database once if the CLI has not been run:

```powershell
python -c "import db; db.init_db()"
```

Start the development server:

```powershell
fastapi dev api.py
```

Open the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Check that the API is running |
| `GET` | `/entries` | List all entries |
| `GET` | `/entries?category=study` | Filter entries by category |
| `GET` | `/entries/{entry_id}` | Retrieve one entry |
| `POST` | `/entries` | Create an entry |
| `PATCH` | `/entries/{entry_id}` | Update selected fields |
| `DELETE` | `/entries/{entry_id}` | Delete an entry |

Example POST body:

```json
{
  "entry_date": "2026-09-09",
  "category": "study",
  "label": "FastAPI",
  "quantity": 30,
  "notes": "Response models"
}
```

## Run the Tests

```powershell
python -m unittest -v
```

Tests use temporary databases and do not modify the local `life.db` file.

## Local Files

The SQLite database, virtual environment, Python cache files, and DB Browser workspace files are ignored by Git. Each developer keeps their own local `life.db` data.

## Roadmap

A browser-based frontend is planned as the likely next stage of Life Dashboard.
