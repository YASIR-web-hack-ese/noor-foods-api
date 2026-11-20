# Noor Foods API

A small FastAPI service for Noor Foods, using SQLModel for database models and
Alembic for version-controlled database migrations.

## Project layout

```text
noor-foods-api/
├── alembic/
│   ├── versions/          # Ordered database migrations
│   ├── env.py             # Alembic connection and model configuration
│   └── script.py.mako     # Template for new migrations
├── src/noor_foods_api/
│   ├── config.py          # Environment-backed application settings
│   ├── database.py        # SQLAlchemy engine and session dependency
│   ├── main.py            # FastAPI application and routes
│   └── models.py          # SQLModel table definitions
├── .env.example           # Local configuration template
├── alembic.ini            # Alembic project settings
├── Dockerfile
├── pyproject.toml
└── uv.lock
```

## Local setup

The API expects PostgreSQL at `localhost:5433` by default. Start the database
from the Noor Foods project directory, then install the API dependencies:

```powershell
docker compose -f ..\..\NOORFOODS\compose.yaml up -d
uv sync
```

`uv sync` is the only environment setup command needed. It creates or updates
the project-local `.venv` from `pyproject.toml` and `uv.lock`, including the
development tools. VS Code is configured to use that same interpreter and the
`src` import path automatically; do not install project packages into a global
Python installation.

Run quality checks with:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run python -c "import noor_foods_api.main"
```

Copy `.env.example` to `.env` when you need to use a different database URL.

## Database workflow

Apply all migrations:

```powershell
uv run alembic upgrade head
```

Check whether the models and database schema differ:

```powershell
uv run alembic check
```

Create a migration after changing a model:

```powershell
uv run alembic revision --autogenerate -m "describe the schema change"
uv run alembic upgrade head
```

Always review generated migrations before applying them. Once a migration has
been applied to a shared database, create a new migration for corrections
instead of editing the old file.

## Run the API

```powershell
uv run fastapi dev src/noor_foods_api/main.py
```

The interactive API documentation is available at `http://localhost:8000/docs`.
