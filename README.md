# FastAPI Users + SQLModel Integration Example

A minimal example demonstrating how to integrate **FastAPI Users** (SQLAlchemy) with **SQLModel** for user authentication and cross-model database relationships.

## Overview

This example covers:

- Using SQLAlchemy User model (required by FastAPI Users) alongside SQLModel entities
- Defining relationships across SQLAlchemy and SQLModel models
- Running Alembic migrations in a mixed setup

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

1. **Install dependencies:**

   ```bash
   uv sync
   source .venv/bin/activate
   ```

2. **Initialize the database:**

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

3. **Create sample data:**

   ```bash
   python create-sample-data.py
   ```

4. **Start the server:**

   ```bash
   python main.py
   ```

5. **Test the API:**
   ```bash
   # Get users (SQLAlchemy) in a group (SQLModel)
   curl http://localhost:8000/user-groups/1/users
   ```

## Project Structure

```
fastapi-users-sqlmodel-example/
├── app/
│   ├── __init__.py
│   ├── app.py              # FastAPI application & routes
│   ├── db.py               # Database connection & session
│   ├── models.py           # SQLAlchemy + SQLModel models
│   ├── schemas.py          # Pydantic schemas
│   └── users.py            # FastAPI Users configuration
├── alembic/                # Database migrations
├── alembic.ini             # Alembic configuration
├── create-sample-data.py   # Sample data creation script
├── main.py                 # Application entry point
├── pyproject.toml          # Project dependencies
└── README.md
```

## Important Differences From [SQLAlchemy Example](https://github.com/fastapi-users/fastapi-users/tree/v14.0.1/examples/sqlalchemy)

### Alembic Setup

- Set `sqlalchemy.url` in `alembic.ini` to a sync URL: `sqlite:///./test.db`
- Add the following to `alembic/env.py`:

```python
from app.models import SQLModel

target_metadata = SQLModel.metadata
```

- Add the following to `alembic/script.py.mako`:

```python
import fastapi_users_db_sqlalchemy
import sqlmodel.sql.sqltypes
```

### Model Integration (app/models.py)

- Set `SQLModel.metadata` to `Base.metadata`
- Set `SQLModel._sa_registry` to `Base.registry`
- Add a relationship between `User` (SQLAlchemy) and `UserGroup` (SQLModel)

### Database Session Management (app/db.py)

- Use SQLModel's `AsyncSession` instead of SQLAlchemy's
- Remove the `create_db_and_tables` function in favor of Alembic

### Application Routes (app/app.py)

- Remove the `lifespan` event that creates tables, since Alembic is used
- Add the `/user-groups/{group_id}/users` endpoint to demonstrate the relationship between SQLAlchemy and SQLModel models
